from django.urls import path

from signature_pdf.web.views import DemoSignatureView

urlpatterns = [
    path('demo/', DemoSignatureView.as_view(), name='demo-signature')
]
