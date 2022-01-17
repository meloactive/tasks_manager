from celery_progress.backend import Progress
from django.shortcuts import render, redirect
from .models import All_Tasks, Owner, Member, Posts, Tasks_Celery, Tasks_List, Full_Tasks_List, Full_Tasks_ID, Users
from django.core.files.storage import FileSystemStorage
from django.http import JsonResponse
from .forms import DownloadForm, UserForm
from celery.app.task import Task
import time
from .tasks import main_task, ProcessDownload, automation_with_selenium, go_to_sleep, testing_selenium


def demo_view(request):
    # If method is POST, process form data and start task
    if request.method == 'POST':
        # Get form instance
        form = DownloadForm(request.POST)

        # form = UserForm(request.POST)

        if form.is_valid():
            # Retrieve URL from form data
            url = form.cleaned_data['url']

            print(f'Downloading: {url}')
            # Create Task
            download_task = ProcessDownload.delay(url)
            # Get ID
            task_id = download_task.task_id
            # Print Task ID
            print(f'Celery Task ID: {task_id}')

            # Return demo view with Task ID
            return render(request, 'progress.html', {'form': form, 'task_id': task_id})
        else:
            # Return demo view
            return render(request, 'progress.html', {'form': form})
    else:
        # Get form instance
        form = DownloadForm()
        # Return demo view
        return render(request, 'progress.html', {'form': form})


def start_automation(request):
    if request.method == 'POST':
        # Get form instance
        form = DownloadForm(request.POST)

        if form.is_valid():
            # Retrieve URL from form data
            url = form.cleaned_data['url']

            print(f'Downloading: {url}')
            # Create Task
            download_task = automation_with_selenium.delay()
            # Get ID
            task_id = download_task.task_id
            # Print Task ID
            print(f'Celery Task ID: {task_id}')

            # Return demo view with Task ID
            return render(request, 'progress.html', {'form': form, 'task_id': task_id})
        else:
            # Return demo view
            return render(request, 'progress.html', {'form': form})
    else:
        # Get form instance
        form = DownloadForm()
        # Return demo view
        return render(request, 'progress.html', {'form': form})


def selenium_test(request):
    task = testing_selenium.delay("https://google.com")
    # form = DownloadForm(request.POST)
    task_id = task.task_id
    return render(request, 'progress.html', {'task_id': task_id})


def sleepy(request):
    task = go_to_sleep.delay(1)
    # print(task.task_id)
    tasks_db = Tasks_Celery(
        task_id=task.task_id, description="sleepy", progress="0", finished="False")
    tasks_db.save()
    return render(request, 'download/sleepy.html', {'task_id': task.task_id})


def index(request):
    members = Member.objects.all()
    context = {'members': members}
    return render(request, 'download/index.html', context)


def celery_check(request):
    members = Tasks_Celery.objects.all()
    context = {'members': members}
    # for member in members:
    # members.sort(reverse=True)
    members = members.order_by('-id')
    celery_task_ids = {member.id: member.task_id for member in members}
    print(celery_task_ids)
    # sorted([(value,key) for (key,value) in celery_task_ids.items()])
    # a = sorted([(value,key) for (key,value) in celery_task_ids.items()])
    # print(a)
    # celery_task_ids.reverse()
    return render(request, 'download/celery_check.html', context={'celery_task_ids': celery_task_ids})


def create(request):
    member = Member(firstname=request.POST['firstname'], lastname=request.POST['lastname'], email=request.POST['email'], dob=request.POST['dob'], phone_number=request.POST['phone_number'],
                    address=request.POST['address'], ssn=request.POST['ssn'], city=request.POST['city'], state=request.POST['state'], password=request.POST['password'])
    member.save()
    return redirect('/')


def edit(request, id):
    members = Member.objects.get(id=id)
    context = {'members': members}
    return render(request, 'download/edit.html', context)


def update(request, id):
    member = Member.objects.get(id=id)
    member.firstname = request.POST['firstname']
    member.lastname = request.POST['lastname']
    member.email = request.POST['email']
    member.dob = request.POST['dob']
    member.phone_number = request.POST['phone_number']
    member.address = request.POST['address']
    member.ssn = request.POST['ssn']
    member.lastname = request.POST['lastname']
    member.password = request.POST['password']
    member.city = request.POST['city']
    member.state = request.POST['state']
    member.save()
    return redirect('/')


def delete(request, id):
    member = Member.objects.get(id=id)
    member.delete()
    return redirect('/')


def upload(request):
    if request.method == 'POST' and request.FILES['upload']:
        upload = request.FILES['upload']
        fss = FileSystemStorage()
        file = fss.save(upload.name, upload)
        file_url = fss.url(file)

        print(str(file_url))

        return render(request, 'download/upload.html', {'file_url': file_url})
    return render(request, 'download/upload.html')


def pause_task(request, id):
    Task.update_state(self=go_to_sleep, task_id=id, state='CANCEL')
    return redirect('/check')


def resume_task(request, tid):
    Task.update_state(self=long_task, task_id=tid, state='RESUME')
    return 'Your task will be resumed !'


def cancel_task(request, tid):
    Task.update_state(self=long_task, task_id=tid, state='CANCEL')
    return 'Your task will be cancelled !'


def selenium_skel_new_tasks(request):
    # task = testing_selenium.delay("https://google.com")
    tasks_db = Tasks_Celery(task_id="Not Assigned", description="start New Automation",
                            progress="0", status="start", finished="False",)

    tasks_db.save()
    print(tasks_db.id)
    task = testing_selenium.delay(melo=tasks_db.id, url="https://google.com")
    # form = DownloadForm(request.POST)
    task_id = task.task_id
    return render(request, 'download/selenium_progress.html', {'task_id': task_id})


def pause_selenium_task(request, id):
    member = Tasks_Celery.objects.get(task_id=id)
    print(member)
    # tasks_db = Tasks_Celery(task_id=task.task_id, description="sleepy", progress="0", finished="False")
    # tasks_db.save()
    member.status = "pause"
    member.save()
    print(member)
    return redirect("/check")


def resume_selenium_task(request, id):
    member = Tasks_Celery.objects.get(task_id=id)
    print(member)
    # tasks_db = Tasks_Celery(task_id=task.task_id, description="sleepy", progress="0", finished="False")
    # tasks_db.save()
    member.status = "resume"
    member.save()
    print(member)
    return redirect("/check")


def cancel_selenium_task(request, id):
    member = Tasks_Celery.objects.get(task_id=id)
    print(member)
    # tasks_db = Tasks_Celery(task_id=task.task_id, description="sleepy", progress="0", finished="False")
    # tasks_db.save()
    member.status = "cancel"
    member.save()
    print(member)
    return redirect("/check")

#####################################  functions with tasks  ###############################################


def get_all_tasks_from_db(request):
    members = Tasks_List.objects.all()
    context = {'members': members}
    return render(request, 'download/new_task.html', context)


def insert_all_tasks_with_id(request):
    if(request.method == "POST"):
        member = Tasks_List(
            task_id=request.POST['task_id'], description=request.POST['description'], extra_values=request.POST['extra_values'])
        member.save()
    members = Tasks_List.objects.all()
    context = {'members': members}
    return render(request, 'download/add_tasks_into_db.html', context)


def delete_tasks(request, id):
    member = Tasks_List.objects.get(id=id)
    member.delete()
    members = Tasks_List.objects.all()
    context = {'members': members}
    return redirect("/insert_all_tasks_with_id")

##################### creating full task from Task_List ##########


def create_task_full(request):
    # create a db to add task with task_id
    # add same task id next task
    # get all tasks list from db
    id_needed = "0"
    # member = Full_Tasks_ID(task_id="1", status="pending")
    # member.save()
    # last_task_id = Full_Tasks_ID.objects.all()
    # print(last_task_id)
    # if(last_task_id is None):
    #     member = Full_Tasks_ID(task_id="1", status="pending")
    #     member.save()
    #     print("last_task_id: " + last_task_id)
    # else:
    last_task_id = Full_Tasks_ID.objects.all()
    for task_id in last_task_id:
        id_needed = task_id.task_id
    print(id_needed)
    if(id_needed == "0"):
        member = Full_Tasks_ID(task_id="1", status="pending")
        member.save()
        last_task_id = Full_Tasks_ID.objects.all()
        for task_id in last_task_id:
            id_needed = task_id.task_id
            print((id_needed))
        # print("last_task_id: " + last_task_id)
    form = UserForm(initial={'full_task_id': id_needed})

    if request.method == 'POST':
        # Get form instance
        form = UserForm(request.POST)

        # form = UserForm(request.POST)

        if form.is_valid():
            # Retrieve URL from form data
            # status = form.cleaned_data['task_func']
            user_inputs = form.cleaned_data['user_inputs']
            full_task_id = form.cleaned_data['full_task_id']
            if(id_needed != '0' and id_needed != full_task_id):
                member = Full_Tasks_ID(task_id=full_task_id, status="pending")
                member.save()
            task_id = form.cleaned_data['task_id']
            member = Full_Tasks_List(
                task_id=task_id, full_task_id=full_task_id, user_inputs=user_inputs, status="pending")
            member.save()
            # task_func = form.cleaned_data['task_func']

            # print(f'Downloading: {task_func}')

    full_tasks = Full_Tasks_List.objects.all()
    # context = {'full_tasks': members}
    tasks = Tasks_List.objects.all()
    # context = {'tasks': tasks}
    # print(tasks)
    return render(request, 'download/create_new_full_task.html', {'form': form, 'full_tasks': full_tasks, 'tasks': tasks})


def add_a_task(request):
    # add new db
    member = Tasks_Celery.objects.get(task_id=id)
    member = Member.objects.get(id=id)
    member.task_id = request.POST['task_id']
    member.func_name = request.POST['func_name']
    member.user_input = request.POST['user_input']


def delete_full_tasks_id(request, id):
    member = Full_Tasks_List.objects.get(id=id)
    member.delete()
    members = Tasks_List.objects.all()
    context = {'members': members}
    return redirect("/create_new_full_task")


def start_task(request):
    full_tasks = Full_Tasks_ID.objects.all()
    print(full_tasks)
    if request.method == 'POST':
        full_task_id = request.POST['full_task_id']
        print(full_task_id)
        task = main_task.delay(full_task_id)
        tasks_db = Tasks_Celery(
            task_id=task.task_id, description="sleepy", progress="0", status='processing', finished="False")
        tasks_db.save()

    return render(request, 'download/tasks_list_start.html', {'full_tasks': full_tasks})


# make a func which will pass some json response
def pass_json_data(request):
    # post

    return JsonResponse({'result': "hello lists"})


def remove_selenium_task(request, id):
    member = Tasks_Celery.objects.get(task_id=id)
    member.delete()

    return redirect("/check")

def remove_all_selenium_tasks(request):
    member = Tasks_Celery.objects.all()
    for m in member:
        member2 = Tasks_Celery.objects.get(id=m.id)
        member2.delete()
    # member.delete()
    return redirect("/check")


def get_all_urls_with_tickbox(request):
    links_arr = []
    myfile = open("links.txt", "r")
    myline = myfile.readline()
    while myline:
        print(myline)
        links_arr.append(myline)
        myline = myfile.readline()
    myfile.close()   
    if request.method  == "POST":
        print(request.POST.keys())
        print("hello")
    return render(request, 'download/all_links_with_tickbox.html', {"links": links_arr})


def get_all_urls_with_tickbox(request):
    links_arr = []
    myfile = open("links.txt", "r")
    myline = myfile.readline()
    while myline:
        print(myline)
        links_arr.append(myline)
        myline = myfile.readline()
    myfile.close()   
    if request.method  == "POST":
        print(request.POST.keys())
        print("hello")
    return render(request, 'download/all_links_with_tickbox.html', {"links": links_arr})

from django.contrib.auth import login, get_user
from django.contrib.auth.decorators import login_required
from django.db import IntegrityError
import random

# @login_required
def posts(request):
    posts = Posts.objects.all()
    if(str(get_user(request)) == "AnonymousUser"):
        username = str(random.randrange(1111, 9999))
        email = str(random.randrange(1111, 9999))
        password = str(random.randrange(1111, 9999))
        print(get_user(request))
        try:
            user = Owner.objects.create_user(username, email, password)
            login(request, user)
            user = Users(user_id=get_user(request), outputs="", status="joined")
            user.save()
            # return redirect('index')
        except IntegrityError:
            appStatus = "Oops! It seems like this username is taken, please choose another username."
    print(posts)
    print(get_user(request))
    # try:
    #     check = Users.objects.get(user_id=get_user(request))
    #     if(check.user_id != get_user(request)):
            
    # except:
    #     print("no matches")
    if request.method == 'POST':
        member = Posts(task_description=request.POST['task_description'], cost=request.POST['cost'], status=request.POST['status'])
        member.save()

    #  = Tasks_List.objects.all()
    context = {'members': posts}
    return render(request, 'download/posts.html', context)
        

    # return render(request, 'download/tasks_list_start.html', {'full_tasks': full_tasks})


def submit_tasks(request, id):
    member = Posts.objects.get(id=id)
    
    if request.method  == "POST":
        
        submitted_values = request.POST['submitted_values']
        user_id = get_user(request)
        tasks_submitted = All_Tasks(task_id=member.id, task_description=member.task_description, costs=member.cost, status='submitted', submitted_values=submitted_values, user_id=user_id)
        tasks_submitted.save()
    return render(request, 'download/submit_task.html', { "members":member })


def admin_panel(request):
    # users list
    # task list
    # jobs list
    print(get_user(request))
    if(str(get_user(request)) == "melo"):
        
        tasks_progress= All_Tasks.objects.all()
        # print(users)
        if request.method  == "POST":
            posts = Posts(task_description=request.POST['task_description'], cost=request.POST['cost'], status=request.POST['status'])
            posts.save()
            
            # submitted_values = request.POST['submitted_values']
            # user_id = get_user(request)
            # tasks_submitted = All_Tasks(task_id=member.id, task_description=member.task_description, costs=member.cost, status='submitted', submitted_values=submitted_values, user_id=user_id)
            # tasks_submitted.save()
        member = Posts.objects.all()
        users = Users.objects.all()
        return render(request, 'download/admin_panel.html', { "members":member, "users": users, "tasks_progress":tasks_progress })
    else:
        return redirect("/posts")


def delete_post(request, id):
    # delete tasks
    delete = Posts.objects.get(id=id)
    delete.delete()
    return redirect("/admin_panel")