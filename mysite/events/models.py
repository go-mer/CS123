from django.db import models
from django.contrib.auth.models import User

class Organization(models.Model):
	Org_ID = models.BigAutoField(primary_key=True)
	Short_Name = models.CharField(max_length=20, blank=False)
	Full_Name = models.CharField(max_length=50, blank=False)
	Description = models.TextField()
	Approved = models.BooleanField(default=False)
	
class UserPosition(models.Model):
    User = models.ForeignKey(User, on_delete=models.CASCADE) 
    Org_ID = models.ForeignKey(Organization, on_delete=models.CASCADE)
    Relation = (
		('Mod', 'Moderator'),
		('Sub', 'Subscriber'),
	)
	
class Event(models.Model):
	Event_ID = models.BigAutoField(primary_key=True)
	Name = models.CharField(max_length=50, blank=False)
	Date_Time = models.DateTimeField(auto_now=False, auto_now_add=False, blank=False)
	Venue = models.CharField(max_length=20, blank=False)
	Description = models.TextField()
	Org_ID = models.ForeignKey(Organization, on_delete=models.CASCADE)
	Eval_Key = models.CharField(max_length=15, blank=False)
	
class EvalForm(models.Model):
	User = models.ForeignKey(User, on_delete=models.CASCADE) 
	Event_ID = models.ForeignKey(Event, on_delete=models.CASCADE)
	Rating = (
		(0),
		(1),
		(2),
		(3),
		(4),
		(5),
		(6),
		(7),
		(8),
		(9),
		(10),
	)
	Strengths = models.TextField()
	Suggestions = models.TextField()
	Learnings = models.TextField()
	Comments = models.TextField()