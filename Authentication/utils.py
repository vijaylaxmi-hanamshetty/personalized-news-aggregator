
 # utils.py
import requests
from django.conf import settings
import logging

def send_sms_notification(to, message):
    """Send SMS notification using the Textbelt API."""
    data = {
        'phone': to,
        'message': message,
        'key': settings.TEXTBELT_KEY
    }

    try:
        response = requests.post(settings.TEXTBELT_API_URL, data=data)
        result = response.json()
        
        if result.get('success'):
            logging.info(f"SMS sent to {to}: {message}")
        else:
            logging.warning(f"Failed to send SMS to {to}: {result.get('error')}")

        return result
    
    except requests.RequestException as e:
        logging.error(f"Error sending SMS: {e}")
        return {'success': False, 'error': str(e)}
