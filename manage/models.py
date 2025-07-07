from django.db import models
from django.contrib.auth import get_user_model

User = get_user_model()

class Project(models.Model):
    title = models.CharField(max_length=200)
    description = models.TextField()
    start_date = models.DateField()
    end_date = models.DateField()

    def __str__(self):
        return self.title

class Task(models.Model):
    STATUS_CHOICES = [
        ('to do', 'To Do'),
        ('in progress', 'In Progress'),
        ('done', 'Done'),
    ]
    project = models.ForeignKey(Project, on_delete=models.CASCADE, related_name='tasks')
    title = models.CharField(max_length=200)
    description = models.TextField()
    assignees = models.ManyToManyField(
    User,
    blank=True,
    related_name='tasks')
    due_date = models.DateField()
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='to do')

    def __str__(self):
        return f"{self.title} ({self.get_status_display()})"
    
from django.dispatch import receiver
from django.db.models.signals import post_save

def user_avatar_path(instance, filename):
    return f'avatars/user_{instance.user.id}/{filename}'

class Profile(models.Model):
    user   = models.OneToOneField(User, on_delete=models.CASCADE, related_name='profile')
    avatar = models.ImageField(
        upload_to=user_avatar_path,
        default='avatars/default.png'
    )

@receiver(post_save, sender=User)
def ensure_profile_exists(sender, instance, **kwargs):
    Profile.objects.get_or_create(user=instance)