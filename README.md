# fishmlserv

### Deploy
![image](https://github.com/user-attachments/assets/b2966e38-55dc-4e07-ba71-ee6accc98640)


### Run
```bash
$ uvicorn src.fishmlserv.main:app --reload  # dev
$ uvicorn src.fishmlserv.main:app --host 0.0.0.0 --port 1234    # customize host, port
```

### Docker
```bash
$ sudo docker build -t <tag name>
$ sudo docker run -d --name <container name> -p 80:1234 <image name> 
```