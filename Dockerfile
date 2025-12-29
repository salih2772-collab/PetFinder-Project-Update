# استفاده از نسخه 3.11 برای سازگاری با کتابخانه‌های جدید
FROM python:3.11-slim

# تنظیم پوشه کاری
WORKDIR /app

# نصب ابزارهای سیستمی ضروری برای XGBoost و FastText
RUN apt-get update && apt-get install -y \
    build-essential \
    libgomp1 \
    && rm -rf /var/lib/apt/lists/*

# کپی فایل نیازمندی‌ها
COPY requirements.txt .

# آپدیت کردن پیپ برای جلوگیری از خطاهای نصب
RUN pip install --upgrade pip

# نصب کتابخانه‌ها
RUN pip install --no-cache-dir -r requirements.txt

# کپی تمام فایل‌های پروژه به داخل کانتینر
COPY . .

# تعیین پورت (استریم‌لیت به صورت پیش‌فرض 8501 است)
EXPOSE 8501

# دستور اجرای اپلیکیشن
CMD ["streamlit", "run", "app.py", "--server.port=8501", "--server.address=0.0.0.0"]
