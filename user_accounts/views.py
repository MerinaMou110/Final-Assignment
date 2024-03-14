from django.shortcuts import render
from .forms import UserRegistrationForm,UserUpdateForm
from django.urls import reverse_lazy
from django.shortcuts import redirect
from django.core.mail import EmailMultiAlternatives
from django.contrib import messages
from django.shortcuts import redirect
from django.template.loader import render_to_string
from django.contrib.auth.views import LoginView, LogoutView
from django.contrib.auth.views import PasswordChangeView
from django.contrib.auth import login,logout
from django.views.generic import FormView
from django.views import View
# Create your views here.

def send_email_user(user,  subject, template):
        message = render_to_string(template, {
            'user' : user,
            
        })
        send_email = EmailMultiAlternatives(subject, '', to=[user.email])
        send_email.attach_alternative(message, "text/html")
        send_email.send()

class UserRegistrationView(FormView):
    template_name = 'user_registration.html'
    form_class = UserRegistrationForm
    success_url = reverse_lazy('login') 
    
    def form_valid(self,form):
        print(form.cleaned_data)
       
        user = form.save()  
        # login(self.request, user) 
        print(user)
        messages.success(
            self.request,
            f'Your Account Registration successfully'
        )
        return super().form_valid(form)
    

class UserLoginView(LoginView):
    template_name = 'user_login.html'
    def get_success_url(self):
        messages.success(
            self.request,
            f'Your Account Logged in successfully'
        )
        return reverse_lazy('home')
    

class UserLogoutView(LogoutView):
    def get_success_url(self):
        if self.request.user.is_authenticated:
            logout(self.request)
        return reverse_lazy('home')
    

class UserAccountUpdateView(View):
    template_name = 'profile.html'

    def get(self, request):
        form = UserUpdateForm(instance=request.user)
        return render(request, self.template_name, {'form': form})

    def post(self, request):
        form = UserUpdateForm(request.POST, instance=request.user)
        if form.is_valid():
            form.save()
            return redirect('profile')  
        return render(request, self.template_name, {'form': form})
    

class CustomPasswordChangeView(PasswordChangeView):
    
    template_name = 'password_change.html'
    success_url = reverse_lazy('profile') 

    def form_valid(self, form):
        response = super().form_valid(form)
        user = self.request.user

        # Send email notification about the password change
        
        send_email_user(self.request.user,  "Password Change Notification", "update_pass_email.html")

        messages.success(self.request, 'Your password has been changed successfully.')
        return response
    
