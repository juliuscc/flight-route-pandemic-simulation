FROM python:3

ADD input /input
ADD lib /lib

RUN pip install networkx

CMD [ "python", "/lib/foo.py" ]
