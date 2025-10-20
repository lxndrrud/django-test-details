from django.shortcuts import render

# Create your views here.
from dal import autocomplete
from .models import Task

class TaskAutocomplete(autocomplete.Select2QuerySetView):
    def get_queryset(self):

        qs = Task.objects.all()

        # Получаем значение service из forwarded-полей
        service_id = self.forwarded.get('service', None)
        if service_id:
            qs = qs.filter(service_id=service_id)

        # Поддержка поиска по title
        if self.q:
            qs = qs.filter(title__icontains=self.q)

        return qs