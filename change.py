# change.py
import ee
from config import AOI_COORDS, CHANGE_THRESHOLD_DB


def get_aoi():
    return ee.Geometry.Rectangle(AOI_COORDS)


def compute_change(baseline, monitor):
    vv_delta = monitor.select('VV').subtract(baseline.select('VV')).rename('VV_delta')
    vh_delta = monitor.select('VH').subtract(baseline.select('VH')).rename('VH_delta')
    ratio_delta = (
        monitor.select('VV_VH_ratio')
        .subtract(baseline.select('VV_VH_ratio'))
        .rename('VV_VH_delta')
    )
    return ee.Image.cat([vv_delta, vh_delta, ratio_delta])


def compute_disturbance_mask(change_image):
    # Disturbance = VV decrease >= threshold (negative delta)
    return (
        change_image.select('VV_delta')
        .lte(-CHANGE_THRESHOLD_DB)
        .rename('disturbance')
    )


def compute_disturbance_stats(mask):
    aoi = get_aoi()
    pixel_area = ee.Image.pixelArea()
    disturbed_area = pixel_area.updateMask(mask).rename('area')
    stats = disturbed_area.reduceRegion(
        reducer=ee.Reducer.sum(),
        geometry=aoi,
        scale=10,
        maxPixels=1e9
    )
    return ee.Number(stats.get('area')).divide(10000)


def run_change_detection(baseline, monitor):
    change = compute_change(baseline, monitor)
    mask = compute_disturbance_mask(change)
    area_ha = compute_disturbance_stats(mask)
    print(f'Estimated disturbed area: {area_ha.getInfo():.1f} ha')
    return {
        'change': change,
        'disturbance_mask': mask,
        'disturbed_area_ha': area_ha
    }