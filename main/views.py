from django.shortcuts import render, redirect
from django.core.mail import send_mail
from django.http import HttpResponse
from django.conf import settings
from django.contrib import messages
from .forms import ContactForm
 # Import your contact form

def index(request):
    return render(request, 'main/index.html')

def frontend_detail(request):
    return render(request, 'main/frontend.html')

def backend(request):
    return render(request, 'main/backend.html')

def database(request):
    return render(request,'main/database.html')

def desktop(request):
    return render(request, 'main/desktop.html')
def software(request):
    return render(request, 'main/software.html')


def contact_view(request):
    if request.method == 'POST':
        form = ContactForm(request.POST)
        if form.is_valid():
            # Send email
            name = form.cleaned_data['name']
            email = form.cleaned_data['email']
            message = form.cleaned_data['message']
            full_message = f"Name: {name}\nEmail: {email}\n\nMessage:\n{message}"

            send_mail(
                subject="New Contact Message from Portfolio",
                message=full_message,
                from_email=settings.EMAIL_HOST_USER,
                recipient_list=[settings.EMAIL_HOST_USER],
                fail_silently=False,
            )

            # After sending the message, render the success message
            return render(request, 'contact_success.html', {'form': form})

    else:
        form = ContactForm()

    return render(request, 'contact.html', {'form': form})


