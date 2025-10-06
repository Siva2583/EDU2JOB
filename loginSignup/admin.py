from django.contrib import admin
from .models import PredHistory, UserPredictionHistory

# This makes your models visible in the admin panel
admin.site.register(PredHistory)
admin.site.register(UserPredictionHistory)