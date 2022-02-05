Запускается проект через main.py
Для создания бд, необходимо открыть проект в среде разработки (Я использовал PyCharm) и в окне Terminal вписать следующее:
1. python и нажать Enter
2. from app import db, create_app и нажать Enter
3. db.create_all(app=create_app()) и нажать Enter
Так создаться бд для работы с приложением. Дальше остается только запустить main.py
