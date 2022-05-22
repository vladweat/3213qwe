from django import forms

from .models import Proposal

class ProposalCreationForm(forms.Form):
    
    long_name = forms.CharField(label='Long name', max_length=200)
    short_name = forms.CharField(label='Short name', max_length=100)
    description = forms.CharField(label='Description', max_length=500)
    
    
    # class Meta:
    #     model = Proposal
    #     fields = ("creator", "long_name", "short_name", "description",)

    