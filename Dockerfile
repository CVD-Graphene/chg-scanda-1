FROM python:3.9-alpine as base
WORKDIR /app
RUN apk update && apk add
RUN apt-get update && apt-get upgrade -y
RUN apt-get install -y libvips
#RUN apk add --no-cache build-base
#RUN apk add --no-cache postgresql-libs
#RUN apk add --no-cache --virtual .build-deps gcc musl-dev postgresql-dev
COPY requirements.txt .
ENV CRYPTOGRAPHY_DONT_BUILD_RUST 1
#RUN apk add --no-cache libffi-dev openssl-dev python3-dev
CMD apt-key adv --keyserver keyserver.ubuntu.com --recv-keys 04EE7237B7D453EC 648ACFD622F3D138
CMD echo "deb http://deb.debian.org/debian buster-backports main" | sudo tee -a /etc/apt/sources.list.d/buster-backports.list
CMD apt update
CMD apt install -t buster-backports libseccomp2
RUN pip install -r requirements.txt --privileged

FROM base as release
EXPOSE 7002
WORKDIR /app/code
CMD [ \
"python", \
"app.py" \
]
