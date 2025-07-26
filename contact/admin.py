from django.contrib import admin
from .models import Contact,Catagory,Activity  # Import your models here
# Register your models here.

admin.site.register(Catagory)
admin.site.register(Contact)
admin.site.register(Activity)