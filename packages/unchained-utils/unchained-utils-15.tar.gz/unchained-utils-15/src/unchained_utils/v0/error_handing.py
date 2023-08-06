import logging
import traceback

from django.core.exceptions import ObjectDoesNotExist
from django.db import IntegrityError
from django.http import JsonResponse


def unchained_exception_handler(exc, context):
    from rest_framework.views import exception_handler
    import sentry_sdk

    response = exception_handler(exc, context)

    if response is not None:
        response.data['status_code'] = response.status_code
    elif isinstance(exc, AssertionError):
        err_data = {'error': str(exc)}
        logging.warning(exc)
        sentry_sdk.capture_exception(exc)
        response = JsonResponse(err_data, safe=True, status=500)
    elif isinstance(exc, IntegrityError):
        err_data = {'error': 'Already exist!'}
        logging.error(exc)
        sentry_sdk.capture_exception(exc)
        response = JsonResponse(err_data, safe=True, status=400)

    elif isinstance(exc, ObjectDoesNotExist):
        err_data = {'error': 'Doesn\'t exist'}
        logging.warning(exc)
        sentry_sdk.capture_exception(exc)
        response = JsonResponse(err_data, safe=True, status=400)

    elif isinstance(exc, Exception):
        err_data = {'error': 'Something wrong in our side!'}
        tb = "\n".join(traceback.format_exception(type(exc), exc, exc.__traceback__))
        logging.error(tb)
        with sentry_sdk.configure_scope() as scope:
            scope.level = 'error'
            sentry_sdk.capture_exception(exc)
        response = JsonResponse(err_data, safe=True, status=500)

    return response
