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

        def get_all_rooms(response, query):
            room_map = {
                0: 'room_desc',
                1: 'room_owner',
                2: 'room_size',
                3: 'rest_room',
                4: 'shower',
                5: 'balcony',
                6: 'rental'
            }
            friends = []
            for tr in response.css(query):
                friend = {}
                index = 0
                for td in tr.css('td'):
                    if index == 0:
                        friend[room_map[index]] = \
                            (extract_from_css(td, 'strong'),
                             extract_from_css(td, 'span'),
                             extract_from_css(td, 'a'),
                             td.css('a::attr(href)').get())
                    else:
                        friend[room_map[index]] = extract_from_css(td)
                    index += 1
                friends.append(friend)
            return friends

        yield {
            'room_num': response.css('label .instalment::text').getall()[-1],
            'room_url': response.url,
            'room_name': extract_from_css(response, '.room-name h1'),
            'room_price': extract_from_css(response, '.room-price-sale'),
            'floor': response.css('.room-detail-box ').css('.room-list')[1].css('label::text').get(),
            'room_info_friend': get_all_rooms(response, '.room-info-firend .room_center table tbody tr')
        }
