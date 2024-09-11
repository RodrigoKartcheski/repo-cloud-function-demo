FROM google/cloud-sdk:slim
COPY requirements.txt requirements.txt
RUN cat requirements.txt  # Adicione isso para verificar se o arquivo foi copiado corretamente
RUN pip install -r requirements.txt
COPY . .
CMD ["python", "main.py"]
