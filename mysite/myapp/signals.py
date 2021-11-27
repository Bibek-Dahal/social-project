from django.db.models.signals import post_save
from django.dispatch import receiver
from account.models import MyUser
from .models import*
@receiver(post_save,sender= MyUser)
def Create_User_Profile(sender ,instance,created,**kwargs):
    if created:
        Profile.objects.create(user = instance)
        # ProfilePic.objects.create(user = instance)
        # CoverPic.objects.create(user=instance)
        # Profile.objects.create(user = instance)

@receiver(post_save,sender= Profile)
def Create_User_CoverPic(sender,instance,created,**kwargs):
    if created:
        ProfilePic.objects.create(user = instance)
        CoverPic.objects.create(user=instance)
        print('Sender',sender)
        print('instance',instance)
        print('Created',created)


