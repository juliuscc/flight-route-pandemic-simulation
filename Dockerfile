# run to build: docker build --tag pandemic .
# run to start: docker run pandemic 

FROM python:3

RUN pip install networkx

ADD input /input
ADD lib /lib

CMD [ "python", "/lib/index.py" ]
