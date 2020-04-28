FROM python:3.8

WORKDIR /application

# Install deps all in one step
RUN apt-get update -y && \
  apt-get install -y \
    apt-transport-https \
    build-essential \
    ca-certificates \
    curl \
    git \
    gnupg \
    software-properties-common \
    wget && \
  # Get all of the signatures we need all at once.
  curl -fsSL https://packages.cloud.google.com/apt/doc/apt-key.gpg | apt-key add - && \
  # IAM Authenticator for EKS
  curl -fsSLo /usr/bin/aws-iam-authenticator https://amazon-eks.s3-us-west-2.amazonaws.com/1.10.3/2018-07-26/bin/linux/amd64/aws-iam-authenticator && \
  chmod +x /usr/bin/aws-iam-authenticator && \
  # Add additional apt repos all at once
  echo "deb http://packages.cloud.google.com/apt cloud-sdk-$(lsb_release -cs) main"               | tee /etc/apt/sources.list.d/google-cloud-sdk.list && \
  echo "deb http://apt.kubernetes.io/ kubernetes-xenial main"                                     | tee /etc/apt/sources.list.d/kubernetes.list       && \
  # Install second wave of dependencies
  apt-get update -y && \
  apt-get install -y \
    kubectl && \
  echo "[global]" >> /etc/pip.conf && \
  echo "index-url = https://artifactory.grubhub.com/artifactory/api/pypi/pypi-repos/simple" >> /etc/pip.conf && \
  echo "index = https://artifactory.grubhub.com/artifactory/api/pypi/pypi-repos" /etc/pip.conf && \
  pip install awscli --upgrade && \
  pip install tox && \
  # Clean up the lists work
  rm -rf /var/lib/apt/lists/*

# Passing --build-arg PULUMI_VERSION=vX.Y.Z will use that version
# of the SDK. Otherwise, we use whatever get.pulumi.com thinks is
# the latest
ARG PULUMI_VERSION=v2.0.0

# Install the Pulumi SDK, including the CLI and language runtimes.
RUN if [ "$PULUMI_VERSION" = "latest" ]; then \
    curl -fsSL https://get.pulumi.com/ | bash; \
  else \
    curl -fsSL https://get.pulumi.com/ | bash -s -- --version $(echo $PULUMI_VERSION | cut -c 2-); \
  fi && \
  mv ~/.pulumi/bin/* /usr/bin

# Install dependencies first so we can cache them independently of application code.
ADD ./requirements.txt /application/
RUN pip3 install -r /application/requirements.txt

# And now install the application.
ADD . /application/

# Use our custom entrypoint to login before running the requested Pulumi command.
ENTRYPOINT ["/application/entrypoint.sh"]
