# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

from scrapy import Item, Field

class TripAdvisorHotelItem(Item):
     # define the fields for your item here like:
    HOTEL_NAME = Field()
    RATING =  Field()
    REVIEW_LEVEL =  Field()
    REVIEW_COUNT =  Field()
    AMENTINIES =  Field()
    FEATURES =  Field()
    HOTEL_PAGE_URL =  Field()
    HOTEL_LISTING_PAGE_URL =  Field()
    HOTEL_LOCATION = Field()
    CONTACT_NUMBER = Field()
    NEARLY_LANDMARK_POINTS = Field()