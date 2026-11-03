from dotenv import load_dotenv
load_dotenv()
from fastapi import FastAPI, Query
from .client.rq_client import queue
from .queue.worker import process_query


app=FastAPI()

@app.get('/')
def root():
    return {"status":"Server is up and running"}

@app.post('/chat')
def chat(
        query: str=Query(... , description="Chat Query from user to be processed by the RAG system")
):
    job= queue.enqueue(process_query, query)

    return {"status":"Query has been enqueued for processing", "job_id": job.id}

@app.get('/job_status')
def get_Result(job_id:str = Query(..., description="Job ID to fetch the result of the processed query")):
    job=queue.fetch_job(job_id=job_id)
    result=job.return_value()

    return {"result": result}