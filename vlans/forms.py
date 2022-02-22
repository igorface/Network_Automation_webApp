from django import forms

class VlanForm(forms.Form):
    vlan_name = forms.CharField(label='Vlan name', max_length=50)
    vlan_name = forms.IntegerField(label='Vlan number')