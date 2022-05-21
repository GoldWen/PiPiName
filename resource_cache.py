import json
# '''
# Author: goldwen
# '''
# # 全局资源cache


exist_name_lib_dict = dict()
# zhouyi_line_list = list()

shijing_json_list = list()
chuci_json_list = list()
tangshi_json_list = list()
songci_json_list = list()

# shijing_line_list = list()
# chuci_line_list = list()
# shijing_json_list = list = list()
# songci_line_list = list()


def init_libs():
    print('>>开始初始化资源')
    init_exist_name_lib()
    # init_zhouyi_text()
    init_json('诗经', 1000, shijing_json_list)
    init_json('楚辞', 1000, chuci_json_list)
    init_json('唐诗', 58000, tangshi_json_list)
    init_json('宋词', 22000, songci_json_list)

    print('>>结束初始化资源')


def init_exist_name_lib():
    print('>>加载名字库...')
    path = 'Chinese_Names'
    with open('data/' + path + '.dat', encoding='utf-8') as f:
        for line in f:
            data = line.split(',')
            name = data[0][1:]
            gender = data[1].replace('\n', '')
            if name in exist_name_lib_dict:
                if gender != exist_name_lib_dict.get(name) or gender == '未知':
                    exist_name_lib_dict[name] = '双'
            else:
                exist_name_lib_dict[name] = gender

    size = len(exist_name_lib_dict)
    print('>>完成加载名字:', size)


def init_json(name, maxsize, json_list):
    print('>>加载', name, '文本...')
    for i in range(0, maxsize, 1000):
        path = 'resources/' + name + '/'+str(i)+'.json'
        with open(path, encoding='utf-8') as f:
            print('>>加载文件', path, '...')
            data = json.loads(f.read())
            size = len(data)
            for j in range(0, size):
                json_list.append(data[j])
    print('>>', name, '一共:', len(json_list), '篇')
