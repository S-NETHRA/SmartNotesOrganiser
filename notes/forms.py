from django import forms
from .models import Note

class NoteForm(forms.ModelForm):
    class Meta:
        model = Note
        fields = ['title', 'content', 'category', 'tags', 'reminder_time', 'image', 'voice_input']
