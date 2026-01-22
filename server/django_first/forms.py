from django import forms
from .models import PromptsModel, StrHistory, UserFeedbackMessage, UserFeedbackAdd, UserFeedbackReport

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

class Str2WordsForm(forms.ModelForm):
    class Meta:
        model = StrHistory

        fields = ['original_text']

        labels = {
            'original_text': 'Введите ваш текст'
        }

        widgets = {
            'original_text': forms.Textarea(
                attrs={
                    'placeholder': 'Введите ваш текст'
                }
            )
        }

class FeedbackAddForm(forms.ModelForm):
    class Meta:
        model = UserFeedbackAdd

class FeedbackMessageForm(forms.ModelForm):
    class Meta:
        model = UserFeedbackMessage

class FeedbackReportForm(forms.ModelForm):
    class Meta:
        model = UserFeedbackReport
