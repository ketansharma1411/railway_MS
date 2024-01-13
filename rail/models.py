from django.db import models

# Create your models here.
class user_info(models.Model):
    username=models.CharField(max_length=50)
    password=models.CharField(max_length=50)
    email=models.CharField(max_length=100)
    is_verified=models.IntegerField(default=0)
    otp=models.IntegerField(default=0000)
    last_login=models.CharField(max_length=80)
    login_status=models.IntegerField(default=0)

class train(models.Model):
    def __str__(self):
        return self.train_name

    train_name=models.CharField(max_length=100)
    train_no=models.IntegerField()
    coach=models.CharField(max_length=40)
    from_st=models.CharField(max_length=100)
    to_st=models.CharField(max_length=100)
    no_tickets=models.IntegerField()

class history(models.Model):
    username=models.CharField(max_length=100)
    email=models.CharField(max_length=100)
    train_no=models.IntegerField()
    from_st=models.CharField(max_length=100)
    to_st=models.CharField(max_length=100)
    coach=models.CharField(max_length=100)
    no_tickets=models.IntegerField()

class booking_details(models.Model):
    username=models.CharField(max_length=100)
    train_no=models.IntegerField()
    passenger_name=models.CharField(max_length=100)
    pnr_no=models.CharField(max_length=100)
    coach_no=models.CharField(max_length=10)
    seat_no=models.IntegerField()
    


    
