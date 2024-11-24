from django.http import JsonResponse


def handler500(request):
    return JsonResponse({"detail": "Sorry, there is some errors on server. Please, try again later"}, status=500)


def handler404(request, exception):
    return JsonResponse({"detail": "Requested resource not found"}, status=404)
