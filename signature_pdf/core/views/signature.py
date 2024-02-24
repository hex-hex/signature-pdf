import base64

from django.core.files.storage import default_storage
from rest_framework.decorators import api_view
from rest_framework.request import Request
from rest_framework.response import Response

from signature_pdf.core.models import Attachment
from signature_pdf.core.utils import upload_file_path


@api_view(['POST', ])
def upload_signature_view(request: Request):
    png_base64 = request.data['img']
    signature_data = png_base64.split(',')[1]
    signature_decoded = base64.b64decode(signature_data)
    path = upload_file_path('png')
    default_storage.save(path, signature_decoded)
    attachment = Attachment(path=path, original_name='signature.png')
    attachment.save()
    return Response({'success': 'true', 'attachment': attachment.slug, 'name': 'signature.png'})
