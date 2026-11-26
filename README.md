## Airtel Telecom Analytics 

A Data Analysis Project ,Sem 3 OJT : Airtel Subscriber data

## The Question :

We are losing nearly one subscriber in four

## Data 

We have 6 tables and a DB file which contains the data of the subscriber of artiel Telecom

## Run the Streamlit dashboard

The dashboard reads `data/raw/airtel.db` in read-only mode. Run the data-preparation
notebook first if the `customer_features` table and supporting views are missing.

```powershell
pip install -r dashboard/requirements.txt
streamlit run dashboard/app.py
```

