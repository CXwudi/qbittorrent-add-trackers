FROM mcr.microsoft.com/devcontainers/base:debian
# FROM mcr.microsoft.com/devcontainers/base:jammy 

ARG DEBIAN_FRONTEND=noninteractive
ARG USER=vscode

RUN DEBIAN_FRONTEND=noninteractive \
    && apt-get update \ 
    && apt-get install -y build-essential --no-install-recommends make \
        ca-certificates \
        git \
        libssl-dev \
        zlib1g-dev \
        libbz2-dev \
        libreadline-dev \
        libsqlite3-dev \
        wget \
        curl \
        llvm \
        libncurses5-dev \
        xz-utils \
        tk-dev \
        libxml2-dev \
        libxmlsec1-dev \
        libffi-dev \
        liblzma-dev

# Python and uv installation
USER $USER
ARG HOME="/home/$USER"
ARG PYTHON_VERSION=3.12
# ARG PYTHON_VERSION=3.10

ENV PYENV_ROOT="${HOME}/.pyenv"
ENV PATH="${PYENV_ROOT}/shims:${PYENV_ROOT}/bin:${HOME}/.local/bin:${HOME}/.cargo/bin:$PATH"

RUN echo "done 0" \
    && curl https://pyenv.run | bash \
    && echo "done 1" \
    && pyenv install ${PYTHON_VERSION} \
    && echo "done 2" \
    && pyenv global ${PYTHON_VERSION} \
    && echo "done 3" \
    && curl -LsSf https://astral.sh/uv/install.sh | sh \
    && echo '[ -f $HOME/.cargo/env ] && source $HOME/.cargo/env' >> ~/.bashrc \
    && echo '[ -f $HOME/.cargo/env ] && source $HOME/.cargo/env' >> ~/.zshrc \
    && pip install --upgrade pip \
    && echo "done 4" \
    && pip install poethepoet \
    && echo "done 5"
