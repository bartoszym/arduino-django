from django.contrib import messages
from django.utils.translation import gettext_lazy as _

def display_message(status, request):
    if status == -1:
        messages.add_message(request, messages.ERROR, _('Arduino is not working, check if it\'s turned on!'))
    if status == -2:
        messages.add_message(request, messages.ERROR, _('Compoments are not correctly connected!'))
        
    return