from flask import Flask, render_template, request, jsonify
from flask_cors import CORS
import requests
from bs4 import BeautifulSoup
import time
import google.generativeai as genai
import os
from collections import Counter

app = Flask(__name__)
CORS(app)

# Configuration
GOOGLE_API_KEY = os.environ.get('GOOGLE_API_KEY', 'AIzaSyC71NkOu9mIlcRCX6d_WWX9jwl1PwMFMZk')
genai.configure(api_key=GOOGLE_API_KEY)
model = genai.GenerativeModel('gemini-2.5-flash-lite')

@app.route('/')
def index():
    """Render the main page"""
    return render_template('index.html')

@app.route('/api/analyze', methods=['POST'])
def analyze_vacancies():
    """
    Analyze vacancies for a given profession
    """
    try:
        data = request.json
        profession = data.get('profession', '').strip()

        if not profession:
            return jsonify({'error': 'Название профессии не указано'}), 400

        # Step 1: Search for vacancies on HH.ru
        url = 'https://api.hh.ru/vacancies'
        params = {
            'text': profession,
            'area': 113,  # Russia
            'per_page': 100,
            'page': 0
        }

        response = requests.get(url, params=params, timeout=10)
        if response.status_code != 200:
            return jsonify({'error': 'Ошибка при поиске вакансий'}), 500

        search_data = response.json()
        vacancy_ids = [item['id'] for item in search_data.get('items', [])]

        if not vacancy_ids:
            return jsonify({'error': 'Вакансии не найдены. Попробуйте изменить запрос.'}), 404

        # Step 2: Process vacancies (YOUR ORIGINAL CODE!)
        all_vacancies_data = []
        all_skills = []

        print("Летсгоу")

        for vacancy_id in vacancy_ids[::10]:  # Take every 10th vacancy like in original
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

        if not all_vacancies_data:
            return jsonify({'error': 'Не удалось получить данные вакансий'}), 500

        # Step 3: Analyze skills
        if all_skills:
            skill_counts = Counter(all_skills)
            top_skills = skill_counts.most_common(10)
            skills_analysis = [
                {'skill': skill, 'count': count}
                for skill, count in top_skills
            ]
        else:
            skills_analysis = []

        # Step 4: AI Analysis (YOUR ORIGINAL PROMPT!)
        all_vacancies_text = [item['description'] for item in all_vacancies_data]
        promptishe = "\n\n--- НОВАЯ ВАКАНСИЯ ---\n\n".join(all_vacancies_text)

        prompt = f"""
Ты — опытный HR-аналитик на рынке IT. Тебе предоставлен набор полных текстов вакансий по запросу '{profession}'.
Твоя задача — проанализировать эти данные и составить краткий, но емкий отчет для человека, который хочет претендовать на эту должность.

Вот данные:
---
{promptishe}
---

Проанализируй ВЕСЬ текст и составь отчет по следующим пунктам:

1.  **Хард-скиллы:** Назови 5-7 самых важных и часто упоминаемых технологий, знаний и инструментов, которые требуются для этой роли.
2.  **Основные рабочие задачи:** Опиши 3-4 типовые задачи, которые предстоит решать специалисту на этой позиции. Пиши простым языком.
3.  **Что выделит кандидата:** Какие технологии или какой опыт часто упоминаются как желательные (в разделах "Будет плюсом")? Перечисли 2-3 пункта.
4.  **Главные рекомендации соискателю:** На основе всего анализа, дай 2 четких совета человеку, который ищет работу по запросу '{profession}'. На какие 2 технологии или навыка ему стоит сделать упор в первую очередь?

Ответ должен быть структурированным, ясным и на русском языке.
"""

        print("\nОтправил запросище.")
        ai_response = model.generate_content(prompt)
        ai_analysis = ai_response.text
        print("\nРезультаты анализа:")
        print(ai_analysis)

        # Step 5: Prepare response
        response = {
            'vacancies': all_vacancies_data,
            'skills': skills_analysis,
            'ai_analysis': ai_analysis,
            'total_vacancies': len(all_vacancies_data)
        }

        return jsonify(response)

    except Exception as e:
        print(f"Error in analyze_vacancies: {str(e)}")
        return jsonify({'error': f'Произошла ошибка: {str(e)}'}), 500

if __name__ == '__main__':
    # For development
    app.run(debug=True, host='0.0.0.0', port=5000)
