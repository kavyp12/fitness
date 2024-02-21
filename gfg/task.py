from celery import shared_task
from django.core.mail import send_mail
from django.template.loader import render_to_string
from django.utils.html import strip_tags

@shared_task
def send_step_count_email(user_email, subject, template, context):
    html_message = render_to_string(template, context)
    plain_message = strip_tags(html_message)
    from_email = 'kavypatel255@gmail.com'  # Update with your email address
    send_mail(subject, plain_message, from_email, [user_email], html_message=html_message)