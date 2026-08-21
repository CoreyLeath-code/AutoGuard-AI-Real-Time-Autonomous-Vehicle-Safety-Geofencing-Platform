FROM python:3.11-slim

WORKDIR /app

# Install dependencies
RUN pip install --no-cache-dir \
    streamlit>=1.34.0 \
    requests>=2.31.0

# Copy application source
COPY apps/ apps/
COPY libs/ libs/

# Run as a non-root user
RUN useradd --uid 1000 --create-home appuser
USER appuser

ENV PYTHONPATH=/app

EXPOSE 8501

HEALTHCHECK --interval=30s --timeout=5s --start-period=30s --retries=3 \
    CMD python3 -c "import urllib.request; urllib.request.urlopen('http://localhost:8501/_stcore/health')"

CMD ["streamlit", "run", "apps/dashboard/streamlit_app.py", \
     "--server.port=8501", "--server.address=0.0.0.0"]
