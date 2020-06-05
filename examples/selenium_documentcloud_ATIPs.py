""" File: selenium_documentcloud_ATIPs.py
Author: Kevin Dick
Date: 2020-06-04
---
Description: A Selenium-based scraper to download the
PDFs listed on the DocumentCloud of Muckrock-Canada.
"""
import os
from selenium import webdriver
import requests
import argparse

parser = argparse.ArgumentParser(description='')
parser.add_argument('-o', '--output_dir', required=True,
                    help='output directory for the PDFs')
parser.add_argument('-v', '--verbose', action='store_true',
                    help='increase verbosity')
args = parser.parse_args()

# EXAMPLE: python3 selenium_documentcloud_ATIPs.py  -o ./Muckrock-Canada/ -v

# Constants for the scraping project
BASE_URL  = 'https://www.documentcloud.org/public/search/Group:%20muckrock-canada'
MATCH_URL = 'documentcloud.org/document'
DRIVER    = '/usr/local/bin/chromedriver' # Specify the location of your own chromedriver installation
MAX_PAGES = 478

def get_page_links(driver, url):
	""" get_page_links
	    With the created driver, navigate to the next page
	    and get all ahref links that match the MATCH_URL.
	    ---
	    Input:  <driver> driver, instantiated driver
	    Output: <list> links, all page links matching the MATCH_URL
	"""
	driver.get(url)
	links = []

	# Obtain a list of the links on this page
	elems = driver.find_elements_by_xpath("//a[@href]")
	for elem in elems:
		link = elem.get_attribute("href")
		if MATCH_URL in link:
			if args.verbose: print(f'adding {link}')
			links.append(link)
	return links

def main():
	""" main function """
	driver = webdriver.Chrome(DRIVER)
	all_links = []

	for i in range(1, MAX_PAGES + 1):
		page = f'{BASE_URL}/p{i}'
		if args.verbose: print(f'acquiring page: {page}')
		links = get_page_links(driver, page)
		for link in links:
			download = link.replace('html', 'pdf')
			filename = download.split('/')[-1]

			if args.verbose: print(f'Downloading: {download}')
			doc = requests.get(download)
			if args.verbose: print(f'Saving: {download}')
			open(os.path.join(args.output_dir, filename), 'wb').write(doc.content)
	driver.quit()

if __name__ == "__main__": main()
