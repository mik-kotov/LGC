Автотесты для loyalty-service

ЯП: Python 3.12.2
Тестовый фреймворк: pytest 8.1.1
Библиотека для веб-тестирования: Selenium WebDriver 
Отчётность: Allure Framework

Установка зависимостей:

pip install -r requirements.txt

Команды для запуска тестов: 

pytest -s -v --alluredir=allure-results
Запуск всех тестов

pytest -s -v -m no_promocode --alluredir=allure-results
Запуск тестов без промокода

pytest -s -v -m with_promocode --alluredir=allure-results
Запуск тестов с промокодом

pytest -s -v -m no_card --alluredir=allure-results
Запуск тестов без карты

pytest -s -v -m with_card --alluredir=allure-results
Запуск тестов с картой

pytest -s -v -m delivered --alluredir=allure-results
Запуск тестов с конечным статусом "Доставлен"

pytest -s -v -m cancelled --alluredir=allure-results
Запуск тестов с конечным статусом "Отменен"

pytest -s -v -m refused --alluredir=allure-results
Запуск тестов с конечным статусом "Отказ"

pytest -s -v -m processed --alluredir=allure-results
Запуск тестов с конечным статусом "Подтвержден"

pytest -s -v -m partial_cancelled --alluredir=allure-results
Запуск тестов с конечным статусом "Частичный отказ"

Отчеты

Генерация: 
allure generate allure-results --clean -o allure-report

Просмотр отчета:
allure open allure-report


Установка Pytest + Selenium:

1. Установить Python версии не ниже 3.12.0
2. Cкачать драйвер Chrome For Testing https://googlechromelabs.github.io/chrome-for-testing/, распаковать
3. В Переменных средах прописать Path до папки chromedriver
4. Клонировать репозиторий и зайти в него
5. Установить зависимости через pip install -r requirements.txt


Установка Allure:

5. Скачать Java Development Kit, распаковать
6. Прописать путь к папке jdk-22 в Системных переменных: имя переменной - JAVA_HOME, значение - адрес (напр. C:\Program Files\Java\jdk-22)
7. Cкачать Аллюр https://github.com/allure-framework/allure2/releases/tag/2.30.0, распаковать
8. В переменных средах прописать Path к папке allure-2.29.0\bin

Примечания:

1. Могут не запускаться тесты без headless-режима драйвера. В этом случае в файле conftest.py нужно разкомментировать строку 26: #options.add_argument("--headless")

2. При ошибках вида "conftest.py:1: in <module>
    from API import data
E   ModuleNotFoundError: No module named 'API'" требуется прописать в Переменных средах: имя переменной - %PYTHONPATH%, значение - путь к корневой директории проекта


Ожидаемый результат: 

1. Команда pytest -s -v -m "processed and no_card" --alluredir=allure-results запускает и успешно завершает тест
2. Команда allure serve подготавливает и открывает в браузере html-отчет