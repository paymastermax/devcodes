from django.db import models

# Create your models here.
class Signup(models.Model):
    uid = models.AutoField(primary_key=True)
    email = models.EmailField(max_length = 60 , unique = True)
    username = models.CharField(max_length = 30 , unique = True)
    # pnumber = models.IntegerField()
    # location = models.CharField(max_length = 30  , default = "Nairobi/Kenya")
    hobby = models.CharField(max_length = 30)
    profilepic = models.ImageField()
    # profilepic = models.FileField()
    password = models.CharField(max_length = 255)
    is_admin = models.BooleanField(default = False)
    # is_activated = models.BooleanField(default = False)

    class Meta:
        db_table = "signup"

# Create your models here.
class Recoverdata(models.Model):
    id = models.AutoField(primary_key = True , serialize = True)
    uid = models.ForeignKey(Signup , related_name = "recnewdb" , on_delete = models.CASCADE , default = 1)
    secret_code = models.CharField(max_length = 10 , default = [*range(10)])
