from django.shortcuts import render
from django.core.mail import send_mail
from django.http import JsonResponse
from django.views.decorators.http import require_POST
import json
from django.views.decorators.csrf import csrf_exempt

# Create your views here.
def index(request):
    return render(request, "index.html")

@csrf_exempt
@require_POST
def send_quote(request):
    try:
        data = json.loads(request.body)

        name     = data.get('name', '').strip()
        phone    = data.get('phone', '').strip()
        email    = data.get('email', '').strip()
        location = data.get('location', '').strip()
        services = data.get('services', [])
        notes    = data.get('notes', '').strip()

        # Build service details string
        service_details = []
        for s in services:
            sname    = s.get('name', '')
            sdetails = s.get('details', '')
            service_details.append(f"  • {sname}: {sdetails}")
        services_str = '\n'.join(service_details) if service_details else '  None specified'

        message = f"""
NEW QUOTE REQUEST — CIPHER DEVELOPERS AND SERVICES
===================================================

CLIENT DETAILS
--------------
Name     : {name}
Phone    : {phone}
Email    : {email}
Location : {location}

SERVICES REQUESTED
------------------
{services_str}

ADDITIONAL NOTES
----------------
{notes if notes else 'None'}

===================================================
Reply directly to this email or call the client to follow up.
        """.strip()

        send_mail(
            subject=f'New Quote Request from {name}',
            message=message,
            from_email='cipherdeveloperz@gmail.com',
            recipient_list=['cipherdeveloperz@gmail.com'],
            fail_silently=False,
        )

        # Auto-reply to client
        if email:
            send_mail(
                subject='Your Quote Request — Cipher Developers And Services',
                message=f"""
Hi {name},

Thank you for reaching out to Cipher Developers And Services.

We have received your quote request and will get back to you within 24 hours.

Your request summary:
{services_str}

Location: {location}

If you need immediate assistance, please call or WhatsApp us at:
+254 710 902 541

Best regards,
Vincent Gichuhi
Cipher Developers And Services
                """.strip(),
                from_email='cipherdeveloperz@gmail.com',
                recipient_list=[email],
                fail_silently=True,
            )

        return JsonResponse({'success': True})

    except Exception as e:
        return JsonResponse({'success': False, 'error': str(e)}, status=500)