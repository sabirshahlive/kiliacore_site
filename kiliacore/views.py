import json
import logging
from django.conf import settings
from django.core.mail import EmailMessage, get_connection
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator
from django.views.generic import TemplateView, View
from django.shortcuts import redirect
from django.urls import reverse

logger = logging.getLogger(__name__)

def send_email(subject, message, to_email, reply_to=None):
    """Send an email using Django's configured email backend. Configured for RESEND"""
    email = EmailMessage(
        subject=subject,
        body=message,
        from_email=settings.DEFAULT_FROM_EMAIL,
        to=[to_email],
        reply_to=[reply_to] if reply_to else None,
    )
    try:
        email.send(fail_silently=False)
        logger.info('Email sent to %s', to_email)
        return True
    except Exception as exc:
        logger.exception('Failed to send email to %s: %s', to_email, exc)
        raise

class LandingView(TemplateView):
    template_name = 'kiliacore_landing.html'

@method_decorator(csrf_exempt, name='dispatch')
class ContactFormView(View):
    def post(self, request, *args, **kwargs):
        try:
            data = json.loads(request.body)
            name = data.get('name', '').strip()
            email = data.get('email', '').strip()
            message = data.get('message', '').strip()

            if not name or not email:
                return JsonResponse(
                    {'status': 'error', 'message': 'Name and email are required.'},
                    status=400
                )

            subject = f"New Contact Request from {name}"
            email_body = f"""
New contact form submission:

Name: {name}
Email: {email}
Message:
{message if message else 'No message provided.'}

---
Sent from KiliaCore landing page.
            """

            send_email(
                subject=subject,
                message=email_body,
                to_email=settings.SUPPORT_EMAIL,
                reply_to=email
            )

            return JsonResponse({
                'status': 'success',
                'message': 'Thanks! Our team will reach out shortly.'
            })

        except json.JSONDecodeError:
            return JsonResponse(
                {'status': 'error', 'message': 'Invalid data.'},
                status=400
            )
        except Exception as e:
            logger.exception('Contact form error')
            return JsonResponse(
                {'status': 'error', 'message': 'Something went wrong. Please try again later.'},
                status=500
            )