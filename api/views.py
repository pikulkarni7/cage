import requests
from django.http import HttpResponse
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from django.views.decorators.csrf import csrf_exempt

from api import tasks



@csrf_exempt
@api_view(["POST"])
def trigger_notify_task(request):
    tasks.notify_mq(data = request.data, exchange='weather_exchange')
    return HttpResponse(status=200)



