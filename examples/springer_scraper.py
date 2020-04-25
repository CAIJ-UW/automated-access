""" File: springer_scraper.py
Author: Kevin Dick
Date: 2020-04-25
---
Description: Scrapes the Springer PDFs from 
the Free-Springer-Ebooks.csv file
"""
import os
from bs4 import BeautifulSoup
import requests
import argparse

parser = argparse.ArgumentParser(description='')
parser.add_argument('-i', '--input', required=False, default='Free-Springer-Ebooks.csv',
                    help='input csv containing info on free Spriinger books')
parser.add_argument('-o', '--output_dir', required=False, default='./pdfs/',
                    help='output file')
parser.add_argument('-v', '--verbose', action='store_true',
                    help='increase verbosity')
args = parser.parse_args()

# EXAMPLE: python3 springer_scraper.py -v

def get_download_link(url):
	html = requests.get(url).text
	bs = BeautifulSoup(html)
	for link in bs.find_all('a'):
    		if link.has_attr('href'):
        		if 'content' in link.attrs['href'] and 'pdf' in link.attrs['href']: return 'https://link.springer.com' + link.attrs['href']


def main():
	""" main function """
	if not os.path.exists(args.output_dir): os.mkdir(args.output_dir)
	for book in open(args.input, 'r').readlines():
		title  = '-'.join(book.split(',')[1].split()) 
		author = '-'.join(book.split(',')[2].split())
		year   = '-'.join(book.split(',')[3].split())
		url    = book.split(',')[-1].strip()
		isbn   = url.split('isbn=')[-1]
		filename = '_'.join([title, author, year]) + '.pdf'
		download = get_download_link(url)

		if args.verbose: print('Title: {}\nAuthor: {}\nYear: {}\nURL: {}\nISBN: {}\nFilename: {}\nDownload: {}\n'.format(title, author, year, url, isbn, filename, download))
		
		cmd = 'curl {} --output {}'.format(download, os.path.join(args.output_dir, filename))
		if args.verbose: print('Downloading {}\n'.format(filename))
		os.system(cmd)	

if __name__ == "__main__": main()
