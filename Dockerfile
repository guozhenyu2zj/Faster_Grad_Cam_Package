FROM python:3.8

RUN mkdir -p /code
 
WORKDIR /code

ADD . /code
 
RUN pip install poetry
RUN poetry install
 
# 运行服务
CMD ["streamlit", "./faster_grad_cam/home.py"]