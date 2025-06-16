FROM python:3.10-slim

WORKDIR /app

COPY ./ui /app/ui
COPY ./requirements.txt /app/requirements.txt

RUN pip install --no-cache-dir -r /app/requirements.txt

# Expone el puerto de Streamlit
EXPOSE 8501

CMD ["streamlit", "run", "ui/app.py", "--server.port=8501", "--server.address=0.0.0.0"]
