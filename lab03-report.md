# Звіт з лабораторної роботи 3

## Розробка базового вебпроєкту

### Інформація про команду
- Назва команди: Немає

- Учасники:
  - Кравчук Владислав Вікторович

## Завдання
3 лабораторна, створити свій вебзастосунок

### Обрана предметна область

Освітні онлайн послуги.

### Реалізовані вимоги

Вкажіть, які рівні завдань було виконано:

- [Виконано] Рівень 1: Створено сторінки "Головна" та "Про нас"
- [Виконано] Рівень 2: Додано мінімум дві додаткові статичні сторінки з меню та адаптивною версткою

## Хід виконання роботи
Поміг штучний інтелект, виправляв помилки штучного інтелекту

### Підготовка середовища розробки

Опишіть процес встановлення та налаштування:

- Python 3.8
- pip instal Flask

### Структура проєкту

Наведіть структуру файлів та директорій вашого проєкту:

```
d:\OneDrive\ladoratorniosn\3laba
├── 3laboratorna.py
```
з виконанням доповнених лабораторних робіт вона буде розширюватись, пока що все одним кодом

### Опис реалізованих сторінок
Головна-все про сайт
Про нас-про команду яка робила цей сайт(я один)
Послуги- послуги які надає сайт
Контакти-емайл та гітхаб розробника(пока що не добавив)
#### Головна сторінка

Головна-все про сайт

#### Сторінка "Про нас"

Про нас-про команду яка робила цей сайт(я один)

#### Додаткові сторінки (якщо реалізовано)

Послуги- послуги які надає сайт
Контакти-емайл та гітхаб розробника(пока що не добавив)

## Ключові фрагменти коду

### Маршрутизація в Flask

Наведіть приклад налаштування маршрутів у файлі `app.py`:

"/" — endpoint: home
"/about" — endpoint: about
"/services" — endpoint: services
"/contact" — endpoint: contact

```python
@app.route('/')
def index():
    return render_template('index.html')
```

### Базовий шаблон

Наведіть фрагмент базового шаблону `base.html`:

base_template = """
<!doctype html>
<html lang="uk">
<head>
    <meta charset="utf-8">
    <meta name="viewport" content="width=device-width,initial-scale=1">
    <script src="https://cdn.tailwindcss.com"></script>
    <title>{{ title }} — Проєкт</title>
</head>
<body class="min-h-screen bg-gray-50 text-gray-800">
    <header class="bg-white shadow">
        <div class="container mx-auto px-4 py-4 flex items-center justify-between">
            <a href="{{ url_for('home') }}" class="text-xl font-semibold">Онлайн послуги</a>
            <nav class="hidden md:flex space-x-4">
                <a href="{{ url_for('home') }}" class="px-3 py-2 rounded {{ 'bg-gray-200' if active=='home' else 'hover:bg-gray-100' }}">Головна</a>
                <a href="{{ url_for('about') }}" class="px-3 py-2 rounded {{ 'bg-gray-200' if active=='about' else 'hover:bg-gray-100' }}">Про нас</a>
                <a href="{{ url_for('services') }}" class="px-3 py-2 rounded {{ 'bg-gray-200' if active=='services' else 'hover:bg-gray-100' }}">Послуги</a>
                <a href="{{ url_for('contact') }}" class="px-3 py-2 rounded {{ 'bg-gray-200' if active=='contact' else 'hover:bg-gray-100' }}">Контакти</a>
            </nav>
            <div class="md:hidden">
                <button id="menuBtn" class="p-2 rounded bg-gray-100">Меню</button>
            </div>
        </div>
        <div id="mobileMenu" class="md:hidden hidden bg-white border-t">
            <div class="px-4 py-2 flex flex-col">
                <a href="{{ url_for('home') }}" class="py-2 {{ 'font-semibold' if active=='home' else '' }}">Головна</a>
                <a href="{{ url_for('about') }}" class="py-2 {{ 'font-semibold' if active=='about' else '' }}">Про нас</a>
                <a href="{{ url_for('services') }}" class="py-2 {{ 'font-semibold' if active=='services' else '' }}">Послуги</a>
                <a href="{{ url_for('contact') }}" class="py-2 {{ 'font-semibold' if active=='contact' else '' }}">Контакти</a>
            </div>
        </div>
    </header>

    <main class="container mx-auto px-4 py-8">
        {{ content|safe }}
    </main>

    <footer class="bg-white border-t mt-12">
        <div class="container mx-auto px-4 py-6 text-sm text-gray-600">
            © 2025 Онлайн послуги — навчальний вебзастосунок. Репозиторій із кодом додається до звіту.
        </div>
    </footer>

    <script>
        // Простий мобільний toggle меню
        document.getElementById('menuBtn')?.addEventListener('click', function(){
            const m = document.getElementById('mobileMenu');
            if (m) m.classList.toggle('hidden');
        });
    </script>
</body>
</html>

## Розподіл обов'язків у команді

Опишіть внесок кожного учасника команди:

- Кравчук Владислав Вікторович - Виправив проблеми коду, дописав код

## Скріншоти

Додайте скріншоти основних сторінок вашого вебзастосунку:
https://lviv1256.com/wp-content/uploads/2018/02/3c99a63cf81c3449bf7199e7af36599a.jpg

### Головна сторінка

![Головна сторінка](<div class="bg-gradient-to-br from-blue-50 to-white p-6 rounded shadow">
                <img src="https://lviv1256.com/wp-content/uploads/2018/02/3c99a63cf81c3449bf7199e7af36599a.jpg" alt="learning" class="w-full rounded">
            </div>)

### Сторінка "Про нас"

нема

### Додаткові сторінки

нема


### Висновки

Опишіть:

- Що вдалося реалізувати успішно:Більшість
- З якими труднощами зіткнулися:Порт, скріни
- Які навички та знання отримали:Як добавляти скріни на сайт, виправління коду
- Які можливості для вдосконалення проєкту бачите:Збільшення директорії проекту

Очікувана оцінка: [7 балів]

Обґрунтування: [Написав більшість коду за допомогою штучного інтелекту]
