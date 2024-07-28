from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver

# Create your models here.
class Post(models.Model):
	title = models.CharField(max_length = 100,blank = True,null = True)
	body = models.TextField()
	image = models.ImageField(upload_to='uploads/post_photos', blank = True,null = True)
	created_on = models.DateTimeField(default = timezone.now)
	author = models.ForeignKey(User, on_delete=models.CASCADE)
	likes = models.ManyToManyField(User, blank=True, related_name='likes')
	dislikes = models.ManyToManyField(User, blank=True, related_name='dislikes')

class Comment(models.Model):
	comment = models.TextField()
	created_on = models.DateTimeField(default = timezone.now)
	author = models.ForeignKey(User, on_delete=models.CASCADE)
	post = models.ForeignKey('Post', on_delete=models.CASCADE)

class UserProfile(models.Model):
	user = models.OneToOneField(User,primary_key=True,verbose_name='user',related_name='profile',on_delete=models.CASCADE)
	name = models.CharField(max_length=30, blank=True, null=True)
	bio = models.TextField(max_length=10000, blank=True, null=True)
	birth_date = models.DateField(blank=True, null=True)
	location = models.CharField(max_length=30, blank=True, null=True)
	picture = models.ImageField(upload_to='uploads/profile_pictures',default='uploads/profile_pictures/default.jpg', blank=True, null=True)
	followers = models.ManyToManyField(User, blank=True, null = True, related_name='followers')

######this section create profile auto after registration

# sender - User
# receiver - decorator(@receiver)
# instance - User object being saved
# created - true/false


@receiver(post_save, sender=User)
def create_user_profile(sender,instance,created,**kwargs):
	if created:
		UserProfile.objects.create(user=instance)

@receiver(post_save,sender=User)
def save_user_profile(sender,instance,**kwargs):
	instance.profile.save() 

############################################################



class ThreadModel(models.Model):
	user = models.ForeignKey(User, on_delete=models.CASCADE,related_name='+')
	receiver = models.ForeignKey(User,on_delete=models.CASCADE,related_name='+')

class MessageModel(models.Model):
	thread = models.ForeignKey('ThreadModel', related_name='+', on_delete=models.CASCADE,blank=True,null=True)
	sender_user = models.ForeignKey(User,on_delete=models.CASCADE,related_name='+')
	receiver_user = models.ForeignKey(User,on_delete=models.CASCADE,related_name='+')
	body = models.CharField(max_length=1000)
	image = models.ImageField(blank=True,null=True,upload_to="media/uploads/message_photos")
	date = models.DateTimeField(default=timezone.now)
	is_read = models.BooleanField(default=False)


# trial
class Article(models.Model):
    title = models.CharField(max_length=200)
    content = models.TextField()

    def __str__(self):
        return self.title