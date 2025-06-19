from django.db import models

class MediaFile(models.Model):
    file = models.FileField(upload_to='uploads/%Y/%m/')
    title = models.CharField(max_length=255, blank=True)
    uploaded_at = models.DateTimeField(auto_now_add=True)
    description = models.TextField(blank=True)
    # Можно добавить связь с членом семьи, если нужно

    def __str__(self):
        return self.title or self.file.name 