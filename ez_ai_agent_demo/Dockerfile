FROM python:3.12
COPY . /app
WORKDIR /app
RUN pip install -r requirements.txt -i https://pypi.tuna.tsinghua.edu.cn/simple
RUN mkdir -p /app/ez
EXPOSE 5555
CMD ["python", "start_server.py"]