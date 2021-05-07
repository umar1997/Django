from django.core.mail import EmailMessage
from rest_framework.permissions import BasePermission, SAFE_METHODS


class Email:
    @staticmethod
    def send_email(data):
        email = EmailMessage(
            subject=data['email_subject'], body=data['email_body'], to=[data['to_email']])
        
        email.send()


class IsOwnerOrReadOnly(BasePermission):
    message = 'Editing User is restricted to the Owner only'

    def has_object_permission(self, request, view, obj):
        if request.method in SAFE_METHODS:
            return True
        return str(obj.email) == str(request.user)
        # return obj.author == request.user