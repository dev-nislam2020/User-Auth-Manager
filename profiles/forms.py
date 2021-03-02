from django import forms
from django.contrib.auth.models import User
from django.core.mail import send_mail

from profiles.models import Profile


# Create your models here.
class ProfileForm(forms.ModelForm):
    first_name = forms.CharField(max_length=100, required=False)
    last_name = forms.CharField(max_length=100, required=False)

    class Meta:
        model = Profile
        fields = ('first_name', 'last_name','dob','blood_group','nationality','gender','marital_status')
        widgets = {
        'dob': forms.DateInput(attrs={'type': 'date'}),
        }   
        
    def __init__(self, request=None, *args, **kwargs):
        self.user = request.user
        super(ProfileForm, self).__init__(*args, **kwargs)
        self.initial['first_name'] = self.user.first_name
        self.initial['last_name'] = self.user.last_name
    
    def clean(self):
        cleaned_data = super(ProfileForm, self).clean()
        
        first_name = cleaned_data.get("first_name")
        last_name = cleaned_data.get("last_name")
        
        self.user.first_name = first_name
        self.user.last_name = last_name
        self.user.save()
        
        return cleaned_data

class ContactForm(forms.Form):
    name = forms.CharField(max_length=50)
    subject = forms.CharField(max_length=100)
    from_email = forms.CharField(widget=forms.EmailInput)
    message = forms.CharField(widget=forms.Textarea(attrs={'rows': 6, 'cols': 22}))

    def send_email(self):
        # send email using the self.cleaned_data dictionary
        name = self.cleaned_data.get('name')
        subject = self.cleaned_data.get('subject')
        subject = name + ' ' + subject
        message = self.cleaned_data.get('message')
        from_email = self.cleaned_data.get('from_email')
            
        return send_mail(subject, message, from_email, ['nislam7944@gmail.com'])
