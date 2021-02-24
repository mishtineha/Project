from django.contrib import admin
from app.models import CustomUser,InvitationStatus

admin.site.register(CustomUser)
admin.site.register(InvitationStatus)

# Register your models here.
