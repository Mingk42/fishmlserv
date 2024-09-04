from datetime import datetime, timedelta
from textwrap import dedent

from airflow import DAG

from airflow.operators.empty import EmptyOperator
from airflow.operators.python import PythonOperator

from airflow.models import TaskInstance

with DAG(
    'fish_ml_serv_std',
    default_args={
        'depends_on_past': False,
        'email_on_failure': False,
        'email_on_retry': False,
        'retries': 1,
        'retry_delay': timedelta(seconds=3)
    },
    description='fish_ml_serv_std',
    schedule="@once",
    start_date=datetime(2024, 9, 1),
    catchup=True,
    tags=["fish","ml","serv", "std"],
) as dag:

    def load_csv():
        import pandas as pd
        
        CLASSES={
            "Bream":"도미",
            "Smelt":"빙어"
        }

        df=pd.read_csv("/home/root2/data/fish/fish100k.csv")
        df["LabelKo"]=df["Label"].apply(lambda x:CLASSES[x])

        return df

    def predict(*op_args,**context):
        import requests as reqs

        df=context['task_instance'].xcom_pull(task_ids=f'load.csv')
        
        nneighbor=op_args[0]
        
        tmp=[]
        
        for i,d in df.iterrows():
            #http://localhost:70/fish_std?length=100&weight=50&nneighbor=5
            resp=reqs.get(f"http://localhost:70/fish_std?length={d['Length']}&weight={d['Weight']}&nneighbor={nneighbor}").text
            tmp.append(eval(resp)["prediction"])

        return tmp

    def agg(**context):
        df=context['task_instance'].xcom_pull(task_ids=f'load.csv')
        pred1=context['task_instance'].xcom_pull(task_ids=f'predict1')
        pred5=context['task_instance'].xcom_pull(task_ids=f'predict5')
        pred15=context['task_instance'].xcom_pull(task_ids=f'predict15')
        pred25=context['task_instance'].xcom_pull(task_ids=f'predict25')
        pred49=context['task_instance'].xcom_pull(task_ids=f'predict49')

        df["pred1"]=pred1
        df["pred5"]=pred5
        df["pred15"]=pred15
        df["pred25"]=pred25
        df["pred49"]=pred49

        accuracy1 = ( sum(df["LabelKo"]==df["pred1"]) / len(df["pred1"]) ) * 100
        accuracy5 = ( sum(df["LabelKo"]==df["pred5"]) / len(df["pred5"]) ) * 100
        accuracy15 = ( sum(df["LabelKo"]==df["pred15"]) / len(df["pred15"]) ) * 100
        accuracy25 = ( sum(df["LabelKo"]==df["pred25"]) / len(df["pred25"]) ) * 100
        accuracy49 = ( sum(df["LabelKo"]==df["pred49"]) / len(df["pred49"]) ) * 100

        print(f"accuracy1:{accuracy1}%")
        print(f"accuracy5:{accuracy5}%")
        print(f"accuracy15:{accuracy15}%")
        print(f"accuracy25:{accuracy25}%")
        print(f"accuracy49:{accuracy49}%")

        df.to_parquet("/home/root2/data/fish/result.parquet")
        

    task_start = EmptyOperator(task_id="start")
    task_end = EmptyOperator(task_id="end")

    load_csv = PythonOperator(
                task_id="load.csv",
                python_callable=load_csv,
            )
    predict1 = PythonOperator(
                task_id = "predict1",
                python_callable=predict,
                op_args=[1]
            )

    predict5 = PythonOperator(
                task_id = "predict5",
                python_callable=predict,
                op_args=[5]
            )

    predict15 = PythonOperator(
                task_id = "predict15",
                python_callable=predict,
                op_args=[15]
            )

    predict25 = PythonOperator(
                task_id = "predict25",
                python_callable=predict,
                op_args=[25]
            )
    predict49 = PythonOperator(
                task_id = "predict49",
                python_callable=predict,
                op_args=[49]
            )
    agg = PythonOperator(
                task_id = "agg",
                python_callable=agg,
            )

    task_start >> load_csv >> [predict1, predict5, predict15, predict25, predict49 ] >> agg >> task_end 
