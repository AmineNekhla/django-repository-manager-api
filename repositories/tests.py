from rest_framework.test import APITestCase
from rest_framework import status
from .models import Repository, CodeFile

class RepositoryAPITestCase(APITestCase):
    def setUp(self):
        self.repo_data = {"name": "Test Repo", "owner": "Alice", "description": "A test repo"}
        
    def test_create_repository(self):
        response = self.client.post("/api/repositories/", self.repo_data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Repository.objects.count(), 1)
        self.assertEqual(Repository.objects.get().name, "Test Repo")

    def test_list_repositories(self):
        Repository.objects.create(**self.repo_data)
        response = self.client.get("/api/repositories/")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        # Because pagination is active, results are in response.data['results']
        self.assertEqual(len(response.data['results']), 1)

    def test_retrieve_repository(self):
        repo = Repository.objects.create(**self.repo_data)
        response = self.client.get(f"/api/repositories/{repo.id}/")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['name'], "Test Repo")


class CodeFileAPITestCase(APITestCase):
    def setUp(self):
        self.repo = Repository.objects.create(name="App", owner="Bob")
        self.file_data = {
            "repository": self.repo.id,
            "name": "main.py",
            "path": "/src/main",
            "file_type": "python",
            "language": "Python",
            "size": 1024,
            "description": "Main entry point"
        }

    def test_create_file(self):
        response = self.client.post("/api/files/", self.file_data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(CodeFile.objects.count(), 1)

    def test_list_files(self):
        CodeFile.objects.create(repository=self.repo, name="main.py", path="/src", file_type="python", size=100)
        response = self.client.get("/api/files/")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data['results']), 1)

    def test_retrieve_file(self):
        cf = CodeFile.objects.create(repository=self.repo, name="main.py", path="/src", file_type="python", size=100)
        response = self.client.get(f"/api/files/{cf.id}/")
        self.assertEqual(response.status_code, status.HTTP_200_OK)


class SearchAPITestCase(APITestCase):
    def setUp(self):
        self.repo = Repository.objects.create(name="App", owner="Bob")
        CodeFile.objects.create(repository=self.repo, name="script.py", path="/script", file_type="python", language="Python", size=100, description="hi")
        CodeFile.objects.create(repository=self.repo, name="style.css", path="/style", file_type="css", language="CSS", size=200, description="hi")

    def test_search_by_name(self):
        response = self.client.get("/api/files/?search=script")
        self.assertEqual(len(response.data['results']), 1)
        self.assertEqual(response.data['results'][0]['name'], "script.py")

    def test_search_by_language(self):
        response = self.client.get("/api/files/?search=CSS")
        self.assertEqual(len(response.data['results']), 1)
        self.assertEqual(response.data['results'][0]['name'], "style.css")

    def test_search_by_file_type(self):
        response = self.client.get("/api/files/?search=python")
        self.assertEqual(len(response.data['results']), 1)
        self.assertEqual(response.data['results'][0]['name'], "script.py")


class CriticalFilesAPITestCase(APITestCase):
    def setUp(self):
        self.repo = Repository.objects.create(name="App", owner="Bob")
        # 1. .env (critical due to name)
        CodeFile.objects.create(repository=self.repo, name=".env", path="/env", file_type="env", size=10)
        # 2. settings.py (critical due to name)
        CodeFile.objects.create(repository=self.repo, name="settings.py", path="/settings", file_type="python", size=100)
        # 3. config file type (critical due to file_type)
        CodeFile.objects.create(repository=self.repo, name="conf.yaml", path="/conf", file_type="config", size=100)
        # 4. missing description (critical due to missing desc)
        CodeFile.objects.create(repository=self.repo, name="unknown.txt", path="/unk", file_type="text", size=100, description="")
        # 5. normal documented file (NOT critical)
        CodeFile.objects.create(repository=self.repo, name="README.md", path="/readme", file_type="markdown", size=100, description="Read me file")

    def test_critical_endpoint_returns_only_critical_files(self):
        response = self.client.get("/api/files/critical/")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        results = response.data['results'] if 'results' in response.data else response.data
        
        # 4 critical files, 1 normal file. Should return exactly 4.
        self.assertEqual(len(results), 4)
        
        names = [f['name'] for f in results]
        self.assertNotIn("README.md", names)
        self.assertIn(".env", names)
        self.assertIn("settings.py", names)
        self.assertIn("conf.yaml", names)
        self.assertIn("unknown.txt", names)


class ValidationAPITestCase(APITestCase):
    def setUp(self):
        self.repo = Repository.objects.create(name="App", owner="Bob")
        self.base_data = {
            "repository": self.repo.id,
            "name": "main.py",
            "path": "/src/main",
            "file_type": "python",
            "language": "Python",
            "size": 1024,
            "description": "Main file"
        }

    def test_duplicate_path_returns_409(self):
        # First request succeeds
        self.client.post("/api/files/", self.base_data)
        # Second request with identical path for the same repository
        response = self.client.post("/api/files/", self.base_data)
        self.assertEqual(response.status_code, status.HTTP_409_CONFLICT)
        self.assertEqual(response.data['detail'], 'A file with this path already exists in the repository.')

    def test_negative_size_rejected(self):
        bad_data = self.base_data.copy()
        bad_data['size'] = -50
        response = self.client.post("/api/files/", bad_data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        # DRF IntegerField(min_value=0) triggers this error automatically for PositiveIntegerField
        self.assertIn('size', response.data)

    def test_missing_required_fields(self):
        response = self.client.post("/api/files/", {})
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn('repository', response.data)
        self.assertIn('name', response.data)
