from django.db.models.signals import post_save
#this is a signal that gets fired when an object is saved
#in this case we want to get a post_save signal when a user is created

from django.contrib.auth.models import User
#user model is going to be the sender

from django.dispatch import receiver
from .models import Profile

@receiver(post_save,sender=User)
def create_profile(sender,instance,created,**kwargs):
    if created:
        Profile.objects.create(user=instance)
        
        
@receiver(post_save,sender=User)
def save_profile(sender,instance,**kwargs):
   instance.profile.save()