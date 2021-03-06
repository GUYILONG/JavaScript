# cjdg_user_batch_quit
import requests
import json
from sys import argv
import time

# 接口文档：http://env.xxynet.com/confluence/pages/viewpage.action?pageId=1806128
# 删除用户 data是参数。


def destroy_user(url_type="bms", **data):
    url = {
        "bms": "http://bms.microc.cn/shopguide/api/user/destroy",
        "pre": "http://pre.xxynet.com/shopguide/api/user/destroy",
        "it": "http://it.xxynet.com/shopguide/api/user/destroy",
        "test": "http://test.xxynet.com/shopguide/api/user/destroy",
    }
    result = requests.get(url[url_type], data).content  # 请求接口地址，传送data数据。
    return_result = json.loads(result.decode(
        "utf-8"))  # 把接口返回来的数据转成一种可以使用的格式。json
    # print(return_result)
    return return_result


def destroy4file(accessToken, appSecret):
    f = open("D:\lol\GIAO\pythonxuexi\sys_user_del.txt", "r", encoding="utf8")
    for idx, i in enumerate(f.readlines()):
        data = {}
        data["accessToken"] = accessToken
        data["appSecret"] = appSecret
        data["accounts"] = i.split("\t")[0].strip()
        try_num = 0
        while try_num <= 3:
            result = destroy_user(**data)
            code = (result.get("code"))
            code = int(code) if code else None
            if code == 200:
                print(
                    f"已完成：【成功】：{data['accounts']}删除成功。")
                break
            else:
                if code == 3001:
                    print(
                        f"已完成：【失败】：接口访问频率过快，正在重试第{try_num}次......")
                    time.sleep(10)
                    try_num += 1
                    continue
                else:
                    print(
                        f"已完成：【失败】：{data['accounts']}，删除失败，原因{result}。")
                    break
        if idx % 2 == 0:
            time.sleep(1)
    f.close()


# 请求accesstooke函数
def request_accesstoken(user_name, password, url_type="bms"):
    url = {
        "bms": "http://bms.microc.cn/shopguide/api/auth/logon",
        "pre": "http://pre.xxynet.com/shopguide/api/auth/logon",
        "it": "http://it.xxynet.com/shopguide/api/auth/logon",
        "test": "http://test.xxynet.com/shopguide/api/auth/logon",
    }
    data = {}
    data["loginName"] = user_name
    data["password"] = password
    data["version"] = 1

    post_data = requests.get(url[url_type], data)
    # print(post_data)
    json_str = json.loads(post_data.content.decode("utf-8"))
    if "accessToken" in json_str:
        accessToken = json_str["accessToken"]
    else:
        accessToken = 0
    return accessToken

# 组织用户拍平表生成


def install_org(accessToken, url_type="bms"):
    url = {
        "bms": "http://bms.microc.cn/shopguide/api/org/install",
        "pre": "http://pre.xxynet.com/shopguide/api/org/install",
        "it": "http://it.xxynet.com/shopguide/api/org/install",
        "test": "http://test.xxynet.com/shopguide/api/org/install",
    }
    data = {}
    data["accessToken"] = accessToken
    post_data = requests.get(url[url_type], data)
    # print(post_data)
    return json.loads(post_data.content.decode("utf-8"))


if __name__ == "__main__":
    acc = argv[1] if len(argv) >= 2 else input("请输入后台账号:")
    pwd = argv[2] if len(argv) >= 3 else input("请输入密码:")
    accessToken = request_accesstoken(acc, pwd)
    if accessToken != 0:
        app_id = accessToken.split("_")[1]
        appSecret = argv[3] if len(argv) >= 4 else input("请输入appSecret:")
        destroy4file(accessToken, appSecret)
        print("生效数据成功：", install_org(accessToken))
    else:
        print("用户名密码错误。")
