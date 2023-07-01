import math
import types
import inspect


class StringUtils(object):
    """字符串工具"""

    @staticmethod
    def not_empty(v):
        if isinstance(v, str) and len(v.strip()) == 0:
            raise ValueError("不能为空")
        if not isinstance(v, int):
            if not v:
                raise ValueError("不能为空")
        return v


class ComputerUtils(object):
    """计算工具"""

    @staticmethod
    def get_total_page(total: int, size: int) -> int:
        return math.ceil(total / size)


class CurdUtils(object):
    """Curd工具"""

    @staticmethod
    def recursive_parent_catalog(catalogs, all_catalogs):
        new_catalogs = []
        catalog_id_map = {catalog.id: catalog for catalog in all_catalogs}

        def __find_parent(_id):
            _catalog = catalog_id_map[_id]
            new_catalogs.append(_catalog)
            _parent_id = _catalog.parent_id
            if _parent_id:
                __find_parent(_parent_id)

        for catalog in catalogs:
            new_catalogs.append(catalog)
            parent_id = catalog.parent_id
            if parent_id:
                __find_parent(parent_id)
        return new_catalogs

    @staticmethod
    def recursive_child_with_catalog_id(catalog_id, all_catalogs):
        ids = [catalog_id]

        def __find_ids(parent_id):
            for item in all_catalogs:
                _parent_id = item.parent_id
                if parent_id == _parent_id:
                    _id = item.id
                    ids.append(_id)
                    __find_ids(_id)

        __find_ids(catalog_id)
        return ids

    @staticmethod
    def parse_2_tree(catalogs):
        """
        解析成树结构
        :param catalogs: 所有目录
        :return:
        """
        tree = list()
        source = list()
        tree_dict = dict()
        for catalog in catalogs:
            source.append(dict(label=catalog.name,
                               id=catalog.id,
                               used=catalog.used,
                               parent_id=catalog.parent_id,
                               project_id=catalog.project_id,
                               children=list()))
        for item in source:
            tree_dict[item["id"]] = item
        for i in tree_dict:
            if tree_dict[i]["parent_id"]:
                parent_id = tree_dict[i]["parent_id"]
                parent = tree_dict[parent_id]
                parent.setdefault("children", []).append(tree_dict[i])
            else:
                tree.append(tree_dict[i])
        return tree


class ModuleUtils(object):
    """模块工具"""

    @staticmethod
    def get_functions_map(code, module_name):
        functions_map = {}
        # 动态创建Python模块
        module = types.ModuleType(module_name)

        # 将代码添加到模块中
        exec(code, module.__dict__)

        # 获取模块中的方法
        for name, function in inspect.getmembers(module, inspect.isfunction):
            # 使用反射调用方法
            result = function
            functions_map.update({name: function})
            # print(f"Method '{name}' returned: {result}")
        return functions_map
