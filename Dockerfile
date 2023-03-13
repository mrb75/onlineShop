# syntax=docker/dockerfile:1
FROM python:3
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1
WORKDIR /onlineShop
RUN pip install --upgrade pip
COPY requirements.txt /onlineShop/
RUN pip install -r requirements.txt
COPY . /onlineShop/


EXPOSE 8000

CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]