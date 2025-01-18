# Курсовая работа: Резервное копирование фотографий с VK на Яндекс.Диск

## Описание проекта
Этот проект представляет собой программу для резервного копирования фотографий с профиля пользователя ВКонтакте на Яндекс.Диск. Программа использует API ВКонтакте для получения фотографий и API Яндекс.Диска для их сохранения. Основные функции программы:

1. Получение фотографий с профиля ВКонтакте с помощью метода photos.get.
2. Сохранение фотографий максимального размера на Яндекс.Диск.
3. Именование фотографий по количеству лайков.
4. Сохранение информации о фотографиях в JSON-файл.
5. Логирование процесса выполнения программы.

## Функциональность
### 1. Получение фотографий с профиля ВКонтакте:

  - Используется метод photos.get для получения списка фотографий.
  - Выбираются фотографии максимального размера.

  ### 2. Сохранение фотографий на Яндекс.Диск:
  
  - Создаётся отдельная папка на Яндекс.Диске для загруженных фотографий.
  - Фотографии сохраняются с именами, соответствующими количеству лайков.
  
   ### 3. Сохранение информации в JSON-файл:

  - В файл info.json записывается информация о каждой фотографии (имя файла, размер, количество лайков).

### 4. Логирование:

- Программа выводит прогресс выполнения в консоль (логирование).

## Требования

Python 3.8 или выше.
- Установленные зависимости (см. requirements.txt).
- Токен доступа к API ВКонтакте.
- Токен доступа к API Яндекс.Диска.

## Установка и запуск
### 1. Клонируйте репозиторий:

    git clone https://github.com/ваш-username/ваш-репозиторий.git
    cd ваш-репозиторий
### 2. Установите зависимости:

    pip install -r requirements.txt
### 3. Настройте токены:

- В файл settings.ini в корне проекта и добавьте токеныи Ваш ID:

      [VK]
      token = Ваш_ВК_токен
      id = Ваш_ID_ВК
      
      [YD]
      token_yd = Ваш_токен_ЯндексДиска
### 4. Запустите программу:

    python main.py


## Пример использования
1. Программа запросит желаемое количество фотографий.
2. Укажите количество фотографий для сохранения.
3. Программа создаст папку на Яндекс.Диске и сохранит туда фотографии.
4. Информация о фотографиях будет сохранена в файл info.json
