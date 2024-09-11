FROM google/cloud-sdk:slim

# Instalar o virtualenv
RUN apt-get update && apt-get install -y python3-virtualenv

# Criar um ambiente virtual e ativá-lo
RUN python3 -m virtualenv /opt/venv
ENV PATH="/opt/venv/bin:$PATH"

# Copiar o arquivo requirements.txt e instalar as dependências no ambiente virtual
COPY requirements.txt requirements.txt
RUN cat requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

# Copiar o restante dos arquivos
COPY . .

# Executar o aplicativo no ambiente virtual
CMD ["python", "main.py"]

