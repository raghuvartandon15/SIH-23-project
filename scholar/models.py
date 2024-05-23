
from django.db import models
from users.models import Student,Institute, StateAuthority
from django.contrib.auth.models import AbstractUser,BaseUserManager,Group


# Inside your app's models.py

from django.contrib.auth.models import AbstractUser


class InstituteUser(BaseUserManager):
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
        extra_fields.setdefault('user_type', 2)
        return self.create_user(username, password, **extra_fields)

class Docs(models.Model):
    
    student = models.ForeignKey(Student, on_delete=models.CASCADE,related_name='attached_docs')
    applicant_photo = models.ImageField(upload_to="user_detail/")
    domicile_certificate = models.ImageField(upload_to="user_detail/")
    income_certficate = models.ImageField(upload_to="user_detail/")
    caste_certificate = models.ImageField(upload_to="user_detail/")
    aadhar_card = models.ImageField(upload_to="user_detail/")
    bonafide = models.ImageField(upload_to="user_detail/")
    fee_receipt = models.ImageField(upload_to="user_detail/")
    passbook = models.ImageField(upload_to="user_detail/")


class ApplicationStatus(models.Model):
    student = models.ForeignKey(Student, on_delete=models.CASCADE)
    institute = models.ForeignKey(Institute, on_delete=models.CASCADE, null=True, blank=True)
    state_authority = models.ForeignKey(StateAuthority, on_delete=models.CASCADE, null=True, blank=True)
    
    # Add fields to track the status at each level
    application_submitted = models.BooleanField(default=False)
    institute_approval = models.BooleanField(default=False)
    state_approval = models.BooleanField(default=False)
    final_approval = models.BooleanField(default=False)
    
    # Additional fields for comments, timestamps, etc., can be added based on requirements
        # Remarks at each level
    institute_remarks = models.TextField(null=True, blank=True)
    state_authority_remarks = models.TextField(null=True, blank=True)

    # Timestamps for each level
    institute_verification_time = models.DateTimeField(null=True, blank=True)
    state_authority_verification_time = models.DateTimeField(null=True, blank=True)
    
    def __str__(self):
        return f"Application Status for {self.student}"