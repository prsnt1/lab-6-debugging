FROM python:3.9

WORKDIR /app

COPY requirements.txt .
RUN pip3 install -r requirements.txt

COPY . .

CMD ["python3", "sharma_prashant_lab-6.py"]