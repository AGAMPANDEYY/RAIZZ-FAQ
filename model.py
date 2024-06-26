from huggingface_hub import login


#loading base model

import torch
from transformers import AutoModelForCausalLM,AutoTokenizer,BitsAndBytesConfig


base_model_id = "mistralai/Mistral-7B-Instruct-v0.2"
bnb_config = BitsAndBytesConfig(
    load_in_4bit=True,
    bnb_4bit_use_double_quant=True,
    bnb_4bit_quant_type="nf4",
    bnb_4bit_compute_dtype=torch.bfloat16
)

base_model = AutoModelForCausalLM.from_pretrained(
    base_model_id,  # Mistral, same as before
    quantization_config=bnb_config,  # Same quantization config as before
    device_map="auto",
    trust_remote_code=True,
)

eval_tokenizer = AutoTokenizer.from_pretrained(
    base_model_id,
    add_bos_token=True,
    trust_remote_code=True,
)
from peft import PeftModel, PeftConfig
from transformers import AutoModelForCausalLM

peft_model_id="AgamP/results"

config=PeftConfig.from_pretrained(peft_model_id)
model= PeftModel.from_pretrained(base_model,peft_model_id)

prompt="How do i track my fitness levels?"

model.eval()

with torch.no_grad():
        def generate_response(prompt):
           model_input = eval_tokenizer(prompt , return_tensors="pt").to("cuda")
           response = (eval_tokenizer.decode(model.generate(**model_input, max_new_tokens=500)[0], skip_special_tokens=True))
           #out = output.split(":")[-1]
           return response
