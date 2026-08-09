from django.shortcuts import render, redirect
from django.core.mail import EmailMessage
from django.http import HttpResponse, JsonResponse
from django.conf import settings
from django.contrib import messages
from .forms import ContactForm
 # Import your contact form

try:
    # Durable backup so a submission is never lost even if the email fails to send.
    from contact.models import ContactMessage
except Exception:
    ContactMessage = None

SERVICES = [
    {
        'icon': 'fa-solid fa-code',
        'title': 'Frontend Developer',
        'desc': 'Designing responsive, interactive, and visually appealing user interfaces using HTML, CSS, Tailwind CSS, and JavaScript.',
        'url_name': 'frontend',
        'image': 'main/images/frontend.avif',
    },
    {
        'icon': 'fa-solid fa-server',
        'title': 'Backend Developer',
        'desc': 'Building robust server-side logic and secure REST APIs with Django and Python to power real-world production systems.',
        'url_name': 'backend',
        'image': 'main/images/backend.jpg',
    },
    {
        'icon': 'fa-solid fa-database',
        'title': 'Database Design & Management',
        'desc': 'Structuring and managing efficient, secure databases with PostgreSQL and MySQL for reliable data flow and storage.',
        'url_name': 'database',
        'image': 'main/images/database.avif',
    },
    {
        'icon': 'fa-solid fa-cloud-arrow-up',
        'title': 'DevOps & Cloud Infrastructure',
        'desc': 'Deploying and managing infrastructure on AWS (EC2, S3) and VPS with Docker, CI/CD workflows, and 99.9% uptime.',
        'url_name': 'devops',
        'image': None,
    },
    {
        'icon': 'fa-solid fa-layer-group',
        'title': 'Software Development',
        'desc': 'Creating scalable, reliable, and user-friendly software — from custom tools to complex enterprise systems.',
        'url_name': 'software',
        'image': 'main/images/software.jpg',
    },
]


def index(request):
    return render(request, 'main/index.html', {'services': SERVICES})

def frontend_detail(request):
    return render(request, 'main/frontend.html')

def backend(request):
    return render(request, 'main/backend.html')

def database(request):
    return render(request,'main/database.html')

def devops(request):
    return render(request, 'main/devops.html')
def software(request):
    return render(request, 'main/software.html')


def contact_view(request):
    """
    Handles the contact form submitted from the single-page site (main/contact.html).
    The form is submitted via fetch() as JSON/AJAX, so this normally returns JsonResponse.
    A non-JS fallback (plain form POST) redirects back to the page with a #contact anchor
    and a `contact=success`/`contact=error` query flag the template can read.
    """
    if request.method != 'POST':
        return redirect('index')

    form = ContactForm(request.POST)
    is_ajax = request.headers.get('x-requested-with', '').lower() == 'xmlhttprequest'

    if not form.is_valid():
        if is_ajax:
            return JsonResponse({'success': False, 'errors': form.errors}, status=400)
        return redirect('/?contact=error#contact')

    name = form.cleaned_data['name']
    email = form.cleaned_data['email']
    message = form.cleaned_data['message']

    # Always keep a durable copy first, so nothing is lost even if email delivery fails.
    if ContactMessage is not None:
        try:
            ContactMessage.objects.create(name=name, email=email, message=message)
        except Exception:
            pass

    recipient = getattr(settings, 'CONTACT_RECIPIENT_EMAIL', None) or settings.EMAIL_HOST_USER
    full_message = f"Name: {name}\nEmail: {email}\n\nMessage:\n{message}"

    try:
        email_msg = EmailMessage(
            subject=f"New portfolio message from {name}",
            body=full_message,
            from_email=settings.EMAIL_HOST_USER,
            to=[recipient],
            reply_to=[email],
        )
        email_msg.send(fail_silently=False)
    except Exception:
        # The message is safely saved above even though the email failed to send.
        if is_ajax:
            return JsonResponse({
                'success': False,
                'errors': {'__all__': [
                    "Your message was saved, but the email notification couldn't be sent right now. "
                    "I'll still see it — or you can email me directly."
                ]},
            }, status=502)
        return redirect('/?contact=error#contact')

    if is_ajax:
        return JsonResponse({'success': True})
    return redirect('/?contact=success#contact')


