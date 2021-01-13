from GIAO.pythonxuexi.gxl import *
from loguru import logger
import requests

class CjdgApi():
    """超级导购的api"""

    def __init__(self,):
        self.token = self.web_token()

    def web_token(self):
        params = {"loginName": "gagauser@gaga", "password": "555666888", "version": 1}
        url = "http://bms.chaojidaogou.com/shopguide/api/auth/logonweb"
        return RequestApi.api(url, params=params).get("token")

    def shop_list(self,data):
        url = "http://bms.chaojidaogou.com/shopguide/orgshopList.jhtml?isShowCreate=1"
        data = {
            "page": 1,
            "rows": 20
        }
        headers = {"Cookie": "accessToken=" + str(self.token)}

        return RequestApi.api(url=url, data=data, headers=headers, method='post')
#-
