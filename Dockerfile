FROM ubuntu:focal
ENV DEBIAN_FRONTEND noninteractive
RUN apt update -y && apt install -y pypy3 samtools
ADD base-counts-count.py    /scripts/base-counts-count.py
ADD base-counts-count       /usr/bin/base-counts-count
ADD base-counts-merge.py    /scripts/base-counts-merge.py
ADD base-counts-merge       /usr/bin/base-counts-merge
ADD base-counts-kld.py      /scripts/base-counts-kld.py
ADD base-counts-kld         /usr/bin/base-counts-kld
