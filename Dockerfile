# run first time to build: docker build --tag pandemic .
# run to start application: docker run pandemic 

FROM python:3

ADD input /input
ADD lib /lib

RUN pip install networkx

CMD [ "python", "/lib/foo.py" ]
