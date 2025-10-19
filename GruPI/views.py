from django.views.decorators.csrf import ensure_csrf_cookie
from django.http import JsonResponse

@ensure_csrf_cookie
def get_csrf_token(request):
    """
    Esta view não faz nada além de garantir que um cookie CSRF
    seja enviado na resposta.
    """
    return JsonResponse({"detail": "CSRF cookie set."})