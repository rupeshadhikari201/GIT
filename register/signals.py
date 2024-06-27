from django.contrib.auth.signals import user_logged_in, user_logged_out, user_login_failed
from django.db.models.signals import post_save
from register.models import User
from django.dispatch import receiver
import logging
logger = logging.getLogger(__name__)

logger.info("Signals module loaded")

# define a receiver function
@receiver(user_logged_in,sender=User)
def login_sucess_receiver_function(sender, request, user, **kwargs):
    '''
    Here sender and **kwargs are mandatory
    '''
    print("Signal handler called")
    print("User Logged in Sucesssfull! ")
    print("sender is : ", sender )
    print("request is : ", request )
    print("user is : ", user )
    print(f'kwargs is : {kwargs}')
    
    
@receiver(user_logged_out,sender=User)
def logout_sucess_receiver_function(sender, request, user, **kwargs):
    '''
    Here sender and **kwargs are mandatory
    '''
    print("Signal handler called")
    print("User Logged in Sucesssfull! ")
    print("sender is : ", sender )
    print("request is : ", request )
    print("user is : ", user )
    print(f'kwargs is : {kwargs}')

@receiver(user_login_failed, sender=User)
def login_failed_receiver_function(sender, credentials, request, **kwargs):
    print("Signal handler called")
    print("User Logged in Sucesssfull! ")
    print("sender is : ", sender )
    print("request is : ", request )
    print("credentials is : ", credentials )
    print(f'kwargs is : {kwargs}')
    
    
# Now we need to connect the the receiver function to a signal. 
# For this there are two method i) Manual Route Connect ii) 
# i. Manual Route Connect
# ii. using  reciever() function
# user_logged_in.connect(login_sucess_receiver_function, sender=User)