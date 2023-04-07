FROM python:3.8

# update the apt package index
RUN apt-get update

ENV DISPLAY=:99

# Copy code to container
COPY . /opt/source_code/

# Setup Virtual Environment
RUN python -m venv /opt/venv
ENV PATH="/opt/venv/bin:$PATH"
RUN pip3 install --upgrade pip

# Install requirements
RUN pip3 install -r /opt/source_code/requirements.txt

ENTRYPOINT ["python3"]

CMD ["-u","/opt/source_code/main.py"]

EXPOSE 80