from django import forms
from .models import Bulletin, MorningTask, EveningTask


class BulletinForm(forms.ModelForm):
    class Meta:
        model = Bulletin
        fields = ("__all__")

class TimeInput(forms.TimeInput):
    input_type = "time"


class MorningTaskForm(forms.ModelForm):

    class Meta:
        model = MorningTask
        fields = '__all__'

        widget = {
            't_ciss': forms.TextInput(attrs={})
        }

        # def __init__(self, *args, **kwargs):
        #     super().__init__(*args, **kwargs)
        #     self.fields["t_lits"].widget = TimeInput()
            
class EveningTaskForm(forms.ModelForm):

    class Meta: 
        model = EveningTask
        fields = '__all__'

    