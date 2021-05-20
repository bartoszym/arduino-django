from django import forms
from django.utils.translation import gettext_lazy as _

class MonthForm(forms.Form):
    month_choices = (
        (1,_('January')),
        (2,_('February')),
        (3,_('March')),
        (4,_('April')),
        (5,_('May')),
        (6,_('June')),
        (7,_('July')),
        (8,_('August')),
        (9,_('September')),
        (10,_('October')),
        (11,_('November')),
        (12,_('December')),
        )
    month = forms.ChoiceField(label=_('Choose month'), choices=month_choices)
    