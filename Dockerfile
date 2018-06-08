FROM oraclelinux:7-slim

RUN yum-config-manager --enable ol7_software_collections --enable ol7_optional_latest && \
    yum -y install gcc rh-python36 && \
    rm -rf /var/cache/yum/*

# Copy in the source
COPY requirements/base.txt /requirements.txt 

# Install build deps, then run `pip install`, then remove unneeded build deps all in a single step. 
RUN scl enable rh-python36 -- pip install -r /requirements.txt

COPY animportantdate/. /usr/src/app/
WORKDIR /usr/src/app

RUN scl enable rh-python36 -- python manage.py migrate

EXPOSE 8000

ENTRYPOINT ["scl", "enable", "rh-python36", "--"]
CMD ["python", "manage.py", "runserver", "0.0.0.0:8000", "--insecure"]
