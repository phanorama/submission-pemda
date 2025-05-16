# Membuat Virtual Environment
python -m venv venv
source venv/bin/activate     # Linux/Mac
venv\Scripts\activate.bat    # Windows

# Install Dependencies
pip install -r requirements.txt

# Menjalankan skrip
python main.py

# Menjalankan unit test pada folder tests
python -m unittest discover -s tests

# Menjalankan test coverage pada folder tests
coverage run -m unittest discover tests

# lihat laporan hasil uji coverage
coverage report

# Url Google Sheets:
https://docs.google.com/spreadsheets/d/136Q8BKDsyuXFVYnOS_D0s9oVIr6b1RQ6OSeGFGEoCpA/edit?usp=sharing

# database postgresql
URL      : postgresql://postgres:123@localhost:5432/fashion_products
Database : fashion_products
Port     : 5432
Username : postgres
Password : 123

# Mematikan Virtual Environment
deactivate