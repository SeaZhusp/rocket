from enum import Enum

from loguru import logger
from sqlalchemy import desc, asc

from app.base.model import RocketBaseModel
from typing import Type, Union

from app.base.schema import RocketBaseSchema
from app.core.enums import DeleteEnum
from app.base.dto import RocketBaseDto
from app.core.exc.exceptions import BusinessException
from functools import wraps
from app.models import Session


def connect(func):
    """
    自动创建session装饰器
    """

    @wraps(func)
    def wrapper(cls, *args, **kwargs):
        try:
            session = kwargs.pop("session", None)
            if session is not None:
                return func(cls, session=session, *args, **kwargs)
            with Session() as ss:
                return func(cls, session=ss, *args, **kwargs)
        except Exception as e:
            import traceback
            logger.exception(traceback.format_exc())
            logger.error(
                f"操作{cls.model.__name__}失败, args：{[*args]}, kwargs：{kwargs}, {func.__name__}方法报错: {e}")
            raise BusinessException(f"操作数据库失败: {e}")

    return wrapper


# 只支持单表
class BaseCurd(object):
    model: Type[RocketBaseModel] = None

    @classmethod
    def __filter_k_v(cls, filter_list: list = None, contains_delete: bool = False, **kwargs):
        """
        获取过滤条件
        :param filter_list: 过滤条件，比较特殊的，or_(xxx == xxx)
        :param kwargs: 不定传参，xx = xx
        :param contains_delete: contains_delete = True时，不过滤删除数据
        :return: conditions
        """
        filter_list = filter_list if filter_list else list()
        # 判断表是否有del_flag字段
        if getattr(cls.model, "deleted", None) and not contains_delete:
            # 只取未删除的数据
            filter_list.append(getattr(cls.model, "deleted") == DeleteEnum.NO.value)
        for k, v in kwargs.items():
            # 过滤None的字段值，注意 0 和 False
            if v is None:
                continue
            elif isinstance(v, (bool, int)):
                filter_list.append(getattr(cls.model, k) == v)
            else:
                # 判断是否模糊查询，必须字符串，字符串开头%或者结尾%
                like = isinstance(v, str) and (v.startswith("%") or v.endswith("%"))
                if like and v != "%%":
                    filter_list.append(getattr(cls.model, k).like(v))
                else:
                    filter_list.append(getattr(cls.model, k) == v)
        return filter_list

    @classmethod
    def query_wrapper(cls, session: Session, filter_list: list = None, _sort: list = None,
                      _fields: Type[RocketBaseDto] = None, _group: list = None, _sort_type: bool = "desc", **kwargs):
        """
        查询数据
        :param session: 会话
        :param filter_list: 过滤条件，比较特殊的，or_(xxx == xxx)
        :param _sort_type: 排序方式，默认True，倒叙
        :param _sort: 排序字段，[xxx.xxx]
        :param kwargs: 不定传参，xx = xx
        :param _fields: Dto 过滤查询
        :param _group: 分组
        :return: 查询语句
        """
        _filter_list = cls.__filter_k_v(filter_list, **kwargs)
        if _fields:
            field_list = []
            for field in _fields.__fields__.keys():
                field_list.append(getattr(cls.model, field))
            query_obj = session.query(*field_list).filter(*_filter_list)
        else:
            query_obj = session.query(cls.model).filter(*_filter_list)
        if _group:
            query_obj = query_obj.group_by(*_group)
        if _sort:  # 有排序字段时，进行排序
            _sorts = []
            for d in _sort:
                if _sort_type == "asc":
                    _sorts.append(asc(getattr(cls.model, d)))
                else:
                    _sorts.append(desc(getattr(cls.model, d)))
            return query_obj.order_by(*_sorts) if _sort else query_obj
        return query_obj

    @classmethod
    @connect
    def get_with_pagination(cls, session: Session, page: int = 1, limit: int = 10, **kwargs):
        """
        分页查询
        :param session: 会话
        :param page: 页码
        :param limit: 大小
        :param kwargs: 不定传参
        :return: 总数，查询对象
        """
        query_obj = cls.query_wrapper(session, **kwargs)
        total = query_obj.count()
        return total, query_obj.limit(limit).offset((page - 1) * limit).all()

    @classmethod
    @connect
    def get_with_params(cls, session: Session, filter_list: list = None,
                        _sort: list = None, _fields: Type[RocketBaseDto] = None, _group: list = None, **kwargs):
        """
        查询数据
        :param session: 会话
        :param filter_list: 过滤条件，比较特殊的，or_(xxx == xxx)
        :param _sort: 排序字段
        :param kwargs:  不定传参，xx = xx
        :param _fields: Dto 过滤查询
        :param _group: 分组
        :return: 查询对象
        """
        query_obj = cls.query_wrapper(session, filter_list, _sort, _fields, _group, **kwargs)
        return query_obj.all()

    @classmethod
    @connect
    def get_with_existed(cls, session: Session, filter_list: list = None, **kwargs):
        """
        判断数据是否存在
        :param session: 会话
        :param filter_list: 过滤条件，比较特殊的，or_(xxx == xxx)
        :param kwargs: 不定传参
        :return:
        """
        _filter_list = cls.__filter_k_v(filter_list, **kwargs)
        query = session.query(cls.model).filter(*_filter_list)
        # 获取结果，ant为true或者false
        ant = session.query(query.exists()).scalar()
        return ant

    @classmethod
    @connect
    def get_with_first(cls, session: Session, **kwargs):
        """
        获取第一条数据
        :param session: 会话
        :param kwargs: 不定传参
        :return:
        """
        sql_obj = cls.query_wrapper(session, **kwargs)
        return sql_obj.first()

    @classmethod
    @connect
    def get_with_id(cls, session: Session, pk: int):
        """
        根据主键id查询数据
        :param session: 会话
        :param pk: 主键id
        :return:
        """
        sql_obj = cls.query_wrapper(session, id=pk)
        return sql_obj.first()

    @classmethod
    @connect
    def update_with_id(cls, session: Session, model: Union[dict, RocketBaseSchema], user: dict = None, not_null=False,
                       **kwargs):
        """
        通过主键id更新数据
        :param session: 会话
        :param model: 更新模型
        :param user: 更新用户数据
        :param not_null: not_null=True 只有非空字段才更新数据
        :return:
        """
        if isinstance(model, dict):
            id = model["id"]
            model_dict = model
        else:
            id = model.id
            model_dict = vars(model)
        query = cls.query_wrapper(session, id=id, **kwargs)
        query_obj = query.first()
        if query_obj is None:
            raise BusinessException("数据不存在")
        for var, value in model_dict.items():
            # 如果value是枚举值，得通过xxx.value获取值
            if isinstance(value, Enum):
                value = value.value
            if not_null:
                # 过滤None的字段值，注意 0 和 False
                if value is None:
                    continue
                if isinstance(value, (bool, int)) or value:
                    setattr(query_obj, var, value)
            else:
                setattr(query_obj, var, value)
            if user:
                # todo: 更新人id和name
                pass
                # setattr(query_obj, "update_id", user["id"])
                # setattr(query_obj, "update_name", user["username"])
        session.commit()
        # session.refresh(query_obj)
        return query_obj

    @classmethod
    @connect
    def update_by_map(cls, session: Session, filter_list: list, user: dict = None, **kwargs):
        """
        批量更新数据
        :param session: 会话
        :param filter_list: 过滤条件
        :param user: 更新人
        :param kwargs: 要更新的数据，k = v
        :return:
        """
        # https://docs.sqlalchemy.org/en/14/errors.html#error-bhk3
        # if getattr(cls.model, "update_id") and getattr(cls.model, "update_name") and user:
        #     kwargs["update_id"] = user["id"]
        #     kwargs["update_name"] = user["username"]
        query_obj = session.query(cls.model).filter(*filter_list)
        query_obj.update(kwargs)
        session.commit()
        return query_obj.all()

    #
    @classmethod
    @connect
    def insert_with_model(cls, session: Session, model_obj: RocketBaseModel):
        """
        :param session: 会话
        :param model_obj: 实例化的表
        :return:
        """
        session.add(model_obj)
        session.flush()
        session.commit()
        return model_obj

    @classmethod
    @connect
    def delete_with_id(cls, session: Session, pk: int, **kwargs):
        """
        通过主键id删除数据
        :param session: 会话
        :param pk: 主键id
        :return:
        """
        query = cls.query_wrapper(session, id=pk, **kwargs)
        query_obj = query.first()
        if query_obj is None:
            raise BusinessException("数据不存在")
        setattr(query_obj, "deleted", DeleteEnum.YES.value)
        session.commit()
        session.refresh(query_obj)
        return query_obj

    @classmethod
    @connect
    def delete_with_params(cls, session: Session, filter_list: list = None, **kwargs):
        """
        按条件删除
        :param session:
        :param filter_list:
        :param kwargs:
        :return:
        """
        query = cls.query_wrapper(session, filter_list, **kwargs)
        query_objs = query.all()
        if query_objs is None:
            raise BusinessException("数据不存在")
        for query_obj in query_objs:
            setattr(query_obj, "deleted", DeleteEnum.YES.value)
            session.commit()
            session.refresh(query_obj)
        return query_objs

    @classmethod
    @connect
    def get_with_join(cls, session: Session, page: int = 1, limit: int = 10, filter_list: list = None,
                      dto: RocketBaseDto = None, query_fields: list = [], _group: list = None,
                      _sort_type: bool = "desc", _sort: list = None, join_con: list = [], **kwargs):
        _filter_list = cls.__filter_k_v(filter_list, **kwargs)
        field_list = []
        if dto:
            for field in dto.__fields__.keys():
                field_list.append(getattr(cls.model, field))
            # field_list += query_fields
            query_obj = session.query(*field_list, *query_fields).filter(*_filter_list)
        else:
            query_obj = session.query(cls.model, *query_fields).filter(*_filter_list)
        query_obj = query_obj.join(*join_con)
        if _group:
            query_obj = query_obj.group_by(*_group)
        if _sort:  # 有排序字段时，进行排序
            _sorts = []
            for d in _sort:
                if _sort_type == "asc":
                    _sorts.append(asc(getattr(cls.model, d)))
                else:
                    _sorts.append(desc(getattr(cls.model, d)))
        total = query_obj.count()
        return total, query_obj.limit(limit).offset((page - 1) * limit).all()

    # @classmethod
    # @connect
    # def get_with_count(cls, session: Session, **kwargs):
    #     """
    #     统计数据
    #     :param session: 会话
    #     :param kwargs:
    #     :return:
    #     """
    #     query = cls.query_wrapper(session, **kwargs)
    #     return query.group_by(cls.model.id).count() if getattr(cls.model, "id", None) else query.count()
