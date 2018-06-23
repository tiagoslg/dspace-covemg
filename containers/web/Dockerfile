FROM ubuntu:16.04
#install base requirements and clear apt/lists
RUN apt-get update && \
    apt-get install -y openjdk-8-jdk && \
    apt-get install -y ant && \
    apt-get install -y wget && \
    apt-get install -y git && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/ && \
    rm -rf /var/cache/oracle-jdk8-installer \
    && rm -rf /var/lib/apt/lists/*;
#create and export JAVA_HOME
ENV JAVA_HOME /usr/lib/jvm/java-8-openjdk-amd64/
RUN export JAVA_HOME
#maven install
RUN wget -O /opt/apache-maven.tar.gz http://mirror.nbtelecom.com.br/apache/maven/maven-3/3.5.3/binaries/apache-maven-3.5.3-bin.tar.gz
RUN tar xzvf /opt/apache-maven.tar.gz -C /opt/
RUN ln -s /opt/apache-maven-3.5.3/ /opt/apache-maven
ENV PATH /opt/apache-maven/bin:$PATH
#dspace install
ENV DSPACE /dspace
ENV DSPACE_INSTALLER $DSPACE/dspace-src
WORKDIR $DSPACE_INSTALLER
RUN useradd -m dspace
RUN chown dspace $DSPACE
# RUN wget -O $DSPACE_INSTALLER/dspace-6.2.tar.gz https://github.com/DSpace/DSpace/releases/download/dspace-6.2/dspace-6.2-src-release.tar.gz
# RUN tar xzvf $DSPACE_INSTALLER/dspace-6.2.tar.gz -C $DSPACE_INSTALLER
# ADD containers/web/local.cfg $DSPACE_INSTALLER/dspace-6.2-src-release/dspace/config/
# RUN ls -l $DSPACE_INSTALLER/dspace-6.2-src-release/dspace/config/local.cfg 
# WORKDIR $DSPACE_INSTALLER/dspace-6.2-src-release/
# RUN mvn package