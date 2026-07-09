from django.db import models
from django.db.models import Q


class Repository(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField(blank=True)
    owner = models.CharField(max_length=100)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name


class CodeFileQuerySet(models.QuerySet):
    def critical(self):
        """
        Returns a queryset of critical files using optimized DB queries.
        """
        critical_names = [".env", "settings.py", "config.py", "security.py", "credentials.json"]
        
        # We construct Q objects to combine multiple ORM OR conditions
        return self.filter(
            Q(size__gt=1_000_000) |
            # We use name__in, and for file_type we do the same.
            # To handle case-insensitivity similarly to the previous Python loop, 
            # we could use __iregex or just simple __in if case matters less, 
            # but let's stick to __in for standard names.
            Q(name__in=critical_names) |
            Q(file_type__in=["config", "security"]) |
            # Equivalent to checking if description is empty
            Q(description__exact="") | Q(description__isnull=True)
        ).order_by('-added_at')


class CodeFileManager(models.Manager):
    def get_queryset(self):
        return CodeFileQuerySet(self.model, using=self._db)

    def critical(self):
        return self.get_queryset().critical()


class CodeFile(models.Model):
    repository = models.ForeignKey(
        Repository,
        on_delete=models.CASCADE,
        related_name="files"
    )
    name = models.CharField(max_length=100)
    path = models.CharField(max_length=255)
    file_type = models.CharField(max_length=50)
    language = models.CharField(max_length=50, blank=True)
    size = models.PositiveIntegerField()
    description = models.TextField(blank=True)
    added_at = models.DateTimeField(auto_now_add=True)

    objects = CodeFileManager()

    @property
    def is_critical(self):
        critical_names = [".env", "settings.py", "config.py", "security.py", "credentials.json"]

        return (
            self.size > 1_000_000
            or self.name.lower() in critical_names
            or self.file_type.lower() in ["config", "security"]
            or not self.description.strip()
        )

    def __str__(self):
        return self.name