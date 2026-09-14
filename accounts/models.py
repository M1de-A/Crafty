from django.contrib.auth.models import User
from django.db import models

class Profile(models.Model):
    ROLE_CHOICES=[('buyer','Покупатель'),('seller','Продавец')]
    user=models.OneToOneField(User,on_delete=models.CASCADE,related_name='profile')
    role=models.CharField(max_length=20,choices=ROLE_CHOICES,default='buyer')
    avatar=models.ImageField(upload_to='profiles/',blank=True)
    verification_status=models.CharField(max_length=20,default='not_started')
    verification_level=models.CharField(max_length=30,default='new')
    trust_score=models.PositiveSmallIntegerField(default=0)
    free_showcases=models.PositiveIntegerField(default=5)
    promotion_priority=models.PositiveSmallIntegerField(default=0)
    payout_priority=models.BooleanField(default=False)
    def __str__(self):return self.user.username
