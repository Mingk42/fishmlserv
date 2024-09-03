# Base Image 
# FROM python:3.9
# FROM python:3.11.9-alpine3.20
FROM datamario24/python311scikitlearn-fastapi:1.0.0

# 
WORKDIR /app

#  
#COPY . /code
COPY  src/fishmlserv/main.py /app/
#COPY  ./requirements.txt /code/
#COPY ./requirements.txt /code/requirements.txt

# 여러번 실행 가능
#RUN pip install --no-cache-dir --upgrade -r /code/requirements.txt
RUN pip install --upgrade pip
RUN pip install --no-cache-dir git+https://github.com/Mingk42/fishmlserv.git@v0.8.1/test
#RUN pip install --no-cache-dir git+https://github.com/Mingk42/fishmlserv.git@v0.8.0/Dhub

# 한 번 만 실행가능, 서버 실행
#CMD ["uvicorn", "src.fishmlserv.main:app", "--host", "0.0.0.0", "--port", "8080"]
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8080"]
