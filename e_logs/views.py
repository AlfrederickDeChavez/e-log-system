from django.shortcuts import render, redirect
from django.http import HttpResponse
from .models import Bulletin, Guest, Department, EveningTask, MorningTask
from django.db.models import Q
from .forms import MorningTaskForm, EveningTaskForm
from .tasks import *


def bulletin(request):

    # FILTERING TABLE RECORDS BASED ON SEARCH VALUES

    if request.method == "GET" and 'query' in request.GET:
        q = request.GET.get('search') if request.GET.get('search') != None else ''
        bulletin = Bulletin.objects.filter(
            Q(author__icontains=q) |
            Q(priority__icontains=q) |
            Q(details__icontains=q)
        ).order_by('-date')

        guest = Guest.objects.filter(
            Q(tower__icontains=q) |
            Q(room__icontains=q) |
            Q(affected_system__icontains=q) |
            Q(attended_by__icontains=q) |
            Q(problem__icontains=q) |
            Q(action__icontains=q) |
            Q(recommendation__icontains=q) |
            Q(status__icontains=q) 
        ).order_by('-date')

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



    # FILTERING TABLE RECORDS BASED ON DATE RANGE
        
    elif request.method == "GET" and 'refresh' in request.GET:

        start_date = request.GET.get('start_date')
        end_date = request.GET.get('end_date')
        bulletin = Bulletin.objects.filter(
            Q(date__gte=start_date, date__lte=end_date) 
        ).order_by('-date')

        guest = Guest.objects.filter(
            Q(date__gte=start_date, date__lte=end_date) 
        ).order_by('-date')

        department = Department.objects.filter(
            Q(date__gte=start_date, date__lte=end_date) 
        ).order_by('-date')

    # NO FILTER OR GET METHOD -- DEFAULT VALUE
        
    else:
        bulletin = Bulletin.objects.all().order_by('-date')
        department = Department.objects.all().order_by('-date')
        guest = Guest.objects.all().order_by('-date')

    context = {'bulletin': bulletin, 'guest': guest, 'department': department}

    return render(request, 'e_logs/bulletin.html', context)


def task(request): 

    morning_form = MorningTaskForm()
    evening_form = EveningTaskForm()

    #SAVE AM SHIFT RECORDS

    if request.method == "POST" and "save-am-shift" in request.POST:

        form = MorningTaskForm(request.POST)
        if form.is_valid():
            form.save()
            print('Form Saved')
        else: 
            print(form.errors)

        return redirect('task')
    

    # RETRIEVE AM SHIFT RECORDS
    if request.method == "GET" and "retrieve-am" in request.GET:
        task = MorningTask.objects.filter(
            Q(date=request.GET.get('morning_shift_date'))
        )[0]

        morning_form = MorningTaskForm(instance=task)

    # SAVE EVENING SHIFT RECORDS
    if request.method == "POST" and "save-pm-shift" in request.POST:

        form = EveningTaskForm(request.POST)

        if form.is_valid():
            form.save()
            print('Form saved')
        else:
            print('Failed to add am records')
            print(form.errors)
        
        return redirect('task')

    if request.method == "GET" and 'retrieve-pm-shift' in request.GET:
        task = EveningTask.objects.filter(
            Q(date=request.GET.get('evening_shift_date'))
        )[0]

        evening_form = EveningTaskForm(instance=task)

    context = {
        'morning_tasks': morning_tasks, 
        'evening_tasks': evening_tasks, 
        'morning_form': morning_form
    }

    return render(request, 'e_logs/task.html', context)

def room_service(request):

    # POST ROOM INCIDENT REPORT 

    if request.method == "POST" and "save_room" in request.POST: 
        tower = request.POST.get("tower")
        room = request.POST.get("room")
        attendee = request.POST.get("attendee")
        affected_system = request.POST.get("system")
        time_reported = request.POST.get("time_reported")
        time_resolved = request.POST.get("time_resolved")
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
            recommendation=recommendation
        )

        return redirect('bulletin')

    context = {'guest': ''}

    return render(request, 'e_logs/room_service.html', context)

def department_service(request):

    # DEPARTMENT INPUT

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

        print(request.POST)

        return redirect('bulletin')

    return render(request, 'e_logs/department.html')

def utilities(request):

    # POST BULLETIN RECORDS

    if request.method == 'POST' and 'bulletin-form' in request.POST:
        bulletin = Bulletin.objects.create(
            author=request.POST.get('author'),
            priority=request.POST.get('priority'),
            details=request.POST.get('details')
        )

        return redirect('bulletin')

    return render(request, 'e_logs/utilities.html')
    


