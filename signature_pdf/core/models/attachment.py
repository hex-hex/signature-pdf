from django.conf.urls.static import static
from django.db import models
from django.urls import reverse

from signature_pdf.core.utils import generate_slug


class Attachment(models.Model):
    slug = models.SlugField(default=generate_slug, unique=True, db_index=True)
    path = models.FileField()
    original_name = models.CharField(max_length=254)
    created_at = models.DateTimeField(auto_now_add=True)
    # active = models.BooleanField(default=True, db_index=True)
    # created_by = models.ForeignKey(Operator, models.SET_NULL, null=True)

    def __str__(self):
        return self.original_name

    @property
    def size(self):
        return self.path.size

    @property
    def download_url(self):
        return reverse('download-attachment', kwargs={'slug': self.slug})

    @property
    def thumbnail_url(self):
        ext = self.original_name.split('.')[-1].lower()
        if ext == 'pdf':
            return static('images/thumbnails/pdf.png')
        elif ext in ['jpg', 'jpeg', 'png', 'bmp', 'gif']:
            return self.download_url
        elif ext in ['doc', 'docx']:
            return static('images/thumbnails/doc.png')
        elif ext in ['xls', 'xlsx']:
            return static('images/thumbnails/xls.png')
        else:
            return static('images/thumbnails/unknown_file_type.png')
