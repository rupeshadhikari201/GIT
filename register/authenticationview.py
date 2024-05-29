from rest_framework.views import APIView
from rest_framework.response import Response
from register.authenication import UserAuthenticationExample
from rest_framework.permissions import IsAuthenticated

class UserAutheniticationExampleView(APIView):
    
    authentication_classes = [UserAuthenticationExample]
    permission_classes = [IsAuthenticated]
    
    def get(self, request, format=None):
        
        context = {
            'msg': 'You are authenticated as : {}'.format(request.user.username)
        }
        
        return Response(context)