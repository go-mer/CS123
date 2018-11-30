import django_tables2 as tables
from .models import Organization

class OrgTable(tables.Table):
    class Meta:
        model = Organization