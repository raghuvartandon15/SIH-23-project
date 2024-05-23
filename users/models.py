

from django.dispatch import receiver
from django.db.models.signals import post_save
from django.db import models
from django.contrib.auth.models import AbstractUser,BaseUserManager,Group
from django.contrib.auth import get_user_model

class CustomUserManager(BaseUserManager):
    def create_user(self, username, password=None, user_type=None, **extra_fields):
        user = self.model(username=username, user_type=user_type, **extra_fields)
        user.set_password(password)
        print(f"Password before save: {user.password}")
        user.save(using=self._db)
        print(f"Password after save: {user.password}")
        return user

    def create_superuser(self, username, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        extra_fields.setdefault('user_type', 4)
        return self.create_user(username, password, **extra_fields)

class CustomUser(AbstractUser):
    # Modify the field type and settings as needed

    USERNAME_FIELD = 'username'
    USER_TYPE_CHOICES = (
        (1, 'Student'),
        (2, 'Institute'),
        (3, 'StateAuthority'),
        (4, 'superuser')
    )

    user_type = models.PositiveSmallIntegerField(choices=USER_TYPE_CHOICES, null=True)
    objects = CustomUserManager()

    def save(self, *args, **kwargs):
        # Set any additional behavior before saving the user
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.username} - {self.get_user_type_display()}"


class StateAuthority(models.Model):
    user = models.OneToOneField(CustomUser, on_delete=models.CASCADE, primary_key=True)
    
    ##  -----State Authority Information----
    state_name = models.CharField(max_length=255)
    state_code = models.CharField(max_length=20, unique=True)
    # Add any other relevant fields specific to the state authority

    def __str__(self):
        return self.state_name



class Institute(models.Model):
    user = models.OneToOneField(CustomUser, on_delete=models.CASCADE, primary_key=True)
    
    ##  -----Institute Information----
    institute_name = models.CharField(max_length=255)
    institute_code = models.CharField(max_length=20, unique=True)
    # Add any other relevant fields specific to the institute

    def __str__(self):
        return self.institute_name
    

class ScholarCategory(models.Model):
    category = models.CharField(max_length=255,null=True,blank=True,default='Scholarship for Minorities')

    def __str__(self):
        return self.category

    
    
class Student(models.Model):
    user = models.OneToOneField(CustomUser, on_delete=models.CASCADE, primary_key=True)
    
    schol_cat = models.ForeignKey(ScholarCategory,on_delete=models.SET_NULL,null=True,blank=True)
    ## Adhaar Card -- 
    adhaar = models.CharField(max_length = 255)
    ##  -----General Information----
    domicile = models.ForeignKey(StateAuthority,on_delete=models.CASCADE,null=True,blank=True)
    # scholar_cat = models.CharField(max_length=255)
    dob = models.DateField(default='2000-01-01')
    gender = models.CharField(max_length=10)
    religion = models.CharField(max_length=255)
    category_caste = models.CharField(max_length=255)
    father_name = models.CharField(max_length=255)
    mother_name = models.CharField(max_length=255)
    annual_income = models.DecimalField(max_digits=10, decimal_places=2,null=True, blank=True)
    phone_number = models.CharField(max_length=15,unique=True, null=True)

    ##   ----Academic Details----
    # current
    institute = models.ForeignKey(Institute, on_delete=models.SET_NULL, null=True, blank=True)
    enrollment_no = models.CharField(max_length=20)
    admission_year = models.IntegerField(null=True, blank=True)
    course = models.CharField(max_length=255,null=True, blank=True)
    
    # Previous 12th Detail
    roll_12 = models.CharField(max_length=20)
    board_name_12 = models.CharField(max_length=255,null=True, blank=True)
    marks_12 = models.DecimalField(max_digits=5, decimal_places=2, null=True, blank=True)
    
    # Previous 10th Detail
    roll_10 = models.CharField(max_length=20, null=True, blank=True)
    board_name_10 = models.CharField(max_length=255, null=True, blank=True)
    marks_10 = models.DecimalField(max_digits=5, decimal_places=2, null=True, blank=True)

    ##  -- Other Details --
    disabled = models.BooleanField(default=False)
    marital_status = models.CharField(max_length=20, null=True, blank=True)
    parents_profession = models.CharField(max_length=255, null=True, blank=True)
    
    ## -- Bank Docs ---
    acc_number = models.CharField(max_length=50)
    ifsc_num = models.CharField(max_length=50)
    

    
    # attached_docs  : related name , use like this : student.attached_docs


    def __str__(self):
        return self.user.username  # Assuming 'username' is a field in AbstractUser


# Create groups during the initial migration
def create_groups(sender, **kwargs):
    Group.objects.get_or_create(name='Student')
    Group.objects.get_or_create(name='Institute')
    Group.objects.get_or_create(name='StateAuthority')



# Connect the create_groups function to the post_migrate signal
models.signals.post_migrate.connect(create_groups, sender=models)

# Disconnect the create_groups function after the initial migration
models.signals.post_migrate.disconnect(create_groups, sender=models)


User = get_user_model()

@receiver(post_save, sender=Institute)
def assign_institute_group(sender, instance, created, **kwargs):
    if created:
        # Assign the Institute group to the user associated with the Institute instance
        user = instance.user
        institute_group, _ = Group.objects.get_or_create(name='Institute')
        user.groups.add(institute_group)


@receiver(post_save, sender=StateAuthority)
def assign_state_authority_group(sender, instance, created, **kwargs):
    if created:
        # Assign the StateAuthority group to the user associated with the StateAuthority instance
        user = instance.user
        state_authority_group, _ = Group.objects.get_or_create(name='StateAuthority')
        user.groups.add(state_authority_group)
