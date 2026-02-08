from django.core.exceptions import ValidationError
def validate_file_size(file):
    max_size = 10
    file_size_in_bytes = max_size * 1024 * 1024

    if file.size > file_size_in_bytes:
        raise ValidationError(
             f'File must be lower or equal than {max_size}!!'
        )