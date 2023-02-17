from django.shortcuts import render, redirect
from django.http import HttpResponse
from .models import Bulletin, Guest, Department
from django.db.models import Q

from .tasks import tasks


def bulletin(request):

    department_data = Department.objects.all().order_by('-date')
    guest = Guest.objects.all().order_by('-date')


    # FILTERING TABLE RECORDS BASED ON SEARCH VALUES

    if request.method == "GET" and 'query' in request.GET:
        q = request.GET.get('search') if request.GET.get('search') != None else ''
        bulletin = Bulletin.objects.filter(
            Q(author__icontains=q) |
            Q(priority__icontains=q) |
            Q(details__icontains=q)
        ).order_by('-date')


    # FILTERING TABLE RECORDS BASED ON DATE RANGE
        
    elif request.method == "GET" and 'refresh' in request.GET:

        start_date = request.GET.get('start_date')
        end_date = request.GET.get('end_date')
        bulletin = Bulletin.objects.filter(
            Q(date__gte=start_date, date__lte=end_date) 
        ).order_by('-date')

    # NO FILTER OR GET METHOD -- DEFAULT VALUE
        
    else:
        bulletin = Bulletin.objects.all().order_by('-date')

    context = {'bulletin': bulletin, 'guest': guest, 'department': department_data}

    return render(request, 'e_logs/bulletin.html', context)


def task(request): 

    if request.method == "GET" and "save-am-shift" in request.GET:
        print(request.GET)

    context = {'tasks': tasks}

    return render(request, 'e_logs/task.html', context)


def room_service(request):

    # ROOM INPUT

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

    # BULLETIN INPUT 

    # POST BULLETIN RECORDS

    if request.method == 'POST' and 'bulletin-form' in request.POST:
        bulletin = Bulletin.objects.create(
            author=request.POST.get('author'),
            priority=request.POST.get('priority'),
            details=request.POST.get('details')
        )

        return redirect('bulletin')

    return render(request, 'e_logs/utilities.html')
    



###### ORIGINAL VIEW -- MODIFIED


# def home(request):

#     # FILTER THE RECORDS - VIA SEARCH OR DATE RANGE

#     q = request.GET.get('search') if request.GET.get('search') != None else ''
    

#     if request.method == "GET" and 'query' in request.GET:
#         bulletin = Bulletin.objects.filter(
#             Q(author__icontains=q) |
#             Q(priority__icontains=q) |
#             Q(details__icontains=q)
#         ).order_by('-date')
        
#     elif request.method == "GET" and 'refresh' in request.GET:

#         start_date = request.GET.get('start_date')
#         end_date = request.GET.get('end_date')
#         bulletin = Bulletin.objects.filter(
#             Q(date__gte=start_date, date__lte=end_date) 
#         ).order_by('-date')
        
#     else:
#         bulletin = Bulletin.objects.all().order_by('-date')


#     context = {'bulletin': bulletin, 'guest': guest, 'department': department_data, 'tasks': tasks}

#     return render(request, 'e_logs/main.html', context)







