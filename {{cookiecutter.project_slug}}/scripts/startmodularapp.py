import os
from cookiecutter.main import cookiecutter
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent
TEMPLATE_DIR = BASE_DIR / "templates" / "modular_app"

def create_app():
    """Генерирует приложение из шаблона."""
    app_name = input("Введите название приложения (например, payments): ").strip()
    app_description = input("Описание приложения: ").strip()
    print(f"Создаю приложение {app_name}...")
    print(f"BASE_DIR: {BASE_DIR}")
    print(f"TEMPLATE_DIR: {TEMPLATE_DIR}")
    
    cookiecutter(
        str(TEMPLATE_DIR),
        extra_context={
            "app_name": app_name,
            "app_description": app_description,
        },
        output_dir=str(BASE_DIR / "apps"),
        no_input=True,
        overwrite_if_exists=False
    )
    print(f"✅ Приложение {app_name} создано в apps/")

if __name__ == "__main__":
    create_app()