# 🚀 Быстрый старт - 3 минуты до деплоя!

## Шаг 1: Получи API ключ (30 секунд)

1. Открой https://makersuite.google.com/app/apikey
2. Войди через Google
3. Нажми "Create API Key"
4. Скопируй ключ

**ВАЖНО:** Это бесплатно!

## Шаг 2: Деплой на Render (2 минуты)

### Вариант A: Через интерфейс Render

1. Открой https://render.com и зарегистрируйся
2. Нажми **"New +"** → **"Web Service"**
3. Подключи свой GitHub репозиторий
4. Render автоматически всё настроит (есть `render.yaml`)
5. Добавь переменную окружения:
   ```
   GOOGLE_API_KEY = твой_ключ_здесь
   ```
6. Нажми **"Create Web Service"**
7. ✅ **ГОТОВО!** Через 2-3 минуты сайт будет работать

### Вариант B: Railway (еще проще!)

1. Открой https://railway.app
2. Нажми **"Start a New Project"**
3. Выбери **"Deploy from GitHub repo"**
4. Выбери свой репозиторий
5. Добавь переменную `GOOGLE_API_KEY`
6. ✅ **ГОТОВО!** Railway сам всё настроит

## Шаг 3: Тестируй

1. Открой свой сайт (ссылка будет в Render/Railway)
2. Введи профессию: `Python разработчик`
3. Жми "Анализировать"
4. Жди 1-2 минуты
5. 🎉 **Получи результаты!**

---

## Локальный запуск (если нужно)

```bash
# 1. Клонируй
git clone https://github.com/твой-username/webscrap.git
cd webscrap

# 2. Установи зависимости
pip install -r requirements.txt

# 3. Создай .env
echo "GOOGLE_API_KEY=твой_ключ" > .env

# 4. Запусти
python app.py

# 5. Открой http://localhost:5000
```

---

## Проблемы?

### Render показывает ошибку
- Проверь что `GOOGLE_API_KEY` добавлен в Environment Variables
- Проверь логи: Dashboard → Logs

### Сайт долго грузит
- Первый запуск может занять ~5 минут (Render загружает всё)
- Render free tier "засыпает" после 15 минут бездействия
- Первый запрос после "сна" будет медленным (~30 сек)

### API не работает
- Убедись что ключ Google Gemini валидный
- Проверь что не превышен лимит бесплатного использования

---

## Полезные ссылки

- 🔑 [Получить Google Gemini API Key](https://makersuite.google.com/app/apikey)
- ☁️ [Render.com](https://render.com)
- 🚂 [Railway.app](https://railway.app)
- 📖 [Полная документация](README.md)

---

⭐ Все работает? Поставь звезду проекту!
