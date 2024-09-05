from django.shortcuts import render,redirect
from .models import Recruiter,Jobseeker,Job,Applications
from django.contrib import messages
from django.contrib.auth import login
from django.contrib.auth.models import User,auth
from django.contrib.auth.decorators import login_required
from django.templatetags.static import static
from django.contrib.auth import update_session_auth_hash
from django.utils import timezone
from django.db.models import Count
from django.db.models import Q
# Create your views here.

def careerhome(request):
    return render(request,'careerhome.html')

def careernav(request):
    return render(request,'careernav.html')

def pricing(request):
    return render(request,'pricing.html')

def careercontact(request):
    return render(request,'careercontact.html')

def recruiterreg(request):
    return render(request,'recruiterreg.html')

def hiring(request):
    if request.method == 'POST':
        cname = request.POST['cname']
        about = request.POST['about']
        uname = request.POST['uname']
        email = request.POST['email']
        password = request.POST['password']
        cpassword = request.POST['cpassword']
        location = request.POST['location']
        image = request.FILES.get('image')

        if password==cpassword:
            if User.objects.filter(username=uname).exists():
                    messages.info(request, 'Username exists')
                    return redirect('recruiterreg')
            elif User.objects.filter(email=email).exists():
                messages.info(request, 'Email already exists')
                return redirect('recruiterreg')
            else:
                user = User.objects.create_user(username=uname, password=password, email=email)
                user.save()

                    # Check if an image was uploaded
                if image==None:
                        # Set default image path using the static function
                    image = static('images/userr.jpg')
                    x = Recruiter(comp_name=cname, image=image, about=about, user=user,location=location)
                    x.save()
                else:    
                    x = Recruiter(comp_name=cname, image=image, about=about, user=user,location=location)
                    x.save()
                messages.success(request, 'Registration Successful ')
                return redirect('recruiterlog')
        else:
            messages.error(request,'Passwords do not match. Please try again.')
            return redirect('recruiterreg')

def candreg(request):
    return render(request,'candreg.html')

def jobseeker(request):
    if request.method == 'POST':
        firstname = request.POST['firstname']
        lastname = request.POST['lastname']
        about = request.POST['about']
        uname = request.POST['uname']
        email = request.POST['email']
        password = request.POST['password']
        cpassword = request.POST['cpassword']
        address = request.POST['address']
      
        image = request.FILES.get('image')
        resume = request.FILES.get('cv')

        if password==cpassword:
            if User.objects.filter(username=uname).exists():
                    messages.info(request, 'Username exists')
                    return redirect('candreg')
            elif User.objects.filter(email=email).exists():
                    messages.info(request, 'Email already exists')
                    return redirect('candreg')
            else:
                user = User.objects.create_user(username=uname,first_name=firstname,last_name=lastname, password=password, email=email)
                user.save()

                    # Check if an image was uploaded
                if image==None:
                        # Set default image path using the static function
                    image = static('images/userr.jpg')
                    x = Jobseeker(resume=resume, image=image, about=about, user=user,address=address)
                    x.save()
                else:    
                    x = Jobseeker(resume=resume, image=image, about=about, user=user,address=address)
                    x.save()
                messages.success(request, 'Registration Successful ')
                return redirect('candlog')
        else:
            messages.error(request,'Passwords do not match. Please try again.')
            return redirect('candreg')

def recruiterlog(request):
    return render(request,'recruiterlog.html')

def rlog(request):
    if request.method=='POST':
        uname=request.POST['user']
        password=request.POST['password']
        user=auth.authenticate(username=uname,password=password)
        if user is not None:
            if user.first_name:
                messages.error(request, 'Invalid Username or Password')
                return redirect('recruiterlog')

               
            else:
                login(request, user)
                return redirect('recruiterhome')
        else:
            messages.error(request,'Invalid Username or password')
            return redirect('recruiterlog')
    return render(request,'recruiterlog.html')


def candlog(request):
    return render(request,'candlog.html')

def clog(request):
    if request.method=='POST':
        uname=request.POST['user']
        password=request.POST['password']
        user=auth.authenticate(username=uname,password=password)
        if user is not None:
            if user.first_name:
                login(request, user)
                return redirect('candhome')
            else:
                messages.error(request, 'Invalid Username or Password')
                return redirect('candlog')

        else:
            messages.error(request,'Invalid Username or password')
            return redirect('candlog')
    return render(request,'candlog.html')

def candnav(request):
    return render(request,'candnav.html')

@login_required(login_url='careerhome')  
def candhome(request):
    currentuser=request.user
    job=Job.objects.all()
    applied_jobs = Applications.objects.filter(user=currentuser).values_list('jobname_id', flat=True)

    query = request.GET.get('search')
    if query:
        job = Job.objects.filter(
            Q(jobname__icontains=query) |
            Q(hire__comp_name__icontains=query) |
            Q(hire__location__icontains=query)
        )
    else:
        job = Job.objects.all()
    return render(request,'candhome.html',{'currentuser':currentuser,'job':job,'applied_jobs':applied_jobs})

@login_required(login_url='careerhome')  
def candpro(request):
    currentuser=request.user
    profile=Jobseeker.objects.get(user=currentuser)
    return render(request,'candpro.html',{'currentuser':currentuser,'profile':profile})

@login_required(login_url='careerhome')  
def update_profile(request):
    if request.method == 'POST':
        user = request.user
        user.first_name = request.POST['first_name']
        user.last_name = request.POST['last_name']
        profile = Jobseeker.objects.get(user=user)
        profile.address = request.POST['address']
        profile.about = request.POST['about']

        new=request.FILES.get('image')
        if new:
            profile.image = new

        newcv=request.FILES.get('cv')
        if newcv:
            profile.resume = newcv

        new_password = request.POST.get('new_password')
        old_password = request.POST.get('old_password')
        if new_password:
            if user.check_password(old_password):
                user.set_password(new_password)
                update_session_auth_hash(request, user)  # Keep the user logged in after changing password
                messages.success(request, 'Profile updated successfully.')
                user.save()
            else:
                messages.error(request, 'Old password is incorrect.')
                return render(request, 'candpro.html', {'profile': profile})
        user.save()
        profile.save()
        if not new_password:
            messages.success(request, 'Profile updated successfully.')
        return redirect('candpro')

def recruiternav(request):
    return render(request,'recruiternav.html')   

@login_required(login_url='careerhome')          
def recruiterhome(request):
    currentuser=request.user
    recruiter=Recruiter.objects.get(user=currentuser)
    return render(request,'recruiterhome.html',{'currentuser':currentuser,'recruiter':recruiter})

@login_required(login_url='careerhome')  
def recupdate_profile(request):
    if request.method == 'POST':
        user = request.user
        prorec = Recruiter.objects.get(user=user)
        prorec.comp_name = request.POST['comp_name']
        prorec.location = request.POST['location']
        prorec.about = request.POST['about']
        new=request.FILES.get('image')
        if new:
            prorec.image = new
        user.save()
        prorec.save()
        messages.success(request, 'Profile updated successfully.')
        return redirect('recruiterhome')
    
@login_required(login_url='careerhome')  
def recruiterpro(request):
    currentuser=request.user
    profile=Recruiter.objects.get(user=currentuser)
    return render(request,'recruiterpro.html',{'currentuser':currentuser,'profile':profile})       

@login_required(login_url='careerhome')  
def change_pass(request):
    if request.method == 'POST':
        user = request.user
        profile = Recruiter.objects.get(user=user)
        new_password = request.POST.get('new_password')
        old_password = request.POST.get('old_password')
        if new_password:
            if user.check_password(old_password):
                user.set_password(new_password)
                update_session_auth_hash(request, user)  # Keep the user logged in after changing password
                messages.success(request, 'Profile updated successfully.')
                user.save()
            else:
                messages.error(request, 'Old password is incorrect.')
                return render(request, 'recruiterpro.html', {'profile': profile})
        user.save()
        profile.save()
        if not new_password:
            messages.success(request, 'Profile updated successfully.')
        return redirect('recruiterpro')     
    
@login_required(login_url='careerhome')  
def postjob(request):
    if request.method == 'POST':
        jobname = request.POST['jobname']
        qualification = request.POST['qualification']
        experience = request.POST['experience']
        details = request.POST['details']
        user = request.user
        recruiter = Recruiter.objects.get(user=user)
        posted_at = timezone.now()
        Job.objects.create(user=user,hire=recruiter, jobname=jobname, qualification=qualification, experience=experience,posted_at=posted_at,about_job=details)
        messages.success(request, 'Job posted successfully.')
        return redirect('recruiterhome')
    
@login_required(login_url='careerhome')  
def recruitermanage(request):
     currentuser=request.user
     posting = Job.objects.filter(user=currentuser).annotate(app_count=Count('applications'))
     return render(request,'recruitermanage.html',{'posting':posting})
    
@login_required(login_url='careerhome')  
def deletejob(request,id):
    job =Job.objects.get(id=id)
    job.cancel = True
    job.save()
    return redirect('recruitermanage')

@login_required(login_url='careerhome')  
def applyjob(request,id):
    job =Job.objects.get(id=id)
    seeker = Jobseeker.objects.get(user=request.user)
    applied_at = timezone.now()
    Applications.objects.create(
        user=request.user,
        hire=job.hire,
        jobname=job,
        seeker=seeker,
        applied_at=applied_at
    )
    messages.success(request, 'Application sent.')
    return redirect('candhome')

@login_required(login_url='careerhome')  
def candmanage(request):
    applications = Applications.objects.filter(user=request.user)
    return render(request, 'candmanage.html', {'applications': applications})

@login_required(login_url='careerhome')  
def withdraw_application(request,id):
    application = Applications.objects.get(id=id, user=request.user)
    application.delete()
    messages.success(request, 'Application successfully withdrawn.')
    return redirect('candmanage') 

@login_required(login_url='careerhome')  
def view_applications(request, id):
    job = Job.objects.get(id=id)
    applications = Applications.objects.filter(jobname=job)
    return render(request, 'view_applications.html', {'job': job, 'applications': applications})

@login_required(login_url='careerhome')  
def select(request,id):
    appli =Applications.objects.get(id=id)
    appli.status = 'selected'
    appli.save()
    job_id = appli.jobname.id
    messages.success(request, 'Application Accepted.')  # Get the job id from the application
    return redirect('view_applications', id=job_id)

@login_required(login_url='careerhome')  
def reject(request,id):
    appli =Applications.objects.get(id=id)
    appli.status = 'rejected'
    appli.save()
    job_id = appli.jobname.id 
    messages.error(request, 'Application Rejected.')
    return redirect('view_applications', id=job_id)


def log_out(request):
    auth.logout(request)
    return redirect('careerhome')

