import config
import requests
import json
import re

getMessage = ""

def getFund(fundCode):
    global getMessage
    url = "http://fundgz.1234567.com.cn/js/%s.js"%fundCode
    # 浏览器头
    headers = {'content-type': 'application/json',
           'User-Agent': 'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:22.0) Gecko/20100101 Firefox/22.0'}
    r = requests.get(url, headers=headers)
    # 返回信息
    if r.status_code != 200:
        getMessage += "该基金代码错误"
        return 0
    text = r.text
    # jzrq：净值日期    dwjz：单位净值    gsz：估算净值    gszzl：估算涨幅
    # 正则表达式，将结果转化为json
    pattern = r'^jsonpgz\((.*)\)'
    # 查找结果
    search = re.findall(pattern, text)
    # 遍历结果
    if search[0] == '':
        getMessage += "获取不到基金代码" + fundCode + "信息"
        return 0
    for i in search:
        data = json.loads(i)
    # print("{}，估算涨幅：{}，估算净值: {}，估值时间：{}".format(data['name'], data['gszzl'], data['gsz'], data['gztime']))
    getMessage += data['name'] + "，估算涨幅：" + data['gszzl'] + "，估算净值:" + data['gsz'] + "，估值时间：" + data['gztime']

def sendMessage(message):
    url = "https://qyapi.weixin.qq.com/cgi-bin/gettoken"
    data = {
            'corpid': config.corpid, 
            'corpsecret': config.corpsecret
            }
    r = requests.get(url, data)
    accessToken = r.json()['access_token']
    headers = {'content-type': 'application/json'}
    data = {
            'touser': config.touser,
            'msgtype': 'text',
            'agentid': config.agentid,
            'text': {
                "content": message
                    }
            }
    urlS = "https://qyapi.weixin.qq.com/cgi-bin/message/send?access_token=" + accessToken
    s = requests.post(urlS, headers = headers, json = data)
    print(s.json())

def main():
    global getMessage
    for index in range(len(config.fundCode)):
        if config.fundCode[index] == '':
            getMessage += "基金代码为空"
        else:
            getFund(config.fundCode[index])
        if index != len(config.fundCode)-1:
            getMessage += "\n"
    sendMessage(getMessage)    

# 提供给腾讯云函数调用的启动函数
def main_handler(event, context):
    try:
        main()
    except Exception as e:
        raise e
    else:
        return 'success'


if __name__ == '__main__':
    # print(extension)
    print(main_handler({}, {}))
