from django.db import models
from django.contrib.auth.models import User
# Create your models here.

STATUS_CHOICES = [
    ('Pending', 'Pending'),
    ('In Progress', 'In Progress'),
    ('Resolved', 'Resolved')
]

class Complaint(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    title = models.CharField(max_length=200)
    description = models.TextField()
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='Pending')
    created_at = models.DateTimeField(auto_now_add=True)
    
    # New fields for images/videos
    image = models.ImageField(upload_to='complaint_images/', blank=True, null=True)
    video = models.FileField(upload_to='complaint_videos/', blank=True, null=True)

    def __str__(self):
        return self.title