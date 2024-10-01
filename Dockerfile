FROM public.ecr.aws/docker/library/python:3.11-slim-bookworm as base

RUN pip install --no-cache "poetry>1.7,<1.8" 
RUN poetry config virtualenvs.create false

WORKDIR /code

COPY ./pyproject.toml ./poetry.lock* ./

RUN poetry install --no-dev --no-interaction --no-ansi --no-root -vv \
    && rm -rf /root/.cache/pypoetry

# Dev Container
FROM base as devcontainer

RUN apt-get update \
    && apt-get install -y \
    curl \
    git \
    unzip \
    vim \
    wget \
    ffmpeg \
    gcc \
    python3-dev \
    sqlite3 \
    && rm -rf /var/lib/apt/lists/* \
    && apt-get clean 

RUN curl "https://awscli.amazonaws.com/awscli-exe-linux-$(uname -m).zip" -o "awscliv2.zip" \
    && unzip awscliv2.zip \
    && ./aws/install --update \
    && echo 'complete -C '/usr/local/bin/aws_completer' aws' >> ~/.bashrc \
    && rm -rf awscliv2.zip ./aws

RUN poetry install --all-extras --no-interaction --no-ansi --no-root -vv \
    && rm -rf /root/.cache/pypoetry

# Download the Chinook SQL script
RUN wget https://raw.githubusercontent.com/lerocha/chinook-database/master/ChinookDatabase/DataSources/Chinook_Sqlite.sql -O /code/Chinook_Sqlite.sql

# Create the Chinook.db database
RUN sqlite3 /code/Chinook.db ".read /code/Chinook_Sqlite.sql"

WORKDIR /workspace

CMD ["tail", "-f", "/dev/null"]
