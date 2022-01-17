from django import forms
from .models import Member, Tasks_Celery, Tasks_List, Full_Tasks_List, Full_Tasks_ID


class DownloadForm(forms.Form):
    url = forms.CharField(max_length=255, widget=forms.TextInput({
        'class': 'form-control',
        'placeholder': 'Enter URL to download...',
    }))


members = Tasks_List.objects.all()
# last_task_id = Full_Tasks_ID.objects.all().order_by("-task_id")[0]
# context = {'members': members}
# tasks -list in the form as task_id desc

INTEGER_CHOICES= [tuple([x,x]) for x in range(1,32)]
# INTEGER_CHOICES = [tuple([x.task_id, x.description]) for x in members]


class UserForm(forms.Form):
    # last_name= forms.CharField(max_length=100)
    # email= forms.EmailField()
    # age= forms.IntegerField()
    task_id = forms.IntegerField(
        label="Task Func:", widget=forms.Select(choices=INTEGER_CHOICES))
    # user_input = forms.CharField(max_length=100)
    user_inputs = forms.CharField(max_length=100)
    # task_name = forms.CharField(max_length=100)
    full_task_id = forms.CharField(max_length=100)
