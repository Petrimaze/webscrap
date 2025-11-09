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

    Request body:
    {
        "profession": "Python разработчик"
    }

    Response:
    {
        "vacancies": [...],
        "skills": [...],
        "ai_analysis": "..."
    }
    """
    try:
        data = request.json
        profession = data.get('profession', '').strip()

        if not profession:
            return jsonify({'error': 'Название профессии не указано'}), 400

        # Step 1: Search for vacancies
        vacancy_ids = search_vacancies(profession)

        if not vacancy_ids:
            return jsonify({'error': 'Вакансии не найдены. Попробуйте изменить запрос.'}), 404

        # Step 2: Fetch vacancy details (every 10th vacancy to speed up)
        all_vacancies_data = []
        all_skills = []

        for vacancy_id in vacancy_ids[::10]:  # Take every 10th vacancy
            vacancy_data = fetch_vacancy_details(vacancy_id)

            if vacancy_data:
                all_vacancies_data.append(vacancy_data)
                all_skills.extend(vacancy_data.get('skills', []))

            # Be nice to the API
            time.sleep(0.5)

            # Limit to 20 vacancies max
            if len(all_vacancies_data) >= 20:
                break

        if not all_vacancies_data:
            return jsonify({'error': 'Не удалось получить данные вакансий'}), 500

        # Step 3: Analyze skills
        skills_analysis = analyze_skills(all_skills)

        # Step 4: AI Analysis
        ai_analysis = perform_ai_analysis(all_vacancies_data, profession)

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

def search_vacancies(profession, per_page=100):
    """
    Search for vacancies on HH.ru

    Args:
        profession: Job title to search for
        per_page: Number of results per page (max 100)

    Returns:
        List of vacancy IDs
    """
    url = 'https://api.hh.ru/vacancies'
    params = {
        'text': profession,
        'area': 113,  # Russia
        'per_page': per_page,
        'page': 0
    }

    try:
        response = requests.get(url, params=params, timeout=10)
        response.raise_for_status()
        data = response.json()

        vacancy_ids = [item['id'] for item in data.get('items', [])]
        return vacancy_ids

    except Exception as e:
        print(f"Error searching vacancies: {str(e)}")
        return []

def fetch_vacancy_details(vacancy_id):
    """
    Fetch detailed information about a vacancy

    Args:
        vacancy_id: Vacancy ID

    Returns:
        Dictionary with vacancy details
    """
    url = f'https://api.hh.ru/vacancies/{vacancy_id}'

    try:
        response = requests.get(url, timeout=10)
        response.raise_for_status()
        vacancy_data = response.json()

        # Parse description HTML
        description_html = vacancy_data.get('description', '')
        soup = BeautifulSoup(description_html, 'html.parser')
        clean_text = soup.get_text(separator='\n')

        # Extract skills
        key_skills_data = vacancy_data.get('key_skills', [])
        skills = [skill['name'].lower() for skill in key_skills_data]

        return {
            'id': vacancy_id,
            'name': vacancy_data.get('name', 'Название не найдено'),
            'url': vacancy_data.get('alternate_url', ''),
            'description': clean_text[:500],  # Limit description length
            'skills': skills
        }

    except Exception as e:
        print(f"Error fetching vacancy {vacancy_id}: {str(e)}")
        return None

def analyze_skills(all_skills):
    """
    Analyze and count skills

    Args:
        all_skills: List of all skills

    Returns:
        List of top 10 skills with counts
    """
    if not all_skills:
        return []

    skill_counts = Counter(all_skills)
    top_skills = skill_counts.most_common(10)

    return [
        {'skill': skill, 'count': count}
        for skill, count in top_skills
    ]

def perform_ai_analysis(vacancies_data, profession):
    """
    Perform AI analysis using Google Gemini

    Args:
        vacancies_data: List of vacancy dictionaries
        profession: Job title

    Returns:
        AI analysis text
    """
    try:
        # Prepare text for analysis
        all_vacancies_text = [item['description'] for item in vacancies_data]
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

        response = model.generate_content(prompt)
        return response.text

    except Exception as e:
        print(f"Error in AI analysis: {str(e)}")
        return f"Не удалось выполнить AI анализ: {str(e)}"

if __name__ == '__main__':
    # For development
    app.run(debug=True, host='0.0.0.0', port=5000)
