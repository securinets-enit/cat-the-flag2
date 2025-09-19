# Use slim Python as base
FROM python:3.11-slim

# Install system dependencies for WeasyPrint (Cairo, Pango, GDK-Pixbuf, etc.)
RUN apt-get update && apt-get install -y \
    build-essential \
    libcairo2 \
    libcairo2-dev \
    libpango-1.0-0 \
    libpangocairo-1.0-0 \
    libgdk-pixbuf-2.0-0 \
    libffi-dev \
    shared-mime-info \
    curl \
    && rm -rf /var/lib/apt/lists/*

# Set working directory
WORKDIR /app

# Copy requirements if you have one, else inline
COPY requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt

# Copy the app
COPY . .

# Flask will read SECRET_KEY and FLAG from env
ENV FLASK_ENV=production \
    PYTHONUNBUFFERED=1

# Run with Gunicorn (more production-like than flask run)
CMD ["gunicorn", "-w", "4", "-b", "0.0.0.0:5000", "app:app"]
