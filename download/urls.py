from django.urls import path, include
from django.conf.urls.static import static
from django.conf import settings 

from .views import delete_post, admin_panel, submit_tasks, posts, get_all_urls_with_tickbox, remove_all_selenium_tasks, remove_selenium_task, pass_json_data, start_task, delete_full_tasks_id, create_task_full, delete_tasks, insert_all_tasks_with_id, cancel_selenium_task, pause_selenium_task,resume_selenium_task, demo_view, selenium_skel_new_tasks, start_automation, sleepy, celery_check, selenium_test, pause_task
from . import views

app_name = 'download'

urlpatterns = [
	# Demo view
    path('admin_panel', admin_panel, name='admin_panel'),
    path(r'submit_tasks/<id>/', submit_tasks, name='submitted_values'),
    path('posts', posts, name='posts'),
	path(r'delete_post/<id>/', delete_post, name='delete_post'),
    path('demo', demo_view, name='demo'),
	path('automation', start_automation, name="automation"),
    path('testing', selenium_skel_new_tasks, name="testing"),
    path('sleepy', sleepy, name="sleepy"),
    path('check', celery_check, name="check"),
    path(r'pause/<id>/', pause_selenium_task, name='pause'),
    path(r'resume/<id>/', resume_selenium_task, name='resume'),
    path(r'cancel/<id>/', cancel_selenium_task, name='cancel'),
    path(r'remove/<id>/', remove_selenium_task, name='remove'),
    path(r'delete_all', remove_all_selenium_tasks, name='delete_all'),
	path('', views.index, name='index'),
    path(r'create', views.create, name='create'),
    path(r'edit/<id>/', views.edit, name='edit'),
    path(r'update/<id>/', views.update, name='update'),
    path(r'delete/<id>/', views.delete, name='delete'),
	path("upload", views.upload, name="upload"),
    # new tasks list for functions
    path(r'insert_all_tasks_with_id', insert_all_tasks_with_id, name='create_functions_task'),
    path(r'delete_tasks/<id>/', delete_tasks, name='delete_tasks'),
    # full tasks impementation
    # delete_full_tasks_id
    path(r'create_new_full_task', create_task_full, name='create_task_full'),
    path(r'delete_full_tasks_id/<id>/', delete_full_tasks_id, name='delete_tasks'),
    # final task start
    path(r'start_task', start_task, name='start_task'),
    path(r'get_all_urls_with_tickbox', get_all_urls_with_tickbox, name='get_all_urls_with_tickbox'),
    
    # path(r'^code_runner$', views.code_runner, name='code_runner'),
    path(r'pass_json_data', pass_json_data, name='pass_json_data'),
    
]+ static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)