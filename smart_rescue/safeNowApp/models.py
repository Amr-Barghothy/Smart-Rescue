from django.db import models
import bcrypt
import re

# Create your models here.
class UserManager(models.Manager):
    def basic_validator_login(self, postData):
        errors = {}
        user = User.objects.filter(email = postData['email'])
        EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')
        if not EMAIL_REGEX.match(postData['email']):
            errors['email'] = "Wrong email address!"
        if len(postData['password']) < 8:
            errors["password"] = "Password should be at least 8 characters"    
        if len(postData['email']) == 0 :   
            errors["emailrequired"] = "Email is required!"  
        if len(postData['password']) == 0 :   
            errors["passwordrequired"] = "Password is required!"    
         
        if not len(user):
            errors['emailnewuser'] = "Email is not registered" 
        return errors

    def basic_validator_reg(self, postData):
        errors = {}
        new_user = User.objects.filter(email = postData['email'])
        if len(postData['password']) < 8:
            errors["password"] = "Password should be at least 8 characters"  
        if len(postData['confirmpassword']) < 8:
            errors["confirmpassword"] = "Confirm Password should be at least 8 characters" 
        if len(postData['lastname']) < 3:
            errors["lastname"] = "Last name should be at least 3 characters" 
        if len(postData['firstname']) < 3:
            errors["firstname"] = "First Name should be at least 3 characters" 
        EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')
        if not EMAIL_REGEX.match(postData['email']):
            errors['email'] = "Wrong email address!"
        if postData['password'] != postData['confirmpassword']:
            errors['password_confirm'] = "Password Dosent Match!"
        if len(postData['email']) == 0 :   
            errors["emailrequired"] = "Email is required!"  
        if len(postData['password']) == 0 :   
            errors["passwordrequired"] = "Password is required!"
        if len(postData['confirmpassword']) == 0 :   
            errors["confirmpasswordrequired"] = "Confrim password is required!"
        if len(postData['lastname']) == 0 :   
            errors["lastnamerequired"] = "Last name is required!"
        if len(postData['firstname']) == 0 :   
            errors["firstnamerequired"] = "First name is required!"   
        if len(new_user):
            errors['emailnewuser'] = "Email already exist" 
        return errors

class User(models.Model):
    firstname = models.CharField(max_length=255)
    lastname = models.CharField(max_length=255)
    email = models.CharField(max_length=255)
    password = models.CharField(max_length=255)
    address = models.CharField(max_length=255)
    DOB = models.DateField()
    role = models.CharField(max_length=255)
    phonenumber = models.CharField(max_length=255)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    objects=UserManager()
    



class CaseEmergency(models.Model):
    title = models.CharField(max_length=255)
    category = models.CharField(max_length=255)
    status = models.CharField(max_length=255)
    long = models.FloatField()
    lat = models.FloatField()
    description = models.CharField(max_length=255)
    image = models.ImageField(upload_to='images/',blank=True)
    audio = models.FileField(upload_to='audio/',blank=True)
    created_by = models.ForeignKey(User, related_name="cases", on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

class Services(models.Model):
    title = models.CharField(max_length=255)
    description = models.CharField(max_length=255)
    location = models.CharField(max_length=255)
    category = models.CharField(max_length=255)
    created_at = models.DateTimeField(auto_now_add=True)
    rating = models.IntegerField()
    owner = models.ForeignKey(User, related_name="services", on_delete=models.CASCADE)
    updated_at = models.DateTimeField(auto_now=True)
    
def get_users():
    return User.objects.all()

def get_user(id):
    return User.objects.get(id = id)

def create_user(post):
    user_password = post['password']
    hash1 = bcrypt.hashpw(user_password.encode(), bcrypt.gensalt()).decode()
    return User.objects.create( firstname = post['firstname'], lastname= post['lastname'] , phonenumber = post['phonenumber'], email =  post['email'], password = hash1, DOB = post['DOB'],address=post['address'])

def login_user(post,session):
    user_exist = User.objects.filter(email=post['email'])
    if user_exist:
        logged_user = user_exist[0]
        if bcrypt.checkpw(post['password'].encode(), logged_user.password.encode()):
            session['user_id'] = logged_user.id
            return True
    return False
    
    
