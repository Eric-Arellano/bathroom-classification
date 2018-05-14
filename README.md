# Bathroom Classification
Uses ML classification to determine if bathroom is gender-inclusive and accessible to people with disabilities.

## Prereqs
1. Chrome Driver, `brew cask install chromeodriver` (only if scraping data)

## To install
1. `python3 -m venv .`
1. `source bin/activate`
1. `pip install -r requirements.txt`

## To run
1. Activate venv: `source bin/activate`
1. Scrape images if not already downloaded: `python src/scrape_images.py`
1. Label images if not already labeled: `python src/labeler.py`
