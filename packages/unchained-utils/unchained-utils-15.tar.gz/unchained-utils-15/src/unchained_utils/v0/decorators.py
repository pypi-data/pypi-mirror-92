from functools import wraps

from django.db.models import QuerySet, Model
from django.db.models.query import RawQuerySet
from drf_yasg import openapi
from drf_yasg.utils import swagger_auto_schema
from rest_framework import serializers
from rest_framework.decorators import api_view, renderer_classes, permission_classes
from rest_framework.renderers import JSONRenderer
from rest_framework.response import Response

def get_serializer(model, fields='__all__'):
    class GenericSerializer(serializers.ModelSerializer):
        class Meta:
            pass
        Meta.model = model
        Meta.fields = fields
    return GenericSerializer

def api(req_model=None,
        res_model=None,
        permissions=tuple(),
        methods=('post',),
        renderers=(JSONRenderer,)):
    def decorator(func):
        @wraps(func)
        @swagger_auto_schema(methods=methods, request_body=req_model, responses={200: openapi.Response('success', res_model)} if req_model else {})
        @api_view(methods)
        @renderer_classes(renderers)
        @permission_classes(permissions)
        def decorated(request):
            args = []
            request_data = request.data
            if func.__code__.co_argcount:
                if req_model:
                    serializer_data = req_model(data=request.data)
                    serializer_data.is_valid(raise_exception=True)
                    request_data = serializer_data.data
                args = [request_data]
            raw_data = func(*args)

            if res_model:
                response_data = res_model(raw_data).data
            elif isinstance(raw_data, QuerySet):
                response_data = get_serializer(raw_data.model)(raw_data,many=True).data
            elif isinstance(raw_data, RawQuerySet):
                response_data = get_serializer(raw_data.model, fields=raw_data.columns)(raw_data, many=True).data
            elif isinstance(raw_data, Model):
                response_data = get_serializer(type(raw_data))(raw_data).data
            else:
                response_data = raw_data
            return Response(response_data)

        return decorated

    return decorator





