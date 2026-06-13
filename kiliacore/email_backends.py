"""
Custom email backend for Resend HTTP API
Use this instead of SMTP when SMTP ports are blocked on Railway
"""
import requests
from django.core.mail.backends.base import BaseEmailBackend
from django.conf import settings


class ResendHTTPBackend(BaseEmailBackend):
    """
    Email backend that uses Resend's HTTP API instead of SMTP
    Configure in settings:
    EMAIL_BACKEND = 'core.email_backends.ResendHTTPBackend'
    RESEND_API_KEY = 'your-api-key'
    """
    
    def __init__(self, fail_silently=False, **kwargs):
        super().__init__(fail_silently=fail_silently, **kwargs)
        self.api_key = getattr(settings, 'RESEND_API_KEY', None)
        if not self.api_key:
            raise ValueError('RESEND_API_KEY must be set in settings')
    
    def send_messages(self, email_messages):
        """
        Send one or more EmailMessage objects and return the number of email
        messages sent.
        """
        if not email_messages:
            return 0
        
        num_sent = 0
        for message in email_messages:
            sent = self._send(message)
            if sent:
                num_sent += 1
        return num_sent
    
    def _send(self, message):
        """Send a single message"""
        try:
            # Prepare request payload
            payload = {
                'from': message.from_email,
                'to': message.to,
                'subject': message.subject,
            }
            
            # Add message body (text or HTML)
            if message.content_subtype == 'html':
                payload['html'] = message.body
            else:
                payload['text'] = message.body
            
            # Add CC if present
            if message.cc:
                payload['cc'] = message.cc
            
            # Add BCC if present
            if message.bcc:
                payload['bcc'] = message.bcc
            
            # Add reply-to if present
            if message.reply_to:
                payload['reply_to'] = message.reply_to
            
            # Send request to Resend API
            response = requests.post(
                'https://api.resend.com/emails',
                headers={
                    'Authorization': f'Bearer {self.api_key}',
                    'Content-Type': 'application/json',
                },
                json=payload,
                timeout=10
            )
            
            if response.status_code == 200:
                return True
            else:
                if not self.fail_silently:
                    raise Exception(f'Resend API error: {response.status_code} - {response.text}')
                return False
                
        except Exception as e:
            if not self.fail_silently:
                raise
            return False
