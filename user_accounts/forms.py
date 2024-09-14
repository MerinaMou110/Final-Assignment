from django.contrib.auth.forms import UserCreationForm
from django import forms
from django.contrib.auth.models import User
from . models import UserAccount
from .constants import  GENDER_TYPE
from django.contrib.auth.forms import PasswordChangeForm


class UserRegistrationForm(UserCreationForm):
    birth_date = forms.DateField(widget=forms.DateInput(attrs={'type':'date'}))
    gender = forms.ChoiceField(choices=GENDER_TYPE)
    
    phone_num = forms.CharField(max_length=15)
    
    class Meta:
        model = User
        fields = ['username', 'password1', 'password2', 'first_name', 'last_name', 'email','gender','phone_num', 'birth_date']
        

     
    def save(self, commit=True):
        
        our_user = super().save(commit=False) 
        our_user.is_active = False
        if commit == True:
            our_user.save() 

            
            phone_num = self.cleaned_data.get('phone_num')
            gender = self.cleaned_data.get('gender')
           
            birth_date = self.cleaned_data.get('birth_date')
            
            
            # Create UserAccount instance and link it to the user
            UserAccount.objects.create(
                user = our_user,
                gender = gender,
               account_no = 100000+ our_user.id,
                birth_date =birth_date,
                phone_num=phone_num,
                
            )

           
        # Return the user instance
        return our_user
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields:
            self.fields[field].widget.attrs.update({
                'class': 'form-control form-control-lg bg-light border-0 rounded-0',
                'style': 'font-size: 14px;'
            })
       

    


class UserUpdateForm(forms.ModelForm):
    birth_date = forms.DateField(widget=forms.DateInput(attrs={'type': 'date'}))
    gender = forms.ChoiceField(choices=GENDER_TYPE)

    class Meta:
        model = User
        fields = ['username', 'first_name', 'last_name', 'email']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields:
            self.fields[field].widget.attrs.update({
                'class': (
                    'appearance-none block w-full bg-gray-200 '
                    'text-gray-700 border border-gray-200 rounded '
                    'py-3 px-4 leading-tight focus:outline-none '
                    'focus:bg-white focus:border-gray-500'
                )
            })
        if self.instance and hasattr(self.instance, 'profile'):
            user_profile = self.instance.profile
            self.fields['gender'].initial = user_profile.gender
            self.fields['birth_date'].initial = user_profile.birth_date

    def save(self, commit=True):
        user = super().save(commit=False)
        if commit:
            user.save()
            user_profile, created = UserProfile.objects.get_or_create(user=user)
            user_profile.gender = self.cleaned_data['gender']
            user_profile.birth_date = self.cleaned_data['birth_date']
            user_profile.save()
        return user
