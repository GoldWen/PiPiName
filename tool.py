from opencc import OpenCC

# 简体转繁体
s2tConverter = OpenCC('s2t')
# 繁体转简体
t2sConverter = OpenCC('t2s')


def convert_tang_s2c():
    for i in range(0, 58000, 1000):
        src_file = 'data/唐诗/poet.tang.'+str(i)+'.json'
        dst_file = 'resources/唐诗/'+str(i)+'.json'
        print('>>转换文件:', src_file)

        source_list = list()
        target_list = list()
        with open(src_file, encoding='utf-8') as f:
            source_list = f.readlines()
            size = len(source_list)
            for j in range(0, size):
                string = convert_str(source_list[j])
                target_list.append(string)
        with open(dst_file, 'w+', encoding='utf-8') as f:
            size = len(target_list)
            for j in range(0, size):
                f.write(target_list[j])


def convert_songci_s2c():
    for i in range(0, 22000, 1000):
        src_file = 'data/宋词/ci.song.'+str(i)+'.json'
        dst_file = 'resources/宋词/'+str(i)+'.json'
        print('>>转换文件:', src_file)

        source_list = list()
        target_list = list()
        with open(src_file, encoding='utf-8') as f:
            source_list = f.readlines()
            size = len(source_list)
            for j in range(0, size):
                string = convert_str(source_list[j])
                target_list.append(string)
        with open(dst_file, 'w+', encoding='utf-8') as f:
            size = len(target_list)
            for j in range(0, size):
                f.write(target_list[j])


def convert_str(src):
    dst = src.replace('paragraphs', 'content')
    dst = dst.replace('rhythmic', 'title')
    
    return dst


convert_tang_s2c()
convert_songci_s2c()
