# -*- coding: utf-8 -*-
import scrapy
from scrapy.loader import ItemLoader
from wikipedia_scraper.items import MovieItem, ImageItem

class MoviesSpider(scrapy.Spider):
    name = 'movies'
    allowed_domains = ['en.wikipedia.org']
    start_urls = ['https://en.wikipedia.org/wiki/List_of_Academy_Award-winning_films']

    def parse(self, response):
        table_rows = response.css('.wikitable tr')[1:][:2]
        for row in table_rows:
            cells = row.css('td')
            link = cells[0].css('a')[0]
            award_data = [
                ''.join(cell.css('::text').getall()).strip()
                for cell in cells
            ]

            loader = ItemLoader(item=MovieItem())
            loader.add_value('year', award_data[1])
            loader.add_value('awards', award_data[2])
            loader.add_value('nominations', award_data[3])
            movie_item = loader.load_item()

            yield response.follow(link, self.parse_movie_links, cb_kwargs={ 'movie_item': movie_item })

    def parse_movie_links(self, response, movie_item):
        infoboxRows = response.css('table.infobox')[0].css('tr')
        loader = ItemLoader(movie_item, selector=infoboxRows)

        loader.add_css('name', '.summary::text')

        image_loader = ItemLoader(item=ImageItem(), selector=infoboxRows.css('a.image img'))
        image_loader.add_css('src', '::attr(src)')
        image_loader.add_css('srcset', '::attr(srcset)')
        image_loader.add_css('alt_text', '::attr(alt)')
        loader.add_value('image', image_loader.load_item())
        
        movie_item_fields = [
            'name', 'image', 'year', 'awards',
            'nominations', 'directed_by', 'produced_by',
            'screenplay_by', 'story_by', 'starring', 'music_by',
            'cinematography', 'edited_by', 'production', 'distributed_by',
            'release_date', 'running_time', 'country', 'language',
            'budget', 'box_office', 'based_on', 'written_by',
            'animation_by', 'layouts_by', 'color_process', 'narrated_by',
            'backgrounds_by'
        ]

        for row in infoboxRows:
            header = row.css('th')
            details = row.css('td')

            header_text = header.css('::text').get()
            header_text = header_text and header_text.strip()
            header_as_key = header_text and '_'.join(header_text.lower().split(' '))

            value = None

            plainlist = details.css('.plainlist')
            if plainlist.get() and header_text != 'Release date':
                value = plainlist.css('li::text').getall()
                value += plainlist.css('li > a::text').getall()
            elif header_text == 'Release date':
                value = plainlist.css('li .published::text').getall()
            else:
                value = details.css('::text').get()
                value = value and value.strip()

            if header_as_key in movie_item_fields:
                loader.add_value(header_as_key, value)

        yield loader.load_item()