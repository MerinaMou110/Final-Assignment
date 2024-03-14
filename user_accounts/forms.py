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
    birth_date = forms.DateField(widget=forms.DateInput(attrs={'type':'date'}))
    gender = forms.ChoiceField(choices=GENDER_TYPE)

    phone_num = forms.CharField(max_length=15)

    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'email']

    def __init__(self, *args, **kwargs):
        super(UserUpdateForm, self).__init__(*args, **kwargs)
        if self.instance:
            try:
                user_account = self.instance.account
            except UserAccount.DoesNotExist:
                user_account = None

            if user_account:
                self.fields['gender'].initial = user_account.gender
                self.fields['birth_date'].initial = user_account.birth_date
                
                self.fields['phone_num'].initial = user_account.phone_num

    def save(self, commit=True):
        user = super(UserUpdateForm, self).save(commit=False)
        if commit:
            user.save()
            user_account, created = UserAccount.objects.get_or_create(user=user)
           
            user_account.gender = self.cleaned_data['gender']
            user_account.birth_date = self.cleaned_data['birth_date']
            user_account.phone_num = self.cleaned_data['phone_num']
            user_account.save()
        return user
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields:
            self.fields[field].widget.attrs.update({
                'class': 'form-control form-control-lg bg-light border-0 rounded-0',
                'style': 'font-size: 14px; padding: 15px;',
            })