FROM python:3.10
ADD ./requirements.txt requirements.txt
RUN apt-get update
RUN apt-get install -y ca-certificates && apt-get install -y htop mc
RUN update-ca-certificates -v
RUN pip3 install --upgrade pip && pip3 install -r requirements.txt

EXPOSE 5000
#CMD ["bash"]
CMD ["flask", "run", "--host=0.0.0.0"]