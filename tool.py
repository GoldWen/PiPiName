from opencc import OpenCC

# 简体转繁体
s2tConverter = OpenCC('s2t')
# 繁体转简体
t2sConverter = OpenCC('t2s')

# 周易简体转繁体


def convert_zhouyi_s2c():
    convert_s2c('周易', 'txt')


def convert_chuci_s2c():
    convert_s2c('楚辞', 'txt')


def convert_shijing_s2c():
    convert_s2c('诗经',  'json')

def convert_s2c(prop, ftype):
    print('>>转换', prop, '文本...')

    source_list = list()
    target_list = list()
    with open('data/' + prop + '.' + ftype, encoding='utf-8') as f:
        source_list = f.readlines()
        size = len(source_list)
        for i in range(0, size):
            string = s2tConverter.convert(source_list[i])
            target_list.append(string)
    with open('data/' + prop+'_繁.' + ftype, 'w+', encoding='utf-8') as f:
        size = len(target_list)
        for i in range(0, size):
            f.write(target_list[i])

    print('>>完成转换', prop, '文本:', len(target_list))


convert_shijing_s2c()