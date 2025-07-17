import requests


def download_large_file_from_google_drive(file_id, destination):
    url = "https://drive.google.com/uc?export=download"
    session = requests.Session()

    # Первый запрос для получения cookies с подтверждением
    response = session.get(url, params={'id': file_id}, stream=True)
    for key, value in response.cookies.items():
        if key.startswith('download_warning'):
            # Если есть предупреждение, добавляем confirm=1 в параметры
            params = {'id': file_id, 'confirm': 1}
            response = session.get(url, params=params, stream=True)
            break

    # Сохраняем файл
    with open(destination, "wb") as f:
        for chunk in response.iter_content(1024 * 1024):  # Загрузка по 1 МБ
            if chunk:
                f.write(chunk)

    print(f"Файл сохранён как {destination}")


# Пример использования
file_id = "1AbC123DeF456GhI"  # Замените на реальный ID файла
destination = "large_file.zip"
download_large_file_from_google_drive(file_id, destination)