import json


result = {}
with open('data', 'r') as fd:
    lines = fd.readlines()
    for line in lines:
        key, value = line.split('：')
        result[key] = value.strip('\n')
json_str = json.dumps(result, indent=4, ensure_ascii=False).encode('utf-8')
print(json_str.decode())


str = "房间	室友	建筑面积	独卫	淋浴	阳台	租金"
for i in str.split(" "):
    print()
    print(str + '\n')


info_strs = [['\n                            ', '建筑面积：约14㎡（以现场勘察为准）', '\n                        '],
['\n                            ', '编号：158707-C', '\n                        '],
['\n                            ', '\n                                户型：3室1卫\n                                                                    ', '合', '\n                                                            ', '\n                        '],
['\n                                                            ', '付款：', '可支持分期付', '[不收中介费]', '\n                                                    '],
['\n                            ', '朝向：南', '\n                        '],
['\n                            ', '房屋核验统一编码：', '190614422680', '\n                        '],
['\n                            ', '楼层：8/32层', '\n                        '],
['\n                            ', '\n                                ', '区域：', '\n                                ', '\n                                                                            ', '滨湖区', '\n                                                                        ', '塘铁桥', '\n                                    ', '观山名筑', '\n                                ', '\n                                ', '查看地图', '\n                            ', '\n                        '],
['\n\n                            ', '地铁：距地铁1号线塘铁桥站800米', '\n                        ']]
result_l = []
for info_str in info_strs:
    item_l = []
    for item in info_str:
        if not item.startswith('\n'):
            item_l.append(item)
    result_l.append(item_l)
print(result_l)
# [['建筑面积：约14㎡（以现场勘察为准）'],
#  ['编号：158707-C'],
#  ['合'],
#  ['付款：', '可支持分期付', '[不收中介费]'],
#  ['朝向：南'],
#  ['房屋核验统一编码：', '190614422680'],
#  ['楼层：8/32层'],
#  ['区域：', '滨湖区', '塘铁桥', '观山名筑', '查看地图'],
#  ['地铁：距地铁1号线塘铁桥站800米']]

str_dict = {}
str_dict.update('付款：', '可支持分期付')
print(str_dict)
