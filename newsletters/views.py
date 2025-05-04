from django.http import JsonResponse
from .forms import SubscriberForm
from django.views.decorators.csrf import csrf_exempt
from rest_framework.decorators import api_view
import json

@csrf_exempt
@api_view(['POST'])
def subscribe(request):
    try:
        data = json.loads(request.body)  # Parse raw JSON
    except json.JSONDecodeError:
        return JsonResponse({'success': False, 'message': 'Invalid JSON.'}, status=400)

    form = SubscriberForm(data)  # Pass parsed JSON dict to the form
    if form.is_valid():
        form.save()
        return JsonResponse({'success': True, 'message': 'Thank you for subscribing!'})
    else:
        return JsonResponse({'success': False, 'errors': form.errors}, status=400)
