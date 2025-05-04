from rest_framework.views import APIView
from django.http import JsonResponse
from feedback.froms import FeedbackForm

# Create your views here.
class FeedbackView(APIView):
    
    def post(self, request):
        try:
            data = request.data 
            form = FeedbackForm(data)
            # validate form 
            if form.is_valid():
                # save form data to model in database
                form.save()
                return JsonResponse({'success': True, 'message': 'Thank you for subscribing!'}, status=200)
            else:
                return JsonResponse({'success': False, 'errors': form.errors}, status=400)
        except:
            return JsonResponse({'success': False, 'message': 'Invalid JSON.'}, status=400)
        
        
