from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.core.mail import send_mail
from gfg import settings
from django.views.decorators.csrf import csrf_protect
from .models import StepCount
from datetime import date
from chartjs.views.lines import BaseLineChartView
import json
from google_auth_oauthlib.flow import InstalledAppFlow, Flow
from django.conf import settings
from user_agents import parse
import logging
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseServerError
from google.oauth2.credentials import Credentials
from googleapiclient.discovery import build
import logging
import datetime  # Assuming you'll need the date module 
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from oauth2client.client import Credentials 
import datetime, time
import google.oauth2.credentials
from .models import Reminder
from django.core.mail import send_mail
from django.template.loader import render_to_string
from django.utils.html import strip_tags
from django.urls import reverse




logger = logging.getLogger(__name__)

# Define the scopes required for Google Fit API
SCOPES = [
    'https://www.googleapis.com/auth/fitness.activity.read',
    'https://www.googleapis.com/auth/userinfo.email',
    'https://www.googleapis.com/auth/userinfo.profile',
    'openid'
]

@csrf_protect
def home(request):
    return render(request, 'authentication/index.html')

@csrf_protect
def signup(request):
    if request.method == 'POST':
        username = request.POST['username']
        email = request.POST['email']
        pass1 = request.POST['pass1']
        pass2 = request.POST['pass2']

        if User.objects.filter(username=username).exists():
            messages.error(request, "Username already exists! Please try a different username.")
            return redirect('home')

        if User.objects.filter(email=email).exists():
            messages.error(request, "Email already registered!")
            return redirect('home')

        if pass1 != pass2:
            messages.error(request, "Passwords do not match!")
            return redirect('home')

        if len(username) > 20:
            messages.error(request, "Username must be under 20 characters!")
            return redirect('home')

        if not username.isalnum():
            messages.error(request, "Username must be alphanumeric!")
            return redirect('home')

        myuser = User.objects.create_user(username, email, pass1)
        myuser.save()
        messages.success(request, "Your account has been successfully created")

        subject = "Welcome to GFG - Django Login!"
        message = f"Hello {myuser.username}!\nWelcome to GFG!\nThank you for visiting our website. We have also sent you a confirmation email, please confirm your email address.\n\nThank you.\nAnubhav Madhav"
        from_email = settings.EMAIL_HOST_USER
        to_list = [myuser.email]
        send_mail(subject, message, from_email, to_list, fail_silently=True)

        return redirect('signin')

    return render(request, 'authentication/signup.html')

@csrf_protect
def signin(request):
    if request.method == 'POST':
        username = request.POST['username']
        pass1 = request.POST['pass1']

        user = authenticate(username=username, password=pass1)

        if user is not None:
            login(request, user)
            fname = user.first_name
            return render(request, "authentication/index.html", {"fname": fname})
        else:
            messages.error(request, "Invalid credentials!")
            return render(request, 'authentication/signin.html')

    return render(request, 'authentication/signin.html')

@csrf_protect
def signout(request):
    logout(request)
    messages.success(request, "Logout Success")    
    return redirect('signin')

def calculate_calories_burned(step_count):
    # Assuming a basic formula for calories burned per step
    calories_per_step = 0.05  # Adjust this value based on your requirements
    return step_count * calories_per_step

class StepCountChart(BaseLineChartView):
    def get_labels(self):
        return [step_data.date for step_data in StepCount.objects.filter(user=self.request.user)]

    def get_providers(self):
        return ["Step Count"]

    def get_data(self):
        return [[step_data.step_count for step_data in StepCount.objects.filter(user=self.request.user)]]

def googlefit_auth(request):
    # Specify the path to the credentials file
    credentials_path = 'templates/static/assets/js/googlefit.json'

    # Set up the Google OAuth flow
    flow = Flow.from_client_secrets_file(
        credentials_path,
        scopes=SCOPES,
        redirect_uri='http://localhost:8000/googlefit/auth/callback/'
    )

    # Generate the authorization URL
    authorization_url, state = flow.authorization_url(
        access_type='offline',
        include_granted_scopes='true'
    )

    # Save the state in the session
    request.session['googlefit_auth_state'] = state
    request.session.modified = True

    # Redirect the user to Google's authentication page
    return redirect(authorization_url)

def googlefit_auth_callback(request):
    # Retrieve the state from the session
    state = request.session.pop('googlefit_auth_state', None)

    # Ensure the state matches the state returned in the callback
    if state is None or state != request.GET.get('state'):
        return redirect('home')  # Redirect to home page if state doesn't match

    # Specify the path to the credentials file
    credentials_path = 'templates/static/assets/js/googlefit.json'

    # Set up the Google OAuth flow
    flow = Flow.from_client_secrets_file(
        credentials_path,
        scopes=SCOPES,
        redirect_uri='http://localhost:8000/googlefit/auth/callback/'
    )

    # Fetch the authorization code from the callback request
    authorization_code = request.GET.get('code')

    try:
        # Exchange the authorization code for access and refresh tokens
        flow.fetch_token(code=authorization_code)

        # Get the credentials object
        credentials = flow.credentials
        

        # Ensure that the necessary fields are present in the credentials object
        if not hasattr(credentials, 'refresh_token') or not hasattr(credentials, 'token_uri') \
                or not hasattr(credentials, 'client_id') or not hasattr(credentials, 'client_secret'):
            raise ValueError("Credentials object is missing necessary fields")

        # Save the necessary fields in he session for refreshing the access token
        request.session['googlefit_credentials'] = {
            'refresh_token': credentials.refresh_token,
            'token_uri': credentials.token_uri,
            'client_id': credentials.client_id,
            'client_secret': credentials.client_secret
        }
        request.session.modified = True

        # Redirect the user to a success page
        return redirect('step')
    except Exception as e:
        # Log the error
        logger.error("Error occurred during token exchange: %s", e)

        # Redirect the user to an error page
        return redirect('error_page')

import datetime  # Assuming you'll need the date module 
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from oauth2client.client import Credentials

#corect the below code 


@login_required
def step(request):
    # Retrieve credentials from session
    token_dict = request.session.get('googlefit_credentials')

    if not token_dict:
        return redirect('googlefit_auth')

    step_count_data = []  # Define step_count_data outside of the try block

    try:
        # Create Credentials object
        credentials = google.oauth2.credentials.Credentials.from_authorized_user_info(token_dict)

        # Build the Google Fit API service
        fit_service = build('fitness', 'v1', credentials=credentials)

        # Retrieve step count data from Google Fit API
        today = datetime.date.today()
        midnight = datetime.datetime.combine(today, datetime.time())
        midnight_next_day = midnight + datetime.timedelta(days=1)

        response = fit_service.users().dataset().aggregate(
            userId='me',
            body={
                "aggregateBy": [{
                    "dataTypeName": "com.google.step_count.delta",
                    "dataSourceId": "derived:com.google.step_count.delta:com.google.android.gms:estimated_steps"
                }],
                "bucketByTime": {"durationMillis": 86400000},  # 1 day
                "startTimeMillis": int(time.mktime(midnight.timetuple())) * 1000,
                "endTimeMillis": int(time.mktime(midnight_next_day.timetuple())) * 1000,
            }
        ).execute()

        # Log the response for debugging
        logger.debug("Response from Google Fit API: %s", response)

        # Process the response and extract step count data
        if isinstance(response, dict):
            step_count_data = response.get('bucket', [])
            # Log step_count_data for debugging
            logger.debug("Step count data: %s", step_count_data)
            # Proceed with further processing
        elif isinstance(response, list):
            # Handle the case where response is a list
            # You may want to log a warning or handle this situation based on your requirements
            logger.warning("Unexpected response type: list")
            pass
        else:
            # Handle the case where response is neither a dictionary nor a list
            # Optionally, log a warning or handle the situation based on your requirements
            logger.warning("Unexpected response type: %s", type(response))
            pass

        # Save step count data to database
        total_steps = 0
        for bucket in step_count_data:
            datasets = bucket.get('dataset', [])
            for dataset in datasets:
                points = dataset.get('point', [])
                # Inside the for loop where `point` is being processed
            for point in points:
                print("Point:", point)  # Add this line for debugging
                if isinstance(point, dict):
                    # Check if 'value' is a list or a dictionary
                    if isinstance(point.get('value'), list):
                        # Handle the case where 'value' is a list
                        for value_dict in point.get('value', []):
                            step_count = value_dict.get('intVal', 0)
                            print("Step count:", step_count)  # Add this line for debugging
                            StepCount.objects.create(user=request.user, date=today, step_count=step_count)
                            total_steps += step_count
                    elif isinstance(point.get('value'), dict):
                        # Handle the case where 'value' is a dictionary
                        step_count = point.get('value', {}).get('intVal', 0)
                        print("Step count:", step_count)  # Add this line for debugging
                        StepCount.objects.create(user=request.user, date=today, step_count=step_count)
                        total_steps += step_count
                else:
                    print("Unexpected type:", type(point))  # Add this line for debugging
                    # Log a warning or handle the situation based on your requirements       
        calories_burned = calculate_calories_burned(total_steps)

        return render(request, 'authentication/step.html', {'step_count_data': step_count_data, 'calories_burned': calories_burned, 'total_steps': total_steps})

    except Exception as e: 
        # Log the exception for debugging
        logger.exception("Error fetching/processing data")
          

        # Replace with your desired error handling
        return render(request, 'authentication/error_page.html', {'error_message': str(e)})

from django.shortcuts import render

def error_page(request):
    return render(request, 'authentication/error_page.html')


from django.core.mail import send_mail
from django.template.loader import render_to_string
from django.utils.html import strip_tags

@login_required
def dailyset(request):
    user = request.user
    if request.method == 'POST':
        # Retrieve form data
        step_goal = request.POST.get('step_goal')
        calories_goal = request.POST.get('calories_goal')
        reminder_time = request.POST.get('reminder_time')
        reminder_day = request.POST.get('reminder_day')

        # Check if all required fields are present
        if not (step_goal and calories_goal and reminder_time and reminder_day):
            messages.error(request, "All fields are required!")
            return redirect('dailyset')

        # Check step count for the reminder's day directly from Google Fit API
        try:
            # Retrieve credentials from session
            token_dict = request.session.get('googlefit_credentials')

            if not token_dict:
                return redirect('googlefit_auth')

            # Create Credentials object
            credentials = google.oauth2.credentials.Credentials.from_authorized_user_info(token_dict)

            # Build the Google Fit API service
            fit_service = build('fitness', 'v1', credentials=credentials)

            # Retrieve step count data from Google Fit API for today
            today = datetime.datetime.strptime(reminder_day, '%Y-%m-%d').date()
            midnight = datetime.datetime.combine(today, datetime.time())
            midnight_next_day = midnight + datetime.timedelta(days=1)

            response = fit_service.users().dataset().aggregate(
                userId='me',
                body={
                    "aggregateBy": [{
                        "dataTypeName": "com.google.step_count.delta",
                        "dataSourceId": "derived:com.google.step_count.delta:com.google.android.gms:estimated_steps"
                    }],
                    "bucketByTime": {"durationMillis": 86400000},  # 1 day
                    "startTimeMillis": int(time.mktime(midnight.timetuple())) * 1000,
                    "endTimeMillis": int(time.mktime(midnight_next_day.timetuple())) * 1000,
                }
            ).execute()

            if isinstance(response, dict):
                step_count_data = response.get('bucket', [])
                if not step_count_data:
                    raise Exception('No step data available')
                try:
                    latest_dataset = step_count_data[0].get('dataset', [None])[0]
                    if latest_dataset is not None:
                        latest_point = latest_dataset.get('point', [None])[0]
                        if latest_point is not None:
                            latest_value = latest_point.get('value', [])
                            latest_step_count = 0
                            if latest_value:
                                latest_step_count = latest_value[0].get('intVal', 0)
                            if latest_step_count < int(step_goal):
                                # Step count is below the goal, send email notification
                                subject = 'Step Count Reminder'
                                context = {
                                    'step_goal': step_goal,
                                    'step_count': latest_step_count,
                                }
                                html_message = render_to_string('authentication/step_count_email.html', context)
                                plain_message = strip_tags(html_message)
                                from_email = 'kavypatel255@gmail.com'  # Update with your email address
                                to_email = user.email
                                send_mail(subject, plain_message, from_email, [to_email], html_message=html_message)
                except KeyError:
                    logger.exception("Bad structure format in the data returned by the API")
        except Exception as e: 
            # Log the exception for debugging
            logger.exception("Error fetching/processing data")

            # Replace with your desired error handling
            return render(request, 'authentication/error_page.html', {'error_message': str(e)})

        # Create new Reminder
        new_reminder = Reminder.objects.create(
            user=user, 
            step_goal=step_goal, 
            calories_goal=calories_goal, 
            reminder_time=reminder_time, 
            reminder_day=reminder_day
        )

        messages.success(request, "Daily reminder set successfully!")
        # Redirect to the admin page for reminders
        return redirect(reverse('admin:authentication_reminder_changelist'))

    return render(request, 'authentication/dailyset.html')




@login_required
def reminders(request):
    user = request.user
    # Retrieve all Reminders for the user
    reminders = Reminder.objects.filter(user=user)
    context = {'reminders': reminders}
    return render(request, 'authentication/reminders.html', context)


def step_count_email(request):
    return render(request, 'authentication/step_count_email.html')