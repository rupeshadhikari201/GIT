from django.core.mail import EmailMessage
import os

class Util:
    @staticmethod
    def send_email(data):
        try:
            email = EmailMessage(
                subject=data['subject'],
                body=data['body'], 
                from_email=os.environ.get('SEND_FROM'), 
                to=[data['to_email']]
            )
            print("The subject is : ", email.subject)
            print("The body is : ", email.body)
            print("Email is send from : ", email.from_email),
            print("Email is send to : ", email.to)
            email.send()
            print("Email sent successfully!")
        except Exception as e:
            print(f"Error sending email: {e}")