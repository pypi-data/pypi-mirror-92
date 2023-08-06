import json

from django.http import HttpResponse
from django.utils.deprecation import MiddlewareMixin
from django.contrib.auth import get_user_model

user_model = get_user_model()
ALL_MODULES = []
"""
ALL_MODULES格式[{'id':1,'name':'概览','children':[{'id':2, 'name':'人群画像'}]}]
"""


class IdCheck(type):
    """元类, 一是判断定义的模块权限类是否id重复, 二是将id,name格式化存入ALL_MODULES变量, 以供其他接口使用"""
    _id_module_map = {}

    def __new__(cls, class_name, class_parent, class_attrs, **kwargs):
        id = class_attrs.get("id", 0)
        module_name = class_attrs.get("name", "")
        if id != 0:
            # id不等于0 说明这个类是一个模块权限类
            assert id not in cls._id_module_map, f"{class_name}的id:{id}已经存在{cls._id_module_map[id]}, 不允许重复"
            assert len(class_parent) == 1, "Module只能单继承"
            cls._id_module_map[id] = class_name
            parent_id = class_parent[0].id
            if parent_id == 0:
                # 继承自id=0的类是一级模块
                ALL_MODULES.append({"id": id, "name": module_name, "children": []})
            else:
                for i in ALL_MODULES:
                    # 其他的是二级模块
                    if parent_id == i["id"]:
                        i["children"].append({"id": id, "name": module_name})
        return super().__new__(cls, class_name, class_parent, class_attrs)


class ModulePermissionBase(object,metaclass=IdCheck):
    id = 0
    name = ""

    @classmethod
    def module_check(cls, user):
        # todo 进行逻辑判断 self.user 是否有self.name的权限
        id = user.id
        instance = user_model.objects.filter(id=id).first()
        if instance:
            if cls.id in instance.function_roles.split(","):
                return True
            else:
                return False
        else:
            return False


class ModuleMiddleWare(MiddlewareMixin):
    def process_view(self, request, view_func, view_args, view_kwargs):
        # todo 在执行视图函数之前进行模块权限判断， 通过view_func拿到Module权限类, 调用module_check方法， 判断name user是否有这个模块的权限
        if issubclass(view_func.cls, ModulePermissionBase):
            if view_func.cls.module_check(request.user):
                return None
            else:
                return HttpResponse(json.dumps({"msg": "无权限"}), status=403)
        return None
