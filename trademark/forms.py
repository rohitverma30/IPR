from django import forms
from .models import trademarkSubmission
class trademarkSubmissionForm(forms.Form):
    name = forms.CharField(label="First Name", max_length=100, required=True)
    surname = forms.CharField(label="Surname", max_length=100, required=True)
    email = forms.EmailField(label="Email", required=True)
    phone = forms.CharField(label="Phone Number", max_length=10, required=True, widget=forms.TextInput(attrs={'pattern': '[0-9]{10}', 'title': 'Enter a valid 10-ditrademarkt phone number'}))
    title = forms.CharField(label="Title of trademark", max_length=200, required=True)
    description = forms.CharField(label="Description of trademark", widget=forms.Textarea, required=True)

class StafftrademarkForm(forms.Form):
    name = forms.CharField(label="First Name", max_length=100, required=True)
    description = forms.CharField(label="Description of trademark", widget=forms.Textarea, required=True)
    content = forms.CharField(label="Content of trademark", widget=forms.Textarea, required=True)
    
class StatusForm(forms.Form):
    email = forms.EmailField(label="Email", required=True)
    status = forms.ChoiceField(
        choices=trademarkSubmission.status_CHOICES,  # Ensure choices are loaded correctly
        widget=forms.RadioSelect,
        required=True
    )
