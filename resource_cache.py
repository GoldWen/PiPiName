# '''
# Author: goldwen
# '''
# # 全局资源cache


exist_name_lib_dict = dict()
zhouyi_line_list = list()

def init_libs():
    print('>>开始初始化资源')
    init_exist_name_lib()
    init_zhouyi_text()
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
    print('>>完成加载名字:',size)

def init_zhouyi_text():
    print('>>加载周易文本...')

    global zhouyi_line_list
    with open('data/' + '周易_繁' + '.txt', encoding='utf-8') as f:
        line_list = f.readlines()
        size = len(line_list)
        for i in range(0, size):
            zhouyi_line_list.append(line_list[i])

        # zhouyi_line_list = f.readlines()
        
    print('>>完成加载周易文本:',len(zhouyi_line_list))   
        
