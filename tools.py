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