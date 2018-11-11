from django.contrib import admin

from .models import Organization, Moderator, Subscription, Event, EvalForm

admin.site.register(Organization)
admin.site.register(Moderator)
admin.site.register(Subscription)
admin.site.register(Event)
admin.site.register(EvalForm)