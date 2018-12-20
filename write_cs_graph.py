import json

adj_list = json.load(open('./adj_list.json'))
url_dict = json.load(open('./url_dict.json'))
url_dict_rev = json.load(open('./url_dict_reverse.json'))

cs_writer = open('./CSgraph.txt', 'w')
for id_ in adj_list:
    links = adj_list[id_]
    for link in links:
        cs_writer.write(url_dict_rev[id_] + '\t' + url_dict_rev[link] + '\n')

cs_writer.close()
