from django.contrib import admin
from django.contrib.auth.models import User, Group
from User.models import User as CustomeUser
# Register your models here.

# unregister default user models to use custom user model 
#admin.site.unregister(User)
admin.site.unregister(Group)

# register custom user and authetication model
admin.site.register(CustomeUser)
