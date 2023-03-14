FROM ubuntu:20.04 as builder

ENV DEBIAN_FRONTEND=noninteractive

RUN apt update \
    && apt install -y --no-install-recommends \
    build-essential \
    python3 \
    python3-pip \
    libgl1-mesa-glx libglib2.0-0 libsm6 libxrender1 libxext6\
    && apt clean \
    && rm -rf /var/cache/apt/archives \
    && rm -rf /var/lib/apt/lists

RUN mkdir -p /code
 
WORKDIR /code

ADD . /code

RUN python3 -m pip install --upgrade pip 
RUN pip install poetry
RUN pip install pytest
RUN poetry install
RUN pip cache purge
RUN poetry cache clear --all pypi

CMD ["poetry", "run", "streamlit", "run", "./faster_grad_cam/home.py"]