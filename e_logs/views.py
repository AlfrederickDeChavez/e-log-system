
# Importing Django Modules
from django.shortcuts import render, redirect
from django.db.models import Q
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib import messages

#Importing Python Modules
import time
from datetime import datetime
from datetime import date
import datetime

#Importing App Modules
from .models import Bulletin, Guest, Department, EveningTask, MorningTask, Asset, Audit, RenewedAsset
from .forms import MorningTaskForm, EveningTaskForm, AssetForm
from .tasks import *
from .functions import *

# Django Module for Emails
from django.core.mail import send_mail, BadHeaderError
from django.http import HttpResponse
from django.contrib.auth.forms import PasswordResetForm
from django.contrib.auth.models import User
from django.template.loader import render_to_string
from django.utils.http import urlsafe_base64_encode
from django.contrib.auth.tokens import default_token_generator
from django.utils.encoding import force_bytes


def login_view(request):

    """
        Authenticating the users.
    """

    if request.user.is_authenticated:
        return redirect('home')

    if request.method == "POST":
        username = request.POST.get('username')
        password = request.POST.get('password')

        user = authenticate(request, username=username, password=password)
        
        if user is not None:
            login(request, user)
            return redirect('home')
        else: 
            messages.error(request, 'User does not exist.')

        for a in Asset.objects.all()[5:]:
            a.delete()

        
    return render(request, 'e_logs/login.html')

def logout_view(request):

    """
        User log out.
    """

    logout(request)
    return redirect('home')

@login_required(login_url='login')
def bulletin(request):

    """
        This page is the home view of the application. It displays the bulletin information, the room incident reports and department 
        incident reports.
        It displays the app server backup free disk space for TBM Opera and BHTL Opera.
        Each table can be exported as an excel file. 
    """

    yesterday = date.today() - timedelta(days=1)
    try:
        disk = EveningTask.objects.get(date='2016-10-01')
        opera = disk.r_dsob[:10]
    except:
        opera = ''
    
    asset = Asset.objects.all()
    for a in asset:
        a.status = asset_status(a)
        a.save()
        track_asset(a)


    warnings = Asset.objects.filter(
        Q(status="initial") |
        Q(status="warning") | 
        Q(status="danger") | 
        Q(current_tracking_date=date.today())
    ).order_by('expiration')

    """
        If user sends a GET request with 'query' on it. The following code is executed. 
    """

    if request.method == "GET" and 'query' in request.GET:
        q = request.GET.get('search') if request.GET.get('search') != None else ''
        bulletin = Bulletin.objects.filter(
            Q(author__icontains=q) |
            Q(priority__icontains=q) |
            Q(details__icontains=q)
        ).order_by('-date')[:50]

        guest = Guest.objects.filter(
            Q(tower__icontains=q) |
            Q(room__icontains=q) |
            Q(affected_system__icontains=q) |
            Q(attended_by__icontains=q) |
            Q(problem__icontains=q) |
            Q(action__icontains=q) |
            Q(recommendation__icontains=q) |
            Q(status__icontains=q) 
        ).order_by('-date')[:50]

        department = Department.objects.filter(
            Q(department__icontains=q) |
            Q(client__icontains=q) |
            Q(affected_system__icontains=q) |
            Q(attended_by__icontains=q) |
            Q(problem__icontains=q) |
            Q(action__icontains=q) |
            Q(recommendation__icontains=q) |
            Q(status__icontains=q) 
        ).order_by('-date')
       
    elif request.method == "GET" and 'refresh' in request.GET:

        try:

            start_date = request.GET.get('start_date')
            end_date = request.GET.get('end_date')
            bulletin = Bulletin.objects.filter(
                Q(date__gte=start_date, date__lte=end_date) 
            ).order_by('-date')[:50]

            guest = Guest.objects.filter(
                Q(date__gte=start_date, date__lte=end_date) 
            ).order_by('-date')[:50]

            department = Department.objects.filter(
                Q(date__gte=start_date, date__lte=end_date) 
            ).order_by('-date')

            datetime.strptime(end_date, '%Y-%m-%d') - datetime.strptime(start_date, '%Y-%m-%d')

        except:
            return redirect('not_found')
        
    else:
        bulletin = Bulletin.objects.all().order_by('-date')[:50]
        department = Department.objects.all().order_by('-date')[:50]
        guest = Guest.objects.all().order_by('-date')[:50]
        
    context = {
        'bulletin': bulletin, 
        'guest': guest, 
        'department': department, 
        'warnings': warnings,
        'yesterday': yesterday,
        'opera': opera
    }

    return render(request, 'e_logs/bulletin.html', context)

@login_required(login_url='login')
def task(request): 

    """
        The task view shows the checklist of task of the MIS personnel. User can navigate between morning shift and evening shift.
        Past data can be retrieve using the data chosen. The displayed data can be updated.
    """
    warnings = Asset.objects.filter(
        Q(status="initial") |
        Q(status="warning") | 
        Q(status="danger") | 
        Q(current_tracking_date=date.today())
    ).order_by('expiration')

    #Initializing the forms
    morning_form = MorningTaskForm()
    evening_form = EveningTaskForm()

    #Use for conditional rendering: components are rendered based on active tabs (morning / evening)
    update_morning_data = False
    update_evening_data = False
    retrieved_task = None

    #Adding new record for the morning
    if request.method == "POST" and "save-am-shift" in request.POST:

        form = MorningTaskForm(request.POST)
        if form.is_valid():
            form.save()
        else: 
            print(form.errors)
        return redirect('task')

    #Retrieving morning records based on date input. If no records were returned, users will be navigated to not found page.
    if request.method == "GET" and "retrieve-am" in request.GET:
        
        try:
            task = MorningTask.objects.filter(
                Q(date=request.GET.get('morning_shift_date'))
            )[0]
            morning_form = MorningTaskForm(instance=task)
            update_morning_data = True
            retrieved_task = task
        except:
            return redirect('not_found')


    # Updating task record for morning. 
    if request.method == "POST" and "update-morning" in request.POST:
        date_filter = request.get_full_path().split('?')[1].split('&')[0].split('=')[1]
        task = MorningTask.objects.filter(
            Q(date=date_filter)
        )[0]

        form = MorningTaskForm(request.POST, instance=task)

        if form.is_valid():
            form.save()
        else:
            print(form.errors)

        return redirect('task')

    # Adding new records for evening tasks
    if request.method == "POST" and "save-pm-shift" in request.POST:

        form = EveningTaskForm(request.POST)

        if form.is_valid():
            form.save()
        else:
            print(form.errors)
        
        return redirect('task')

    
    # Retrieving past records based on date input. If no records were returned, user navigated to not found page.
    if request.method == "GET" and 'retrieve-pm' in request.GET:
        try:
            task = EveningTask.objects.filter(
                Q(date=request.GET.get('evening_shift_date'))
            )[0]

            evening_form = EveningTaskForm(instance=task)
            update_evening_data = True
            retrieved_task = task
        except:
            return redirect('not_found')


    # Updates evening records. 
    if request.method == "POST" and "update-evening" in request.POST:
        date_filter = request.get_full_path().split('?')[1].split('&')[0].split('=')[1]
        task = EveningTask.objects.filter(
            Q(date=date_filter)
        )[0]

        form = EveningTaskForm(request.POST, instance=task)

        if form.is_valid():
            form.save()
            print('Form Save')
        else:
            print(form.errors)

        return redirect('task')

    context = {
        'morning_tasks': morning_tasks, 
        'evening_tasks': evening_tasks, 
        'morning_form': morning_form,
        'evening_form': evening_form,
        'show_morning_update': update_morning_data,
        'show_evening_update': update_evening_data,
        'task': retrieved_task,
        'warnings': warnings
    }

    return render(request, 'e_logs/task.html', context)

@login_required(login_url='login')
def room_service(request):

    """
        Room service view is the page for adding new incident report. It includes a form that takes input from
        the user and save it to the database.

        After each assistance for the guest, this is where MIS personnel records the incident.
    """

    warnings = Asset.objects.filter(
        Q(status="initial") |
        Q(status="warning") | 
        Q(status="danger") | 
        Q(current_tracking_date=date.today())
    ).order_by('expiration')

    # POST ROOM INCIDENT REPORT 
    if request.method == "POST" and "save_room" in request.POST: 
        
        tower = request.POST.get("tower")
        room = request.POST.get("room")
        attendee = request.POST.get("attendee")
        affected_system = request.POST.get("system")
        time_reported = convert_time(request.POST.get("time_reported"))
        time_resolved = convert_time(request.POST.get("time_resolved"))
        problem = request.POST.get("problem")
        status = request.POST.get("status")
        action = request.POST.get("action")
        recommendation = request.POST.get("recommendation")
 
        room = Guest.objects.create(
            tower=tower,
            room=room,
            attended_by=attendee,
            affected_system=affected_system,
            time_reported=time_reported,
            time_resolved=time_resolved,
            problem=problem,
            status=status,
            action=action,
            recommendation=recommendation,
            date=date.today()
        )

        return redirect('bulletin')

    context = {'warnings': warnings}

    return render(request, 'e_logs/room_service.html', context)

@login_required(login_url='login')
def department_service(request):

    """ Department service view is the page for adding new incident report. It includes a form that takes input from
        the user and save it to the database.

        After each assistance for the a specific department, this is where MIS personnel records the incident. """

    warnings = Asset.objects.filter(
        Q(status="initial") |
        Q(status="warning") | 
        Q(status="danger") | 
        Q(current_tracking_date=date.today())
    ).order_by('expiration')

    # POST DEPARTMENT INCIDENT REPORT
    if request.method == 'POST' and 'save_department' in request.POST:
        department = request.POST.get("department")
        client = request.POST.get("client")
        attendee = request.POST.get("attendee")
        affected_system = request.POST.get("system")
        time_reported = request.POST.get("time_reported")
        time_resolved = request.POST.get("time_resolved")
        problem = request.POST.get("problem")
        status = request.POST.get("status")
        action = request.POST.get("action")
        recommendation = request.POST.get("recommendation")

        dept = Department.objects.create(
            department=department,
            client=client,
            attended_by=attendee,
            affected_system=affected_system,
            time_reported=time_reported,
            time_resolved=time_resolved,
            problem=problem,
            status=status,
            action=action,
            recommendation=recommendation
        )

        return redirect('bulletin')

    context = {'warnings': warnings}

    return render(request, 'e_logs/department.html', context)

@login_required(login_url='login')
def utilities(request):

    """
        Utilities view is where the MIS personnel add records of bulletin.
    """

    warnings = Asset.objects.filter(
        Q(status="initial") |
        Q(status="warning") | 
        Q(status="danger") | 
        Q(current_tracking_date=date.today())
    ).order_by('expiration')

    # POST BULLETIN RECORDS

    if request.method == 'POST' and 'bulletin-form' in request.POST:
        
        bulletin = Bulletin.objects.create(
            author=request.POST.get('author'),
            priority=request.POST.get('priority'),
            details=request.POST.get('details'),
            date=date.today(),
            time=time.strftime("%H:%M:%S", time.localtime())
        )

        return redirect('bulletin')

    context = {'warnings': warnings}

    return render(request, 'e_logs/utilities.html', context)

@login_required(login_url='login')
def assets(request):

    """
        Assets view displayed the assets of the MIS and indicator to identify when will the assets expire.

        RED --> has a status == 'danger' which is 30 days before expiration
        ORANGE --> has a status == 'warning' which is 60 days before expiration
        YELLOW -- > has a status == 'initial' which is 90 days before expiration

        User can update and delete records
    """
    
    asset = Asset.objects.all()
    for a in asset:
        a.status = asset_status(a)
        a.save()
        track_asset(a)

    warnings = Asset.objects.filter(
        Q(status="initial") |
        Q(status="warning") | 
        Q(status="danger") | 
        Q(current_tracking_date=date.today())
    ).order_by('expiration')


    """
        Filter the renewed assets records.
    """


    if request.method == "GET" and 'query' in request.GET:
        q = request.GET.get('search') if request.GET.get('search') != None else ''
        renewed = RenewedAsset.objects.filter(
            Q(name__icontains=q) |
            Q(supplier__icontains=q) |
            Q(schedule__icontains=q)
        )

    elif request.method == "GET" and 'refresh' in request.GET:
        try:
            start_date = request.GET.get('start_date')
            end_date = request.GET.get('end_date')
            renewed = RenewedAsset.objects.filter(
                Q(tracking_date__gte=start_date, tracking_date__lte=end_date) 
            )

        except:
            return redirect('not_found')

    else: 
        renewed = RenewedAsset.objects.all()

    """
        Set selected asset as done. The selected asset extends the expiration date based on schedule. 
    """

    if request.method == "POST":
        remark_asset = Asset.objects.get(id=request.POST.get('id'))

        RenewedAsset.objects.create(
            name = remark_asset.name,
            description = remark_asset.description,
            supplier = remark_asset.supplier,
            purchase_date = remark_asset.purchase_date,
            expiration = remark_asset.expiration,
            schedule = remark_asset.schedule,
            tracking_date = remark_asset.current_tracking_date,
            remarks = request.POST.get('remark')
        )


        remark_asset.expiration = renew_asset(remark_asset)
        remark_asset.current_tracking_date = remark_asset.next_tracking_date
        remark_asset.remarks = request.POST.get('remark')
        remark_asset.save()

        

        return redirect('assets')

    context = {
        'assets': asset,
        'warnings': warnings, 
        'renewed': renewed
    }

    return render(request, 'e_logs/assets.html', context)

@login_required(login_url='login')
def create_asset(request):

    """
        Create asset view is where the user (MIS) add new asset or equipment. 
    """

    title = "Add New Asset"
    form = AssetForm()

    if request.method == "POST":

        expiration = request.POST.get('expiration')
    
        Asset.objects.create(
            name=request.POST.get('name'),
            description=request.POST.get('description'),
            supplier=request.POST.get('supplier'),
            purchase_date=request.POST.get('purchase_date'),
            expiration=expiration,
            status='fresh',
            schedule=request.POST.get('schedule'),
            current_tracking_date=date.today(),
            next_tracking_date=recur_asset(request.POST.get('schedule'))
        )

        return redirect('assets')

    context = {
        'form': form,
        'title': title,
    }
    return render(request, 'e_logs/asset_form.html', context)

@login_required(login_url='login')
def update_asset(request, pk):

    """
        Update asset view is where the user can update the record upon selecting it from the assets page / table.
        The same form for creating asset is displayed but the fields were already filled by the selected data.

        Each updates is monitored. It is recorded on the database who and when the data was updated.
    """

    asset = Asset.objects.get(id=pk)
    form = AssetForm(instance=asset)
    title = 'Update Asset'

    if request.method == "POST":
        
        
        if asset.schedule == request.POST.get('schedule'):
            Audit.objects.create(
                asset_id=asset.id,
                name=asset.name,
                description=asset.description,
                supplier=asset.supplier,
                purchase_date=asset.purchase_date,
                expiration=asset.expiration,
                action="Updated",
                author=request.user,
                status=asset.status,
                schedule=asset.schedule,
                current_tracking_date=asset.current_tracking_date,
                next_tracking_date=asset.next_tracking_date
            )
            form = AssetForm(request.POST, instance=asset)
            if form.is_valid():
                form.save()
                return redirect('assets')
            else:
                print(form.errors)

            return redirect('assets')

        else:

            Audit.objects.create(
                name=asset.name,
                description=asset.description,
                supplier=asset.supplier,
                purchase_date=asset.purchase_date,
                expiration=asset.expiration,
                schedule=asset.schedule,
                action="Updated",
                author=request.user
            )
            
            form = AssetForm(request.POST, instance=asset)
            if form.is_valid():

                form.save()

                asset.next_tracking_date = recur_asset(asset.schedule)
                asset.save()
                return redirect('assets')
            else:
                print(form.errors)

            return redirect('assets')

    context = {
        'asset': asset,
        'form' : form,
        'title': title
    }
    
    return render(request, 'e_logs/asset_form.html', context)

@login_required(login_url='login')
def delete_asset(request, pk):

    """
        Delete asset view renders a confirmation message for deleting the selected data.

        The delete action is monitored. It is recorded in the database who deletes the data and when it is deleted.
    """
    asset = Asset.objects.get(id=pk)

    if request.method == "POST":
        Audit.objects.create(
            name=asset.name,
            description=asset.description,
            supplier=asset.supplier,
            purchase_date=asset.purchase_date,
            expiration=asset.expiration,
            action="Deleted",
            author=request.user
        )
        asset.delete()
        return redirect('assets')

    context = {
        'asset': asset
    }
    return render(request, 'e_logs/delete_asset.html', context)

@login_required(login_url='login')
def asset_details(request, pk):

    """
        Displays the details of each asset.
    """
    asset = Asset.objects.get(id=pk)
    context = {
        'asset': asset
    }
    return render(request, 'e_logs/asset_details.html', context)

@login_required(login_url='login')
def print_asset(request, pk):
    return render(request, 'e_logs/print_asset.html')

@login_required(login_url='login')
def not_found(request):

    """
        Renders a not found page whenever the user retrieves an null object.
    """
    return render(request, 'e_logs/not_found.html')

def password_reset_request(request):
    if request.method == "POST":
        password_reset_form = PasswordResetForm(request.POST)
        if password_reset_form.is_valid():
            data = password_reset_form.cleaned_data['email']
            associated_users = User.objects.filter(Q(email=data))
            if associated_users.exists():
                for user in associated_users:
                    subject = "Password Reset Requested"
                    email_template_name = "e_logs/password/password_email_reset.txt"
                    c = {
                        "email":user.email,
                        'domain':'127.0.0.1:8000',
                        'site_name': 'Website',
                        "uid": urlsafe_base64_encode(force_bytes(user.pk)),
                        "user": user,
                        'token': default_token_generator.make_token(user),
                        'protocol': 'http',
                    }
                    email = render_to_string(email_template_name, c)
                    try:
                        send_mail(subject, email, 'admin@gmail.com' , [user.email], fail_silently=False)
                    except BadHeaderError:
                        return HttpResponse('Invalid header found.')
                    
                    return redirect ("password_reset_done")

    return render(request, 'e_logs/password/password_reset.html')




def audit_logs(request):

    audits = Audit.objects.all().order_by('-modified_date')

    context = {
        'audits': audits
    }
    return render(request, 'e_logs/audit_logs.html', context)


def versions(request, pk):

    version_list = Audit.objects.filter(asset_id=pk).order_by('-modified_date')
    

    context = {
        'versions': version_list,
        'name': version_list[0].name
    }
    return render(request, 'e_logs/versions.html', context)