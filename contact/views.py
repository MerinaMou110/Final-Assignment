from django.shortcuts import render, redirect
from django.contrib import messages
from django.core.mail import send_mail
from django.conf import settings
from .models import Contact

def contact_submit(request):
    if request.method == 'POST':
        name = request.POST.get('name')
        email = request.POST.get('email')
        subject = request.POST.get('subject')
        message = request.POST.get('message')

        # Save contact information to the database
        Contact.objects.create(name=name, email=email, subject=subject, message=message)

        # Send email notification
        send_mail(
            f'New Contact Form Submission: {subject}',
            f'You have received a new contact form submission from {name} ({email}).\n\nMessage: {message}',
            settings.EMAIL_HOST_USER,
            [settings.EMAIL_HOST_USER],
            fail_silently=False,
        )

        # Show success message
        messages.success(request, 'Your message has been submitted successfully!')
        
        # Redirect to the same page
        return redirect('contact_submit')

    return render(request, 'contact_form.html')
