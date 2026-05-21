# pipeline.py
import ee
from config import (
    AOI_COORDS, S1_COLLECTION, POLARISATIONS, INSTRUMENT_MODE, ORBIT_PASS,
    BASELINE_START, BASELINE_END, MONITOR_START, MONITOR_END,
    MIN_SCENES_BASELINE, MIN_SCENES_MONITOR
)


def get_aoi():
    return ee.Geometry.Rectangle(AOI_COORDS)


def get_collection(start, end):
    aoi = get_aoi()
    col = (
        ee.ImageCollection(S1_COLLECTION)
        .filterBounds(aoi)
        .filterDate(start, end)
        .filter(ee.Filter.eq('instrumentMode', INSTRUMENT_MODE))
        .filter(ee.Filter.eq('orbitProperties_pass', ORBIT_PASS))
        .filter(ee.Filter.listContains('transmitterReceiverPolarisation', 'VV'))
        .filter(ee.Filter.listContains('transmitterReceiverPolarisation', 'VH'))
        .select(POLARISATIONS)
    )
    return col


def apply_speckle_filter(image):
    filtered = image.focal_median(radius=1, kernelType='square', units='pixels')
    return filtered.copyProperties(image, image.propertyNames())


def build_composite(collection, label=''):
    filtered = collection.map(apply_speckle_filter)
    composite = filtered.median()

    if label:
        n = collection.size().getInfo()
        print(f'{label} scene count: {n}')
        if label == 'baseline' and n < MIN_SCENES_BASELINE:
            print(f'  WARNING: only {n} baseline scenes (want >= {MIN_SCENES_BASELINE})')
        if label == 'monitor' and n < MIN_SCENES_MONITOR:
            print(f'  WARNING: only {n} monitor scenes (want >= {MIN_SCENES_MONITOR})')

    return composite


def build_vv_vh_ratio(composite):
    ratio = composite.select('VV').subtract(composite.select('VH')).rename('VV_VH_ratio')
    return composite.addBands(ratio)


def get_baseline_composite():
    col = get_collection(BASELINE_START, BASELINE_END)
    return build_vv_vh_ratio(build_composite(col, label='baseline'))


def get_monitor_composite():
    col = get_collection(MONITOR_START, MONITOR_END)
    return build_vv_vh_ratio(build_composite(col, label='monitor'))