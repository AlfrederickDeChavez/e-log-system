from django.shortcuts import render, redirect
from django.http import HttpResponse
from .models import Bulletin, Guest, Department, EveningTask, MorningTask, Asset
from django.db.models import Q
from .forms import MorningTaskForm, EveningTaskForm, AssetForm
from .tasks import *
from datetime import date
import time
import pandas as pd
from datetime import datetime
from .functions import convert_time, add_eight_hours, convert_str_to_time, convert_task_time, asset_status
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required

@login_required(login_url='login')
def bulletin(request):

    asset = Asset.objects.all()
    for a in asset:
        a.status = asset_status(a.expiration)
        a.save()

    warnings = Asset.objects.filter(
        Q(status="initial") |
        Q(status="warning") |
        Q(status="danger") 
    )

    # FILTERING TABLE RECORDS BASED ON SEARCH VALUES

    # if request.method == "GET" and 'query' in request.GET:
    #     q = request.GET.get('search') if request.GET.get('search') != None else ''
    #     bulletin = Bulletin.objects.filter(
    #         Q(author__icontains=q) |
    #         Q(priority__icontains=q) |
    #         Q(details__icontains=q)
    #     ).order_by('-date')

    #     guest = Guest.objects.filter(
    #         Q(tower__icontains=q) |
    #         Q(room__icontains=q) |
    #         Q(affected_system__icontains=q) |
    #         Q(attended_by__icontains=q) |
    #         Q(problem__icontains=q) |
    #         Q(action__icontains=q) |
    #         Q(recommendation__icontains=q) |
    #         Q(status__icontains=q) 
    #     ).order_by('-date')

    #     department = Department.objects.filter(
    #         Q(department__icontains=q) |
    #         Q(client__icontains=q) |
    #         Q(affected_system__icontains=q) |
    #         Q(attended_by__icontains=q) |
    #         Q(problem__icontains=q) |
    #         Q(action__icontains=q) |
    #         Q(recommendation__icontains=q) |
    #         Q(status__icontains=q) 
    #     ).order_by('-date')



    # FILTERING TABLE RECORDS BASED ON DATE RANGE
        
    # elif request.method == "GET" and 'refresh' in request.GET:

    #     start_date = request.GET.get('start_date')
    #     end_date = request.GET.get('end_date')
    #     bulletin = Bulletin.objects.filter(
    #         Q(date__gte=start_date, date__lte=end_date) 
    #     ).order_by('-date')

    #     guest = Guest.objects.filter(
    #         Q(date__gte=start_date, date__lte=end_date) 
    #     ).order_by('-date')

    #     department = Department.objects.filter(
    #         Q(date__gte=start_date, date__lte=end_date) 
    #     ).order_by('-date')

        # datetime.strptime(end_date, '%Y-%m-%d') - datetime.strptime(start_date, '%Y-%m-%d')

        

    # NO FILTER OR GET METHOD -- DEFAULT VALUE
        
    # else:
    bulletin = Bulletin.objects.all().order_by('-date')[:50]
    department = Department.objects.all().order_by('-date')[:50]
    guest = Guest.objects.all().order_by('-date')
    
    context = {'bulletin': bulletin, 'guest': guest, 'department': department, 'warnings': warnings}

    return render(request, 'e_logs/bulletin.html', context)

@login_required(login_url='login')
def task(request): 

    morning_form = MorningTaskForm()
    evening_form = EveningTaskForm()
    update_morning_data = False
    update_evening_data = False
    retrieved_task = None
    warnings = Asset.objects.filter(
        Q(status="initial") |
        Q(status="warning") |
        Q(status="danger") 
    )

    #SAVE AM SHIFT RECORDS

    if request.method == "POST" and "save-am-shift" in request.POST:

        form = MorningTaskForm(request.POST)
        if form.is_valid():
            form.save()
        else: 
            print(form.errors)
        return redirect('task')

    # RETRIEVE AM SHIFT RECORDS
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


    # UPDATE MORNING RECORDS 
    if request.method == "POST" and "update-morning" in request.POST:
        date = request.get_full_path().split('?')[1].split('&')[0].split('=')[1]
        task = MorningTask.objects.filter(
            Q(date=date)
        )[0]

        form = MorningTaskForm(request.POST, instance=task)

        if form.is_valid():
            form.save()
        else:
            print(form.errors)

        return redirect('task')

    # SAVE EVENING SHIFT RECORDS
    if request.method == "POST" and "save-pm-shift" in request.POST:

        form = EveningTaskForm(request.POST)

        if form.is_valid():
            form.save()
        else:
            print(form.errors)
        
        return redirect('task')

    
    # RETRIEVE EVENING RECORDS
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


    # UPDATE EVENING RECORDS 
    if request.method == "POST" and "update-evening" in request.POST:
        date = request.get_full_path().split('?')[1].split('&')[0].split('=')[1]
        task = EveningTask.objects.filter(
            Q(date=date)
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
    warnings = Asset.objects.filter(
        Q(status="initial") |
        Q(status="warning") |
        Q(status="danger") 
    )

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
    warnings = Asset.objects.filter(
        Q(status="initial") |
        Q(status="warning") |
        Q(status="danger") 
    )

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
    warnings = Asset.objects.filter(
        Q(status="initial") |
        Q(status="warning") |
        Q(status="danger") 
    )

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
    asset = Asset.objects.all()
    for a in asset:
        a.status = asset_status(a.expiration)
        a.save()

    warnings = Asset.objects.filter(
        Q(status="initial") |
        Q(status="warning") |
        Q(status="danger") 
    )

    context = {
        'assets': asset,
        'warnings': warnings, 
    }

    return render(request, 'e_logs/assets.html', context)

@login_required(login_url='login')
def create_asset(request):
    title = "Add New Asset"
    form = AssetForm()

    if request.method == "POST":
    
        purchase_date = request.POST.get('purchase_date')  
        expiration = request.POST.get('expiration')   
         
        Asset.objects.create(
            name=request.POST.get('name'),
            description=request.POST.get('description'),
            supplier=request.POST.get('supplier'),
            purchase_date=purchase_date,
            expiration=expiration,
            status=asset_status(expiration)
        )
        return redirect('assets')

    context = {
        'form': form,
        'title': title,
    }
    return render(request, 'e_logs/asset_form.html', context)

@login_required(login_url='login')
def update_asset(request, pk):
    asset = Asset.objects.get(id=pk)
    form = AssetForm(instance=asset)
    title = 'Update Asset'

    if request.method == "POST":
        form = AssetForm(request.POST, instance=asset)
        if form.is_valid():
            form.save()
            return redirect('assets')
        else:
            print(form.errors)

    context = {
        'asset': asset,
        'form' : form,
        'title': title
    }
    
    return render(request, 'e_logs/asset_form.html', context)

@login_required(login_url='login')
def delete_asset(request, pk):
    asset = Asset.objects.get(id=pk)

    if request.method == "POST":
        asset.delete()
        return redirect('assets')

    context = {
        'asset': asset
    }
    return render(request, 'e_logs/delete_asset.html', context)


@login_required(login_url='login')
def asset_details(request, pk):
    asset = Asset.objects.get(id=pk)
    return HttpResponse(f'This is the {asset} details')

def login_view(request):
    if request.method == "POST":
        username = request.POST.get('username')
        password = request.POST.get('password')

        user = authenticate(request, username=username, password=password)
        
        if user is not None:
            login(request, user)
            return redirect('home')
        else: 
            print(user)
    return render(request, 'e_logs/login.html')

@login_required(login_url='login')
def not_found(request):
    return render(request, 'e_logs/not_found.html')
