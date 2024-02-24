from django.urls import path

from signature_pdf.core.views.attachment import download_attachment_view
from signature_pdf.core.views.signature import upload_signature_view

urlpatterns = [
    path('signature/', upload_signature_view, name='signature'),
    path('attachment/download/<str:slug>/', download_attachment_view, name='download-attachment'),
]
