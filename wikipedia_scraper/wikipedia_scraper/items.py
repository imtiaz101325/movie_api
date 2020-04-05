# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

from scrapy import Field, Item

class MovieItem(Item):
    name = Field()
    image = Field()
    year = Field()
    awards = Field()
    nominations = Field()
    directed_by = Field()
    produced_by = Field()
    screenplay_by = Field()
    story_by = Field()
    starring = Field()
    music_by = Field()
    cinematography = Field()
    edited_by = Field()
    production = Field()
    distributed_by = Field()
    release_date = Field()
    running_time = Field()
    country = Field()
    language = Field()
    budget = Field()
    box_office = Field()
    based_on = Field()
    written_by = Field()
    animation_by = Field()
    layouts_by = Field()
    color_process = Field()
    narrated_by = Field()
    backgrounds_by = Field()


class ImageItem(Item):
    src = Field()
    srcset = Field()
    alt_text = Field()