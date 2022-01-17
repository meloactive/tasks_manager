from __future__ import absolute_import, unicode_literals

# Celery
from celery import shared_task, current_task

from .models import Member, Tasks_Celery, Tasks_List, Full_Tasks_List, Full_Tasks_ID
from celery_progress_demo.celery import app
# Celery-progress
from celery_progress.backend import ProgressRecorder
from celery_progress_demo.celery import app

import random
# from screenshot import Screenshot_Clipping
from selenium import webdriver, common
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.action_chains import ActionChains
# from Screenshot import Screenshot_Clipping
# ob=Screenshot_Clipping.Screenshot()

# Task imports
import os
import time
import subprocess
import re
import sys
# from flask import render_template, jsonify
from celery.app.task import Task
# import pyautogui
import bezier
import numpy as np
# pyautogui.FAILSAFE = False


@shared_task(bind=True)
def ProcessDownload(self, url):
    # Announce new task (celery worker output)
    print('Download: Task started')

    # Saved downloaded file with this name
    filename = 'file_download'
    # Wget command (5 seconds timeout)
    command = f'wget {url} -T 5 -O {filename}'
    # command = f'curl -o ./{filename} {url}'

    # Start download process
    download = subprocess.Popen(command.split(
        ' '), stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
    # Read each output line and update progress
    update_progress(self, download)

    # Make sure wget process is terminated
    download.terminate()
    try:
        # Wait 100ms
        download.wait(timeout=0.1)
        # Print return code (celery worker output)
        print(f'Subprocess terminated [Code {download.returncode}]')
    except subprocess.TimeoutExpired:
        # Process was not terminated in the timeout period
        print('Subprocess did not terminate on time')

    # Check if process was successfully completed (return code = 0)
    if download.returncode == 0:
        # Delete file
        try:
            folder = os.getcwd()
            # filepath = os.path.join(folder, filename)
            # os.remove(filepath)
        except:
            print('Could not delete file')
        # Return message to update task result
        return 'Download was successful!'
    else:
        # Raise exception to indicate something wrong with task
        raise Exception('Download timed out, try again')


def update_progress(self, proc):
    # Create progress recorder instance
    progress_recorder = ProgressRecorder(self)

    while True:
        # Read wget process output line-by-line
        line = proc.stdout.readline()

        # If line is empty: break loop (wget process completed)
        if line == b'':
            break

        linestr = line.decode('utf-8')
        print(linestr)
        if '%' in linestr:
            # Find percentage value using regex

            percentage = re.findall('[0-9]{0,3}%', linestr)[0].replace('%', '')
            # Print percentage value (celery worker output)
            print(percentage)
            # Build description
            # if(percentage == "100"):
            # import os
            folder = os.path.abspath(os.getcwd())
            progress_description = 'Downloading (' + \
                str(percentage) + '%)' + str(folder)
            # Update progress recorder
            progress_recorder.set_progress(
                int(percentage), 100, description=progress_description)
        else:
            # Print line
            print(linestr)

        # Sleep for 100ms
        time.sleep(0.1)


# selenium progress with db updates
@shared_task(bind=True)
def automation_with_selenium(self):
    progress_recorder = ProgressRecorder(self)
    for i in range(11):
        time.sleep(1)
        percentage = i * 10
        progress_description = 'Downloading (' + str(percentage) + '%)'
        # Update progress recorder
        progress_recorder.set_progress(
            int(percentage), 100, description=progress_description)


# @shared_task(bind=True)
@app.task(name='go_to_sleep', bind=True)
def go_to_sleep(self, duration):

    self.update_state(state='PROGRESS')
    progress_recorder = ProgressRecorder(self)
    print("hello")
    # f = open("demofile2.txt", "a")
    # f.write("Now the file has more content!")
    # f.close()
    print()
    while app.AsyncResult(self.request.id).state == 'PAUSING' or app.AsyncResult(self.request.id).state == 'PAUSED':
        if app.AsyncResult(self.request.id).state == 'PAUSING':
            print(self.request.id + 'PAUSED')
            self.update_state(state='PAUSED')
            # task_status.status = 'PAUSED'
            # BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
            f = open("demofile2.txt", "a")
            f.write("Now the file has more content!")
            f.close()
            # db.session.commit()

    ########### CHECKING FOR RESUME ###########
    if app.AsyncResult(self.request.id).state == 'RESUME':
        print(self.request.id + 'RESUMED')
        self.update_state(state='PROCESSING')
        # task_status.status = 'PROCESSING'
        # db.session.commit()

    if app.AsyncResult(self.request.id).state == 'PROCESSING':
        print('PROCESSING')
        self.update_state(state='PROCESSING')
        f = open("proessing.txt", "a")
        f.write("Now the file has more content!")
        f.close()

    ########### CHECKING FOR CANCEL ###########
    if app.AsyncResult(self.request.id).state == 'CANCEL':
        print(self.request.id + 'CANCELLED')
        self.update_state(state='CANCELLED')
        # db.session.rollback()
        # task_status.status = 'CANCELLED'
        # db.session.commit()
        return 'CANCELLED'

    for i in range(50):
        time.sleep(duration)
        progress_recorder.set_progress(i*2 + 1, 100, f'On iteration {i}')
    return 'Done'

# added an extra id for db.query nd task_id


@shared_task(bind=True)
def testing_selenium(self, melo, url):

    task_status = Tasks_Celery.objects.get(id=melo)
    ######## STARTING THE TASK ##########
    # task_status = Task_status.query.get(sno)
    task_status.task_id = self.request.id
    print(self.request.id)
    # self.update_state(state='processing')
    task_status.status = 'processing'
    # db.session.commit()
    task_status.save()
    progress_recorder = ProgressRecorder(self)
    print("check_progress: " + str(check_progress(task_status.task_id)))
    while(str(check_progress(task_status.task_id)) == "pause"):
        print("Task is paused")

    while(str(check_progress(task_status.task_id)) == "cancel"):
        print("Task is cancelled!")
        sys.exit("cancelled")
        # return "cancelled"
    # if(check_progress(task_id) == "resume"):
    #     print("Task ")
    driver = webdriver.Chrome(
        '/home/melodic/Documents/testing_cel/django-celery-progress-demo_3/chromedriver_linux64/chromedriver')
    driver.get('https://www.seleniumhq.org')
    progress_recorder.set_progress(10, 100, f'loading...')

    print("check_progress: " + str(check_progress(task_status.task_id)))
    while(check_progress(task_status.task_id) == "pause"):
        print("Task is paused")

    while(str(check_progress(task_status.task_id)) == "cancel"):
        print("Task is cancelled!")
        sys.exit("cancelled")
        # return "cancelled"
    # if(check_progress(task_id))
    driver.get(url)
    print("check_progress: " + str(check_progress(task_status.task_id)))
    progress_recorder.set_progress(100, 100, f'loading...' + url)
    # print()
    # for i in range(50):
    #     time.sleep(duration)
    #     progress_recorder.set_progress(i*2 + 1, 100, f'On iteration {i}')
    return 'Done'


# progress should be controllable
#  maybe I can use some db with update for task no.

# A function is needed for always getting db updates

def update_progress_db(task_id, status):
    members = Tasks_Celery.objects.get(task_id=task_id)

    if(members.finished == False):
        if(status == "pause"):
            members.status = "pause"
            members.save()
            return "pause"
        if(status == "resume"):
            members.status = "resume"
            members.save()
            return "resume"


def check_progress(task_id):
    members = Tasks_Celery.objects.get(task_id=task_id)
    print(members)
    # if(members.finished == False):
    if(members.status == "pause"):
        return "pause"
    elif(members.status == "resume"):
        return "resume"
    elif(members.status == "cancel"):
        return "cancel"
    else:
        return "resume"
# def check_progress(task_id):
    # return "resume"


global driver
# go to a webpage

# global url2, session_id
url2 = ""
session_id = ""
def go_to_page(url):
    texts = ""
    global url2, session_id
    with open("browser.txt", "r") as f:
        texts = f.readline()
    global driver
    if(texts != ""):
        driver = webdriver.Remote(command_executor=texts.split(" ")[0],desired_capabilities={})
        driver.close()   # this prevents the dummy browser
        driver.session_id = texts.split(" ")[1]
        driver.get(str(url))
    else:

        options = webdriver.ChromeOptions()
        # options.add_experimental_option("debuggerAddress", "127.0.0.1:9222")
        options.add_argument('--user-data-dir=chrome_profiles/Profile\ 1')
        # options.add_argument("debuggerAddress=127.0.0.1:9222")
        options.add_argument(
            'user_agent=Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/60.0.3112.50 Safari/537.36')
        options.add_argument('--no-sandbox')
        options.add_argument('--start-maximized')
        options.add_argument('--start-fullscreen')
        options.add_argument('--single-process')
        options.add_argument('--disable-dev-shm-usage')
        # options.add_argument("--incognito")
        options.add_argument('--disable-blink-features=AutomationControlled')
        options.add_argument('--disable-blink-features=AutomationControlled')
        options.add_experimental_option('useAutomationExtension', False)
        options.add_experimental_option("excludeSwitches", ["enable-automation"])
        options.add_argument("disable-infobars")
        
        #
        # specify headless mode
        # options.add_argument('headless')
        # specify the desired user agent
        # options.add_argument()
        # driver = webdriver.Chrome(chrome_options=options)
        
        driver = webdriver.Chrome(
            '/home/melodic/Documents/testing_cel/django-celery-progress-demo_3/chromedriver_linux64/chromedriver', chrome_options=options)
        driver.get(str(url))
        url2 = driver.command_executor._url       #"http://127.0.0.1:60622/hub"
        session_id = driver.session_id  
        print(url2)
        print(session_id)
        with open("browser.txt", "w") as f:
            f.write(str(url2) + " " + str(session_id))

# click a button(button_name):


def click_button(button_name):
    driver.find_element_by_xpath("//a[text()='"+button_name+"']").click()


#  clicking a link
def click_link(link):
    driver.findElement(By.xpath("//a[@href='"+link+"']")).click();


def pause_task(id):
    member = Tasks_Celery.objects.get(task_id=id)
    print(member)
    # tasks_db = Tasks_Celery(task_id=task.task_id, description="sleepy", progress="0", finished="False")
    # tasks_db.save()
    member.status = "pause"
    member.save()
    print(member)
    # return redirect("/check")

def mouse_bezier_movement():

    # Disable pyautogui pauses (from DJV's answer)
    pyautogui.MINIMUM_DURATION = 0
    pyautogui.MINIMUM_SLEEP = 0
    pyautogui.PAUSE = 0

    # We'll wait 5 seconds to prepare the starting position
    start_delay = 1 
    print("Drawing curve from mouse in {} seconds.".format(start_delay))
    pyautogui.sleep(start_delay)

    # For this example we'll use four control points, including start and end coordinates
    start = pyautogui.position()
    end = start[0]+600, start[1]+200
    # Two intermediate control points that may be adjusted to modify the curve.
    control1 = start[0]+125, start[1]+100
    control2 = start[0]+375, start[1]+50

    # Format points to use with bezier
    control_points = np.array([start, control1, control2, end])
    points = np.array([control_points[:,0], control_points[:,1]]) # Split x and y coordinates

    # You can set the degree of the curve here, should be less than # of control points
    degree = 3
    # Create the bezier curve
    curve = bezier.Curve(points, degree)
    # You can also create it with using Curve.from_nodes(), which sets degree to len(control_points)-1
    # curve = bezier.Curve.from_nodes(points)

    curve_steps = 50  # How many points the curve should be split into. Each is a separate pyautogui.moveTo() execution
    delay = 1/curve_steps  # Time between movements. 1/curve_steps = 1 second for entire curve

    # Move the mouse
    for i in range(1, curve_steps+1):
        # The evaluate method takes a float from [0.0, 1.0] and returns the coordinates at that point in the curve
        # Another way of thinking about it is that i/steps gets the coordinates at (100*i/steps) percent into the curve
        x, y = curve.evaluate(i/curve_steps)
        print(x,y)
        pyautogui.moveTo(x, y)  # Move to point in curve
        pyautogui.sleep(delay)  # Wait delay



def page_random_view(time_given):
    y = 1000
    t = 0
    t1 = time.time() 
    total_inner = 0
    for timer in range(0,time_given):
            driver.execute_script("window.scrollTo(0, "+str(y)+")")
            y += 1000
            
            mouse_bezier_movement()
            
            time.sleep(1)
            pageHeight = driver.execute_script("return document.body.scrollHeight")
            totalScrolledHeight = driver.execute_script("return window.pageYOffset + window.innerHeight")
            t2 = time.time()
            t = int(t2-t1)
            # -1 is to make sure the rounding issues
            if((pageHeight-1)<=totalScrolledHeight):
                totalScrolledHeight = driver.execute_script("return window.pageYOffset - window.innerHeight")
                # print("pass")
                if(total_inner == 0):
                    total_inner = timer
                for i in range(total_inner):
                    totalScrolledHeight = driver.execute_script("return window.pageYOffset - window.innerHeight")
                    # mouse_bezier_movement()
                    # time.sleep(1)

                # break
            else:
                continue
            if(t == timer):

                print("pass")
                break



def get_all_links():
    links = []
    elems = driver.find_elements_by_tag_name('a')
    for elem in elems:
        href = elem.get_attribute('href')
        if href is not None:
            print(href)
            links.append(href)
            with open("links.txt", "a") as fi:
                fi.write(href+"\n")
    return links

# get image of current page
# def get_current_page_screesnshot(image_name, save_path):
#     img_url=ob.full_Screenshot(driver, save_path=save_path, image_name=image_name)


def get_values_from_page(xpath, attr):
    # while True:
    #     try:
    time.sleep(5)
    count_text = driver.find_element_by_xpath(str(xpath))
    # count_text.get_attribute
    ccc = count_text.get_attribute(str(attr))
        #     break
        # except common.exceptions.NoSuchElementException:
        #     print("Fail.")
    print(ccc)
    f = open("fiverr_req.txt", "r")
    # print(f.readline())
    # with open("fiverr_req.txt", "w") as f:
    #     f.write(ccc)
    if(f.readline() == ccc or ccc == "0"):
        driver.quit()
        exit()
    import pyttsx3
    engine = pyttsx3.init()
    engine.setProperty("rate", 100)
    engine.say("You've got " + str(ccc) + "requests")
    engine.runAndWait()
    with open("fiverr_req.txt", "w") as f:
        f.write(ccc)
    return ccc


def go_to_page_without_opening_browser(url):
    driver.get(str(url))

def type_something(words):
    pyautogui.write(words, interval=0.25)

def run_tasks_using_task_id(task_id, inp, celery_task_id, user_inputs=""):
    # get task id func

    if(task_id == "1"):
        print("job started 1")
        go_to_page(user_inputs)
        with open('page.html', 'w+') as f:
            f.write(driver.page_source)
            f.close()

    if(task_id == "2"):
        print("job started 2")
        click_button(user_inputs)
    if(task_id == "3"):
        print("job started 3")
        page_random_view(int(user_inputs))
    if(task_id == "4"):
        return get_all_links()
    if(task_id == "5"):
        return get_values_from_page(user_inputs.split(",")[0], user_inputs.split(",")[1].strip())
    if(task_id == "6"):
        go_to_page_without_opening_browser(user_inputs)
    if(task_id == "7"):
        page_random_view(user_inputs)
    if(task_id == "8"):
        pause_task(celery_task_id)
    if(task_id == "9"):
        type_something(user_inputs)
    if(task_id == "10"):
        click_link(user_inputs)
    # if some task has some inputs to take in the middle


    image_name = "/home/melodic/Documents/testing_cel/django-celery-progress-demo_3/download/static/download/images/" + \
        str(inp) + ".png"
    driver.save_screenshot(image_name)


@shared_task(bind=True)
def main_task(self, full_task_id):
    # get all tasks from task id
    # loop and get func name and user inputs
    # add a progress system
    progress_recorder = ProgressRecorder(self)
    # print(full_task_id)
    print(self.request.id)
    self.update_state(state='PROCESSING')
    time.sleep(2)
    print(app.AsyncResult(self.request.id).state)
    full_tasks_with_id = Full_Tasks_List.objects.filter(
        full_task_id=full_task_id)
    # print(full_tasks_with_id)
    percentage = 100
    task_percent = percentage / len(full_tasks_with_id)
    i = 1
    for tasks in full_tasks_with_id:
        # get indiv tasks number and run the final task
        # progress percentage calc
        # add status change of the task
        member = Tasks_Celery.objects.get(task_id=self.request.id)
        print(member)
        if(member.status == "pause"):
            print("task paused: ")
            self.update_state(state='PAUSE')
        if(member.status == "cancel"):
            print("task paused: ")
            self.update_state(state='CANCEL')
            exit()
        if(member.status == "resume"):
            self.update_state(state='PROCESSING')
        while(app.AsyncResult(self.request.id).state == "PAUSE"):
            # print("task paused: " )
            member = Tasks_Celery.objects.get(task_id=self.request.id)
            if(member.status == "resume"):
                self.update_state(state='PROCESSING')
            if(member.status == "cancel"):
                print("task cancelled: ")
                self.update_state(state='CANCEL')
                exit()
            # exit()

        if(len(full_tasks_with_id) == i):
            task_percent = 100
            i = 1

        task_desc = Tasks_List.objects.get(task_id=tasks.task_id)
        progress_description = {'links': "https://google.com" + str(task_desc.description), 'desc': 'Surfing: ' + str(task_desc.description) + ", inputs: " + str(
            tasks.user_inputs) + ", percent: " + str(int(task_percent) * i) + "%", 'url': "/static/download/images/" + str(i) + ".png"}
        # Update progress recorder
        progress_recorder.set_progress(
            int(task_percent * i), 100, description=progress_description)
        i = i + 1
        urls = run_tasks_using_task_id(
            tasks.task_id, str(i),self.request.id, tasks.user_inputs)
        if(urls):
            task_desc = Tasks_List.objects.get(task_id=tasks.task_id)
            progress_description = {'links': str(urls), 'desc': 'Surfing: ' + str(task_desc.description)  + ", inputs: " + str(
                tasks.user_inputs) + ", percent: " + str(int(task_percent) * i) + "%", 'url': "/static/download/images/" + str(i) + ".png"}
            # Update progress recorder
            progress_recorder.set_progress(
                int(task_percent * i), 100, description=progress_description)
    driver.quit()


#  create progress system
# def update_progress_from_db():
#     progress_recorder = ProgressRecorder(self)
#     full_tasks_with_id = Full_Tasks_List.objects.filter(full_task_id=full_task_id)
#     percentage = 100
#     task_percent = percentage / len(full_tasks_with_id)
#     progress_description = 'Downloading (' + str(percentage) + '%)' + str(folder)
#     # Update progress recorder
#     progress_recorder.set_progress(
#         int(task_percent), 100, description=progress_description)


# def update_progress(self, proc):
#     # Create progress recorder instance
#     progress_recorder = ProgressRecorder(self)

#     while True:
#         # Read wget process output line-by-line
#         line = proc.stdout.readline()

#         # If line is empty: break loop (wget process completed)
#         if line == b'':
#             break

#         linestr = line.decode('utf-8')
#         print(linestr)
#         if '%' in linestr:
#             # Find percentage value using regex

#             percentage = re.findall('[0-9]{0,3}%', linestr)[0].replace('%', '')
#             # Print percentage value (celery worker output)
#             print(percentage)
#             # Build description
#             # if(percentage == "100"):
#             # import os
#             folder = os.path.abspath(os.getcwd())
#             progress_description = 'Downloading (' + \
#                 str(percentage) + '%)' + str(folder)
#             # Update progress recorder
#             progress_recorder.set_progress(
#                 int(percentage), 100, description=progress_description)
#         else:
#             # Print line
#             print(linestr)

#         # Sleep for 100ms
#         time.sleep(0.1)


@shared_task(bind=True)
def start_task_from_tasks(self, full_task_ids):
    full_tasks = Full_Tasks_ID.objects.all()
    print(full_tasks)
    # if request.method == 'POST':
    full_task_id = full_task_ids
    print(full_task_id)
    task = main_task.delay(full_task_id)
    tasks_db = Tasks_Celery(
        task_id=task.task_id, description="sleepy", progress="0", status='processing', finished="False")
    tasks_db.save()

# cteate a task number in the db where
# def