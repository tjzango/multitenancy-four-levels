from django.contrib import admin
from .models import Pool, Choice,Vote
from tenants.models import Tenant
# Register your models here.


admin.site.register(Pool)
admin.site.register(Choice) 
admin.site.register(Vote)
admin.site.register(Tenant)