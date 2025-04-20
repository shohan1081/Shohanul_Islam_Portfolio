from django.core.mail import send_mail
from django.shortcuts import render, redirect
from django.contrib import messages
from .forms import ContactForm
from .models import ContactMessage  # If you are saving to DB

def contact_view(request):
    if request.method == 'POST':
        form = ContactForm(request.POST)
        if form.is_valid():
            # Save to database (optional)
            ContactMessage.objects.create(
                name=form.cleaned_data['name'],
                email=form.cleaned_data['email'],
                message=form.cleaned_data['message']
            )
            
            # Send email notification
            send_mail(
                'New Contact Form Submission',  # Subject of the email
                form.cleaned_data['message'],  # Body of the email
                form.cleaned_data['email'],  # Sender's email
                ['your-email@example.com'],  # Receiver's email
                fail_silently=False,
            )

            # Show success message
            messages.success(request, "Message sent successfully!")
            return redirect('contact')
    else:
        form = ContactForm()

    return render(request, 'main/contact.html', {'form': form})
