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
    # 'execution_timeout': timedelta(seconds=300),
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
    bash_command='mkdir -p tmp/workflow/data/ ',
    dag=dag,
)

DescargaApi = BashOperator(
    task_id='PrepararEntorno',
    depends_on_past=False,
    bash_command='cd tmp/workflow/ && https://github.com/yoskitar/API-Prediccion-Humedad-Temperatura-CC/API',
    dag=dag,
)

DescargaDatosHumedad = BashOperator(
    task_id='DescargaTemperatura',
    depends_on_past=False,
    bash_command='cd tmp/workflow/data/ && wget https://github.com/manuparra/MaterialCC2020/raw/master/humidity.csv.zip',
    dag=dag,
)

DescargaDatosTemperatura = BashOperator(
    task_id='DescargaHumedad',
    depends_on_past=False,
    bash_command='cd tmp/workflow/data/ && wget https://github.com/manuparra/MaterialCC2020/raw/master/temperature.csv.zip',
    dag=dag,
)

#Dependencias - Construcción del grafo DAG
[DescargaApi,PrepararEntorno] >> [DescargaDatosTemperatura,DescargaDatosHumedad]