FROM debian:11

WORKDIR /root/app

ENV DEBIAN_FRONTEND noninteractive

ENV USER root

EXPOSE 5901
EXPOSE 6080

USER root

COPY build /root/build/

RUN cd /root/build &&\
    cp /etc/apt/sources.list /etc/apt/sources.list.backup &&\
    sed -i s/deb.debian.org/mirrors.cloud.tencent.com/g /etc/apt/sources.list &&\
    sed -i s/security.debian.org/mirrors.cloud.tencent.com/g /etc/apt/sources.list &&\
    apt update &&\
    apt install -y unzip curl wget python3 python3-pip tigervnc-standalone-server fonts-droid-fallback &&\
    wget -c https://packages.microsoft.com/repos/edge/pool/main/m/microsoft-edge-stable/microsoft-edge-stable_100.0.1185.29-1_amd64.deb &&\
    dpkg -i microsoft-edge-stable_100.0.1185.29-1_amd64.deb || true &&\
    apt install -f -y &&\
    wget -c https://msedgedriver.azureedge.net/100.0.1185.29/edgedriver_linux64.zip &&\
    unzip edgedriver_linux64.zip &&\
    mv msedgedriver /usr/bin/msedgedriver &&\
    pip3 config set global.index-url https://pypi.tuna.tsinghua.edu.cn/simple &&\
    pip3 install -r /root/build/requirements.txt &&\
    apt autoremove -y &&\
    apt autoclean &&\
    rm -rf /root/build

COPY app /root/app/

COPY --chmod=777 xstartup /root/.vnc/

COPY --chmod=777 docker-entrypoint.sh /usr/bin/

CMD ["docker-entrypoint.sh"]
