# syntax=docker/dockerfile:1.3
FROM python:3.9-slim

# Use the secret during build
RUN --mount=type=secret,id=git_token \
    git clone https://$GIT_TOKEN:x-oauth-basic@github.com/Edipool/chatbot_support_for_X5.git

WORKDIR /app
COPY . .

RUN tree

CMD ["python3", "baseline.py"]
