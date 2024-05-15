

import io
from fastapi import FastAPI,HTTPException, Request
from typing import List
from pydantic import BaseModel
from model import generate_response, eval_tokenizer, model



app=FastAPI(title="RAIZZ-FAQ-Bot")

class Query(BaseModel):
    query_prompt:str

class response(BaseModel):
    response:str

#api endpoints

@app.get("/")

def read_root():
  return{"message: Welcome to the FAQ Bot!"}

@app.post("/chat")

def chat(message:Query):

    model_input = eval_tokenizer(message , return_tensors="pt").to("cuda")
    model.eval()
    with torch.no_grad():
        response = (eval_tokenizer.decode(model.generate(**model_input, max_new_tokens=500)[0], skip_special_tokens=True))
        #out = output.split(":")[-1]
    return{"response":response}


@app.post("/chatbot", response_model=response,status_code=200)

async def make_prediction(request:Query):
    try:
        prompt=request.query_prompt
        model_input = eval_tokenizer(prompt, return_tensors="pt").to("cuda")
        with torch.no_grad():
           model_answer = (eval_tokenizer.decode(model.generate(**model_input, max_new_tokens=500)[0], skip_special_tokens=True))
          #out = output.split(":")[-1]
           return response(response=model_answer)
    except Exception as e:
        raise HTTPException(status_code=500,detail=str(e))