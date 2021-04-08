# Automatically created by: shub deploy

from setuptools import setup, find_packages

setup(
    name         = 'google_reviwer',
    version      = '1.0',
    packages     = find_packages(),
    package_data={'google_reviwer': ['resources/url.csv']},
    entry_points = {'scrapy': ['settings = google_reviwer.settings']},
)
