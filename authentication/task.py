# import logging
# from celery import shared_task
# from django.core.mail import send_mail
# from google.oauth2.credentials import Credentials
# from googleapiclient.discovery import build
# from django.template.loader import render_to_string
# from django.utils.html import strip_tags
# from .models import Reminder
# impaort datetime
# import time

# logger = logging.getLogger(__name__)

# @shared_task
# def send_reminder_email(user_email, step_goal, latest_step_count, subject, template_name):
#     try:
#         context = {
#             'step_goal': step_goal,
#             'latest_step_count': latest_step_count,
#         }
#         html_message = render_to_string(template_name, context)
#         plain_message = strip_tags(html_message)
#         from_email = 'kavypatel255@gmail.com'  # Update with your email address
#         to_email = user_email  # Use the provided user email
#         send_mail(subject, plain_message, from_email, [to_email], html_message=html_message)
#         logger.info(f"Reminder email sent to {user_email}")
#     except Exception as e:
#         logger.error(f"Failed to send reminder email to {user_email}: {e}")

# @shared_task
# def fetch_step_data():
#     today = datetime.date.today()
#     reminders_today = Reminder.objects.filter(reminder_day=today)

#     for reminder in reminders_today:
#         try:
#             credentials = Credentials.from_authorized_user_info(reminder.user.googlefit_credentials)
#             fit_service = build('fitness', 'v1', credentials=credentials)

#             midnight_today = datetime.datetime.combine(today, datetime.time())
#             midnight_tomorrow = midnight_today + datetime.timedelta(days=1)

#             response = fit_service.users().dataset().aggregate(
#                 userId='me',
#                 body={
#                     "aggregateBy": [{
#                         "dataTypeName": "com.google.step_count.delta",
#                         "dataSourceId": "derived:com.google.step_count.delta:com.google.android.gms:estimated_steps"
#                     }],
#                     "bucketByTime": {"durationMillis": 86400000},
#                     "startTimeMillis": int(time.mktime(midnight_today.timetuple())) * 1000,
#                     "endTimeMillis": int(time.mktime(midnight_tomorrow.timetuple())) * 1000,
#                 }
#             ).execute()

#             step_count_data = response.get('bucket', [])
#             if step_count_data:
#                 latest_dataset = step_count_data[0].get('dataset', [None])[0]
#                 if latest_dataset:
#                     latest_point = latest_dataset.get('point', [None])[0]
#                     if latest_point:
#                         latest_value = latest_point.get('value', [])
#                         latest_step_count = 0
#                         if latest_value:
#                             latest_step_count = latest_value[0].get('intVal', 0)
#                         # Update the latest_step_count in the reminder object
#                         reminder.latest_step_count = latest_step_count
#                         reminder.save()
#                         # Call the send_reminder_email task with correct arguments
#                         if latest_step_count >= int(reminder.step_goal):
#                             send_reminder_email.delay(reminder.user.email, reminder.step_goal, latest_step_count,
#                                                       'Congratulations!', 'authentication/congrats.html')
#                         else:
#                             send_reminder_email.delay(reminder.user.email, reminder.step_goal, latest_step_count,
#                                                       'Step Count Reminder', 'authentication/step_count_email.html')
#         except Exception as e:
#             logger.error(f"Failed to fetch step data for reminder {reminder.id}: {e}")
