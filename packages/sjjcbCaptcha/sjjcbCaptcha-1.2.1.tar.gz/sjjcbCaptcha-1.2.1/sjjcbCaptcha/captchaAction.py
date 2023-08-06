# -*- coding: utf-8 -*-



"""
Created on  01.22 15:11:25 2021
@author: fanzijian
describe:滑块验证码检测接口
configuration：linux,py3.7
"""

import json

import requests


class ComplexEncoder(json.JSONEncoder):
    """
    对象序列化
    """

    def default(self, obj):
        return obj.__dict__


def send_post(rest_url, params):
    """
    以json发送post请求
    Args:
        rest_url: 请求地址
        params: 参数

    Returns:

    """
    # headers = {"User-Agent": "okhttp/3.11.0 Zuiyou/4.7.1"}
    headers = {'Content-type': 'application/json'}
    json_data = json.dumps(params, ensure_ascii=False, cls=ComplexEncoder)
    byte_data = json_data.encode('utf-8')
    response_text = requests.post(url=rest_url, data=byte_data, headers=headers).text
    return response_text

class captchaAction():

  def send_get(rest_url):
    """
    以json发送post请求
    Args:
        rest_url: 请求地址
        params: 参数

    Returns:

    """
    headers = {'Content-type': 'application/json'}
    #headers = {'Content-type': 'application/x-www-form-urlencoded'}
    response_text = requests.get(url=rest_url, headers=headers).text
    return response_text



class ResponseErrException(Exception):
    """
    异常信息解决
    """
    def __init__(self, value):
        self.value = value

    def __str__(self):
        return self.value


def parse_json(json_rst):
    """
    解析json，获取返回消息
    Args:
        json_rst:
    Returns:
    """
    if json_rst is None or json_rst == "":
        raise ResponseErrException("返回消息为空")
    try:
        json_data = json.loads(json_rst, encoding="utf-8")
    except Exception as e:
        raise ResponseErrException("解析异常，返回消息：" + json_rst)
    status_msg = json_data["message"]
    if "200" != json_data["code"]:
        raise ResponseErrException(status_msg)
    return json_data["data"]


if __name__ == "__main__":
    hklength = "400"
    tokenid = "12345678909876543"
    rst_json = captchaAction.send_get("http://192.168.220.10:30306/img/check?hklength=" + hklength + "&tokenid=" +tokenid+" ")
    try:
        json_data = json.dumps(rst_json, ensure_ascii=False, cls=ComplexEncoder)
        print("java 返回值 => : " +json_data)
    except ResponseErrException as e:
        print("err:" + e.value)