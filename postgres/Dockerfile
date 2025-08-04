FROM postgres:17.5

ENV LANGUAGE=ru_RU.utf8
ENV LANG=ru_RU.utf8
ENV LC_ALL=ru_RU.utf8

RUN apt-get update && \
    apt-get install locales -y  && \ 
    sed -i 's/# ru_RU.UTF-8 UTF-8/ru_RU.UTF-8 UTF-8/g' /etc/locale.gen && \
    locale-gen ru_RU.utf8 && \ 
    update-locale LANG=ru_RU.utf8 LANGUAGE=ru_RU.utf8 LC_ALL=ru_RU.utf8 && \
    rm -rf /var/vib/apt/lists/*

WORKDIR /db

EXPOSE 5432
