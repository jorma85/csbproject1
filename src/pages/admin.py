from django.urls import path
from django.contrib import admin
from django.contrib.admin.views.decorators import staff_member_required
from django.utils.decorators import method_decorator
from django.template.response import TemplateResponse
from .models import Account, Message

@admin.register(Account)
class bankAdmin(admin.ModelAdmin):
    list_display=('user','balance')
    def get_urls(self):
        urls=super().get_urls()
        custom_urls=[
            path('bankadmin/', 
                 self.bankadmin_view, 
                 name='bankadmin')
        ]
        return custom_urls+urls
    #fix for Flaw #1 (broken access control), enforces the requirement to be logged in as a staff member to view this custom admin page
    #@method_decorator(staff_member_required)
    def bankadmin_view(self, request):
        accounts = Account.objects.select_related('user').all()
        context=dict(
            self.admin_site.each_context(request),
            accounts=accounts,
            title="glorping"
        )

        return TemplateResponse(request, "admin/thebankler.html", context)
#@admin.register(Message)
#class messageAdmin(admin.ModelAdmin):

