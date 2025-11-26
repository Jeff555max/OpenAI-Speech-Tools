# Импорт стандартных и сторонних библиотек
import argparse
import os
from pathlib import Path
from dotenv import load_dotenv
from openai import OpenAI


def text_to_speech(
    text: str,
    output_path: Path,
    model: str = "gpt-4o-mini-tts",
    voice: str = "nova",
) -> None:
    """
    Синтезирует речь из текста с помощью OpenAI и сохраняет аудио в файл.
    """
    # Загружаем переменные окружения из .env (если файл есть)
    load_dotenv()

    # Проверяем наличие API-ключа
    if not os.getenv("OPENAI_API_KEY"):
        raise SystemExit("Не найден OPENAI_API_KEY. Укажите его в .env или переменных окружения.")

    client = OpenAI()

    # Синтез речи и сохранение результата в файл
    with client.audio.speech.with_streaming_response.create(
        model=model,
        voice=voice,
        input=text,
    ) as response:
        response.stream_to_file(str(output_path))

    print(f"Аудио сохранено в: {output_path}")


def main() -> None:
    parser = argparse.ArgumentParser(
        description="TTS (text-to-speech) с помощью OpenAI: текст -> аудиофайл"
    )
    parser.add_argument(
        "text",
        type=str,
        nargs="?",
        help="Текст для озвучивания (если не указан — будет запрошен интерактивно)",
    )
    parser.add_argument(
        "output_audio",
        type=Path,
        nargs="?",
        default=Path("speech.mp3"),
        help="Путь к выходному аудиофайлу (по умолчанию: speech.mp3)",
    )
    parser.add_argument(
        "--model",
        type=str,
        default="gpt-4o-mini-tts",
        help="Модель для синтеза речи (по умолчанию: gpt-4o-mini-tts)",
    )
    parser.add_argument(
        "--voice",
        type=str,
        default="nova",
        help="Голос для синтеза (по умолчанию: nova)",
    )

    args = parser.parse_args()

    # Если текст не передан через аргументы, спросить у пользователя
    if not args.text:
        args.text = input("Введите текст для озвучивания: ").strip()
        if not args.text:
            print("Текст не введён. Завершение работы.")
            return

    # Запуск синтеза речи
    text_to_speech(
        text=args.text,
        output_path=args.output_audio,
        model=args.model,
        voice=args.voice,
    )


if __name__ == "__main__":
    main()


