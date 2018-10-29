from django import forms

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
	Date_Time = forms.DateTimeField()
	Venue = forms.CharField(max_length=20)
	Description = forms.CharField(widget=forms.Textarea)
	Org_ID = forms.DecimalField()
	Eval_Key = forms.CharField(max_length=15)
	
	def clean(self):
		cleaned_data = super(EventForm, self).clean()
		Name = cleaned_data.get('Name')
		Date_Time = cleaned_data.get('Date_Time')
		Venue = cleaned_data.get('Venue')
		Description = cleaned_data.get('Description')
		Org_ID = cleaned_data.get('Org_ID')
		Eval_Key = cleaned_data.get('Eval_Key')
		if not Name and not Date_Time and not Venue and not Description and not Org_ID and not Eval_Key:
			raise forms.ValidationError('You have to write something!')