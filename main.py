# main.py
# Entry point for Belinga SAR change detection pipeline
# Usage: python main.py

import ee
from config import GEE_PROJECT, BASELINE_START, BASELINE_END, MONITOR_START, MONITOR_END
from pipeline import get_baseline_composite, get_monitor_composite
from change import run_change_detection
from export import export_all


def main():
    print('Initialising GEE...')
    ee.Initialize(project=GEE_PROJECT)
    print(f'Project: {GEE_PROJECT}')
    print(f'Baseline: {BASELINE_START} to {BASELINE_END}')
    print(f'Monitor:  {MONITOR_START} to {MONITOR_END}')
    print()

    print('Building baseline composite...')
    baseline = get_baseline_composite()

    print('Building monitor composite...')
    monitor = get_monitor_composite()

    print()
    print('Running change detection...')
    results = run_change_detection(baseline, monitor)

    print()
    print('Submitting exports...')
    export_all(
        baseline=baseline,
        monitor=monitor,
        change=results['change'],
        mask=results['disturbance_mask']
    )

    print()
    print('Done. Check Google Drive for outputs once export tasks complete.')


if __name__ == '__main__':
    main()