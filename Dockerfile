FROM python:3.10-slim

WORKDIR /app

# نصب ابزارهای سیستمی ضروری
RUN apt-get update && apt-get install -y \
    build-essential \
    libgomp1 \
    && rm -rf /var/lib/apt/lists/*

COPY requirements.txt .

# --- خط جدید و مهم: آپدیت کردن پیپ ---
RUN pip install --upgrade pip

# نصب کتابخانه‌ها
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

EXPOSE 8501

CMD ["streamlit", "run", "app.py", "--server.address=0.0.0.0"]