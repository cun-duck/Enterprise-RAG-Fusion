FROM nvidia/cuda:12.2.0-base-ubuntu22.04

ENV DEBIAN_FRONTEND=noninteractive
RUN apt-get update && \
    apt-get install -y python3.10 python3-pip git && \
    ln -s /usr/bin/python3.10 /usr/bin/python

WORKDIR /app
COPY . .

RUN pip install -r requirements.txt --no-cache-dir && \
    python -m spacy download en_core_web_trf

EXPOSE 8000
CMD ["uvicorn", "api.fastapi_app:app", "--host", "0.0.0.0", "--port", "8000"]
