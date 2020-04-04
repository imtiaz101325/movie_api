# -*- coding: utf-8 -*-
import scrapy


class MoviesSpider(scrapy.Spider):
    name = 'movies'
    allowed_domains = ['en.wikipedia.org']
    start_urls = ['https://en.wikipedia.org/wiki/List_of_Academy_Award-winning_films']

    def parse(self, response):
        relative_movie_links = response.css('.wikitable i a')[34:40]

        yield from response.follow_all(relative_movie_links, self.parse_movie_links)

    def parse_movie_links(self, response):
        infoboxRows = response.css('table.infobox')[0].css('tr')        
        movie = {}

        for row in infoboxRows:
            header = row.css('th')
            details = row.css('td')

            header_text = header.css('::text').get()
            header_text = header_text and header_text.strip()
            details_text = details.css('::text').get()
            details_text = details_text and details_text.strip()

            if header_text and details_text:
                movie[header_text.strip()] = details_text.strip()
            
            name = header.css('.summary::text').get()
            if name:
                movie['name'] = name

            image = details.css('a.image img')
            if image.get():
                srcset = image.css('::attr(srcset)').get()
                src = image.css('::attr(src)').get()
                alt_text = image.css('::attr(alt)').get()
                movie['image'] = {
                    'src': src,
                    'srcset': srcset,
                    'alt_text': alt_text
                }
            
            #TODO: fix broken text
            plainlist = details.css('.plainlist')
            if plainlist.get() and header_text != 'Release date':
                movie[header_text] = plainlist.css('li::text').getall()
                movie[header_text] += plainlist.css('li > a::text').getall()
            
            
            if header_text == 'Release date':
                movie[header_text] = plainlist.css('li .published::text').getall()
        
        yield movie