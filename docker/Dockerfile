FROM ubuntu:20.04

# Install Packages
RUN apt-get update
RUN apt-get install -y software-properties-common
RUN apt-get install -y python3-dev python3-setuptools python3-pip libboost-all-dev

RUN apt-get install -y vim 
RUN pip3 install ipdb

RUN python3 -m pip install scons