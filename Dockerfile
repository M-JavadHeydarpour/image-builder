FROM bitnami/kaniko:1.15.0 AS kaniko

FROM python:3.9-slim AS runtime

LABEL maintainer="djawad.dev@gmail.com"

COPY --from=kaniko /kaniko /kaniko

ENV PATH $PATH:/usr/local/bin:/kaniko
ENV DOCKER_CONFIG /kaniko/.docker/
ENV DOCKER_CREDENTIAL_GCR_CONFIG /kaniko/.config/gcloud/docker_credential_gcr_config.json

RUN mkdir -p /data/codes
