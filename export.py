# export.py
import ee
from config import AOI_COORDS, EXPORT_FOLDER, EXPORT_SCALE, EXPORT_CRS


def get_aoi():
    return ee.Geometry.Rectangle(AOI_COORDS)


def export_image(image, filename, bands=None, scale=None):
    aoi = get_aoi()
    if bands:
        image = image.select(bands)
    task = ee.batch.Export.image.toDrive(
        image=image.clip(aoi),
        description=filename,
        folder=EXPORT_FOLDER,
        fileNamePrefix=filename,
        region=aoi,
        scale=scale or EXPORT_SCALE,
        crs=EXPORT_CRS,
        maxPixels=1e9,
        fileFormat='GeoTIFF'
    )
    task.start()
    print(f'Export submitted: {filename} -> Google Drive/{EXPORT_FOLDER}/')
    print(f'  Monitor at: https://code.earthengine.google.com/ (Tasks tab)')
    return task


def export_all(baseline, monitor, change, mask):
    tasks = []
    tasks.append(export_image(baseline, 'belinga_baseline_composite', bands=['VV', 'VH']))
    tasks.append(export_image(monitor,  'belinga_monitor_composite',  bands=['VV', 'VH']))
    tasks.append(export_image(change,   'belinga_change_delta',       bands=['VV_delta', 'VH_delta']))
    tasks.append(export_image(mask,     'belinga_disturbance_mask'))
    return tasks