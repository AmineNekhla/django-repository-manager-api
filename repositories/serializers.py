from rest_framework import serializers
from .models import Repository, CodeFile
from .validators import validate_file_extension


class CodeFileSerializer(serializers.ModelSerializer) :
    is_critical = serializers.ReadOnlyField()
    # Apply our reusable field-level validator
    name = serializers.CharField(validators=[validate_file_extension])

    class Meta:
        model = CodeFile
        fields = [
            "id",
            "repository",
            "name",
            "path",
            "file_type",
            "language",
            "size",
            "description",
            "added_at",
            "is_critical",
        ]

    def validate(self, data):
        """
        Object-level validation.
        This is where we validate data that requires looking at multiple fields at once.
        """
        name = data.get('name', '')
        file_type = data.get('file_type', '').lower()

        # If a user claims the file type is python, the extension MUST be .py
        if file_type == 'python' and not name.endswith('.py'):
            raise serializers.ValidationError({
                "name": "If file_type is 'python', the file name must end with '.py'."
            })
            
        return data

class RepositorySerializer(serializers.ModelSerializer):
    files = CodeFileSerializer(many=True, read_only=True)

    class Meta:
        model = Repository
        fields = [
            "id",
            "name",
            "description",
            "owner",
            "created_at",
            "files",
        ]