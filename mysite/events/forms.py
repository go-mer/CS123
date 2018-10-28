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