from django.contrib import admin
from django import forms
from .models import User, Service, Task, ServiceRequest
from dal import autocomplete


class TaskInline(admin.TabularInline):
    model=Task
    extra = 0


class ServiceRequestForm(forms.ModelForm):
    class Meta:
        model = ServiceRequest
        fields = '__all__'
        widgets = {
            'task': autocomplete.ModelSelect2(
                url='task-autocomplete',
                forward=['service'],  # ← передаём выбранное поле service
                attrs={'data-placeholder': 'Выберите задачу...'}
            )
        }

# Register your models here.
@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    pass

@admin.register(Service)
class ServiceAdmin(admin.ModelAdmin):
    inlines = [TaskInline]

@admin.register(ServiceRequest)
class ServiceRequestAdmin(admin.ModelAdmin):
    form = ServiceRequestForm
    