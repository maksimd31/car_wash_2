from django.views.decorators.csrf import csrf_exempt
from django.shortcuts import render


@csrf_exempt
def handle_bad_request(request, exception):
    return render(request, 'error.html', {'error_message': 'невозможно обработать запрос'}, status=400)


@csrf_exempt
def handle_forbidden(request, exception):
    return render(request, 'error.html', {'error_message': 'Доступ запрещен'}, status=403)


@csrf_exempt
def handle_not_found(request, exception):
    return render(request, 'error.html', {'error_message': 'Страница не найдена'}, status=404)


@csrf_exempt
def handle_server_error(request):
    return render(request, 'error.html', {'error_message': 'Ошибка сервера'}, status=500)
