from datetime import timedelta
from airflow import DAG
from airflow.operators.bash_operator import BashOperator
from airflow.utils.dates import days_ago

default_args = {
    'owner': 'airflow',
    'depends_on_past': False,
    'start_date': days_ago(2),
    'email': ['osc9718@gmail.com'],
    'email_on_failure': False,
    'email_on_retry': False,
    'retries': 1,
    'retry_delay': timedelta(minutes=1),
    # 'queue': 'bash_queue',
    # 'pool': 'backfill',
    # 'priority_weight': 10,
    # 'end_date': datetime(2016, 1, 1),
    # 'wait_for_downstream': False,
    # 'dag': dag,
    # 'sla': timedelta(hours=2),
    'execution_timeout': timedelta(seconds=1500),
    # 'on_failure_callback': some_function,
    # 'on_success_callback': some_other_function,
    # 'on_retry_callback': another_function,
    # 'sla_miss_callback': yet_another_function,
    # 'trigger_rule': 'all_success'
}

#Inicialización del grafo DAG de tareas para el flujo de trabajo
dag = DAG(
    'practica2_prediccion_temp_hum',
    default_args=default_args,
    description='Orquestación del servicio de prediccion',
    schedule_interval=timedelta(days=1),
)

# Operadores o tareas
PrepararEntorno = BashOperator(
    task_id='PrepararEntorno',
    depends_on_past=False,
    bash_command='mkdir -p /tmp/workflow/data/',
    dag=dag,
)

DescargaApi = BashOperator(
    task_id='DescargaApi',
    depends_on_past=True,
    bash_command='wget -O /tmp/workflow/master.zip https://github.com/yoskitar/API-Prediccion-Humedad-Temperatura-CC/archive/master.zip',
    dag=dag,
)

DescargaDatosHumedad = BashOperator(
    task_id='DescargaHumedad',
    depends_on_past=True,
    bash_command='wget -O /tmp/workflow/data/humidity.csv.zip https://github.com/manuparra/MaterialCC2020/raw/master/humidity.csv.zip',
    dag=dag,
)

DescargaDatosTemperatura = BashOperator(
    task_id='DescargaTemperatura',
    depends_on_past=True,
    bash_command='wget -O /tmp/workflow/data/temperature.csv.zip https://github.com/manuparra/MaterialCC2020/raw/master/temperature.csv.zip',
    dag=dag,
)

Descomprimir = BashOperator(
    task_id='Descomprimir',
    depends_on_past=True,
    bash_command='unzip /tmp/workflow/master.zip -d /tmp/workflow/ & unzip /tmp/workflow/data/temperature.csv.zip -d /tmp/workflow/data/ & unzip /tmp/workflow/data/humidity.csv.zip -d /tmp/workflow/data/',
    dag=dag,
)

#Dependencias - Construcción del grafo DAG
PrepararEntorno >> [DescargaApi,DescargaDatosTemperatura,DescargaDatosHumedad] >> Descomprimir