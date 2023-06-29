from django.db import models
from datetime import datetime

# Model for Quadra admin info
class user_info(models.Model):
    objects = None
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=100, null=True, blank=True)
    email = models.EmailField(null=True, blank=True)
    password = models.TextField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = "user_info"

class post_info(models.Model):
    objects = None
    id = models.AutoField(primary_key=True)
    title = models.CharField(max_length=30, null=True, blank=True)
    discription = models.CharField(max_length=100, null=True, blank=True)
    content = models.CharField(max_length=100, null=True, blank=True)    
    creation_date = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = "post_info"


class Liked_Saved(models.Model):
    objects = None
    id = models.AutoField(primary_key=True)
    user = models.ForeignKey(user_info,
                               null=True,
                               blank=True,
                               on_delete=models.CASCADE)
    post = models.ForeignKey(post_info,
                                     null=True,
                                     blank=True,
                                     on_delete=models.CASCADE)
    is_liked = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = "liked_saved_user"



# User Session Token
class UserSessionToken(models.Model):
    objects = None
    id = models.AutoField(primary_key=True)
    token = models.TextField(null=True, blank=True)
    user = models.ForeignKey(user_info, null=True,blank=True, on_delete=models.DO_NOTHING)
    updated_at = models.DateTimeField(auto_now=True)
    created_at = models.DateTimeField(auto_now=True)

    def save(self, *args, **kwargs):
        self.updated_at = datetime.now()
        return super(UserSessionToken, self).save(*args, **kwargs)

    class Meta:
        db_table = "user_session"
