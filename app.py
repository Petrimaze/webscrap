from flask import Flask, render_template, request, jsonify
from flask_cors import CORS
import requests
from bs4 import BeautifulSoup
import time
import google.generativeai as genai
import os
import pandas as pd

app = Flask(__name__)
CORS(app)

# Configuration
GOOGLE_API_KEY = os.environ.get('GOOGLE_API_KEY', 'AIzaSyC71NkOu9mIlcRCX6d_WWX9jwl1PwMFMZk')
genai.configure(api_key=GOOGLE_API_KEY)
model = genai.GenerativeModel('gemini-2.5-flash')

@app.route('/')
def index():
    """Render the main page"""
    return render_template('index.html')

@app.route('/api/analyze', methods=['POST'])
def analyze_vacancies():
    """
    Analyze vacancies - YOUR ORIGINAL CODE wrapped in Flask!
    """
    try:
        data = request.json
        PROFESSION_NAME = data.get('profession', '').strip()

        if not PROFESSION_NAME:
            return jsonify({'error': 'Название профессии не указано'}), 400

        # Collect vacancy_ids from 5 pages (like you had before this code)
        url = 'https://api.hh.ru/vacancies'
        vacancy_ids = []

        for page in range(5):
            params = {
                'text': PROFESSION_NAME,
                'area': 113,
                'per_page': 100,
                'page': page
            }
            response = requests.get(url, params=params, timeout=10)
            if response.status_code == 200:
                search_data = response.json()
                page_vacancy_ids = [item['id'] for item in search_data.get('items', [])]
                vacancy_ids.extend(page_vacancy_ids)
            time.sleep(0.3)

        if not vacancy_ids:
            return jsonify({'error': 'Вакансии не найдены. Попробуйте изменить запрос.'}), 404

        # ===== YOUR ORIGINAL CODE STARTS HERE =====

        all_vacancies_data = []
        all_skills = []

        print("Летсгоу")

        for vacancy_id in vacancy_ids[::10]:

            vacancy_url = f'https://api.hh.ru/vacancies/{vacancy_id}'
            response = requests.get(vacancy_url)

            if response.status_code == 200:
                vacancy_data = response.json()

                description_html = vacancy_data.get('description', '')
                soup = BeautifulSoup(description_html, 'html.parser')
                clean_text = soup.get_text(separator='\n')

                key_skills_data = vacancy_data.get('key_skills', [])
                current_vacancy_skills = [skill['name'].lower() for skill in key_skills_data]
                all_skills.extend(current_vacancy_skills)

                vacancy_info = {
                    'id': vacancy_id,
                    'name': vacancy_data.get('name', 'Название не найдено'),
                    'url': vacancy_data.get('alternate_url', 'URL не найден'),
                    'description': clean_text
                }

                all_vacancies_data.append(vacancy_info)
                print(f"Вакансия {vacancy_id} обработана.")
            time.sleep(0.5)

        print("Я ТОЧНО ВСЕ")

        all_vacancies_text = [item['description'] for item in all_vacancies_data]

        pd.set_option('display.max_colwidth', None)
        df = pd.DataFrame(all_vacancies_data)

        promptishe = "\n\n--- НОВАЯ ВАКАНСИЯ ---\n\n".join(all_vacancies_text)

        prompt = f"""
Ты — опытный HR-аналитик на рынке IT. Тебе предоставлен набор полных текстов вакансий по запросу '{PROFESSION_NAME}'.
Твоя задача — проанализировать эти данные и составить краткий, но емкий отчет для человека, который хочет претендовать на эту должность.

Вот данные:
---
{promptishe}
---

Проанализируй ВЕСЬ текст и составь отчет по следующим пунктам:

1.  **Хард-скиллы:** Назови 5-7 самых важных и часто упоминаемых технологий, знаний и инструментов, которые требуются для этой роли.
2.  **Основные рабочие задачи:** Опиши 3-4 типовые задачи, которые предстоит решать специалисту на этой позиции. Пиши простым языком.
3.  **Что выделит кандидата:** Какие технологии или какой опыт часто упоминаются как желательные (в разделах "Будет плюсом")? Перечисли 2-3 пункта.
4.  **Главные рекомендации соискателю:** На основе всего анализа, дай 2 четких совета человеку, который ищет работу по запросу '{PROFESSION_NAME}'. На какие 2 технологии или навыка ему стоит сделать упор в первую очередь?

Ответ должен быть структурированным, ясным и на русском языке.
"""

        print("\nОтправил запросище.")
        # Increase Google API timeout to 5 minutes for large prompts
        response = model.generate_content(
            prompt,
            request_options={"timeout": 300}
        )
        print("\nРезультаты анализа:")
        print(response.text)

        # Skills analysis (your matplotlib part adapted for web)
        if all_skills:
            skills_series = pd.Series(all_skills)
            skill_counts = skills_series.value_counts()[:10]
            df_skills = skill_counts.reset_index()
            df_skills.columns = ['Навык', 'Частота']

            # Convert to JSON format for Chart.js
            skills_analysis = [
                {'skill': row['Навык'], 'count': int(row['Частота'])}
                for _, row in df_skills.iterrows()
            ]
        else:
            skills_analysis = []

        # ===== YOUR ORIGINAL CODE ENDS HERE =====

        # Return results
        result = {
            'vacancies': all_vacancies_data,
            'skills': skills_analysis,
            'ai_analysis': response.text,
            'total_vacancies': len(all_vacancies_data)
        }

        return jsonify(result)

    except Exception as e:
        print(f"Error in analyze_vacancies: {str(e)}")
        import traceback
        traceback.print_exc()
        return jsonify({'error': f'Произошла ошибка: {str(e)}'}), 500

if __name__ == '__main__':
    # For development
    app.run(debug=True, host='0.0.0.0', port=5000)
