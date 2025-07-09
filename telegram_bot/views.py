import json
from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt
from .tasks import process_telegram_message, send_telegram_notification
import logging

logger = logging.getLogger(__name__)

@csrf_exempt
def telegram_webhook(request):
    logger.info("Telegram webhook received a request!")
    if request.method == 'POST':
        logger.info("Received a POST request")
        message_json = json.loads(request.body)
        logger.info("Message JSON loaded")
        logger.info("Sending task to Celery...")
        process_telegram_message.apply_async(args=[message_json], routing_key='celery')
        send_telegram_notification.delay("Test message") # Отправляем простую задачу
        logger.info("Task sent to Celery")
        return HttpResponse("OK")
    return HttpResponse("Invalid request", status=400)