from django import forms

from scholar.models import Docs
from django import forms
from users.models import Institute, Student
from django.forms import ValidationError
       
# class InstituteForm(forms.ModelForm):
#     class Meta:
#         model = Institute
#         fields = ['username', 'password']
#         widgets = {
#             'password': forms.PasswordInput(),
#         }
#         labels = {
#             'username': 'Username',
#             'password': 'Password',
#         }
#         required = {
#             'username': True,
#             'password': True,
#         }

    # def clean(self):
    #     cleaned_data = super().clean()
    #     password = cleaned_data.get("password")
    #     password2 = cleaned_data.get("password2")
    #     if password != password2:
    #         raise forms.ValidationError(
    #             "Passwords do not match"
    #         )
        
#Student Model : 

# class ScholarCategory(models.Model):
#     category = models.CharField(max_length=255,null=True,blank=True,default='Scholarship for Minorities')

    
    
# class Student(models.Model):
#     user = models.OneToOneField(CustomUser, on_delete=models.CASCADE, primary_key=True)
    
#     schol_cat = models.ForeignKey(ScholarCategory,on_delete=models.SET_NULL,null=True,blank=True)
#     ## Adhaar Card -- 
#     adhaar = models.CharField(max_length = 255)
#     ##  -----General Information----
#     domicile = models.ForeignKey(StateAuthority,on_delete=models.CASCADE,null=True,blank=True)
#     scholar_cat = models.CharField(max_length=255)
#     dob = models.DateField(default='2000-01-01')
#     gender = models.CharField(max_length=10)
#     religion = models.CharField(max_length=255)
#     category_caste = models.CharField(max_length=255)
#     father_name = models.CharField(max_length=255)
#     mother_name = models.CharField(max_length=255)
#     annual_income = models.DecimalField(max_digits=10, decimal_places=2,null=True, blank=True)
#     phone_number = models.CharField(max_length=15,unique=True, null=True)

#     ##   ----Academic Details----
#     # current
#     institute = models.ForeignKey(Institute, on_delete=models.SET_NULL, null=True, blank=True)
#     enrollment_no = models.CharField(max_length=20)
#     admission_year = models.IntegerField(null=True, blank=True)
#     course = models.CharField(max_length=255,null=True, blank=True)
    
#     # Previous 12th Detail
#     roll_12 = models.CharField(max_length=20)
#     board_name_12 = models.CharField(max_length=255,null=True, blank=True)
#     marks_12 = models.DecimalField(max_digits=5, decimal_places=2, null=True, blank=True)
    
#     # Previous 10th Detail
#     roll_10 = models.CharField(max_length=20, null=True, blank=True)
#     board_name_10 = models.CharField(max_length=255, null=True, blank=True)
#     marks_10 = models.DecimalField(max_digits=5, decimal_places=2, null=True, blank=True)

#     ##  -- Other Details --
#     disabled = models.BooleanField(default=False)
#     marital_status = models.CharField(max_length=20, null=True, blank=True)
#     parents_profession = models.CharField(max_length=255, null=True, blank=True)
    
#     ## -- Bank Docs ---
#     acc_number = models.CharField(max_length=50)
#     ifsc_num = models.CharField(max_length=50)
    

    
#     # attached_docs  : related name , use like this : student.attached_docs


#     def __str__(self):
#         return self.user.username  # Assuming 'username' is a field in AbstractUser

class StudentScholarshipForm(forms.ModelForm):
    class Meta:
        model = Student
        fields  = '__all__'
        #specify value 
        exclude = ['user']


        labels = {
            'schol_cat': 'Scholarship Category',
            'adhaar': 'Adhaar Card',
            'domicile': 'Domicile',
            
            
        }
        #widgets for dob
        widgets = {
            'dob': forms.DateInput(attrs={'type': 'date'}),
        }
        #radiobutton for gender
        
        

    def clean_schol_cat(self):
        schol_cat = self.cleaned_data['schol_cat']
        if schol_cat is None:
            raise ValidationError("Please select a scholarship category.")
        return schol_cat

class UserDocsForm(forms.ModelForm):
    class Meta:
        model = Docs
        fields = [
            'applicant_photo',
            'domicile_certificate',
            'income_certficate',
            'caste_certificate',
            'aadhar_card',
            'bonafide',
            'fee_receipt',
            'passbook',
        ]
        labels = {
            'applicant_photo': 'Applicant Photo',
            'domicile_certificate': 'Domicile Certificate',
            'income_certficate': 'Income Certificate',
            'caste_certificate': 'Caste Certificate',
            'aadhar_card': 'Aadhar Card',
            'bonafide': 'Bonafide',
            'fee_receipt': 'Fee Receipt',
            'passbook': 'Passbook',
        }
        
        required = {
            'applicant_photo': True,
            'domicile_certificate': True,
            'income_certificate': True,
            'caste_certificate' : True,
            'aadhar_card': True,
            'bonafide': True,
            'fee_receipt': True,
            'passbook': True,
            
        }
        
        