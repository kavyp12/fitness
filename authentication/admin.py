# authentication/admin.py

from django.contrib import admin
from .models import StepCount, Reminder, CaloriesBurned

admin.site.register(StepCount)
admin.site.register(Reminder)
admin.site.register(CaloriesBurned)
