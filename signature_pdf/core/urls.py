from django.urls import path

from signature_pdf.core.views.signature import upload_signature_view

urlpatterns = [
    path('signature/', upload_signature_view, name='signature')
]
