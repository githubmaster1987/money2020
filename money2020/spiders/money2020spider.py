# -*- coding: utf-8 -*-
import scrapy
import random, base64
import re
import os
import json
import sys
import csv
import proxylist
import useragent
from scrapy.http import Request, FormRequest
from money2020.items import Money2020Item


class Money2020spiderSpider(scrapy.Spider):
	name = 'money2020spider'
	# allowed_domains = ['us.money2020.com']
	start_url = 'https://us.money2020.com/2017-speakers-text-list'

	proxy_lists = proxylist.proxys
	useragent_lists = useragent.user_agent_list

	def set_proxies(self, url, callback, headers=None):
		if headers:
			req = Request(url=url, callback=callback,dont_filter=True, headers=headers)
		else:
			req = Request(url=url, callback=callback,dont_filter=True)

		proxy_url = random.choice(self.proxy_lists)
		user_pass=base64.encodestring('amagca:Vztgn8fJ').strip().decode('utf-8')
		req.meta['proxy'] = "http://" + proxy_url
		req.headers['Proxy-Authorization'] = 'Basic ' + user_pass

		user_agent = random.choice(self.useragent_lists)
		req.headers['User-Agent'] = user_agent
		return req

	def __init__(self, method ="", *args, **kwargs):
		super(Money2020spiderSpider, self).__init__(*args, **kwargs)
		self.method = method

	def start_requests(self):
		req = self.set_proxies(self.start_url, self.parse_url)
		yield req

	def parse_url(self, response):
		speaker_lists = response.xpath("//div[@class='speakers-keynote-block']")
		print "Total Block = ", len(speaker_lists)

		div_list = speaker_lists[1].xpath("div[contains(@class, 'sponsors-text-list-dynamic-wrapper')]")
		print "Div List Len = ", len(div_list)

		href_links = []
		for div_item in div_list:
			sub_speaker_list = div_item.xpath(".//div[contains(@class, 'w-col-3')]")

			print "**************************"
			print "Speaker List Len = ", len(sub_speaker_list)

			for speaker_item in sub_speaker_list:
				href_link = response.urljoin(speaker_item.xpath("a/@href").extract_first().strip())
				name = speaker_item.xpath("a/text()").extract_first().strip()

				href_links.append(href_link)
		
		print "Total = ", len(href_links)

		for i, href_link in enumerate(href_links):
			href_link = "https://us.money2020.com/speakers/jay-fulcher"
			req = self.set_proxies(href_link, self.parse_detail)
			yield req
			return

	def parse_detail(self, response):
		# print "**********", response.url

		col2_div = response.xpath("//div[contains(@class, 'speaker-detail-col2')]")
		col1_div = response.xpath("//div[contains(@class, 'speaker-detail-col1')]")

		name_str = col2_div.xpath("h1/text()").extract_first().strip().encode("utf8")
		title_str = col2_div.xpath(".//div[@class='speaker-detail-title']/text()").extract_first().strip().encode("utf8")
		try:
			company_str = col2_div.xpath("a[@class='speaker-detail-company-link']/text()").extract_first().strip().encode("utf8")
		except:
			company_str = col2_div.xpath("div[@class='speaker-detail-company-no-link']/text()").extract_first().strip().encode("utf8")

		bio_str_list = col2_div.xpath("div[contains(@class, 'speaker-detail-bio')]//text()").extract()
		bio_str = " ".join(bio_str_list).encode("utf8")

		session_item_list = col1_div.xpath(".//div[contains(@class, 'speaker-detail-dynamic-list-sessions')]")
		session_list = []

		# print "Session=", len(session_item_list)

		for session_item in session_item_list:
			session_item_str = session_item.xpath(".//a[@class='speaker-detail-session-information']/text()").extract_first()
			
			if session_item_str != None:
				session_list.append(session_item_str.strip().encode("utf8"))

		# print session_list

		item = Money2020Item()
		item["name"] = name_str
		item["title"] = title_str
		item["company"] = company_str
		item["bio"] = bio_str
		item["session"] = "\r\n".join(session_list)
		item["url"] = response.url

		yield item
		# print item