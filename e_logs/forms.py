from django import forms
from .models import Bulletin, MorningTask, EveningTask, Asset

class BulletinForm(forms.ModelForm):
    class Meta:
        model = Bulletin
        fields = ("__all__")

class MorningTaskForm(forms.ModelForm):

    AUTHORS = [
        ('', 'Select a name'),
        ('Jeff', 'Jeff'),
        ('Roy', 'Roy'),
        ('Mark', 'Mark'),
        ('Fernand', 'Fernand')
    ]

    checked_by = forms.ChoiceField(choices=AUTHORS)

    class Meta:
        model = MorningTask
        fields = '__all__'
        widgets = {
            't_lits': forms.TimeInput(attrs={'class': 'tac', 'type': 'time'}),
            't_ciss': forms.TimeInput(attrs={'class': 'tac', 'type': 'time'}),
            't_cass': forms.TimeInput(attrs={'class': 'tac', 'type': 'time'}),
            't_cebu': forms.TimeInput(attrs={'class': 'tac', 'type': 'time'}),
            't_boas': forms.TimeInput(attrs={'class': 'tac', 'type': 'time'}),
            't_cwrge': forms.TimeInput(attrs={'class': 'tac', 'type': 'time'}),
            't_utbeb': forms.TimeInput(attrs={'class': 'tac', 'type': 'time'}),
            't_alicbu': forms.TimeInput(attrs={'class': 'tac', 'type': 'time'}),
            't_ceu': forms.TimeInput(attrs={'class': 'tac', 'type': 'time'}),
            't_cdl': forms.TimeInput(attrs={'class': 'tac', 'type': 'time'}),
            't_cvti': forms.TimeInput(attrs={'class': 'tac', 'type': 'time'}),
            't_cppc': forms.TimeInput(attrs={'class': 'tac', 'type': 'time'}),
            't_ccrgt': forms.TimeInput(attrs={'class': 'tac', 'type': 'time'}),

            'r_lits': forms.TextInput(attrs={'autocomplete': 'off'}),
            'r_ciss': forms.TextInput(attrs={'autocomplete': 'off'}),
            'r_cass': forms.TextInput(attrs={'autocomplete': 'off'}),
            'r_cebu': forms.TextInput(attrs={'autocomplete': 'off'}),
            'r_boas': forms.TextInput(attrs={'autocomplete': 'off'}),
            'r_cwrge': forms.TextInput(attrs={'autocomplete': 'off'}),
            'r_utbeb': forms.TextInput(attrs={'autocomplete': 'off'}),
            'r_alicbu': forms.TextInput(attrs={'autocomplete': 'off'}),
            'r_ceu': forms.TextInput(attrs={'autocomplete': 'off'}),
            'r_cdl': forms.TextInput(attrs={'autocomplete': 'off'}),
            'r_cvti': forms.TextInput(attrs={'autocomplete': 'off'}),
            'r_cppc': forms.TextInput(attrs={'autocomplete': 'off'}),
            'r_ccrgt': forms.TextInput(attrs={'autocomplete': 'off'}),


        }
        
class EveningTaskForm(forms.ModelForm):

    AUTHORS = [
        ('', 'Select a name'),
        ('Jeff', 'Jeff'),
        ('Roy', 'Roy'),
        ('Mark', 'Mark'),
        ('Fernand', 'Fernand')
    ]

    checked_by = forms.ChoiceField(choices=AUTHORS)

    class Meta: 
        model = EveningTask
        fields = '__all__'
        widgets = {
            't_dsob': forms.TimeInput(attrs={'class': 'tac', 'type': 'time'}),
            't_ceu': forms.TimeInput(attrs={'class': 'tac', 'type': 'time'}),
            't_cass': forms.TimeInput(attrs={'class': 'tac', 'type': 'time'}),
            't_uebu': forms.TimeInput(attrs={'class': 'tac', 'type': 'time'}),
            't_alicbu': forms.TimeInput(attrs={'class': 'tac', 'type': 'time'}),
            't_ciss': forms.TimeInput(attrs={'class': 'tac', 'type': 'time'}),
            't_cpss': forms.TimeInput(attrs={'class': 'tac', 'type': 'time'}),
            't_ccrgt': forms.TimeInput(attrs={'class': 'tac', 'type': 'time'}),
            't_cvti': forms.TimeInput(attrs={'class': 'tac', 'type': 'time'}),
            't_ltos': forms.TimeInput(attrs={'class': 'tac', 'type': 'time'}),
        }

class AssetForm(forms.ModelForm):

    SCHEDULE = [
        ('', 'Select schedule'),
        ('Daily', 'Daily'),
        ('Weekly', 'Weekly'),
        ('Monthly', 'Monthly'),
        ('Yearly', 'Yearly'),
        ('No Recurring', 'No Recurring')
    ]

    schedule = forms.ChoiceField(choices=SCHEDULE)

    class Meta:
        model = Asset
        fields = ['name', 'description', 'supplier', 'purchase_date', 'expiration', 'schedule']
        widgets = {
        'purchase_date': forms.DateInput(attrs={'type': 'date'}),
        'expiration': forms.DateInput(attrs={'type': 'date'}),
        }
        
