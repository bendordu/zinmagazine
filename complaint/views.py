from django.shortcuts import render
from django.http import JsonResponse
from django.contrib.auth.decorators import login_required
from django.views.decorators.http import require_POST
from likes.decorators import ajax_required


@ajax_required
@login_required
@require_POST
def complaint(request):
    model = request.POST.get('complaint')
    model(model=model)
    complaint_obj = complaint.objects.get(id=request.POST.get('id'))
    return JsonResponse({'status':'ok'})
