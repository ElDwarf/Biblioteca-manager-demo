from django.forms import ModelForm

from .models import Loan


class LoanForm(ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['user'].widget.attrs.update('hidden', '1')

    class Meta:
        fields = ['member', 'book', 'user', 'due_date']
