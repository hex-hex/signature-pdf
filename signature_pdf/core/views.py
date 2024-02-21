import logging
import os

import fitz
from django.core.files.storage import default_storage, DefaultStorage
from django.http import HttpRequest, JsonResponse, FileResponse, HttpResponseNotAllowed, HttpResponse
# HttpResponseForbidden,
from django.shortcuts import redirect
from django.templatetags.static import static
from djangorestframework_camel_case.render import CamelCaseJSONRenderer, CamelCaseBrowsableAPIRenderer
from rest_framework import serializers
from rest_framework.decorators import api_view, renderer_classes
# permission_classes
from rest_framework.response import Response

# from signature_pdf.core.auth.staff import IsOperator
from signature_pdf.core.models import Attachment
from signature_pdf.core.utils import upload_file_path

logger = logging.getLogger(__name__)


class AttachmentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Attachment
        fields = ['slug', 'original_name', 'download_url', 'thumbnail_url', 'size']


@api_view(['POST', ])
# @permission_classes([IsOperator, ])
def upload_attachment_view(request: HttpRequest):
    if request.method != 'POST':
        return HttpResponseNotAllowed(['POST'])
    try:
        file = request.FILES['file']
        path = upload_file_path(file.name)
        default_storage.save(path, file)
        attachment = Attachment(path=path,
                                original_name=file.name,
                                # created_by=request.user.operator
                                )
        attachment.save()
        return JsonResponse({'success': 'true', 'attachment': attachment.slug, 'name': file.name})
    except Exception as e:
        print(str(e))
        return JsonResponse({'success': 'false', 'msg': str(e)}, status=500)


@api_view(['GET', ])
# @permission_classes([IsOperator, ])
def thumbnail_attachment_view(request: HttpRequest, slug: str):
    if request.method != 'GET':
        return HttpResponseNotAllowed(['GET'])
    # if not hasattr(request.user, 'operator'):
    #     return HttpResponseForbidden()
    attachment = Attachment.objects.get(slug=slug)
    split_tup = os.path.splitext(attachment.path.name)
    match split_tup[1].lower():
        case '.pdf':
            if request.GET.get('deep', 'false') == 'true':
                return HttpResponse(deep_preview_pdf(attachment), content_type='image/png')
            return redirect(static('images/thumbnails/pdf.png'))
        case '.doc' | '.docx':
            return redirect(static('images/thumbnails/doc.png'))
        case '.xls' | '.xlsx':
            return redirect(static('images/thumbnails/xls.png'))
        case _:
            return redirect('download-attachment', slug=attachment.slug)


def deep_preview_pdf(attachment: Attachment):
    storage = DefaultStorage()
    with storage.open(attachment.path.name, 'rb') as f:
        pdf_data = f.read()
        pdf_file: fitz.Document = fitz.Document(stream=pdf_data, filetype='pdf')
        for page in pdf_file.pages():
            return page.get_pixmap().pil_tobytes(format='png', optimize=True)


@api_view(['GET', ])
# @permission_classes([IsOperator, ])
def download_attachment_view(request: HttpRequest, slug: str):
    if request.method != 'GET':
        return HttpResponseNotAllowed(['GET'])
    # if not hasattr(request.user, 'operator'):
    #     return HttpResponseForbidden()
    attachment = Attachment.objects.get(slug=slug)
    file_response = FileResponse(attachment.path)
    file_response['Content-Disposition'] = 'attachment; filename=' + attachment.original_name
    return file_response


@api_view(['GET', ])
# @permission_classes([IsOperator, ])
@renderer_classes([CamelCaseBrowsableAPIRenderer, CamelCaseJSONRenderer, ])
def attachment_type_view(request: HttpRequest, slug: str):
    if request.method != 'GET':
        return HttpResponseNotAllowed(['GET'])
    # if not hasattr(request.user, 'operator'):
    #     return HttpResponseForbidden()
    attachment = Attachment.objects.get(slug=slug)
    split_tup = os.path.splitext(attachment.path.name)
    match split_tup[1].lower():
        case '.pdf':
            response_data = {
                'type': 'pdf',
                'content_Type': 'application/pdf',
                'thumbnail_type': 'image/png'
            }
        case '.doc':
            response_data = {
                'type': 'document',
                'content_Type': 'application/msword',
                'thumbnail_type': 'image/png'
            }
        case '.docx':
            response_data = {
                'type': 'document',
                'content_type': 'application/vnd.openxmlformats-officedocument.wordprocessingml.document',
                'thumbnail_type': 'image/png'
            }
        case '.xls':
            response_data = {
                'type': 'spreadsheet',
                'content_type': 'application/vnd.ms-excel',
                'thumbnail_type': 'image/png'
            }
        case '.xlsx':
            response_data = {
                'type': 'spreadsheet',
                'content_type': 'application/vnd.openxmlformats-officedocument.spreadsheetml.sheet',
                'thumbnail_type': 'image/png'
            }
        case '.jpg' | '.jpeg':
            response_data = {
                'type': 'image',
                'content_type': 'image/jpeg',
                'thumbnail_type': 'image/jpeg'
            }
        case '.png':
            response_data = {
                'type': 'image',
                'content_type': 'image/png',
                'thumbnail_type': 'image/png'
            }
        case '.gif':
            response_data = {
                'type': 'image',
                'content_type': 'image/gif',
                'thumbnail_type': 'image/gif'
            }
        case '.bmp':
            response_data = {
                'type': 'image',
                'content_type': 'image/bmp',
                'thumbnail_type': 'image/bmp'
            }
        case _:
            response_data = {
                'type': 'unknown',
                'content_type': 'application/octet-stream',
                'thumbnail_type': 'application/octet-stream',
            }
    return Response(response_data)
