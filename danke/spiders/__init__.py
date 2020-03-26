# This package will contain the spiders of your Scrapy project
#
# Please refer to the documentation for information on how to create and manage
# your spiders.
import scrapy


class DanKeSpider(scrapy.Spider):
    name = "danke"
    r_urls = []

    def start_requests(self):
        urls = [
            'https://www.danke.com/room/wx'
        ]
        for url in urls:
            yield scrapy.Request(url=url, callback=self.parse)

    def parse(self, response):
        room_links = response.css('div.r_lbx_cena a')
        yield from response.follow_all(room_links, self.parse_room_info)
        pagination_links = response.css('div.page a')
        yield from response.follow_all(pagination_links, self.parse)
        # for r_url in response.css('div.r_lbx div.r_lbx_cena a::attr(href)').getall():
        #     self.r_urls.append(r_url)

    def parse_room_info(self, response):
        def extract_from_css(ele, query=''):
            query = query + ' ::text'
            ele_content = ele.css(query).get()
            return ele_content.strip() if ele_content else ele_content

        def get_room_info():
            room_info = {
                response.css('.room-price .price-list label::text').get():
                    response.css('span .room-price-sale::text').get() + \
                    response.css('.room-price-sale em::text').get(),
            }
            infos = response.css('.room-list-box .room-detail-box .room-list').getall()
            for info in infos:
                key, value = info.css('label::text').get().strip().split('：')
                if key == '区域':
                    value = info.css('label div::attr(title)')

        yield {
            'room_url': response.url,
            'room_info': get_room_info(),
            'room_friends': get_room_friends()
        }
