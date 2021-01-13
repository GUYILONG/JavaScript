import requests
import os
from loguru import logger
import pandas as pd
# from GUYLONG.kaigeTask.toexcle import ToExcle

logger.add("youngor.log", encoding="utf8")

gxl = 100


def get_token(appid=None, secret=None):
    url = "https://opentest.youngor.com.cn/api/get_token"
    data = {
        "appid": "364ec50520715734b4c02ddcc295560e",
        "secret": "d02276d8d77af15272f4a364b270717b"
    }
    response = requests.post(url, json=data)
    if response.status_code == 200:
        code = response.json().get("code")
        if code == 0:
            # 表示成功
            data = response.json().get("data")
            access_token = data.get("access_token")
            refresh_token = data.get("refresh_token")
            expires_in = data.get("expires_in")
            return access_token


class base:
    def __init__(self, token) -> None:
        self.token = token

    def request(self, url, method="POST", **kwargs):
        headers = {
            "Authorization": f"Bearer {self.token}"
        }
        kwargs["headers"] = headers
        response = requests.request(method=method, url=url, **kwargs)
        if response.status_code == 200:
            return self.response(response.json())

    def response(self, raw:dict):
        return raw


class shop(base):
    def __init__(self, token) -> None:
        super().__init__(token)

    def request(self, api_name, method, env="prod", **kwargs):
        host_list = {
            "prod": "https://opentest.youngor.com.cn/boeto/qudao/shop/",
            "test": "https://test.youngor.com.cn/boeto/qudao/shop/",
        }
        # env = os.getenv("Path")
        # host_name = "https://opentest.youngor.com.cn/boeto/qudao/shop/"
        # host_name = "https://test.youngor.com.cn/boeto/qudao/shop/"
        host_name = host_list.get(env)
        url = f"{host_name}{api_name}"
        return super().request(url, method=method, **kwargs)

    def list(self, start_date='2019-01-01', end_date='2021-01-11', page=1, size=20):
        api_name = "list"
        data = {
            "page": page,
            "size": size,
            "startDate": start_date,
            "endDate": end_date
        }
        response = self.request(api_name=api_name, method="POST", json=data)
        return response

    def all(self, start_date='2020-01-01', end_date='2021-01-08'):
        page = 1
        page_size = 200
        while 1:
            response = self.list(start_date=start_date,
                                 end_date=end_date, page=page, size=page_size)
            rows = response.get("list")
            if rows:
                page += 1
                for row in rows:
                    yield row
            else:
                logger.error({"page": page})
            if len(rows) < page_size:
                break

    def get(self, shop_id):
        data = {}
        return data

    def create(self, data):
        pass

    def copy(self, shop_id):
        data = self.get(shop_id)
        self.create(data)

    def update(self, shop_id, data):
        pass

    def update_gps(self, shop_id, lat, lng):
        data = self.get(shop_id)
        data["lat"] = lat
        data["lng"] = lng
        self.update(data)


def Rqk():
    token = get_token()
    s = shop(token)
    result = [row for row in s.all()]
    df = pd.DataFrame(result)
    df.to_excel("youngor_mdm_user.xlsx")
    # xiao = s.list().get("list")
    # ToExcle.dict_to_excle("GUYILONG111.xlsx", xiao)

   # logger.debug(s.list())


if __name__ == "__main__":
    Rqk()
