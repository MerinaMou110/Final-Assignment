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
from django.contrib.auth import login,logout, get_user_model
from django.views.generic import FormView
from django.views import View
# Create your views here.
from django.contrib.sites.shortcuts import get_current_site
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.utils.encoding import force_bytes, force_str
from .tokens import account_activation_token
from django.core.mail import EmailMessage
from .models import UserAccount

def send_email_user(user,  subject, template):
        message = render_to_string(template, {
            'user' : user,
            
        })
        send_email = EmailMultiAlternatives(subject, '', to=[user.email])
        send_email.attach_alternative(message, "text/html")
        send_email.send()

# class UserRegistrationView(FormView):
#     template_name = 'user_registration.html'
#     form_class = UserRegistrationForm
#     success_url = reverse_lazy('login') 
    
#     def form_valid(self,form):
#         print(form.cleaned_data)
       
#         user = form.save()  
#         # login(self.request, user) 
#         print(user)
#         messages.success(
#             self.request,
#             f'Your Account Registration successfully'
#         )
#         return super().form_valid(form)

            #this is for email confirmation      
def activate(request, uidb64, token):
    User = get_user_model()
    try:
        uid = force_str(urlsafe_base64_decode(uidb64))
        user = User.objects.get(pk=uid)
    except:
        user = None

    if user is not None and account_activation_token.check_token(user, token):
        user.is_active = True
        user.save()

        messages.success(request, "Thank you for your email confirmation. Now you can login your account.")
        return redirect('login')
    else:
        messages.error(request, "Activation link is invalid!")

    return redirect('home')

def activateEmail(request, user, to_email):
    mail_subject = "Activate your user account."
    message = render_to_string("template_active_account.html", {
        'user': user.username,
        'domain': get_current_site(request).domain,
        'uid': urlsafe_base64_encode(force_bytes(user.pk)),
        'token': account_activation_token.make_token(user),
        "protocol": 'https' if request.is_secure() else 'http'
    })
    email = EmailMessage(mail_subject, message, to=[to_email])
    if email.send():
        messages.success(request, f'Dear {user}, please go to you email {to_email} inbox and click on \
                received activation link to confirm and complete the registration. Note: Check your spam folder.')
    else:
        messages.error(request, f'Problem sending email to {to_email}, check if you typed it correctly.')


class UserRegistrationView(FormView):
    template_name = 'user_registration.html'
    form_class = UserRegistrationForm
    success_url = reverse_lazy('login') 
    
    def form_valid(self,form):
        print(form.cleaned_data)
       
        user = form.save(commit=False)  
        user.is_active=False
        user.save()

        UserAccount.objects.create(
            user=user,
            gender=form.cleaned_data.get('gender'),
            account_no=100000 + user.id,  # Example calculation for account_no
            birth_date=form.cleaned_data.get('birth_date'),
            phone_num=form.cleaned_data.get('phone_num'),
        )
        activateEmail(self.request,user,form.cleaned_data.get('email'))

        # login(self.request, user) 
        print(user)
        # messages.success(
        #     self.request,
        #     f'Your Account Registration successfully'
        # )
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
    
