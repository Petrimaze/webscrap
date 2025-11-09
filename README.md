# 📊 HH.ru Анализатор Вакансий - MVP

**Простое веб-приложение для анализа вакансий с HeadHunter с помощью AI**

Заходишь, вводишь профессию → получаешь анализ вакансий!

![Python](https://img.shields.io/badge/Python-3.8+-blue.svg)
![Flask](https://img.shields.io/badge/Flask-3.0.0-green.svg)
![License](https://img.shields.io/badge/license-MIT-blue.svg)

## 🚀 Быстрый деплой (3 минуты!)

### Вариант 1: Render (Рекомендуется - бесплатно!)

1. Зарегистрируйся на [Render.com](https://render.com)
2. Нажми "New +" → "Web Service"
3. Подключи свой GitHub репозиторий
4. Render автоматически определит настройки из `render.yaml`
5. Добавь переменную окружения:
   - Ключ: `GOOGLE_API_KEY`
   - Значение: твой ключ от Google Gemini ([получить тут](https://makersuite.google.com/app/apikey))
6. Нажми "Create Web Service"
7. Готово! Через 2-3 минуты твой сайт будет доступен

### Вариант 2: Railway

1. Зарегистрируйся на [Railway.app](https://railway.app)
2. Нажми "New Project" → "Deploy from GitHub repo"
3. Выбери свой репозиторий
4. Добавь переменную `GOOGLE_API_KEY`
5. Deploy! Готово за пару минут

### Вариант 3: Локально (для разработки)

```bash
# Клонируй репо
git clone https://github.com/yourusername/webscrap.git
cd webscrap

# Создай виртуальное окружение
python -m venv venv
source venv/bin/activate  # На Windows: venv\Scripts\activate

# Установи зависимости
pip install -r requirements.txt

# Создай .env файл
echo "GOOGLE_API_KEY=твой_ключ_здесь" > .env

# Запусти
python app.py
```

Открой http://localhost:5000

## ✨ Как пользоваться

1. **Открой сайт**
2. **Введи профессию** (например: "Python разработчик", "Frontend developer", "Data Scientist")
3. **Жми "Анализировать"**
4. **Жди 1-2 минуты** пока соберутся данные
5. **Получи результат:**
   - 🤖 AI-анализ с рекомендациями
   - 📊 График топ-10 навыков
   - 📋 Список вакансий

## 🎯 Что внутри

- **Flask** - простой веб-сервер
- **HH.ru API** - реальные вакансии
- **Google Gemini AI** - умный анализ (модель: gemini-2.5-flash-lite)
- **Chart.js** - красивые графики
- **Bootstrap стили** - современный дизайн

## 📁 Структура

```
webscrap/
├── app.py              # 🔧 Основной код (Flask + логика)
├── templates/
│   └── index.html      # 🎨 Главная страница
├── static/
│   ├── css/style.css   # 💅 Стили
│   └── js/app.js       # ⚡ JavaScript
├── requirements.txt    # 📦 Зависимости Python
├── render.yaml         # ☁️ Конфиг для Render
├── Procfile           # 🚀 Для Heroku/Railway
└── README.md          # 📖 Эта инструкция
```

## 🔑 Получить API ключ Google Gemini

1. Иди на https://makersuite.google.com/app/apikey
2. Войди через Google аккаунт
3. Нажми "Create API Key"
4. Скопируй ключ
5. Добавь в переменные окружения на Render/Railway или в `.env` файл локально

**Важно:** API ключ **БЕСПЛАТНЫЙ** для личного использования!

## 🐛 Проблемы?

### "Вакансии не найдены"
- Попробуй другую формулировку профессии
- Используй русский язык: "Python разработчик" вместо "Python developer"

### "API Error"
- Проверь, что `GOOGLE_API_KEY` установлен правильно
- Убедись что ключ валидный

### Долго грузится
- Это нормально! Собираем и анализируем ~20 вакансий
- Обычно занимает 1-2 минуты

## 🎓 Для преподавателя

Это MVP (Minimum Viable Product) - минимально работающий продукт:

✅ **Работает из коробки** - просто задеплой и пользуйся
✅ **Реальные данные** - интеграция с HH.ru API
✅ **AI анализ** - использует Google Gemini
✅ **Визуализация** - графики навыков
✅ **Современный UI** - адаптивный дизайн
✅ **Бесплатный хостинг** - Render/Railway free tier

## 📝 Примеры запросов

```
Python разработчик
Frontend developer
Data Scientist
DevOps инженер
QA engineer
Product Manager
```

## 🔧 Технические детали

### API Endpoint

**POST** `/api/analyze`

Request:
```json
{
  "profession": "Python разработчик"
}
```

Response:
```json
{
  "vacancies": [...],
  "skills": [...],
  "ai_analysis": "...",
  "total_vacancies": 20
}
```

### Логика работы

1. Ищем вакансии на HH.ru по ключевому слову
2. Берем каждую 10-ую вакансию (максимум 20)
3. Парсим описание и навыки
4. Считаем топ-10 навыков
5. Отправляем все в Gemini AI для анализа
6. Показываем результат пользователю

## 🚀 Что можно улучшить

- [ ] Кэширование результатов
- [ ] Фильтры по городам/зарплате
- [ ] Экспорт в PDF
- [ ] Сравнение нескольких профессий
- [ ] История поисков
- [ ] Регистрация пользователей

## 📄 Лицензия

MIT License - используй свободно!

## 👨‍💻 Автор

Сделано с ❤️ для анализа IT-вакансий

---

⭐ **Нравится проект? Поставь звезду на GitHub!**

🔗 **Задеплоил?** Скинь ссылку, посмотрим что получилось!
