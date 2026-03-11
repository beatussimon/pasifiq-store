from django import forms
from .models import Message

class MessageForm(forms.ModelForm):
    class Meta:
        model = Message
        fields = ('sender_name', 'sender_phone', 'sender_email', 'subject', 'content')
        widgets = {
            'content': forms.Textarea(attrs={'rows': 5, 'placeholder': 'Your message...'}),
            'sender_name': forms.TextInput(attrs={'placeholder': 'Your full name'}),
            'sender_phone': forms.TextInput(attrs={'placeholder': '+1 234 567 8900'}),
            'sender_email': forms.EmailInput(attrs={'placeholder': 'your@email.com'}),
            'subject': forms.TextInput(attrs={'placeholder': 'Subject (optional)'}),
        }
