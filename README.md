# Dspace Covemg

## 1. Estrutura de diretórios disponiblizada:
    a. dspace-src: Diretório com os códigos fonte do Dspace, personalizados para a distribuição da COVEMG. Estes arquivos devem ser compilados em um servidor Tomcat ou similar, conforme Instruções de Instalação
    b. backup-db: Diretório com o backup do banco de dados mais recente.
    c. assetstore: Diretório onde estão armazenados os arquivos atualmente existentes no repositório da COVEMG. Um diretório similar a este é criado durante a instalação padrão e deve ser substituído após a instalação completa do repositório e restauração do banco de dados.

## 2. Resumo da instalação atual:
    a. Dspace:
        1. DSpace version: 6.3
        2. SCM revision: db2c2e7e0c973434cc6e680128496651cdd27eed
        3. SCM branch: master
        4. OS: Red Hat Enterprise Linux Server release 7.5 (Maipo) - x86_64
        5. Banco de dados: psql (PostgreSQL) 9.2.24
        6. Applications:
            1. Discovery: enabled.
            2. JRE: Oracle Corporation version 1.8.0_191
            3. Ant version: Apache Ant(TM) version 1.9.13 compiled on July 10 2018
            4. Maven version: 3.5.4
            5. DSpace home: /web/dspace
    b. Configuration
        1. Base DSpace URL:     http://www.comissaodaverdade.mg.gov.br
        2. Nome hospedeiro DSpace: www.comissaodaverdade.mg.gov.br
        3. Nome do site: DSpace COVEMG
        4. Nome da base de dados: org.dspace.storage.rdbms.hibernate.postgres.DSpacePostgreSQL82Dialect
        5. URL da base de dados: jdbc:postgresql://localhost:5432/dspace
        6. JDBC Driver: PostgreSQL JDBC Driver
        7. Número máximo de DB Connections in Pool:     8192
        8. SMTP Servidor de correio: smtp.gmail.com
        9. para o endereço de e-mail: comissaoverdademg@gmail.com
        10. Comentários do destinatário: comissaoverdademg@gmail.com
        11. Administração geral da página e-mail: comissaoverdademg@gmail.com
    c. Java Runtime
        1. Java Runtime Environment Version: 1.8.0_191
        2. Java Runtime Environment Vendor: OpenJDK 64-Bit Server VM

## 3. Instruções de Instalação:
    a. A melhor forma de instalar um ambiente Dspace é seguindo o tutorial oficial (https://wiki.duraspace.org/display/DSDOC6x/Installing+DSpace). Uma cópia deste manual pode ser encontrada no arquivo manual_instalação.pdf.
    b. Após a criação da base de dados e do usuário dspace (Item 4.3, subitem 4 do manual), será necessário trocar a variável db.password, do arquivo local.cfg dentro do diretório dspace-src/dspace/config

## 4. Sobre o diretório assetstore:
    a. Com o objetivo de melhor aproveitar os arquivos enviados pelos usuários, e para garantir maior segurança dos mesmos, o Dspace renomeia os arquivos enviados e os organiza dentro de uma estrutura de diretórios própria, seguindo uma série de hashs.
    b. Para fazer a relação entre arquivos e itens, é utilizada a estrutura relacional da base de dados conforme explicado na página:
        1. https://wiki.duraspace.org/display/DSDOC6x/Storage+Layer#StorageLayer-BitstreamStore
        2. Uma cópia da estrutura de banco utilizada pelo Dspace se encontra no arquivo dspace6-schema.png
