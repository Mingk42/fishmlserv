# Base Image 
FROM python:3.9
# FROM python:3.11.9-alpine3.20


# 
WORKDIR /code

#  
COPY . /code
#COPY ./requirements.txt /code/requirements.txt

# 여러번 실행 가능
RUN pip install --no-cache-dir --upgrade -r /code/requirements.txt

# 한 번 만 실행가능, 서버 실행
CMD ["uvicorn", "src.fishmlserv.main:app", "--host", "0.0.0.0", "--port", "8080"]
