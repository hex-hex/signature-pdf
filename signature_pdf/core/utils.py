import datetime
import os
import uuid

import ulid


def generate_slug():
    return ulid.new()


def upload_file_path(file_extension: str):
    date_now = datetime.datetime.now()
    uuid_name = str(uuid.uuid5(uuid.NAMESPACE_DNS, str(date_now)))
    file_extension = file_extension.lower().replace('jpg', 'jpeg')
    return f'attachments/{uuid_name}-{date_now.isoformat()}{file_extension}'
