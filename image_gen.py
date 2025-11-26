import argparse
import base64
import os
from pathlib import Path

from dotenv import load_dotenv
from openai import OpenAI


def generate_image(
    prompt: str,
    output_path: Path,
    model: str = "gpt-image-1",
    size: str = "1024x1024",
) -> None:
    """
    Generate an image from text using OpenAI and save it to a file.
    """
    # Загружаем переменные окружения из .env (если файл есть)
    load_dotenv()

    if not os.getenv("OPENAI_API_KEY"):
        raise SystemExit("Не найден OPENAI_API_KEY. Укажите его в .env или переменных окружения.")

    client = OpenAI()

    result = client.images.generate(
        model=model,
        prompt=prompt,
        size=size,
        n=1,
    )

    image_base64 = result.data[0].b64_json
    image_bytes = base64.b64decode(image_base64)
    output_path.write_bytes(image_bytes)

    print(f"Изображение сохранено в: {output_path}")


def main() -> None:
    parser = argparse.ArgumentParser(
        description="Генерация изображений через OpenAI: текстовый промпт -> изображение"
    )
    parser.add_argument(
        "prompt",
        type=str,
        nargs="?",
        default="Фuturистичный город на закате в стиле цифровой иллюстрации",
        help="Текстовый промпт для генерации изображения "
        "(по умолчанию: футуристичный город на закате)",
    )
    parser.add_argument(
        "output_image",
        type=Path,
        nargs="?",
        default=Path("image.png"),
        help="Путь к выходному файлу с изображением (по умолчанию: image.png)",
    )
    parser.add_argument(
        "--model",
        type=str,
        default="gpt-image-1",
        help="Модель для генерации изображений (по умолчанию: gpt-image-1)",
    )
    parser.add_argument(
        "--size",
        type=str,
        default="1024x1024",
        help="Размер изображения, например 512x512, 1024x1024 (по умолчанию: 1024x1024)",
    )

    args = parser.parse_args()

    generate_image(
        prompt=args.prompt,
        output_path=args.output_image,
        model=args.model,
        size=args.size,
    )


if __name__ == "__main__":
    main()


