import json
import re
import random

from opencc import OpenCC

from name import Name
from stroke_number import get_stroke_number
# from resource_cache import zjw

from resource_cache import shijing_json_list, chuci_json_list, tangshi_json_list, songci_json_list
from resource_cache import exist_name_lib_dict as exist_name
from wuge import check_wuge_config, get_stroke_list
from config import name_source, last_name, dislike_words, \
    min_stroke_count, max_stroke_count, allow_general, name_validate, \
    check_name, check_name_resource


# 简体转繁体
s2tConverter = OpenCC('s2t')
# 繁体转简体
t2sConverter = OpenCC('t2s')


def get_names(nameCondition):
    lastName = nameCondition.lastName
    source = int(nameCondition.nameSource)
    stroke_list = get_stroke_list(lastName, allow_general)
    # print(stroke_list)
    names = set()

    if source == 2:
        print('>>从楚辞生成名字...一共', len(chuci_json_list), '篇')
        get_name_txt_from_jsons(
            chuci_json_list, stroke_list, names, nameCondition)
    elif source == 1:
        print('>>从诗经生成名字...一共', len(shijing_json_list), '篇')
        get_name_txt_from_jsons(
            shijing_json_list, stroke_list, names, nameCondition)
    elif source == 5:
        print('>>从唐诗生成名字...一共', len(tangshi_json_list), '篇')
        get_name_txt_from_jsons(
            tangshi_json_list, stroke_list, names, nameCondition)
    elif source == 7:
        print('>>从宋词生成名字...一共', len(songci_json_list), '篇')
        get_name_txt_from_jsons(
            songci_json_list, stroke_list, names, nameCondition)
    return names

# def get_name_txt_from_lines(line_list, names, nameCondition):
#     return;


def get_name_txt_from_jsons(json_list, stroke_list, names, nameCondition):
    gender = nameCondition.gender

    json_length = len(json_list)
    start = random.randint(0, json_length-1)
    print("start from ", start)

    for i in range(0, json_length):
        # 随机从第src_idx篇开始
        src_idx = (start+i) % json_length
        poet = json_list[src_idx]
        sentences = poet['content']
        title = poet['title']
        sentence_len = len(sentences)

        for j in range(0, sentence_len):
            sentence = sentences[j]
            # 转繁体
            sentence = s2tConverter.convert(sentence)
            # sentences = re.split('！？，。,.?! \n', string)
            sentence = sentence.strip()

            # 转换笔画数
            strokes = list()
            for ch in sentence:
                if is_chinese(ch):
                    strokes.append(get_stroke_number(ch))
                else:
                    strokes.append(0)

               # 判断是否包含指定笔画数
            for stroke in stroke_list:
                if stroke[0] in strokes and stroke[1] in strokes:
                    index0 = strokes.index(stroke[0])
                    index1 = strokes.index(stroke[1])
                    if index0 < index1:
                        name0 = sentence[index0]
                        name1 = sentence[index1]
                        name = buildName(name0 + name1, title, sentence)

                        if name.first_name == '':
                            continue

                        # 如果简体的笔画数超出限定范围，则不要
                        if name.stroke_number1 < min_stroke_count and name.stroke_number1 > max_stroke_count and \
                                name.stroke_number2 < min_stroke_count and name.stroke_number2 > max_stroke_count:
                            continue

                        # 性别过滤
                        if name_validate and gender != "" and name.gender != gender and name.gender != "双" and name.gender != "未知":
                            continue

                        # 不喜欢字过滤
                        if contain_bad_word(name.first_name):
                            continue

                        names.add(name)

                    if len(names) == nameCondition.count:
                        return


def get_name_txt_from_lines(line_list, names, nameCondition):
    stroke_list = get_stroke_list(nameCondition.lastName, allow_general)

    size = len(line_list)
    progress = 0
    for i in range(0, size):
        # for i in range(0, 50):
        # 生成进度
        if (i + 1) * 100 / size - progress >= 10:
            progress += 10
            print('>>正在生成名字...' + str(progress) + '%')
        string = line_list[i]
        if re.search(r'\w', string) is None:
            continue
        string_list = re.split('！？，。,.?! \n', string)
        # print('string_list', string_list)
        check_and_add_names(names, string_list, stroke_list, nameCondition)
        if len(names) == nameCondition.count:
            break


def get_source(source, validate, stroke_list, gender):
    print(stroke_list)
    # exist_name = dict()
    # if validate:
    #     print('>>加载名字库...')
    #     get_name_valid('Chinese_Names', exist_name)

    names = set()
    # 默认
    if source == 0:
        get_name_dat('Chinese_Names', names, stroke_list)
    # 诗经
    elif source == 1:
        print('>>加载诗经...')
        get_name_json('诗经', names, 'content', stroke_list)
    # 楚辞
    elif source == 2:
        print('>>加载楚辞...')
        get_name_txt('楚辞', names, stroke_list)
    # 论语
    elif source == 3:
        print('>>加载论语...')
        get_name_json('论语', names, 'paragraphs', stroke_list)
    # 周易
    elif source == 4:
        print('>>从周易生成名字...一共', len(zhouyi_line_list), '行')
        # get_name_txt('周易', names, stroke_list)
        get_name_txt_from_lines(zhouyi_line_list, names, stroke_list, gender)
    # 唐诗
    elif source == 5:
        print('>>加载唐诗...')
        for i in range(0, 58000, 1000):
            get_name_json('唐诗/poet.tang.' + str(i), names,
                          'paragraphs', stroke_list)
    # 宋诗
    elif source == 6:
        print('>>加载宋诗...')
        for i in range(0, 255000, 1000):
            get_name_json('宋诗/poet.song.' + str(i), names,
                          'paragraphs', stroke_list)
    # 宋词
    elif source == 7:
        print('>>加载宋词...')
        for i in range(0, 22000, 1000):
            get_name_json('宋词/ci.song.' + str(i), names,
                          'paragraphs', stroke_list)
    else:
        print('词库号输入错误')

    print('>>筛选名字...')
    # 检查名字是否存在并添加性别
    if validate:
        if source != 0:
            names = get_intersect(names, exist_name)

    return names


def get_intersect(names, exist_name):
    result = set()
    for i in names:
        if i.first_name in exist_name.keys():
            i.gender = exist_name[i.first_name]
            result.add(i)
    return result


# deprecated
# 加载名字库
def get_name_valid(path, exist_names):
    with open('data/' + path + '.dat', encoding='utf-8') as f:
        for line in f:
            data = line.split(',')
            name = data[0][1:]
            gender = data[1].replace('\n', '')
            if name in exist_names:
                if gender != exist_names.get(name) or gender == '未知':
                    exist_names[name] = '双'
            else:
                exist_names[name] = gender


def get_name_dat(path, names, stroke_list):
    with open('data/' + path + '.dat', encoding='utf-8') as f:
        line_list = f.readlines()
        size = len(line_list)
        progress = 0
        for i in range(0, size):
            # 生成进度
            if (i + 1) * 100 / size - progress >= 5:
                progress += 5
                print('>>正在生成名字...' + str(progress) + '%')
            data = line_list[i].split(',')
            if len(data[0]) == 2:
                name = data[0]
            else:
                name = data[0][1:]
            # 转繁体
            name = s2tConverter.convert(name)
            gender = data[1].replace('\n', '')
            if len(name) == 2:
                # 转换笔画数
                strokes = list()
                strokes.append(get_stroke_number(name[0]))
                strokes.append(get_stroke_number(name[1]))
                # 判断是否包含指定笔画数
                for stroke in stroke_list:
                    if stroke[0] == strokes[0] and stroke[1] == strokes[1]:
                        names.add(Name(name, '', gender))


def get_name_txt(path, names, stroke_list):
    with open('data/' + path + '.txt', encoding='utf-8') as f:
        line_list = f.readlines()
        size = len(line_list)
        progress = 0
        for i in range(0, size):
            # 生成进度
            if (i + 1) * 100 / size - progress >= 10:
                progress += 10
                print('>>正在生成名字...' + str(progress) + '%')
            # 转繁体
            string = s2tConverter.convert(line_list[i])
            if re.search(r'\w', string) is None:
                continue
            string_list = re.split('！？，。,.?! \n', string)


def get_name_json(path, names, column, stroke_list):
    with open('data/' + path + '.json', encoding='utf-8') as f:
        data = json.loads(f.read())
        size = len(data)
        progress = 0
        for j in range(0, size):
            # 生成进度
            if (j + 1) * 100 / size - progress >= 10:
                progress += 10
                print('>>正在生成名字...' + str(progress) + '%')
            for string in data[j][column]:
                # 转繁体
                string = s2tConverter.convert(string)
                sentences = re.split('！？，。,.?! \n', string)
                check_and_add_names(
                    names, sentences,  stroke_list, nameCondition)


def check_and_add_names(names, sentences, stroke_list, nameCondition):
    for sentence in sentences:
        sentence = sentence.strip()
        check_and_add_names_from_sentence(
            names, sentence, stroke_list, nameCondition)
        if len(names) == nameCondition.count:
            break


def check_and_add_names_from_sentence(names, sentence, stroke_list, nameCondition):
    gender = nameCondition.gender
    # 转换笔画数
    strokes = list()
    for ch in sentence:
        if is_chinese(ch):
            strokes.append(get_stroke_number(ch))
        else:
            strokes.append(0)
    # 判断是否包含指定笔画数
    for stroke in stroke_list:
        if stroke[0] in strokes and stroke[1] in strokes:
            index0 = strokes.index(stroke[0])
            index1 = strokes.index(stroke[1])
            if index0 < index1:
                name0 = sentence[index0]
                name1 = sentence[index1]
                name = buildName(name0 + name1, sentence)

                if name.first_name == '':
                    continue

                # 如果简体的笔画数超出限定范围，则不要
                if name.stroke_number1 < min_stroke_count and name.stroke_number1 > max_stroke_count and \
                        name.stroke_number2 < min_stroke_count and name.stroke_number2 > max_stroke_count:
                    continue

                # 性别过滤
                if name_validate and gender != "" and name.gender != gender and name.gender != "双" and name.gender != "未知":
                    continue

                # 不喜欢字过滤
                if contain_bad_word(name.first_name):
                    continue

                names.add(name)

            if len(names) == nameCondition.count:
                break


def buildName(firstName, title, sentence):
    name = Name(firstName, title, sentence, '')
    if name_validate:
        if firstName in exist_name.keys():
            name.gender = exist_name[firstName]
        else:
            name.first_name = ''
    return name


# 判断是否为汉字
def is_chinese(uchar):
    if u'\u4e00' <= uchar <= u'\u9fa5':
        return True
    else:
        return False


def check_resource(name):
    if len(name) != 3:
        return
    print('正在生成名字来源...\n')
    check_name_json('诗经', name, 'content')
    check_name_txt('楚辞', name)
    check_name_json('论语', name, 'paragraphs')
    check_name_txt('周易', name)
    for i in range(0, 58000, 1000):
        check_name_json('唐诗/poet.tang.' + str(i), name, 'paragraphs')
    for i in range(0, 255000, 1000):
        check_name_json('宋诗/poet.song.' + str(i), name, 'paragraphs')
    for i in range(0, 22000, 1000):
        check_name_json('宋词/ci.song.' + str(i), name, 'paragraphs')


def check_name_json(path, name, column):
    with open('data/' + path + '.json', encoding='utf-8') as f:
        data = json.loads(f.read())
        size = len(data)
        for i in range(0, size):
            poem = data[i]
            for string in poem[column]:
                string_list = re.split('！？，。,.?! \n', string)
                title = path
                if path == '诗经':
                    title = '诗经 ' + poem['title'] + ' ' + \
                        poem['chapter'] + ' ' + poem['section']
                elif path == '论语':
                    title = '论语 ' + poem['chapter']
                elif path.startswith('唐诗'):
                    title = '唐诗 ' + poem['title'] + ' ' + poem['author']
                elif path.startswith('宋诗'):
                    title = '宋诗 ' + poem['title'] + ' ' + poem['author']
                elif path.startswith('宋词'):
                    title = '宋词 ' + poem['rhythmic'] + ' ' + poem['author']
                check_name_resource(title, name, string_list)


def check_name_txt(path, name):
    with open('data/' + path + '.txt', encoding='utf-8') as f:
        line_list = f.readlines()
        size = len(line_list)
        for i in range(0, size):
            if re.search(r'\w', line_list[i]) is None:
                continue
            string_list = re.split('！？，。,.?! \n', line_list[i])
            check_name_resource(path, name, string_list)


def check_name_resource(title, name, string_list):
    for sentence in string_list:
        if title.startswith('唐诗') or title.startswith('宋诗'):
            # 转简体
            title = t2sConverter.convert(title)
            sentence = t2sConverter.convert(sentence)
        if name[1] in sentence and name[2] in sentence:
            index0 = sentence.index(name[1])
            index1 = sentence.index(name[2])
            if index0 < index1:
                # return {'resource': {
                #     'title': title,
                #     'sentence': sentence.strip().replace(name[1], '「' + name[1] + '」') \
                #       .replace(name[2], '「' + name[2] + '」') + '\n'
                # }}
                print(title)
                print(sentence.strip().replace(name[1], '「' + name[1] + '」')
                      .replace(name[2], '「' + name[2] + '」') + '\n')


def contain_bad_word(first_name):
    for word in first_name:
        if word in dislike_words:
            return True
    return False
