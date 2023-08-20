from django.db import models

class Ride(models.Model):
    effort_id = models.CharField(max_length=35)
    effort_name = models.CharField(max_length=35)
    athlete_username = models.CharField(max_length=35)
    segment_name = models.CharField(max_length=35)
    segment_id = models.CharField(max_length=35)
    start_date_time = models.CharField(max_length=35)
    elapsed_time = models.CharField(max_length=35)
    moving_time =  models.CharField(max_length=35)
    effort_distance = models.CharField(max_length=35)
    segment_distance = models.CharField(max_length=35)
    average_watts = models.CharField(max_length=35)
    average_heart_rate = models.CharField(max_length=35)
    max_heart_rate =  models.CharField(max_length=35)
