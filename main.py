import functions_framework
import os, json
from google.cloud import bigquery, storage


# Triggered by a change in a storage bucket
@functions_framework.cloud_event
def main_gcs(cloud_event):
    # Use o objeto correto para acessar os dados do evento
    data = cloud_event.data

    # Acessando os dados do evento corretamente
    event_id = cloud_event["id"]  # Certifique-se de que o ID está no payload
    event_type = cloud_event["type"]

    sourceRaw = os.environ.get('SOURCE_RAW')
    fileType = os.environ.get('FILE_TYPE')
    dataSet_name = os.environ.get('DATASET_ID')
    tableName = os.environ.get('TABLE_NAME')

    # Acessando os atributos do objeto 'data' corretamente
    bucket = data.get("bucket")
    name = data.get("name")

    if sourceRaw in name and name.endswith(fileType):
        print(name)

        # Corrigindo a formatação de string
        gcs_uri = f"gs://{bucket}/{name}"

        # Iniciando o cliente do BigQuery
        client = bigquery.Client()

        # Referência para a tabela
        table_ref = client.dataset(dataSet_name).table(tableName)

        # Configuração de job para carregar CSV
        job_config = bigquery.LoadJobConfig(
            source_format=bigquery.SourceFormat.CSV,
            skip_leading_rows=1,
            autodetect=True
        )

        # Tentando carregar os dados
        try:
            load_job = client.load_table_from_uri(gcs_uri, table_ref, job_config=job_config)
            load_job.result()  # Espera o job completar

            table = client.get_table(table_ref)  # Obtém a tabela carregada

            print(f"Loaded {table.num_rows} rows into {dataSet_name}:{tableName}.")

        except Exception as e:
            print(f"Error loading data into BigQuery: {str(e)}")
        
    metageneration = data.get("metageneration")
    timeCreated = data.get("timeCreated")
    updated = data.get("updated")

    # Exibir as informações do evento
    print(f"Event ID: {event_id}")
    print(f"Event type: {event_type}")
    print(f"Bucket: {bucket}")
    print(f"File: {name}")
    print(f"Metageneration: {metageneration}")
    print(f"Created: {timeCreated}")
    print(f"Updated: {updated}")
    

'''
gcloud functions deploy python-finalize-function \
--gen2 \
--runtime=python312 \
--region=us-central1 \
--source=gs://gcs-to-bigquery-3065/fu/source_function.zip \
--entry-point=main_gcs \
--trigger-event-filters="type=google.cloud.storage.object.v1.finalized" \
--trigger-event-filters="bucket=gcs-to-bigquery-3065" \
--allow-unauthenticated \
--timeout=120s \
--max-instances=2 \
--set-env-vars=SOURCE_RAW=raw/,FILE_TYPE=.csv,DATASET_ID=dataset_demo,TABLE_NAME=table_demo,LOG_EXECUTION_ID=true
'''
