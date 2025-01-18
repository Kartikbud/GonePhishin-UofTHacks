from django.contrib import admin
from .models import CallAnalysis

@admin.register(CallAnalysis)
class CallAnalysisAdmin(admin.ModelAdmin):
    list_display = ('timestamp', 'text', 'is_scam', 'confidence')
    list_filter = ('is_scam', 'timestamp')
    search_fields = ('text',) 