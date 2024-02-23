import base64

from rest_framework.decorators import api_view
from rest_framework.request import Request
from rest_framework.response import Response


@api_view(['POST', ])
def upload_signature_view(request: Request):
    png_base64 = request.data['img']
    signature_data = png_base64.split(',')[1]
    signature_decoded = base64.b64decode(signature_data)

    with open("imageToSave.png", "wb") as fh:
        fh.write(signature_decoded)

    return Response({'success': 'true'}, status=200)
