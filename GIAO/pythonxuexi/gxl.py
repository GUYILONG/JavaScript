from logging import exception
import requests
import pandas as pd
from loguru import logger

logger.add("ygezuzhu.log",encoding="utf8")


class ToExcle():
    """生成exlce方法"""

    @classmethod
    def dict_to_excle(self, file_path=None, rows=None):
        """
        data/sql-->dict-->excle
        数据类型为字典转excle
        """

        # 1.取数据
        df1 = pd.DataFrame(rows)
        # 2.保存至excel文件
        writer = pd.ExcelWriter(file_path)
        df1.to_excel(writer, encoding='utf8', index=False)
        # 6.保存
        writer.save()

    @classmethod
    def tuple_to_excle(cls, file_path=None, rows=None, columns=None):
        """
        data/sql-->tuple-->excle
        数据类型为元组/列表转excle
        file_path: 文件路径
        rows: 列表/元组数据
        columns: excle头部字段 ['编码','描述']
        """
        # 1.取数据
        # 2.保存至excel文件
        writer = pd.ExcelWriter(file_path)
        df = pd.DataFrame(rows, columns=columns)
        df.to_excel(writer, encoding='utf8', index=False)
        writer.save()


class RequestApi():
    """请求api"""

    @classmethod
    def api(cls, url: str = ..., params: dict = None, data: dict = None, headers: dict = None, jsons: dict = None,
            method: str = 'GET'):
        """网络请求公共方法"""
        conditions = {"url": url}
        if params:
            conditions["params"] = params
        if data:
            conditions["data"] = data
        if headers:
            conditions["headers"] = headers
        if jsons:
            conditions["json"] = jsons
        conditions["method"] = method.lower()
        print(conditions)
        try:
            result = requests.request(**conditions)
            return result.json()
        except BaseException as error_reason:
            conditions["error_reason"] = error_reason
            cls.except_func(**conditions)
            raise Exception(error_reason)

    @classmethod
    def except_func(cls, *args, **kwargs):
        """异常处理请求失败数据"""
        try:
            pass
            # LogBaseError().api_error(*args, **kwargs)
        except:
            pass


class NewShop():
    """获取课程列表"""

    def __init__(self):
        self.Token = self.token()

    def token(self):
        url = "https://opentest.youngor.com.cn/api/get_token"
        data = {
            "appid": "364ec50520715734b4c02ddcc295560e",
            "secret": "d02276d8d77af15272f4a364b270717b"
        }
        ret = RequestApi.api(url=url, jsons=data, method='post')
        print(ret)
        return ret.get("data").get("access_token")

    def get(self, data):
        headers = {
            "Authorization": f"Bearer {self.Token}"
        }
        url = "https://opentest.youngor.com.cn/boeto/qudao/jied/list"
        return RequestApi.api(url=url, headers=headers, jsons=data, method='post')

    def main(self):
        """通过分页查询获取所有数据"""
        data = {
            "start_date": "2020-01-01",
            "end_date": "2020-01-11",
            "page": 1,
            "size": 20
        }
        total_rows = []  # 存放所有的店铺数据

        current_page = 1  # 当前页码
        total_page = int(int(self.get(data).get("total")) / 20)  # 通过总条数计算总页码数
        #logger.debug(total_page)
        print(total_page)
        
        while True:
            if current_page > total_page:  # 当前页码大于最大页码,跳出循环
                break
            data["page"] = current_page  # 更新参数,页码更新
            total_rows += self.get(data).get("list")  # 获取数据,加入总数据列表
            logger.debug(total_rows)
            current_page += 1  # 页码+1 循环继续
        ToExcle.dict_to_excle('雅戈尔组织.xlsx', total_rows)  # 一次性批量写入excle


if __name__ == '__main__':
    NewShop().main()
