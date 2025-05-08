from django.shortcuts import render

# Create your views here.

from .models import Note

def home(request):
    notes = Note.objects.all().order_by('-updated_at')
    return render(request, 'notes/home.html', {'notes': notes})
