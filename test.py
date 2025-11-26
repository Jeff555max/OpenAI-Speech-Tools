from openai import OpenAI
import sys
import time

client = OpenAI(
    api_key="***REMOVED***",
    base_url="https://api.proxyapi.ru/openai/v1",
)

video = client.videos.create(
    model="sora-2",
    prompt="Видео стильной ночной сцены в неоновой стилистике: крутой антропоморфный кот в кожаной куртке и тёмных очках едет на мощном мотоцикле по мокрой городской улице. Вокруг ярко светятся неоновые вывески — розовые, синие, фиолетовые, бирюзовые, отражаясь в лужах и на хроме мотоцикла. Камера плавно облетает героя: крупные планы морды кота, блеск его очков, детализированная шерсть с неоновыми бликами, затем — динамичный ракурс сзади, когда он ускоряется по проспекту. В воздухе лёгкая дымка, усиливающая свечение неона. На заднем плане — футуристические небоскрёбы, неоновые контуры, светящиеся трассеры от огней. Мотоцикл оставляет позади световой шлейф. Атмосфера — синтвейв, киберпанк, ночной драйв. Высокая детализация, глубокие тени, яркие акценты, кинематографичная цветокоррекция с фиолетово-сине-розовой палитрой. Эффект лёгкого slow-motion, ощущение скорости и стиля",
)

print("Генерация видео началась:", video)

progress = getattr(video, "progress", 0)
bar_length = 30

while video.status in ("in_progress", "queued"):
    video = client.videos.retrieve(video.id)
    progress = getattr(video, "progress", 0)

    filled_length = int((progress / 100) * bar_length)
    bar = "=" * filled_length + "-" * (bar_length - filled_length)
    status_text = "В очереди" if video.status == "queued" else "Обработка"

    sys.stdout.write(f"\r{status_text}: [{bar}] {progress:.1f}%")
    sys.stdout.flush()
    time.sleep(2)

sys.stdout.write("\n")

if video.status == "failed":
    message = getattr(
        getattr(video, "error", None), "message", "Генерация видео не удалась"
    )
    print(message)
else:
    print("Генерация видео завершена:", video)
    print("Скачивание видео...")

    content = client.videos.download_content(video.id, variant="video")
    content.write_to_file("video.mp4")

    print("Файл video.mp4 сохранён")
