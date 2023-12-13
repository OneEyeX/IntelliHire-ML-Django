from django.contrib import admin

from .models import ApplyJob, Industry, Job, State

# Register your models here.
admin.site.register(Job)
admin.site.register(Industry)
admin.site.register(State)
admin.site.register(ApplyJob)
