# 📊 HH.ru Анализатор Вакансий

Современное веб-приложение для анализа вакансий с HeadHunter с использованием AI

![Python](https://img.shields.io/badge/Python-3.8+-blue.svg)
![Flask](https://img.shields.io/badge/Flask-3.0.0-green.svg)
![License](https://img.shields.io/badge/license-MIT-blue.svg)

## ✨ Возможности

- 🔍 **Поиск вакансий** - Автоматический сбор вакансий с HeadHunter API
- 🤖 **AI Анализ** - Интеллектуальный анализ вакансий с помощью Google Gemini
- 📈 **Визуализация** - Красивые графики топ-навыков
- 💼 **Подробный отчет** - Анализ хард-скиллов, задач и рекомендации
- 🎨 **Современный дизайн** - Адаптивный интерфейс с градиентами

## 🚀 Быстрый старт

### Требования

- Python 3.8+
- pip

### Установка

1. Клонируйте репозиторий:
```bash
git clone https://github.com/yourusername/webscrap.git
cd webscrap
```

2. Создайте виртуальное окружение:
```bash
python -m venv venv

# Windows
venv\Scripts\activate

# Linux/Mac
source venv/bin/activate
```

3. Установите зависимости:
```bash
pip install -r requirements.txt
```

4. Настройте API ключ Google Gemini:
```bash
# Создайте файл .env
echo "GOOGLE_API_KEY=your_api_key_here" > .env
```

> 💡 Получить API ключ можно на [Google AI Studio](https://makersuite.google.com/app/apikey)

5. Запустите приложение:
```bash
python app.py
```

6. Откройте в браузере:
```
http://localhost:5000
```

## 📖 Использование

1. Введите название профессии (например, "Python разработчик")
2. Нажмите "Анализировать"
3. Подождите 1-2 минуты
4. Получите подробный анализ:
   - AI-отчет с рекомендациями
   - График топ-10 навыков
   - Список проанализированных вакансий

## 🏗️ Структура проекта

```
webscrap/
├── app.py                 # Flask приложение (backend)
├── requirements.txt       # Зависимости Python
├── .gitignore            # Git ignore файл
├── README.md             # Документация
├── templates/
│   └── index.html        # Главная страница
└── static/
    ├── css/
    │   └── style.css     # Стили
    └── js/
        └── app.js        # JavaScript логика
```

## 🎨 Технологии

### Backend
- **Flask** - Веб-фреймворк
- **BeautifulSoup4** - Парсинг HTML
- **Requests** - HTTP запросы
- **Google Generative AI** - AI анализ

### Frontend
- **HTML5/CSS3** - Разметка и стили
- **JavaScript (ES6+)** - Логика
- **Chart.js** - Графики
- **Google Fonts (Inter)** - Шрифты

## 🔧 API Endpoints

### `POST /api/analyze`

Анализирует вакансии для указанной профессии.

**Request:**
```json
{
  "profession": "Python разработчик"
}
```

**Response:**
```json
{
  "vacancies": [...],
  "skills": [...],
  "ai_analysis": "...",
  "total_vacancies": 20
}
```

## 🌐 Деплой

### Heroku

1. Создайте файл `Procfile`:
```
web: gunicorn app:app
```

2. Деплой:
```bash
heroku create your-app-name
heroku config:set GOOGLE_API_KEY=your_api_key
git push heroku main
```

### Render / Railway / Vercel

Аналогично - используйте `gunicorn app:app` для запуска.

## ⚙️ Конфигурация

### Переменные окружения

- `GOOGLE_API_KEY` - API ключ Google Gemini (обязательно)
- `FLASK_ENV` - Окружение Flask (development/production)

### Настройки в коде

В `app.py` можно изменить:
- Количество анализируемых вакансий (по умолчанию: 20)
- Регион поиска (по умолчанию: Россия, area=113)
- Модель AI (по умолчанию: gemini-2.5-flash)

## 📝 Примеры запросов

- "Python разработчик"
- "Frontend developer"
- "Data Scientist"
- "DevOps инженер"
- "Product Manager"

## 🐛 Решение проблем

### Ошибка API ключа
- Проверьте, что `GOOGLE_API_KEY` установлен в `.env`
- Убедитесь, что ключ валидный

### Не находятся вакансии
- Попробуйте изменить формулировку запроса
- Проверьте подключение к интернету

### Ошибки при установке
```bash
# Обновите pip
pip install --upgrade pip

# Переустановите зависимости
pip install -r requirements.txt --force-reinstall
```

## 🤝 Вклад

Буду рад вашим Pull Request'ам!

1. Fork проекта
2. Создайте ветку (`git checkout -b feature/AmazingFeature`)
3. Commit изменения (`git commit -m 'Add some AmazingFeature'`)
4. Push в ветку (`git push origin feature/AmazingFeature`)
5. Откройте Pull Request

## 📄 Лицензия

MIT License - используйте свободно!

## 👨‍💻 Автор

Создано с ❤️ для анализа IT-вакансий

## 🙏 Благодарности

- [HeadHunter API](https://dev.hh.ru/)
- [Google Gemini AI](https://ai.google.dev/)
- [Flask](https://flask.palletsprojects.com/)
- [Chart.js](https://www.chartjs.org/)

---

⭐ Если проект помог, поставьте звезду!
