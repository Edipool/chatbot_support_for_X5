FROM python:3.9-slim

RUN apt-get update && apt-get install -y git

RUN --mount=type=secret,id=git_token \
    bash -c 'GIT_TOKEN=$(cat /run/secrets/git_token) && git clone https://$GIT_TOKEN:x-oauth-basic@github.com/Edipool/chatbot_support_for_X5.git'

WORKDIR /chatbot_support_for_X5/backend/src/advanced

RUN pip install --no-cache-dir -r requirements.txt

EXPOSE 8082
