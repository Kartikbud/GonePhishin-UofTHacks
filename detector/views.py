from django.shortcuts import render
from .models import CallAnalysis

def monitor_view(request):
    """View for the real-time monitoring page"""
    return render(request, 'detector/monitor.html')

def history_view(request):
    """View to see past call analyses"""
    analyses = CallAnalysis.objects.all().order_by('-timestamp')
    return render(request, 'detector/history.html', {'analyses': analyses}) 