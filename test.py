from crawl import fetch_job_details
import json
import pandas as pd

# 테스트할 Job ID 리스트 (예: 수집된 ID들)
df = pd.read_csv("random_50_jobs.csv")
print(df.columns)

