# {{cookiecutter.project_slug}}/scripts/create_modular_app.py
import os
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent.parent  # Корень проекта (myproject/)
TEMPLATES_DIR = BASE_DIR / "templates" / "modular_app"

def create_template_structure():
    """Создает полную структуру шаблона для новых приложений"""
    template_dir = TEMPLATES_DIR / "{{cookiecutter.app_name}}"
    
    # Основные файлы приложения
    files = {
        "__init__.py.jinja": "",
        "apps.py.jinja": """from django.apps import AppConfig

class {{cookiecutter.app_name|capitalize}}Config(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = "apps.{{cookiecutter.app_name}}"
    verbose_name = "{{app_description}}"
""",
        "urls.py.jinja": """from django.urls import path
from .views.web.example import {{cookiecutter.app_name|capitalize}}ExampleView

app_name = "{{cookiecutter.app_name}}"
urlpatterns = [
    path("", {{cookiecutter.app_name|capitalize}}ExampleView.as_view(), name="example"),
]
""",
        "admin.py.jinja": """from django.contrib import admin
from .models.example import {{cookiecutter.app_name|capitalize}}Example

admin.site.register({{cookiecutter.app_name|capitalize}}Example)
"""
    }

    # Поддиректории и их содержимое
    subdirs = {
        "models": {
            "__init__.py.jinja": "",
            "example.py.jinja": """from django.db import models
from core.models.base import TimeStampedModel

class {{cookiecutter.app_name|capitalize}}Example(TimeStampedModel):
    \"\"\"Пример модели для приложения {{cookiecutter.app_name}}.\"\"\"
    name = models.CharField(max_length=100)
    
    def __str__(self):
        return self.name
"""
        },
        "services": {
            "__init__.py.jinja": ""
        },
        "views": {
            "__init__.py.jinja": "",
            "web": {
                "__init__.py.jinja": "",
                "example.py.jinja": """from django.views import View
from django.shortcuts import render

class {{cookiecutter.app_name|capitalize}}ExampleView(View):
    \"\"\"Пример вьюхи для Web.\"\"\"
    def get(self, request):
        return render(request, "{{cookiecutter.app_name}}/example.html")
"""
            },
            "api": {
                "__init__.py.jinja": "",
                "example.py.jinja": """from django.http import JsonResponse
from django.views import View

class {{cookiecutter.app_name|capitalize}}ApiView(View):
    \"\"\"Пример API-вьюхи.\"\"\"
    def get(self, request):
        return JsonResponse({"message": "Hello from {{cookiecutter.app_name}} API!"})
"""
            }
        },
        "templates/{{cookiecutter.app_name}}": {
            "auth": {
                "login.html.jinja": """{% raw %}{% extends "base.html" %}

{% block content %}
<h1>Login for {{cookiecutter.app_name}}</h1>
{% endblock %}
{%- endraw %}
"""
            },
            "partials": {
                "__init__.py.jinja": ""
            }
        },
        "tests": {
            "__init__.py.jinja": "",
            "test_models.py.jinja": """from django.test import TestCase
from apps.{{cookiecutter.app_name}}.models.example import {{cookiecutter.app_name|capitalize}}Example

class {{cookiecutter.app_name|capitalize}}ModelTests(TestCase):
    def test_model_creation(self):
        obj = {{cookiecutter.app_name|capitalize}}Example.objects.create(name="Test")
        self.assertEqual(str(obj), "Test")
""",
            "test_views.py.jinja": """from django.test import TestCase
from django.urls import reverse

class {{cookiecutter.app_name|capitalize}}ViewTests(TestCase):
    def test_home_view(self):
        response = self.client.get(reverse("{{cookiecutter.app_name}}:example"))
        self.assertEqual(response.status_code, 200)
"""
        }
    }

    # Создаем основную директорию шаблона
    os.makedirs(template_dir, exist_ok=True)

    # Создаем основные файлы
    for filename, content in files.items():
        filepath = template_dir / filename
        os.makedirs(filepath.parent, exist_ok=True)
        with open(filepath, "w", encoding="utf-8") as f:
            f.write(content)

    # Рекурсивно создаем поддиректории и файлы
    def create_subdirs(base_path, structure):
        for name, content in structure.items():
            path = base_path / name
            if isinstance(content, dict):
                os.makedirs(path, exist_ok=True)
                create_subdirs(path, content)
            else:
                with open(path, "w", encoding="utf-8") as f:
                    f.write(content)

    create_subdirs(template_dir, subdirs)

    # Создаем cookiecutter.json
    cookiecutter_json = template_dir.parent / "cookiecutter.json"
    with open(cookiecutter_json, "w", encoding="utf-8") as f:
        f.write("""{
  "app_name": "myapp",
  "app_description": "Описание приложения"
}""")

    print(f"✅ Шаблон для приложений создан в {template_dir.parent}")

if __name__ == "__main__":
    create_template_structure()