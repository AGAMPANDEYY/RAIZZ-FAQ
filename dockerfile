FROM python:3.11.0

WORKDIR /faq-chatbot

COPY ./requirements.txt /faq-chatbot/requirements.txt

RUN pip install --no-cache-dir --upgrade -r /faq-chatbot/requirements.txt

RUN useradd -m -u 1000 user

USER user 

ENV HOME=/home/user \ 
    PATH=/home/user/.local/bin:$PATH

WORKDIR $HOME/app

COPY --chown=user . $HOME/app

CMD ["uvicorn", "app:app","--host","0.0.0.0","--port","7860"]
