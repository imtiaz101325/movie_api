# -*- coding: utf-8 -*-
from scrapy import Field, Item
from scrapy.loader.processors import TakeFirst, MapCompose

def process_year(year):
    return year[:4]

class MovieItem(Item):
    name = Field(
        output_processor=TakeFirst()
    )
    image = Field(
        output_processor=TakeFirst()
    )
    year = Field(
        input_processor=MapCompose(process_year),
        output_processor=TakeFirst()
    )
    awards = Field(
        output_processor=TakeFirst()
    )
    nominations = Field(
        output_processor=TakeFirst()
    )
    directed_by = Field()
    produced_by = Field()
    screenplay_by = Field()#
    story_by = Field()
    starring = Field()#added for now
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
    src = Field(
        output_processor=TakeFirst()
    )
    srcset = Field(
        output_processor=TakeFirst()
    )
    alt_text = Field(
        output_processor=TakeFirst()
    )