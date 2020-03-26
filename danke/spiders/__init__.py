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
        def get_room_info():
            room_info_dict = {
                'room_url': response.url,
                'brother_rooms': []
            }
            room_infos = []
            for room in response.css('div.room-list'):
                infos = []
                for info in room.xpath('descendant-or-self::text()').extract():
                    if not info.startswith('\n'):
                        infos.append(info)
                room_infos.append(infos)
            self.format_room_info(room_infos, room_info_dict)
            room_info_dict['brother_rooms'] = self.get_bro_rooms(response)
            return room_info_dict



        yield {
            'room_info': get_room_info()
        }

    def format_room_info(self, room_infos, room_info_dict):
        for room_info in room_infos:
            if len(room_info) == 1:
                if '：' in room_info[0]:
                    room_info_dict.update([tuple(room_info[0].split('：'))])
            else:
                room_info_dict.update([tuple([room_info[0].split('：')[0], str(room_info[1:])])])
        return room_info_dict

    def list2dict(self, l):
        target = {}
        for i in l:
            target[i] = None
        return target

    def get_bro_rooms(self, response):
        bro_rooms = []
        fl = self.get_bro_room_fields(response)
        for room in response.css('div.room-info-firend div.room_center tbody tr'):
            bro_room_dict = self.list2dict(fl)
            i = 0
            for f in room.css('td'):
                if fl[i] in ['独卫', '淋浴', '阳台']:
                    bro_room_dict[fl[i]] = self.get_rf_status(f)
                else:
                    bro_room_dict[fl[i]] = \
                        self.rm_content_line_in_list(f.xpath('descendant-or-self::text()').extract())
                i += 1
            bro_rooms.append(bro_room_dict)
        return bro_rooms

    def get_rf_status(self, f):
        if f.css('i.text_mute'):
            return "true"
        else:
            return "false"

    def rm_content_line_in_list(self, l):
        r = []
        for i in l:
            r.append(self.rm_content_line(i))
        return r

    def rm_content_line(self, content):
        if content.startswith('\n') or content.endswith('\n'):
            content = content.strip('\n')
        content = content.strip()
        return content

    def get_bro_room_fields(self, response):
        return response.css('div.room-info-firend div.room_center thead tr th::text').extract()
