from django.contrib.auth import get_user_model

from rest_framework.response import Response
from rest_framework.views import APIView
from .middleware import ALL_MODULES

user_model = get_user_model()


class ModuleView(APIView):
    """Iframe视图"""

    def get(self, request):
        query_params = request.query_params.dict()
        dataset = ProceePermission(request).get_dataset(query_params)
        return Response(data={"functionRoles": dataset})

    def put(self, request, select=None):
        query_params = request.data
        obj = ProceePermission(request).update_permission(query_params)
        if not obj:
            return Response({"message": "该用户不存在"})
        return Response({"message": "success"})


class ProceePermission(object):

    def __init__(self, request):
        self.user = request.user
        self.request = request

    def get_dataset(self, query_params):
        get_dataset_func = getattr(user_model, "get_dataset", None)
        if get_dataset_func:
            dataset = get_dataset_func(query_params=query_params)
            return dataset

        get_denied_func = getattr(user_model, "get_denied_modules", None)
        if get_denied_func:
            self.denied_modules = get_denied_func(query_params=query_params)
        else:
            self.denied_modules = []

        email = query_params.get('email')
        self.select_modules = user_model.objects.filter(email=email).values("function_roles").first().get(
            'function_roles').split(',')
        all_models = ALL_MODULES
        dataset = []
        for one_level in all_models:
            for two_level in one_level.get("children", []):
                self.add_status(two_level)
            self.add_status(one_level)
            dataset.append(one_level)

        return dataset

    def update_permission(self, query_params):
        get_update_function = getattr(user_model, "updte_permission", None)
        email = query_params.get('email')
        systemRoles = query_params.get('systemRoles')
        functionRoles = query_params.get('functionRoles')
        if get_update_function:
            obj = get_update_function(query_params=query_params)
            return obj
        # 公用的model只控制模块表，更新用户的模块权限，至于用户的系统权限各项目在自己的更新方法去实现
        obj = user_model.objects.filter(email=email).update(function_roles=",".join([str(i) for i in functionRoles]))
        return obj

    def add_status(self, data):
        if str(data["id"]) in self.select_modules:
            data.update(value=True, show=True)
        else:
            data.update(value=False, show=True)
        if str(data["id"]) in self.denied_modules:
            data.update(canOperated=False)
        else:
            data.update(canOperated=True)
