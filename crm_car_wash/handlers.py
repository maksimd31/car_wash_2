from django.views.decorators.csrf import csrf_exempt
from django.http import HttpResponseBadRequest, HttpResponseForbidden, HttpResponseNotFound, HttpResponseServerError


@csrf_exempt
def handle_bad_request(request, exception):
    """
    handler400
    Error 400
    :return: невозможно обработать запрос
    """
    return HttpResponseBadRequest("невозможно обработать запрос")


@csrf_exempt
def handle_forbidden(request, exception):
    """
    handler403
    Error 403
    :return:Доступ запрещен
    """
    return HttpResponseForbidden("Доступ запрещен")


@csrf_exempt
def handle_not_found(request, exception):
    """
    handler404
    Error 404
    :return:Страница не найдена
    """
    return HttpResponseNotFound("Страница не найдена")


@csrf_exempt
def handle_server_error(request):
    """
    handler500
    Error 500
    :return:ошибка сервера
    """
    return HttpResponseServerError("Ошибка сервера")
