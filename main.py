'''
Author: your name
Date: 2021-10-08 15:16:23
LastEditTime: 2021-10-13 12:37:43
LastEditors: Please set LastEditors
Description: In User Settings Edit
FilePath: \PiPiName\main.py
'''
from config import name_source, last_name, dislike_words, \
    min_stroke_count, max_stroke_count, allow_general, name_validate, \
    check_name, check_name_resource
from name_set import check_resource, get_source, get_names
from wuge import check_wuge_config, get_stroke_list
import flask
import json
from flask import request
from resource_cache import init_libs
from name_condition import NameCondition

server = flask.Flask(__name__)


def contain_bad_word(first_name):
    for word in first_name:
        if word in dislike_words:
            return True
    return False

# server.config['JSON_AS_ASCII'] = False
# @server.route()可以将普通函数转变为服务 登录接口的路径、请求方式


@server.route('/rest/namer/detail', methods=['get', 'post'])
def nameDetail():
    checkName = request.args.get('checkName')
    wuge = check_wuge_config(checkName)
    # ip = request.client_address
    # if request.META.get('HTTP_X_FORWARDED_FOR'):
    #     ip = request.META.get("HTTP_X_FORWARDED_FOR")
    # else:
    #     ip = request.META.get("REMOTE_ADDR")
    # resource = check_resource(checkName)
    # print(resource)
    # 模式，有w和a，w就是写模式，每次都会重新写日志，覆盖之前的日志
    # a是追加模式，默认如果不写的话，就是追加模式
    file_handle = open('log/detail.txt', mode='a', encoding='utf-8')
    file_handle.write('api:/rest/namer/detail'+'；ip:'+'；姓名:'+checkName+'；\n')
    resu = {'code': 200, 'message': 'success', 'data': wuge}
    return json.dumps(resu, ensure_ascii=False)


@server.route('/rest/namer/list', methods=['get', 'post'])
def namelist():
    lastName = request.args.get('lastName')
    gender = request.args.get('gender')
    nameSource = request.args.get('nameSource')
    count = int(request.args.get('count'))
    if count == 5:
        print('count is ', count)
    ip = request.remote_addr
    file_handle = open('log/list.txt', mode='a', encoding='utf-8')
    file_handle.write('api:/rest/namer/list'+'；ip:'+ip+'；姓名:' +
                      lastName+'；性别:'+gender+'；古诗词来源:'+nameSource + '；\n')
    # if len(check_name) == 3:
    #     # 查看姓名配置
    #     check_wuge_config(check_name)
    #     if check_name_resource:
    #        check_resource(check_name)
    #     print(">>输出完毕")
    # else:
    # 起名
    names = []
    dataNames = []
    nameCondition = NameCondition(lastName, gender, nameSource, count)
    print('请求参数:', nameCondition.lastName, nameCondition.gender,
          nameCondition.nameSource, nameCondition.count)
    for i in get_names(nameCondition):
        item = {}
        item['namer'] = str(lastName + i.first_name)
        item['stroke_number1'] = i.stroke_number1
        item['stroke_number2'] = i.stroke_number2
        item['gender'] = i.gender
        item['source'] = i.source
        item['title'] = i.title
        names.append(i)
        dataNames.append(item)
    print(">>输出结果...")
    names.sort()
    print(">>输出完毕，请查看「names.txt」文件")
    data = dataNames
    resu = {'code': 200, 'message': 'success', 'data': data}
    return json.dumps(resu, ensure_ascii=False)


@server.route('/rest/healthy/test', methods=['get', 'post'])
def test_healthy():
    healthy = request.args.get('healthy')
    result = {'code': 200, 'message': 'success', 'data': healthy}
    return json.dumps(result, ensure_ascii=False)


if __name__ == '__main__':
    print("start app")
    init_libs()
    print("libs initialized")
    # 指定端口、host,0.0.0.0代表不管几个网卡，任何ip都可以访问
    server.run(debug=True, port=9021, host='0.0.0.0')
