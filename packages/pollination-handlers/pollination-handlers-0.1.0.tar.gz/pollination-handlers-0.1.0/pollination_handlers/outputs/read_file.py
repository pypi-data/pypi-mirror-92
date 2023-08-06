"""Handlers for daylight factor simulation."""
import os


def read_DF_from_path(result_file):
    """Read daylight factor values from a radiance .res result file."""
    if not os.path.isfile(result_file):
        raise ValueError('Invalid file path: %s' % result_file)
    with open(result_file) as inf:
        results = [min(float(line), 100) for line in inf]
    return results
