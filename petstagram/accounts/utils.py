from django.template.loader import render_to_string
from mailjet_rest import Client
from django.conf import settings


def send_welcome_email(email, username):
    mailjet = Client(auth=(settings.MAILJET_API_KEY, settings.MAILJET_SECRET_KEY), version='v3.1')
    # Load the HTML content from the template
    html_content = render_to_string('accounts/email-greeting.html', {'username': username})
    data = {
        'Messages': [
            {
                "From": {
                    "Email": "zh.yordanova@students.softuni.bg",
                    "Name": "Your Name"
                },
                "To": [
                    {
                        "Email": email,
                        "Name": username
                    }
                ],
                "Subject": "My first Mailjet Email!",
                "TextPart": "Greetings from Mailjet!",
                "HTMLPart": html_content
            }
        ]
    }
    result = mailjet.send.create(data=data)
    # print(result.json())


