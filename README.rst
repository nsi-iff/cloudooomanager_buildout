CloudoooManager Buildout
=====================


Sistema operacional
-------------------

Todos os serviços são desenvolvidos sob o sistema operacional Debian 6 (Squeeze) 64 bits e seu funcionamento só
é garantido em tal sistema operacional.

Dependências do sistema
-----------------------

Para o funcionamento do serviço, é necessário que os seguintes pacotes estejam instalados no sistema: python-dev, python-setuptools, python-webunit, libxml2-dev, libxslt1-dev, python-docutils, gnuplot, e python-opencv.

Durante a instalação do serviço, ao executar o comando *make*, todas essas dependências serão devidamente instaladas.

**IMPORTANTE**: este buildout depende do *servicequeue_buildout*  e do *sam_buildout* devidamente configurados e funcionando.


Arquitetura
-----------

Como pode ser visto no pacote "nsi.cloudooo" o sistema consiste em um webservice RESTful hostiado por padrão na porta 8886
na url "http://localhost:8886/". Ele responde aos verbos POST e GET. Cada verbo correspondendo a uma ação do serviço de granularização:
POST para submeter um documento, GET para verificar o estado da granularização. Todos os verbos recebem parâmetros no formato "json",
para melhor interoperabilidade com qualquer outra ferramenta.


POST
    Recebe em um parâmetro "doc" o documento a ser convertido codificado em base64, para evitar problemas de encoding.
    Responde a requisição com as chaves onde estarão os grãos correspondentes a ele no SAM. Também pode-se passar um link
    para o documento, no parâmetro "doc_link", ou até mesmo a chave de um documento pré-armazenado no SAM, no parâmetro "sam_uid".
    No último caso, o documento precisa estar armazenado seguindo a estrutura {"doc":documento}.
    É possível enviar uma URL para receber um "callback" assim que o documento for convertido. Caso o parâmetro "callback"
    seja fornecido, ao término da conversão, um dos workers realizará uma requisição para tal URL com o verbo
    POST, fornecendo no corpo dela uma chave "doc_key", que é a chave do documento, "done" com valor verdadeiro e a
    chave "grains_keys", com a chave para acesso aos grãos, que estarão organizados em "images" e "files" (grãos do tipo tabela).
    Caso aconteça algum problema durante a granularização do documento, no callback a chave "done" terá valor falso e haverá uma chave
    "error" com valor verdadeiro, além da chave do documento, "doc_key". O sistema responde com a chave do documento, "doc_key",
    que pode ser usada para verificar se o processo daquele documento já foi concluído e também para acessar as chaves onde cada grão
    dele foi armazenado no SAM.

GET
    Também é possível receber se um determinado documento já foi convertido fazendo uma requisição do tipo GET para o servidor,
    passando como parâmetro "key" a chave do documento que é retornada pelo método POST. O retorno será uma chave
    "done", com valor verdadeiro caso os grão estejam prontos, e falso para o contrário.
    Além disso, ele pode ser usado para ter acesso às chaves dos grãos referentes ao documento, caso seja passado um único parâmetro
    "doc_key" na requisição. Seu retorno será um dicionário contendo as chaves de acesso para cada grão, separadas nas chaves
    "images" e "files" do dicionário.


Bibliotecas
-----------

- Cyclone
Cyclone é um fork do Tornado, um webserver criado originalmente pelo FriendFeed,
que foi comprado pelo Facebook mais tarde e teve seu código aberto. É baseado no
Twisted e tem suporte a bancos noSQL, como MongoDB e Redis, XMLRPC e JsonRPC,
além de um cliente HTTP assíncrono.

- txredisapi
É uma API que promove acesso assíncrono ao banco de dados Redis, feita em cima do Twisted.

- nsi.multimedia
API criada pelo próprio NSI para granularização de documentos usando o Cloudooo.


Instalação
----------

Assumindo que o SAM já está devidamente instalado e iniciado na máquina, criar
um ambiente virtual usando Python 2.6, sem a opção no-site-packages e com o
mesmo ativado executar “make” na pasta do buildout.


Executando
----------

Na pasta do buildout do SAM, executar: “bin/samctl start”, adicionar um usuário
para o CloudoooManager com: “bin/add-user.py test test” e na pasta do buildout
do CloudoooManager executar: “bin/cloudooomanager_ctl start”.

É indispensável que o serviço de filas esteja ligado para que tudo funciona
perfeitamente. Para instalar o serviço de filas basta baixar o *servicequeue_buildout*
e rodar o  utilitário *make* contido nele. Depois, basta executar o comando
*bin/rabbitmq-server -detached* para ativar o serviço de filas.

Tudo deverá estar funcionando normalmente (caso contrário me mande um e-mail).


Rodando os testes
-----------------

Com o SAM em execução, adicionar o usuário “test”, com senha “test” nele
utilizando: “bin/add-user.py test test”. Depois na raiz do buildout do
VideoConvert executar: “make test”.


Testes de carga
---------------

Com o serviço de armazenamento (SAM) rodando e com o usuário "test", com senha "test", basta executar
*make load_test* para rodar os testes de carga. Automaticamente, depois que o teste terminar, um relatório em HTMl
será gerado na pasta *tests/funkload_report* com informações e gráficos relevantes sobre o tete.

Para alterar configurações do servidor de granularização e do teste de carga, ver arquivo *tests/CloudoooManagerBench.conf*.
