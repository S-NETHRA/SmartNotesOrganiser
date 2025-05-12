from django.shortcuts import render, redirect, get_object_or_404
from .models import Note
from .forms import NoteForm
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login, logout
import pytesseract
from PIL import Image
import speech_recognition as sr

@login_required
def home(request):
    query = request.GET.get('q')
    if query:
        notes = Note.objects.filter(user=request.user, title__icontains=query)
    else:
        notes = Note.objects.filter(user=request.user).order_by('-updated_at')
    return render(request, 'notes/home.html', {'notes': notes})

@login_required
def create_note(request):
    if request.method == 'POST':
        form = NoteForm(request.POST, request.FILES)
        if form.is_valid():
            note = form.save(commit=False)
            note.user = request.user
            if note.image:
                text = pytesseract.image_to_string(note.image)
                note.content += f"\n\n[OCR Text]:\n{text}"
            if note.voice_input:
                r = sr.Recognizer()
                with sr.AudioFile(note.voice_input.path) as source:
                    audio = r.record(source)
                    try:
                        text = r.recognize_google(audio)
                        note.content += f"\n\n[Voice Text]:\n{text}"
                    except:
                        note.content += "\n\n[Voice Text]: Unable to transcribe"
            note.save()
            return redirect('home')
    else:
        form = NoteForm()
    return render(request, 'notes/create.html', {'form': form})

@login_required
def edit_note(request, pk):
    note = get_object_or_404(Note, pk=pk)
    form = NoteForm(request.POST or None, request.FILES or None, instance=note)
    if form.is_valid():
        form.save()
        return redirect('home')
    return render(request, 'notes/edit.html', {'form': form})

@login_required
def delete_note(request, pk):
    note = get_object_or_404(Note, pk=pk)
    if request.method == 'POST':
        note.delete()
        return redirect('home')
    return render(request, 'notes/delete.html', {'note': note})

