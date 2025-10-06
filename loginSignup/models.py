from django.db import models
from django.contrib.auth.models import User


class UserPredictionHistory(models.Model):
    # ForeignKey to auth_user table
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='predictions')
    
    # Prediction / profile fields
    major = models.CharField(max_length=100, blank=True)
    cgpa = models.DecimalField(max_digits=4, decimal_places=2, null=True, blank=True)
    degree = models.CharField(max_length=100, blank=True, null=True)
    
    # Store skills as list (JSONField) for flexibility
    skills = models.JSONField(default=list, blank=True)
    
    year_of_graduation = models.IntegerField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user.username} - {self.major}"


# 🔥 New table for storing every prediction attempt
class PredHistory(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="pred_history")
    major = models.CharField(max_length=100, blank=True)
    cgpa = models.DecimalField(max_digits=4, decimal_places=2, null=True, blank=True)
    degree = models.CharField(max_length=100, blank=True, null=True)
    skills = models.TextField(blank=True, null=True)
    year_of_graduation = models.IntegerField(null=True, blank=True)
    predicted_output = models.TextField(blank=True, null=True)  # 🔥 Add this
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user.username} - {self.major}"


