from sqlalchemy import Column, Integer, String, Boolean, TIMESTAMP, UniqueConstraint, Index, VARCHAR
from sqlalchemy.ext.declarative import declarative_base


class Article(declarative_base()):
    __tablename__ = "articles"
    __table_args__ = {'sqlite_autoincrement': True}
    id = Column(Integer, name="id", primary_key=True)
    articleId = Column(Integer, name="ArticleId")
    title = Column(String, name="Title")
    releaseTime = Column(String, name="ReleaseTime")
    index = Column(Integer, name="Index")  # 在当日文章中的排序
    delFlag = Column(Integer, name="DelFlag")
    copyrightStatus = Column(Integer, name="CopyrightStatus")
    digest = Column(String, name="Digest")
    url = Column(String, name="Url")
    author = Column(String, name="Author")
    fileId = Column(Integer, name="FileId")
    account = Column(String, name="Account")  # 微信公众号名称
    cover = Column(String, name="Cover")
    sourceUrl = Column(String, name="SourceUrl")
    releaseTime_unix = Column(Integer, name="ReleaseTimeUnix")
