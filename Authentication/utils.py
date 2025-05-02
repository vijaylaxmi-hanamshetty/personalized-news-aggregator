from twilio.rest import Client
from django.conf import settings
import phonenumbers
from twilio.base.exceptions import TwilioRestException

def send_sms(to_number, message_body):
    try:
        # Parse and validate phone number
        parsed_number = phonenumbers.parse(to_number, None)
        if not phonenumbers.is_valid_number(parsed_number):
            raise ValueError("Invalid phone number.")

        formatted_number = phonenumbers.format_number(
            parsed_number, phonenumbers.PhoneNumberFormat.E164
        )

        # Initialize Twilio client
        client = Client(settings.TWILIO_ACCOUNT_SID, settings.TWILIO_AUTH_TOKEN)

        # Send SMS
        message = client.messages.create(
            body=message_body,
            from_=settings.TWILIO_PHONE_NUMBER,
            to=formatted_number
        )
        return message.sid

    except (phonenumbers.NumberParseException, ValueError) as e:
        print(f"[SMS Error] Invalid phone number: {to_number} - {e}")
        return None
    except TwilioRestException as e:
        print(f"[Twilio Error] {e}")
        return None
