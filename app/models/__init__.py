from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

from config import Config

engine = create_engine(Config.SQLALCHEMY_DATABASE_URI, pool_recycle=1500)
Session = sessionmaker(engine, expire_on_commit=False)

# 创建对象的基类
Base = declarative_base()
