import scrapy
import time
import json

class listingSpider(scrapy.Spider):
    name = "rentals"

    def start_requests(self):
        urls = [
            'https://vancouver.craigslist.ca/d/apts-housing-for-rent/search/apa'#,
            #'https://vancouver.craigslist.ca/d/sublets-temporary/search/sub',
            #'https://vancouver.craigslist.ca/d/rooms-shares/search/roo'
        ]
        for url in urls:
            yield scrapy.Request(url=url, callback=self.parse_link_page)

    def parse_link_page(self, response):
        for ad in response.css("div.content li.result-row"):
            link = ad.css("a::attr(href)").extract_first()
            yield response.follow(link, callback=self.parse_rental_page)

        next_page = response.css("div.paginator a.next::attr(href)").extract_first()
        if next_page is not None:
            next_page = response.urljoin(next_page)
            yield scrapy.Request(next_page, callback=self.parse_link_page)

    def parse_rental_page(self, response):
        def extract_with_css(query, i=0, all=False):
            extracted_data = response.css(query).extract()
            if len(extracted_data)>0 and len(extracted_data)>=(i+1) and not all:
                return extracted_data[i]
            elif all:
                return extracted_data
            else:
                return None

        data_line = {
            'title': extract_with_css("title::text"),
            'id': extract_with_css("div.postinginfos p.postinginfo::text",0).replace("post id: ",""),
            'url': response.url,
            'posted': extract_with_css("div.postinginfos p.postinginfo time::attr(datetime)",0),
            'updated': extract_with_css("div.postinginfos p.postinginfo time::attr(datetime)",1),
            'user data': extract_with_css("#postingbody::text"),
            'latitude': extract_with_css("div.mapbox #map::attr(data-latitude)"),
            'longitude': extract_with_css("div.mapbox #map::attr(data-longitude)"),
            'accuracy': extract_with_css("div.mapbox #map::attr(data-accuracy)"),
            'image_urls': extract_with_css("a.thumb img::attr(src)", all=True),
            'attrs': extract_with_css("div.mapAndAttrs p.attrgroup span::text", all=True),
            'available': extract_with_css("div.mapAndAttrs p.attrgroup span.property_date::attr(data-date)")
        }

        yield data_line
