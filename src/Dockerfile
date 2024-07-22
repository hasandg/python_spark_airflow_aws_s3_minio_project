# VERSION 0.0.1
# AUTHOR: hasandg
# DESCRIPTION: Airflow container with Python, SPARK and AWS binaries.
# BUILD: docker build --rm -t docker-airflow-custom:latest .


FROM ${AIRFLOW_IMAGE_NAME:-apache/airflow:2.9.3}
LABEL maintainer=hasandg

# Never prompts the user for choices on installation/configuration of packages
ENV DEBIAN_FRONTEND noninteractive
ENV TERM linux

SHELL ["/bin/bash", "-o", "pipefail", "-e", "-u", "-x", "-c"]

USER root

# to make ps command work in /usr/local/spark/bin/load-spark-env.sh
RUN apt-get update && apt-get install -y procps && rm -rf /var/lib/apt/lists/*

USER airflow

# Airflow
ARG AIRFLOW_VERSION=2.9.3
ARG AIRFLOW_HOME=/usr/local/airflow
ARG AIRFLOW_DEPS=""
ARG PYTHON_DEPS=""
ARG SPARK_VERSION=3.5.1
ARG HADOOP_VERSION=3
ENV AIRFLOW_GPL_UNIDECODE yes


COPY requirements.txt /requirements.txt


RUN pip install -r /requirements.txt \
    && pip install apache-airflow-providers-apache-spark
 #   && pip install apache-airflow-providers-amazon


## Begin JAVA installation
USER root

# Java is required in order to spark-submit work
# Install OpenJDK-17
#RUN curl -LO https://download.java.net/java/GA/jdk17.0.2/dfd4a8d0985749f896bed50d7138ee7f/8/GPL/openjdk-17.0.2_linux-x64_bin.tar.gz && \
RUN curl -LO https://download.java.net/java/GA/jdk17.0.2/dfd4a8d0985749f896bed50d7138ee7f/8/GPL/openjdk-17.0.2_linux-aarch64_bin.tar.gz && \
    tar xvf openjdk-17.0.2_linux-aarch64_bin.tar.gz && \
    rm openjdk-17.0.2_linux-aarch64_bin.tar.gz && \
    #tar xvf openjdk-17.0.2_linux-x64_bin.tar.gz && \
    mkdir --parents /usr/lib/jvm/ && \
    mv jdk-17.0.2 /usr/lib/jvm/

# Setup JAVA_HOME
ENV JAVA_HOME /usr/lib/jvm/jdk-17.0.2
RUN export JAVA_HOME

ENV PATH $PATH:$JAVA_HOME/bin

## Finished JAVA installation

## SPARK files and variables

ENV SPARK_HOME /usr/local/spark

# Spark submit binaries and jars (Spark binaries must be the same version of spark cluster)
RUN cd "/tmp" && \
    curl -LO "https://archive.apache.org/dist/spark/spark-${SPARK_VERSION}/spark-${SPARK_VERSION}-bin-hadoop${HADOOP_VERSION}.tgz" && \
    tar -xvzf "spark-${SPARK_VERSION}-bin-hadoop${HADOOP_VERSION}.tgz" && \
    mkdir -p "${SPARK_HOME}/bin" && \
    mkdir -p "${SPARK_HOME}/assembly/target/scala-2.13/jars" && \
    cp -a "spark-${SPARK_VERSION}-bin-hadoop${HADOOP_VERSION}/bin/." "${SPARK_HOME}/bin/" && \
    cp -a "spark-${SPARK_VERSION}-bin-hadoop${HADOOP_VERSION}/jars/." "${SPARK_HOME}/assembly/target/scala-2.13/jars/" && \
    rm "spark-${SPARK_VERSION}-bin-hadoop${HADOOP_VERSION}.tgz"

RUN chmod 755 ${SPARK_HOME}/bin/*

# Create SPARK_HOME env var
RUN export SPARK_HOME
ENV PATH $PATH:/usr/local/spark/bin


COPY spark/assets/jars/** /usr/local/spark/assembly/target/scala-2.13/jars/

# Install Apache Hadoop
ARG HADOOP_VERSION=2.10.1
ENV HADOOP_HOME=/opt/hadoop
ENV HADOOP_CONF_DIR=/etc/hadoop
ENV MULTIHOMED_NETWORK=1
ENV USER=root

RUN HADOOP_URL="https://archive.apache.org/dist/hadoop/common/hadoop-$HADOOP_VERSION/hadoop-$HADOOP_VERSION.tar.gz" \
    && curl 'https://dist.apache.org/repos/dist/release/hadoop/common/KEYS' | gpg --import - \
    && curl -fSL "$HADOOP_URL" -o /tmp/hadoop.tar.gz \
    && curl -fSL "$HADOOP_URL.asc" -o /tmp/hadoop.tar.gz.asc \
    && gpg --verify /tmp/hadoop.tar.gz.asc \
    && mkdir -p "${HADOOP_HOME}" \
    && tar -xvf /tmp/hadoop.tar.gz -C "${HADOOP_HOME}" --strip-components=1 \
    && rm /tmp/hadoop.tar.gz /tmp/hadoop.tar.gz.asc \
    && ln -s "${HADOOP_HOME}/etc/hadoop" /etc/hadoop \
    && mkdir "${HADOOP_HOME}/logs" \
    && mkdir /hadoop-data

ENV PATH="$HADOOP_HOME/bin/:$PATH"

# Install Apache Hive
ARG HIVE_VERSION=3.1.3
ENV HIVE_HOME=/opt/hive
ENV HIVE_CONF_DIR=/etc/hive

RUN HIVE_URL="https://archive.apache.org/dist/hive/hive-${HIVE_VERSION}/apache-hive-${HIVE_VERSION}-bin.tar.gz" \
    && curl -fSL 'https://downloads.apache.org/hive/KEYS' | gpg --import - \
    && curl -fSL "$HIVE_URL" -o /tmp/hive.tar.gz \
    && curl -fSL "$HIVE_URL.asc" -o /tmp/hive.tar.gz.asc \
    && gpg --verify /tmp/hive.tar.gz.asc \
    && mkdir -p "${HIVE_HOME}" \
    && tar -xf /tmp/hive.tar.gz -C "${HIVE_HOME}" --strip-components=1 \
    && rm /tmp/hive.tar.gz /tmp/hive.tar.gz.asc \
    && ln -s "${HIVE_HOME}/etc/hive" "${HIVE_CONF_DIR}" \
    && mkdir "${HIVE_HOME}/logs"

ENV PATH="$HIVE_HOME/bin/:$PATH"


USER ${AIRFLOW_UID}


EXPOSE 8060 5555 8793

