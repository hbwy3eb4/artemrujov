from django.shortcuts import render, redirect
from .models import MediaFile
from .forms import MediaFileForm

def media_archive(request):
    files = MediaFile.objects.order_by('-uploaded_at')
    if request.method == 'POST':
        form = MediaFileForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect('media_archive')
    else:
        form = MediaFileForm()
    return render(request, 'mediaarchive/archive.html', {'form': form, 'files': files}) 