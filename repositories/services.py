from .models import CodeFile, Repository
from .exceptions import DuplicateFileException

class CodeFileService:
    @staticmethod
    def create_code_file(validated_data):
        """
        Business logic for creating a CodeFile.
        """
        repo = validated_data.get('repository')
        path = validated_data.get('path')
        
        # BUSINESS RULE: A repository cannot have two files with the exact same path.
        if CodeFile.objects.filter(repository=repo, path=path).exists():
            raise DuplicateFileException()
            
        code_file = CodeFile.objects.create(**validated_data)
        return code_file
