import os
from django.core.exceptions import ValidationError
import magic


def validate_file(file, max_size_mb=5, allowed_extensions=None, allowed_content_types=None):
    # Validate file size
    if file.size > max_size_mb * 1024 * 1024:
        raise ValidationError(f"File size should not exceed {max_size_mb}MB.")
    elif file.size == 0:
        raise ValidationError(f"File should not be empty.")

    # Validate file extension
    if allowed_extensions:
        ext = os.path.splitext(file.name)[1].lower()
        if ext not in allowed_extensions:
            raise ValidationError(
                f"File extension '{ext}' is not allowed. Allowed extensions are: {', '.join(allowed_extensions)}")

    # Validate content type
    if allowed_content_types:
        mime = magic.Magic(mime=True)
        content_type = mime.from_buffer(file.read(1024))
        file.seek(0)

        if content_type not in allowed_content_types:
            raise ValidationError(
                f"File content type '{content_type}' is not allowed. Allowed types are: {', '.join(allowed_content_types)}")

    return True