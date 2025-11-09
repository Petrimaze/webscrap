// App State
let currentChart = null;

// DOM Elements
const searchForm = document.getElementById('searchForm');
const professionInput = document.getElementById('professionInput');
const searchBtn = searchForm.querySelector('.search-btn');
const btnText = searchBtn.querySelector('.btn-text');
const btnLoader = searchBtn.querySelector('.btn-loader');
const loadingState = document.getElementById('loadingState');
const loadingStatus = document.getElementById('loadingStatus');
const progressFill = document.getElementById('progressFill');
const resultsSection = document.getElementById('resultsSection');
const errorState = document.getElementById('errorState');
const errorMessage = document.getElementById('errorMessage');

// Event Listeners
searchForm.addEventListener('submit', handleSearch);

// Handle Search Form Submit
async function handleSearch(e) {
    e.preventDefault();

    const profession = professionInput.value.trim();
    if (!profession) return;

    // Reset UI
    hideAllSections();
    showLoading();

    try {
        // Start analysis
        const response = await fetch('/api/analyze', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({ profession }),
        });

        if (!response.ok) {
            throw new Error('Ошибка при анализе вакансий');
        }

        const data = await response.json();

        if (data.error) {
            throw new Error(data.error);
        }

        // Show results
        displayResults(data);

    } catch (error) {
        console.error('Error:', error);
        showError(error.message);
    }
}

// Show Loading State
function showLoading() {
    searchBtn.disabled = true;
    btnText.classList.add('hidden');
    btnLoader.classList.remove('hidden');
    loadingState.classList.remove('hidden');

    // Simulate progress updates
    let progress = 0;
    const progressInterval = setInterval(() => {
        progress += 5;
        if (progress <= 90) {
            progressFill.style.width = progress + '%';

            // Update status messages
            if (progress < 30) {
                loadingStatus.textContent = 'Собираем данные с HeadHunter...';
            } else if (progress < 60) {
                loadingStatus.textContent = 'Обрабатываем вакансии...';
            } else {
                loadingStatus.textContent = 'Анализируем с помощью AI...';
            }
        } else {
            clearInterval(progressInterval);
        }
    }, 200);
}

// Display Results
function displayResults(data) {
    hideAllSections();
    resultsSection.classList.remove('hidden');

    // Display AI Analysis
    displayAIAnalysis(data.ai_analysis);

    // Display Skills Chart
    displaySkillsChart(data.skills);

    // Display Vacancies List
    displayVacancies(data.vacancies);

    // Reset form
    searchBtn.disabled = false;
    btnText.classList.remove('hidden');
    btnLoader.classList.add('hidden');
}

// Display AI Analysis
function displayAIAnalysis(analysis) {
    const container = document.getElementById('aiAnalysisContent');

    // Format the AI analysis text with proper HTML
    const formattedAnalysis = formatAnalysisText(analysis);
    container.innerHTML = formattedAnalysis;
}

// Format Analysis Text
function formatAnalysisText(text) {
    // Convert markdown-style formatting to HTML
    let formatted = text;

    // Headers (## Header -> <h3>Header</h3>)
    formatted = formatted.replace(/##\s*(.+)/g, '<h3>$1</h3>');

    // Bold (**text** -> <strong>text</strong>)
    formatted = formatted.replace(/\*\*(.+?)\*\*/g, '<strong>$1</strong>');

    // Lists (- item or * item -> <ul><li>item</li></ul>)
    formatted = formatted.replace(/^[-*]\s+(.+)/gm, '<li>$1</li>');
    formatted = formatted.replace(/(<li>.*<\/li>)/s, '<ul>$1</ul>');

    // Line breaks
    formatted = formatted.replace(/\n\n/g, '</p><p>');
    formatted = '<p>' + formatted + '</p>';

    // Clean up
    formatted = formatted.replace(/<p><h3>/g, '<h3>');
    formatted = formatted.replace(/<\/h3><\/p>/g, '</h3>');
    formatted = formatted.replace(/<p><ul>/g, '<ul>');
    formatted = formatted.replace(/<\/ul><\/p>/g, '</ul>');
    formatted = formatted.replace(/<p>\s*<\/p>/g, '');

    return formatted;
}

// Display Skills Chart
function displaySkillsChart(skills) {
    const ctx = document.getElementById('skillsChart');

    // Destroy existing chart if it exists
    if (currentChart) {
        currentChart.destroy();
    }

    // Prepare data
    const labels = skills.map(s => s.skill);
    const data = skills.map(s => s.count);

    // Create gradient
    const gradient = ctx.getContext('2d').createLinearGradient(0, 0, 400, 0);
    gradient.addColorStop(0, '#667eea');
    gradient.addColorStop(1, '#764ba2');

    // Create chart
    currentChart = new Chart(ctx, {
        type: 'bar',
        data: {
            labels: labels,
            datasets: [{
                label: 'Количество упоминаний',
                data: data,
                backgroundColor: gradient,
                borderRadius: 8,
                borderSkipped: false,
            }]
        },
        options: {
            indexAxis: 'y',
            responsive: true,
            maintainAspectRatio: false,
            plugins: {
                legend: {
                    display: false
                },
                tooltip: {
                    backgroundColor: 'rgba(0, 0, 0, 0.8)',
                    padding: 12,
                    cornerRadius: 8,
                    titleFont: {
                        size: 14
                    },
                    bodyFont: {
                        size: 13
                    }
                }
            },
            scales: {
                x: {
                    beginAtZero: true,
                    grid: {
                        color: 'rgba(0, 0, 0, 0.05)'
                    },
                    ticks: {
                        font: {
                            size: 12
                        }
                    }
                },
                y: {
                    grid: {
                        display: false
                    },
                    ticks: {
                        font: {
                            size: 12,
                            weight: '500'
                        }
                    }
                }
            }
        }
    });
}

// Display Vacancies
function displayVacancies(vacancies) {
    const container = document.getElementById('vacanciesList');
    const countElement = document.getElementById('vacancyCount');

    countElement.textContent = `${vacancies.length} ${pluralizeVacancies(vacancies.length)}`;

    const vacanciesHTML = vacancies.map(vacancy => `
        <div class="vacancy-item">
            <h4>${escapeHtml(vacancy.name)}</h4>
            <p>${escapeHtml(vacancy.description.substring(0, 150))}...</p>
            <a href="${escapeHtml(vacancy.url)}" target="_blank" rel="noopener noreferrer">
                Открыть вакансию →
            </a>
        </div>
    `).join('');

    container.innerHTML = vacanciesHTML;
}

// Show Error
function showError(message) {
    hideAllSections();
    errorState.classList.remove('hidden');
    errorMessage.textContent = message;

    searchBtn.disabled = false;
    btnText.classList.remove('hidden');
    btnLoader.classList.add('hidden');
}

// Hide All Sections
function hideAllSections() {
    loadingState.classList.add('hidden');
    resultsSection.classList.add('hidden');
    errorState.classList.add('hidden');
}

// Utility Functions
function pluralizeVacancies(count) {
    const lastDigit = count % 10;
    const lastTwoDigits = count % 100;

    if (lastTwoDigits >= 11 && lastTwoDigits <= 19) {
        return 'вакансий';
    }

    if (lastDigit === 1) {
        return 'вакансия';
    }

    if (lastDigit >= 2 && lastDigit <= 4) {
        return 'вакансии';
    }

    return 'вакансий';
}

function escapeHtml(unsafe) {
    if (typeof unsafe !== 'string') return '';
    return unsafe
        .replace(/&/g, "&amp;")
        .replace(/</g, "&lt;")
        .replace(/>/g, "&gt;")
        .replace(/"/g, "&quot;")
        .replace(/'/g, "&#039;");
}

// Initialize
document.addEventListener('DOMContentLoaded', () => {
    console.log('HH.ru Vacancy Analyzer initialized');
});
