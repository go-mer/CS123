from django import forms
from django.contrib.auth.models import User

class RegisterForm(forms.Form):
    username = forms.CharField(max_length=60)
    first_name = forms.CharField(max_length=60)
    last_name = forms.CharField(max_length=60)
    email = forms.EmailField()
    password1 = forms.CharField(widget=forms.PasswordInput)
    password2 = forms.CharField(widget=forms.PasswordInput)
    
    def clean_username(self):
        cleaned_data = super(RegisterForm, self).clean()
        username = cleaned_data['username'].lower()
        r = User.objects.filter(username=username)
        if r.count():
            raise forms.ValidationError("Username already exists")
        return username
		
    def clean_name(self):
        cleaned_data = super(RegisterForm, self).clean()
        first_name = cleaned_data['first_name'].lower()
        last_name = cleaned_data['last_name'].lower()
        if not first_name and not last_name:
            raise forms.ValidationError("Please type in your name")
			
    def clean_email(self):
        cleaned_data = super(RegisterForm, self).clean()
        email = cleaned_data['email'].lower()
        r = User.objects.filter(email=email)
        if r.count():
            raise  forms.ValidationError("Email already exists")
        return email
		
    def clean_password2(self):
        cleaned_data = super(RegisterForm, self).clean()
        password1 = cleaned_data.get('password1')
        password2 = cleaned_data.get('password2')
        if password1 and password2 and password1 != password2:
            raise forms.ValidationError("Password don't match")
        return password2

class OrgReqForm(forms.Form):
	Short_Name = forms.CharField(max_length=20)
	Full_Name = forms.CharField(max_length=50)
	Description = forms.CharField(widget=forms.Textarea)
	
	def clean(self):
		cleaned_data = super(OrgReqForm, self).clean()
		Short_Name = cleaned_data.get('Short_Name')
		Full_Name = cleaned_data.get('Full_Name')
		Description = cleaned_data.get('Description')
		if not Short_Name and not Full_Name and not Description:
			raise forms.ValidationError('You have to write something!')
			
class EventForm(forms.Form):
    Name = forms.CharField(max_length=50)
    Date = forms.DateField(widget=forms.widgets.DateInput(attrs={'type': 'date'}))
    Time = forms.TimeField(widget=forms.widgets.TimeInput(attrs={'type': 'time'}))
    Venue = forms.CharField(max_length=20)
    Description = forms.CharField(widget=forms.Textarea)
    Eval_Key = forms.CharField(max_length=15)

    def clean(self):
        cleaned_data = super(EventForm, self).clean()
        Name = cleaned_data.get('Name')
        Date = cleaned_data.get('Date')
        Time = cleaned_data.get('Time')
        Venue = cleaned_data.get('Venue')
        Description = cleaned_data.get('Description')
        Eval_Key = cleaned_data.get('Eval_Key')
        if not Name and not Date and not Time and not Venue and not Description and not Eval_Key:
            raise forms.ValidationError('You have to write something!')

class ViewEventForm(forms.Form):
    Eval_Key = forms.CharField(max_length=15)
	
    def clean(self):
        cleaned_data = super(ViewEventForm, self).clean()
        Eval_Key = cleaned_data.get('Eval_Key')
        if not Eval_Key:
            raise forms.ValidationError('You have to write something!')
			
class Evaluation(forms.Form):
    Rating = forms.IntegerField(min_value=0, max_value=10)
    Strengths = forms.CharField(widget=forms.Textarea)
    Suggestions = forms.CharField(widget=forms.Textarea)
    Learnings = forms.CharField(widget=forms.Textarea)
    Comments = forms.CharField(widget=forms.Textarea)

    def clean(self):
        cleaned_data = super(Evaluation, self).clean()
        Rating = cleaned_data.get('Rating')
        Strengths = cleaned_data.get('Strengths')
        Suggestions = cleaned_data.get('Suggestions')
        Learnings = cleaned_data.get('Learnings')
        Comments = cleaned_data.get('Comments')
        if not Rating and not Strengths and not Suggestions and not Learnings and not Comments:
            raise forms.ValidationError('You have to write something!')
