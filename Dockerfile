FROM ubuntu:latest
RUN apt-get update && apt-get install -y curl ca-certificates
RUN curl -fsSL https://clis.cloud.ibm.com/install/linux | sh
RUN ibmcloud plugin install tg
COPY regreso.py /app/
WORKDIR /app
RUN chmod +x regreso.py
CMD ["python3", "regreso.py"]
