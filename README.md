# Automação Web em Python.

## Objetivo do Projeto:

- Automatizar uma demanda repititiva, referente a documentos/processos contidos em um software web, para tramitação de processos/documentos, da Câmara dos Deputados de Brasília - DF.
- Estes processos/documentos autorizam o acesso a Câmara, fora do horário de expediente, sendo que todos estes possuem data de validade.
- Com o vencimento destas autorizações, os documentos/processos devem ser arquivados, com o objetivo de facilitar a consulta de autorizações vigentes.
- Desta forma, o objetivo deste software é arquivar todas as autorizações que estão vencidas, tendo sua utilização exclusiva a Câmara dos Deputados de Brasília - DF.

## Autor:

- [@cezzarCz](https://github.com/cezzarCz)

## Licença

[MIT](https://choosealicense.com/licenses/mit/)

## Passo a passo para utilização:

A partir deste ponto presume-se que:

- 1°: O computador do usuário já tenha o executável do software.
- 2°: O computador do usuário está conectado a intranet da Câmara dos Deputados de Brasília - DF.
- 3°: O ponto do usuário ja tem acesso a pasta "ACESSO.UT", onde ficam as autorizações mencionadas anteriormente.
- 4°: Para que a automação seja efetiva, os processos/documentos referentes, devem ter atrelados a si, tarefas
  anteriormente criada (No própio EDOC), sendo que é através do prazo de conclusão desta tarefa (O mesmo prazo de validade da autorização),
  que o software consegue analisar se ainda esta vigente ou não.

- A utilização do software em si, de certa forma é simples, sendo constituído por:
- 1° Executar a automação.
- 2° Aguardar o Google Chrome abrir e se redirecionar para a página de login do EDOC.
- 3° Neste momento o usuário tem exatos 2 minutos para inserir o usuário e senha, e clicar no botão "Entrar".
  > Caso o tempo se esgote e o login não seja feito, o programa será automaticamente interrompido.
- 4° Após o login, a automação irá começar a busca por autorizações vencidas.
  > Nesta etapa existem dois possíveis cenários, desconsiderando erros referentes ao própio EDOC, sendo eles:
        - 1°: A automação não encontra nem uma autorização vencida, abre um popup indicando que não haviam
        autorizações vencidas.
        - 2°: A automação encontra uma autorização vencida (Com a data menor do que no dia atual), e faz todo
        o processo de arquivar a mesma. Repetindo esta ação até que todas as autorizações vencidas sejam arquivadas.
        Assim mostrando o popup indicando quantas autorizações foram arquivadas.
- 5° Ao fim do arquivamento, o usuário deve clicar no botão do popup aberto, para encerrar definitivamente o programa.

OBS: Com a conclusão bem sucedida do software, o mesmo cria um arquivo de logs na área de trabalho, chamado 'arquivamento',
sendo que neste arquivo estará contido informações sobre cada execução, separados por data e hora.

# Dependências do Software

Dependências necessárias para o funcionamento correto da automação.
Preferencialmente este software deve ser executado com a conexão da intranet da Câmara dos Deputados - Brasília - DF.

## Ambiente de Execução

- **Python**: O software foi desenvolvido e testado utilizando a versão `3.11.9` do Python.
- [https://www.python.org/downloads/](https://www.python.org/downloads/)

## Bibliotecas e Pacotes

- **Selenium**: Versão `4.12.0`. O Selenium é uma ferramenta poderosa para automação de navegadores web:

  ```bash
  pip install selenium==4.12.0
  ```
