# {{cookiecutter.project_slug}}/scripts/create_modular_app.py
import os
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent  # Корень проекта (myproject/)
APPS_DIR = BASE_DIR / "apps"  # Путь к apps/

# Шаблоны для файлов
APP_CONFIG_TEMPLATE = """from django.apps import AppConfig

class {app_name_camel}Config(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = "apps.{app_name}"
"""

URLS_TEMPLATE = """from django.urls import path
from .views.web import home  # Example: import view

app_name = "{app_name}"
urlpatterns = [
    path("", home, name="home"),
]
"""

ADMIN_TEMPLATE = """from django.contrib import admin

# Register your models here
"""

def create_app(app_name: str):
    """Создаёт модульное приложение в apps/"""
    app_dir = APPS_DIR / app_name
    os.makedirs(app_dir, exist_ok=True)
    
    # 1. Обязательные файлы
    (app_dir / "__init__.py").write_text("")
    (app_dir / "apps.py").write_text(
        APP_CONFIG_TEMPLATE.format(
            app_name_camel=app_name.capitalize(),
            app_name=app_name
        )
    )
    (app_dir / "urls.py").write_text(
        URLS_TEMPLATE.format(app_name=app_name)
    )
    (app_dir / "admin.py").write_text(ADMIN_TEMPLATE)
    
    # 2. Поддиректории
    subdirs = [
        "models/__init__.py",
        "services/__init__.py",
        "views/__init__.py",
        "views/web/__init__.py",
        "views/web/home.py",  # Пример файла с вьюхой
        "views/api/__init__.py",
        "forms/__init__.py",
        f"templates/{app_name}/auth/login.html",  # Пример шаблона
        f"templates/{app_name}/partials/__init__.py",
        "tests/__init__.py",
        "tests/test_models/__init__.py",  # Пример: тесты моделей
        "tests/test_views/__init__.py",   # Тесты вьюх
    ]
    
    for file_path in subdirs:
        full_path = app_dir / file_path
        os.makedirs(full_path.parent, exist_ok=True)
        if not full_path.exists():
            if file_path.endswith(".html"):
                full_path.write_text(f"{{% extends 'base.html' %}}\n\n{{% block content %}}\n{{% endblock %}}")
            else:
                full_path.write_text("")
    
    print(f"✅ Приложение {app_name} создано в {app_dir}")

if __name__ == "__main__":
    for app in ["users", "core"]:
        create_app(app)