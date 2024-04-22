import json
from django.http import HttpResponse
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt
from graphene_django.views import GraphQLView


class CustomGraphQLView(GraphQLView):
    """"
    Рассматривал несколько решений
        1 Через Middleware
        2 Через декораторы над каждой schema
        3 И вот это через переопределение dispatch, решение показалось логичным и отлично работающим с
         тестовыми кейсами, но после написания я нашёл как это можно обходить, поэтому считаю его не правильным
        4 Так же думаю возможно это реализовать через более глубокое переопределение, и кастомизацию
        но уверен есть куда более лучшее решение, но упираюсь в поверхностное знание graphql
        p.s Решение достаточно абстрактное, нужно организовать больше проверок, для стабильной работы, 
            так же можно вынести schema которые не нужно выводить в отдельный объект
    """
    @method_decorator(csrf_exempt)
    def dispatch(self, request, *args, **kwargs):
        data = self.parse_body(request)
        if data.get("operationName") == "QueryIntrospection" and not request.user.is_authenticated:
            result, status_code = self.get_response(request, data, {})
            json_data = json.loads(result)
            check_delete_schema = json_data.get("data").get("type").get("fields")
            for item in check_delete_schema:
                if item.get("name") == "user":
                    check_delete_schema.remove(item)
            json_data_in_str = (json.dumps(json_data, separators=(",", ":")))
            return HttpResponse(
                status=status_code, content=json_data_in_str, content_type="application/json"
            )
        else:
            return super(CustomGraphQLView, self).dispatch(request, *args, **kwargs)
