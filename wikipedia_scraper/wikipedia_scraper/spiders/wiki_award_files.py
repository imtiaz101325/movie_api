# -*- coding: utf-8 -*-
import scrapy
from scrapy.linkextractors import LinkExtractor
from scrapy.spiders import CrawlSpider, Rule


class WikiAwardFilesSpider(CrawlSpider):
    name = 'wiki_award_files'
    allowed_domains = ['en.wikipedia.org']
    start_urls = ['https://en.wikipedia.org/wiki/List_of_Academy_Award-winning_films/']

    rules = (
        Rule(LinkExtractor(allow=r'Items/'), callback='parse_item', follow=True),
    )

    def parse_item(self, response):
        relative_movie_links = response.css('.wikitable.sortable a:nth-child(2n+1)')

        yield from response.follow_all(relative_movie_links, self.parse_movie_links)

    def parse_movie_links(self, response):
        pass