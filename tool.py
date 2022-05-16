from opencc import OpenCC

# 简体转繁体
s2tConverter = OpenCC('s2t')
# 繁体转简体
t2sConverter = OpenCC('t2s')

# 周易简体转繁体
def convert_zhouyi_s2c():
    print('>>转换周易文本...')

    source_list = list()
    target_list = list()
    with open('data/' + '周易' + '.txt', encoding='utf-8') as f:
        source_list = f.readlines()
        size = len(source_list)
        for i in range(0, size):
            string = s2tConverter.convert(source_list[i])
            target_list.append(string)
    with open('data/' + '周易_繁' + '.txt', 'w+', encoding='utf-8') as f:
        size = len(target_list)
        for i in range(0, size):
            f.write(target_list[i])
        
    print('>>完成转换周易文本:',len(target_list))   