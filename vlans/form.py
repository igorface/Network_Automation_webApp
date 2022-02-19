from django import forms

class VlanForm(forms.Form):
    Vlan_name = forms.CharField(label='Vlan name', max_length=100)