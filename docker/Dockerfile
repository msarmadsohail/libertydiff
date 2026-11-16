FROM python:3.12-trixie@sha256:cad37dd20c7cac861af9003af8796d03ea7a998ec1e3a664429740fc9d7d2691

ARG NGSPICE_VERSION=44.2+ds-1
ARG CHARLIB_COMMIT=987e90f5286b11c3a548749f93b689a7b8723003
ARG MAGIC_COMMIT=2c6d97b2f21003fa1778d5658eb02b32724399ab
ARG PYSPICE_COMMIT=da81c4d013c9140c8833711be05c52299b260e16

RUN apt-get update && apt-get install -y --no-install-recommends \
    ngspice=${NGSPICE_VERSION} libngspice0-dev=${NGSPICE_VERSION} \
    build-essential git ca-certificates tcl-dev tk-dev libcairo2-dev \
    libx11-dev libxext-dev libxrender-dev libxft-dev libfontconfig1-dev \
    libfreetype6-dev libreadline-dev zlib1g-dev libllvm18 \
    && rm -rf /var/lib/apt/lists/*

RUN git clone https://github.com/RTimothyEdwards/magic.git /opt/magic-src \
    && cd /opt/magic-src && git checkout ${MAGIC_COMMIT} \
    && ./configure --prefix=/opt/magic && make -j4 && make install

RUN git clone https://github.com/stineje/CharLib.git /opt/charlib \
    && cd /opt/charlib && git checkout ${CHARLIB_COMMIT} \
    && pip install . \
    && pip install --force-reinstall --no-cache-dir --no-binary pyspice \
       "pyspice @ git+https://github.com/infinitymdm/PySpice.git@${PYSPICE_COMMIT}"

ENV PATH=/opt/magic/bin:$PATH
WORKDIR /work
CMD ["sh", "-c", "ngspice --version | head -2; magic --version; charlib --help | head -2"]
