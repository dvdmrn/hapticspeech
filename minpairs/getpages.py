from lxml import html
import requests
import re


def findMinPair(s):
	match = re.findall('[a-z]+ [a-z]+', s)
	if match:
		return match
	else:
		return ["DELETETHIS"]


def getMinPairs(url):
	page = requests.get(url)
	tree = html.fromstring(page.content)
	minpairList = tree.xpath('//pre/text()')
	title = tree.xpath('//h1/text()')
	if len(minpairList):
		return findMinPair(minpairList[0])
	else:
		return []



