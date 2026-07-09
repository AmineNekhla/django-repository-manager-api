import os
from rest_framework import serializers

def validate_file_extension(name):
    """
    Field-level validator to ensure a file name actually has an extension.
    This logic is extracted here so it can be reused across multiple serializers if needed.
    """
    ext = os.path.splitext(name)[1]
    if not ext:
        raise serializers.ValidationError("File name must have an extension.")
    return name
