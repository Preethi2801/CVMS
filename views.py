from django.shortcuts import render,redirect,HttpResponse
from cvmsapp.EmailBackEnd import EmailBackEnd
from django.contrib.auth import  logout,login
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from cvmsapp.models import CustomUser,AddVisitor
from django.db.models import Q
from datetime import datetime
from django.db.models import Count
from django.utils import timezone
from datetime import timedelta

from django.contrib.auth import get_user_model
User = get_user_model()



from django.contrib.auth.forms import AuthenticationForm


def BASE(request):
    return render(request,'base.html')


def LOGIN(request):
    return render(request,'login.html')

def doLogin(request):
    if request.method == 'POST':
        user = EmailBackEnd.authenticate(request,
                                         username=request.POST.get('email'),
                                         password=request.POST.get('password')
                                         )
        if user!=None:
            login(request,user)
            return redirect('index')
            
        else:
                messages.error(request,'Email or Password is not valid')
                return redirect('login')
    else:
            messages.error(request,'Email or Password is not valid')
            return redirect('login')
        


def doLogout(request):
    logout(request)
    return redirect('login')

@login_required(login_url='/')
def INDEX(request):
    end_date = timezone.now()
    start_date = end_date - timedelta(days=7)
    today = end_date.date()
    yesterday = today - timedelta(days=1)
    visitor_count = AddVisitor.objects.all().count()

    # Filter data for the last seven days
    data_count_last_seven_days = AddVisitor.objects.filter(created_at__range=(start_date, end_date)).count()
    
    # Filter data for today
    data_count_today = AddVisitor.objects.filter(created_at__date=today).count()
    
    # Filter data for yesterday
    data_count_yesterday = AddVisitor.objects.filter(created_at__date=yesterday).count()
    
    return render(request, 'index.html', {
        'data_count_last_seven_days': data_count_last_seven_days,
        'data_count_today': data_count_today,
        'data_count_yesterday': data_count_yesterday,
        'visitor_count': visitor_count,
    })


login_required(login_url='/')
def PROFILE(request):
    user = CustomUser.objects.get(id = request.user.id)
    context = {
        "user":user,
    }
    return render(request,'profile.html',context)
    

@login_required(login_url = '/')
def PROFILE_UPDATE(request):
    if request.method == "POST":
        profile_pic = request.FILES.get('profile_pic')
        first_name = request.POST.get('first_name')
        last_name = request.POST.get('last_name')
        email = request.POST.get('email')
        username = request.POST.get('username')
        password = request.POST.get('password')

        try:
            customuser = CustomUser.objects.get(id = request.user.id)
            customuser.first_name = first_name
            customuser.last_name = last_name
            

            if password !=None and password != "":
                customuser.set_password(password)
            if profile_pic !=None and profile_pic != "":
               customuser.profile_pic = profile_pic
            customuser.save()
            messages.success(request,"Your profile has been updated successfully")
            return redirect('profile')

        except:
            messages.error(request,"Your profile updation has been failed")
    return render(request, 'profile.html')

@login_required(login_url = '/')
def ADD_VISITOR(request):
    if request.method == "POST":
        fullname = request.POST.get('fullname')
        email = request.POST.get('email')        
        mobilenumber = request.POST.get('mobilenumber')
        address = request.POST.get('address')
        whomtomeet = request.POST.get('whomtomeet')
        department = request.POST.get('department')
        reasontomeet = request.POST.get('reasontomeet')

        visitor = AddVisitor(fullname=fullname,
                             email=email,
                             mobilenumber=mobilenumber,
                             address=address,
                             whomtomeet=whomtomeet,
                             department=department,
                             reasontomeet=reasontomeet,)
        visitor.save()
        messages.success(request, "Visitor details have been saved")
        return redirect('add_visitor')

    return render(request, 'visitors-form.html')


login_required(login_url='/')
def MANAGE_VISITOR(request):
    visitor1 = AddVisitor.objects.all()
    
    context = {
         'visitor1':visitor1,
    }

    return render(request,'manage-visitor.html',context)

login_required(login_url='/')
def UPDATE_VISITOR(request,id):
    visitor = AddVisitor.objects.filter(id=id)
    
    context = {
         'visitor':visitor,
    }

    return render(request,'update-visitor.html',context)

def UPDATE_VISITOR_REMARK(request):
    if request.method == 'POST':
        visitor_id= request.POST.get('vis_id')
        remark = request.POST['remark']
        status = request.POST['status']
        visitor= AddVisitor.objects.get(id=visitor_id)
        visitor.remark = remark
        visitor.status = status
        visitor.save()
        messages.success(request,"Remark has been updated successfully")
        return redirect('manage_visitor')
    
    
    return render(request,'update-visitor.html')



def DELETE_VISITOR(request,id):
    visitor = AddVisitor.objects.get(id=id)
    visitor.delete()
    messages.success(request,'Record Delete Succeesfully!!!')
    
    return redirect('manage_visitor')


def Between_Date_Report(request):
    start_date = request.GET.get('start_date')
    end_date = request.GET.get('end_date')

    visitor = []

    if start_date and end_date:
        # Validate the date inputs
        try:
            start_date = datetime.strptime(start_date, '%Y-%m-%d').date()
            end_date = datetime.strptime(end_date, '%Y-%m-%d').date()
        except ValueError:
            return render(request, 'between-date.html', {'visitor': visitor, 'error_message': 'Invalid date format'})

        # Filter visitors between the given date range
        visitor = AddVisitor.objects.filter(created_at__range=(start_date, end_date))

    return render(request, 'between-date.html', {'visitor': visitor,'start_date':start_date,'end_date':end_date})
    

def Search(request):
    if request.method == "GET":
        query = request.GET.get('query', '')
        if query:
            # Filter records where fullname or mobilenumber contains the query
            visitor = AddVisitor.objects.filter(fullname__icontains=query) | AddVisitor.objects.filter(mobilenumber__icontains=query)
            messages.info(request, "Search against " + query)
            return render(request, 'search.html', {'visitor': visitor, 'query': query})
        else:
            print("No Record Found")
            return render(request, 'search.html', {})
     



def CHANGE_PASSWORD(request):
     context ={}
     ch = User.objects.filter(id = request.user.id)
     
     if len(ch)>0:
            data = User.objects.get(id = request.user.id)
            context["data"]:data            
     if request.method == "POST":        
        current = request.POST["cpwd"]
        new_pas = request.POST['npwd']
        user = User.objects.get(id = request.user.id)
        un = user.username
        check = user.check_password(current)
        if check == True:
          user.set_password(new_pas)
          user.save()
          messages.success(request,'Password Change  Succeesfully!!!')
          user = User.objects.get(username=un)
          login(request,user)
        else:
          messages.success(request,'Current Password wrong!!!')
          return redirect("change_password")
     return render(request,'change-password.html')

   
    

            
     
