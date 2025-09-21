# -------- base image --------
FROM python:3.12-slim AS runtime

# --- system deps (just in case) ---
RUN apt-get update -qq && \
    apt-get install --no-install-recommends -y build-essential && \
    rm -rf /var/lib/apt/lists/*

# --- create non-root user ---
ENV APP_HOME=/app
RUN useradd --create-home --home-dir $APP_HOME appuser
WORKDIR $APP_HOME

# --- install python deps ---
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# --- copy challenge source ---
COPY . .

# --- switch to non-root user ---
USER appuser

# --- network / process setup ---
EXPOSE 8000
ENV PYTHONUNBUFFERED=1

# --- launch the FastAPI app with uvicorn ---
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]