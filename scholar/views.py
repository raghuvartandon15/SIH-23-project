from multiprocessing import AuthenticationError
from django.http import HttpResponseRedirect, HttpResponse
from django.shortcuts import get_object_or_404, render, redirect, reverse
# from scholar.forms import InstituteForm
from scholar.models import *
from scholar.forms import UserDocsForm
from scholar.models import ApplicationStatus

from django.contrib.auth import login, logout
from django.contrib.auth import authenticate, login
from django.contrib.auth.forms import AuthenticationForm
from scholar.forms import StudentScholarshipForm

from users.models import Student,Institute,StateAuthority,ScholarCategory
from scholar.models import Docs
from django.contrib import messages
from users.decorators import group_required


def update_scholar_application(request,id):
    # if request.method == "POST":
    context = {"dc" : "fd"}
    return render(request,'update_scholar_application.html',context)
        
        
    
def update_scholar_application2(request,id):
    ...

def home(request):
    return render(request, 'scholar/homepage.html')


def student_dashboard(request):
    student = Student.objects.get(user=request.user)
    approval  = ApplicationStatus.objects.get(student=student)
    print(student)
    applied = approval.application_submitted
    inst_val  = approval.institute_approval

    return render(request,'scholar/student_dashboard.html',{'inst_val':inst_val,'applied':applied})


        

def institute_login(request):
    if request.method == "POST":
        username = request.POST.get('username')
        password = request.POST.get('password')
        print(username,password)
        try:
            institute = Institute.objects.get(user__username=username)
            print(institute,"institute")
        except Institute.DoesNotExist:
            messages.info(request, "Invalid Username!!")
            return HttpResponseRedirect(reverse('scholar:institute_login'))
        
        # Check if the user type is Institute
        if institute.user.user_type != 2: # Assuming 2 is the user_type for Institute
            messages.error(request, 'Invalid user type. Please log in as an Institute.')
            return HttpResponseRedirect(reverse('scholar:institute_login'))
        
        user = authenticate(username=username, password=password)
        print("authenticated")
        if user is not None and user == institute.user:
            login(request, user)
            print("logged in")
            return HttpResponseRedirect(reverse('scholar:institute_dashboard'))
        else:
            messages.error(request, 'Invalid credentials.')
            return HttpResponseRedirect(reverse('scholar:institute_login'))

    return render(request, 'scholar/institute_login.html')

    
def institute_logout(request):
    logout(request)
    return HttpResponseRedirect(reverse('scholar:institute_login'))
    
# def student
def institute_dashboard(request):

    current_user = request.user
    institute = Institute.objects.get(user=current_user)

    # Get all student applications associated with the current institute
    student_applications = Student.objects.filter(institute=institute)
    print(student_applications)

    context = {'student_applications': student_applications}
    return render(request, 'scholar/institute_dashboard.html',context)

from django.shortcuts import render, get_object_or_404


def student_details(request, student_id):

    student = get_object_or_404(Student, pk=student_id)
    print(student)

    context = {'student': student}
    
    return render(request, 'scholar/student_view_in_institute.html', context)

  
def state_login(request):
    if request.method == "POST":
        username = request.POST.get('username')
        password = request.POST.get('password')
        print(username,password)
        try:
            state = StateAuthority.objects.get(user__username=username)
            print(state,"State")
        except Institute.DoesNotExist:
            messages.info(request, "Invalid Username!!")
            return HttpResponseRedirect(reverse('scholar:state_login'))
        
        # Check if the user type is State
        if state.user.user_type != 3: # Assuming 2 is the user_type for StateAuthority
            messages.error(request, 'Invalid user type. Please log in as an State.')
            return HttpResponseRedirect(reverse('scholar:state_login'))
        
        user = authenticate(username=username, password=password)
        print("authenticated")
        if user is not None and user == state.user:
            login(request, user)
            print("logged in")
            return HttpResponseRedirect(reverse('scholar:state_dashboard'))
        else:
            messages.error(request, 'Invalid credentials.')
            return HttpResponseRedirect(reverse('scholar:state_login'))

    return render(request, 'scholar/state_login.html')
    
def state_dashboard(request):
    return render(request,'scholar/state_dashboard.html')
    
    
def state_logout(request):
    logout(request)
    return HttpResponseRedirect(reverse('scholar:state_login'))

def view_details(request, student_id):
    student = get_object_or_404(Student, id=student_id)
    docs = Docs.objects.get(student=student)
    
    context = {'student': student, 'docs': docs}
    return render(request, 'view_details.html', context)

# @group_required('Student')
# def Scholar_application(request):
    
#     if request.method == 'POST':
#         print('posted')
#         form = StudentScholarshipForm(request.POST)
#         if form.is_valid():
#             print('valid')
#         # Save the form data to create a new Student instance
#             student_instance.user = request.user
#             student_instance = form.save()
#             print('saved',student_instance)
#             # Now associate the logged in user with the Student instance
            
#             return HttpResponseRedirect(reverse('scholar:Scholar_application2'))  # Replace 'success_page' with your actual success page URL

#     else:
#         form = StudentScholarshipForm()



@group_required('Student')
def Scholar_application(request):
    if request.method == 'POST':
        print('posted')
        form = StudentScholarshipForm(request.POST)
        if form.is_valid():
            print('valid')
            student_instance = form.save(commit=False)
            student_instance.user = request.user
            student_instance.save()
            print('saved',student_instance)
            return HttpResponseRedirect(reverse('scholar:Scholar_application2'))
        else:
            print('invalid')
            print(form.errors)
    else:
        form = StudentScholarshipForm()

    return render(request, 'scholar/scholar_application.html', {'form': form})

        
        

    # details = Student.objects.get(user=request.user)
    # scholar_categories = ScholarCategory.objects.all()
        # return render(request,'scholar/scholar_application.html',{'form': form})



# def Scholar_application2(request):
#     if request.method == "POST":
        
#         data = request.POST
        
#         applicant_photo = request.FILES.get('applicant_photo')
#         domicile_certificate = request.FILES.get('applicant_photo')
#         income_certficate = request.FILES.get('income_certficate')
#         caste_certificate = request.FILES.get('caste_certificate')
#         aadhar_card = request.FILES.get('aadhar_card')
#         bonafide = request.FILES.get('bonafide')
#         fee_receipt = request.FILES.get('fee_receipt')
#         passbook = request.FILES.get('passbook')

#         student_files = Docs.objects.create(
#             student = request.user.student,
#             applicant_photo = applicant_photo,
#             domicile_certificate = domicile_certificate,
#             income_certficate = income_certficate,
#             caste_certificate = caste_certificate,
#             aadhar_card = aadhar_card,
#             bonafide = bonafide,
#             fee_receipt = fee_receipt,
#             passbook = passbook,
#         )
#         student_files.save()
#         return HttpResponseRedirect(reverse('scholar:student_dashboard'))
        
#     return render(request,'scholar/scholar_application2.html')

@group_required('Student')
def Scholar_application2(request):
    if request.method == 'POST':
        form = UserDocsForm(request.POST, request.FILES)
        print(request.POST)  # Add this line to print POST data
        print(request.FILES)
        if form.is_valid():
            print('valid')
            # Save the document form data
            docs_instance = form.save(commit=False)
            print(docs_instance)
            # Associate the document with the logged-in student
            docs_instance.student = request.user.student
            docs_instance.save()
            print('saved')

            student_application_status = get_object_or_404(ApplicationStatus, student=request.user.student)
            student_application_status.application_submitted = True
            student_application_status.save()
            print('application status updated')
            return HttpResponseRedirect(reverse('scholar:student_dashboard'))
        else:
            print('invalid')
            print(form.errors)
    else:
        form = UserDocsForm()

    return render(request, 'scholar/scholar_application2.html', {'form': form})


def student_view_institute(request):
    return render(request,'scholar/student_view_in_institute.html')
#aise hoga ye wrna create se to nya student ka bn jaega The view scholar.views.Scholar_application didn't return an HttpResponse object. It returned None instead.The view scholar.views.Scholar_application didn't return an HttpResponse object. It returned None instead.
# ok  student login and scholar_application ko integrate kar diya hu css k saath base.html use kiya hu
#ok great
#ok
#wse session chat khol lo  baad meh comment ko hataa denge
#



        # data = request.POST
        # print(data)
        # scholar_cat = data.get('scholarshipname')
        # aadhaar = data.get('adhaar')
        # dob = data.get('dob')
        # father_name = data.get('father_name')
        # mother_name = data.get('mother_name')
        # gender = data.get('gender')
        # domicile = data.get('domicile')
        # phone_number  = data.get('phone_number')
        # annual_income = data.get('annual_income')
        # category = data.get('annual_income')
        # religion = data.get('religion')
        
        # enrollment = data.get('enrollment')
        # adm_year = data.get('adm_year')

        # board_name_12  = data.get('pre_board')
        # marks_12 = data.get('percentage')
        
        
        # disabled = data.get('disabled')
        # parents_profession = data.get('parents_profession')
        # acc_number = data.get('acc_no')
        # ifsc_num = data.get('ifsc')
        
        # current_student = Student.objects.get(user=request.user)
        # print(current_student)
        
        #  # Retrieve or create a Student object associated with the current user
        # current_student, created = Student.objects.get_or_create(user=request.user)
        

        # print('checked')
        # # current_student.applicant_name = applicant_name,
        # current_student.schol_cat = scholar_cat,
        # current_student.adhaar = aadhaar,
        # current_student.dob = dob,
        # current_student.father_name = father_name,
        # current_student.mother_name = mother_name,
        # current_student.gender = gender,
        # current_student.annual_income = annual_income,
        # current_student.category_caste = category,
        # current_student.religion = religion,
        # current_student.phone_number = phone_number
        # current_student.enrollment = enrollment,
        # current_student.admission_year = adm_year,
    
        # current_student.board_name_12 = board_name_12,
        # current_student.marks_12 = marks_12,

        # current_student.disabled = disabled,
        # current_student.parents_profession = parents_profession,
        # current_student.acc_number = acc_number,
        # current_student.ifsc_num = ifsc_num,
        # current_student.domicile = domicile,
        
        # print(current_student.domicile)
        # print(current_student.domicile,"jfriogjeri;ogj")
        
        
        # current_student.save()


def approve_at_institute(request, student_id):
    print('toggle_approval')
    application = get_object_or_404(ApplicationStatus,student=student_id)
    print(application)
    print(application.institute_approval) 
    if request.method == 'POST':
        print("HIHBUHVJBNKJBH")
        # Get the approval status from the form submission
        approval_status = request.POST.get('approval_status')
        

        # Toggle the 'approved' field
        application.institute_approval = True
        application.save()
        print('approved')
        
        return HttpResponseRedirect(reverse('scholar:institute_dashboard'))