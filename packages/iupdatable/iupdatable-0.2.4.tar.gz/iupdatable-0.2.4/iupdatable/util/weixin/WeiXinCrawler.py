from datetime import datetime
import json
from typing import Type
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from sqlalchemy import create_engine, or_, and_, inspect, Table, MetaData, Column
from iupdatable.util.weixin.models import Article
from iupdatable import Status, Logger, File
import requests
from requests.packages.urllib3.exceptions import InsecureRequestWarning
import re
from urllib.parse import urlparse, parse_qs


class WeiXinCrawler(object):
    _wei_xin_name: str
    _seed_url: str
    _template_url: str
    _sqlite_session: None
    _db_file_url: str
    _max_count: int

    def __init__(self):
        Logger.instance().config(log_file_full_path="WeiXinCrawler.log")

    def _init_db(self, db_path):
        db_path = db_path.strip()
        if not File.exist(db_path):
            url = "sqlite:///" + db_path
            engine = create_engine(url)
            session = sessionmaker(bind=engine)
            self._sqlite_session = session()
            Article.metadata.create_all(engine)

    def start(self, wei_xin_name="", seed_url="", max_count=-1, db_path=""):
        """
        开始抓取任务
        :param wei_xin_name: 微信公众号的名称
        :param seed_url: 种子链接
        :param max_count: 最多抓取多少页，默认：-1，表示抓取所有历史消息
        :param db_path: 用于保存的数据库文件路径
        :return:
        """
        try:
            Logger.instance().info("开始任务...")
            if wei_xin_name == "":
                Logger.instance().error("请填写微信公众号名称！")
                return None
            if seed_url == "":
                Logger.instance().error("请填写种子链接！")
                return None
            if "offset=" not in seed_url:
                Logger.instance().error("种子链接填写错误！")
                return None
            db_path = db_path.strip()
            if db_path == "":
                self._db_file_url = "sqlite:///微信公众号历史消息.db"
            else:
                if not File.exist(db_path):
                    Logger.instance().warning("首次使用，创建数据库文件：{0}".format(db_path))
                    self._init_db(db_path)
                self._db_file_url = "sqlite:///" + db_path
            self._template_url = re.sub("(?<=offset=)(?:[0-9]{0,3})", "{0}", seed_url)
            self._seed_url = seed_url
            self._max_count = max_count
            self._wei_xin_name = wei_xin_name

            engine = create_engine(self._db_file_url)
            session = sessionmaker(bind=engine)
            self._sqlite_session = session()

            can_continue = True
            offset = 0
            while can_continue:
                if offset > self._max_count != -1:
                    break
                grab_result = self._grab_articles(offset)
                if grab_result == Status.retry:
                    grab_result = self._grab_articles(offset)
                if isinstance(grab_result, dict):
                    can_continue = grab_result["continue"]
                    if can_continue:
                        offset = grab_result["next_offset"]
                    else:
                        Logger.instance().info("全部抓取完毕！")
                        break
                else:
                    Logger.instance().error("多次重试失败！")
                    break
            Logger.instance().info("任务完成，已退出！")
        except Exception as e:
            Logger.error(repr(e), is_with_debug_info=True)
            return -1

    def _grab_articles(self, offset):
        try:
            url = self._template_url.format(offset)
            headers = {
                "User-Agent": "MicroMessenger"
            }
            requests.packages.urllib3.disable_warnings(InsecureRequestWarning)
            response = requests.get(url, headers=headers, verify=False)
            if response.status_code == 200:
                json_result = json.loads(response.text)
                if json_result["errmsg"] == "ok":
                    new_json = json.loads(json_result["general_msg_list"])
                    general_msg_list = new_json["list"]
                    for i, msg in enumerate(general_msg_list):
                        comm_msg_info = msg["comm_msg_info"]
                        release_time_unix = comm_msg_info["datetime"]
                        if "app_msg_ext_info" not in msg:
                            continue
                        app_msg_ext_info = msg["app_msg_ext_info"]

                        article = self._dict_to_model(app_msg_ext_info, release_time_unix)
                        if article:
                            add_result = self._add_or_update_record(article, "articleId", Article)
                            if add_result:
                                log = "{0} - {1}. {2}".format(article.releaseTime, article.index, article.title)
                                Logger.instance().info(log)
                        for j, sub_msg in enumerate(app_msg_ext_info["multi_app_msg_item_list"]):
                            article = self._dict_to_model(sub_msg, release_time_unix)
                            if article:
                                add_result = self._add_or_update_record(article, "articleId", Article)
                                if add_result:
                                    log = "{0} - {1}. {2}".format(article.releaseTime, article.index, article.title)
                                    Logger.instance().info(log)
                    if json_result["can_msg_continue"] == 1:
                        result = {
                            "continue": True,
                            "next_offset": int(json_result["next_offset"])
                        }
                        return result
                    else:
                        result = {
                            "continue": False
                        }
                        return result
                else:
                    return Status.retry
            else:
                return Status.retry
        except Exception as e:
            Logger.error(repr(e), is_with_debug_info=True)
            return Status.retry

    def _add_or_update_record(self, record, compare_property_name: str, entity: Type[declarative_base]):
        """
        增加或更新一条数据库记录
        :param record: 一条 entity 类型的记录实例
        :param compare_property_name: 要比较的字段名称，注意：该值为 entity 中的名称，不是数据库的字段名
        :param entity: 数据库的实体类，确保其基类为 declarative_base
        :return: 插入：Status.added，更新：Status.existing，异常：Status.failed
        """
        try:
            skip_column_list = ["id"]
            query_result = self._sqlite_session.query(entity) \
                .filter(getattr(entity, compare_property_name) == getattr(record, compare_property_name)).first()
            if query_result:
                for member in inspect(entity).attrs:
                    member_name = member.key
                    column_name = member.expression.key
                    if column_name in skip_column_list:
                        continue
                    setattr(query_result, member_name, getattr(record, member_name))
                self._sqlite_session.commit()
                return Status.existing
            else:
                self._sqlite_session.add(record)
                self._sqlite_session.commit()
                return Status.added
        except Exception as e:
            Logger.error(repr(e), is_with_debug_info=True)
            return Status.failed

    @staticmethod
    def _get_url_param_value(url: str, param_name):
        parsed_uri = urlparse(url)
        return parse_qs(parsed_uri.query)[param_name][0]

    def _dict_to_model(self, msg: dict, release_time_unix):
        article = Article()
        article.url = msg["content_url"]
        if "mid" not in article.url:
            return None
        mid = int(self._get_url_param_value(article.url, "mid"))
        article.index = int(self._get_url_param_value(article.url, "idx"))
        article.articleId = mid * 10 + article.index
        article.title = msg["title"]
        article.digest = msg["digest"]
        article.releaseTime_unix = release_time_unix
        article.releaseTime = "{0}".format(datetime.fromtimestamp(release_time_unix))
        article.delFlag = msg["del_flag"]
        article.copyrightStatus = msg["copyright_stat"]
        article.author = msg["author"]
        article.fileId = msg["fileid"]
        article.account = self._wei_xin_name
        article.cover = msg["cover"]
        article.sourceUrl = msg["source_url"]
        return article
