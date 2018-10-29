from django.contrib import admin

from .models import Organization, Event, UserPosition, EvalForm

admin.site.register(Organization)
admin.site.register(Event)
admin.site.register(UserPosition)
admin.site.register(EvalForm)