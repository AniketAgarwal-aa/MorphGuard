FROM python:3.10-slim
ENV PYTHONDONTWRITEBYTECODE=1 PYTHONUNBUFFERED=1 MORPHGUARD_ROOT=/opt/morphguard
WORKDIR /opt/morphguard
RUN useradd --create-home --uid 10001 appuser
COPY requirements-inference.txt ./
RUN pip install --no-cache-dir -r requirements-inference.txt
COPY src ./src
COPY app ./app
COPY config ./config
RUN mkdir -p data/metadata
COPY data/metadata/dataset_summary.json data/metadata/metadata_summary.json data/metadata/class_distribution.csv data/metadata/corrupted_images.csv data/metadata/duplicate_images.csv ./data/metadata/
RUN mkdir -p models/metadata models/trained
RUN chown -R appuser:appuser /opt/morphguard
USER appuser
EXPOSE 8501
CMD ["streamlit", "run", "app/main.py", "--server.address=0.0.0.0", "--server.port=8501"]
