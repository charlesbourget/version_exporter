FROM redhat/ubi8

USER 0

ENV PYTHONPATH=/usr/lib64/python3.6/site-packages/

RUN dnf update -y && \
    dnf install python3-rpm python39 -y

RUN python3 -m pip install poetry==1.0.0

WORKDIR /opt
COPY config.yaml .

WORKDIR /version_exporter
COPY . .

EXPOSE 9998

RUN poetry install --no-root --no-dev

CMD poetry run python -m version_exporter