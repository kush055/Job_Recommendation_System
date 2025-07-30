from django.contrib import admin
from accounts.models import Activity  #  Correct

@admin.register(Activity)
class ActivityAdmin(admin.ModelAdmin):
    list_display = ('user', 'action', 'timestamp')
    search_fields = ('user__username', 'action')
    list_filter = ('timestamp',)
