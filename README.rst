****************
Version exporter
****************

Small exporter used to export version of locally installed rpm package in a centos, rhel or fedora remote server.

.. role:: bash(code)
   :language: bash

Usage
=====

This program can only work on rhel based system (ex. centos, fedora, rhel, ...)

1. Copy :bash:`config.yaml.sample` and name it :bash:`config.yaml`;
2. Modify the content of :bash:`config.yaml` to include all the package you want;
3. Modify if needed the file :bash:`docker-compose.yml`. For example if your rpm database is not in `/var/lib/rpm` you will need to find it and change the volume path;
4. Run the docker-compose: :bash:`docker-compose up -d`

Dev
===

Requirements:
- python (>=3.6)
- poetry (>=1.0.0)

Install all dependencies and enter in the virtualenv::

   poetry install
   poetry shell

Use poethepoet as a task runner::
   
   poe -h
