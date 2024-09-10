FROM python:3.9-slim
WORKDIR /app
RUN pip install --upgrade pip && pip install pipenv
COPY Pipfile Pipfile.lock ./
RUN pipenv install
COPY . .
EXPOSE 5000
ENV HOST=0.0.0.0
CMD ["pipenv", "run", "python", "main.py"]