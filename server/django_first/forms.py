from django import forms
from .models import PromptsModel

class AddPromptForm(forms.ModelForm):
    class Meta:
        model = PromptsModel
        fields = ['name', 'prompt', 'description']
        labels = {
            'name': 'Введите название промпта',
            'prompt': 'Введите промпт',
            'description': 'Введите краткое описание промпта',
        }
        widgets = {
            'name': forms.TextInput(attrs={'placeholder': 'Название промпта'}),
            'prompt': forms.Textarea(attrs={'placeholder': 'Ваш промпт'}),
            'description': forms.TextInput(attrs={'placeholder': 'Краткое описание промпта'}),
        }
