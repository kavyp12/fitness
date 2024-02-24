from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone

class StepCount(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    date = models.DateField()
    step_count = models.IntegerField(default=0)

    def __str__(self):
        return f"{self.user.username} - {self.date}"


class Reminder(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    step_goal = models.IntegerField()
    calories_goal = models.IntegerField()
    reminder_time = models.TimeField(null=False)
    reminder_day = models.DateField()
    # latest_step_count = models.IntegerField(default=0)  # Add this field
    create_now = models.DateTimeField(default=timezone.now)  # Add this field

    def __str__(self):
        return f"Reminder for {self.user.username} on {self.reminder_day} at {self.reminder_time}"

class CaloriesBurned(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    date = models.DateField()
    calories = models.FloatField()

    def __str__(self):
        return f"{self.user.username} - {self.date}"