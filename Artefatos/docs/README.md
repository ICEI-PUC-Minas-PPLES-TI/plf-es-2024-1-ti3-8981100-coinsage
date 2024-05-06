# Documento de Visão

## Projeto
**CoinSage** - Sistema de Análise de Criptomoedas

## Autores
- Frederico Martins Rodrigues
- João Gabriel Amorim Pádua
- José Victor Mendes Dias
- Kimberly Liz Spencer Lourenço
- Rubens Marcelo Ramos dos Santos

## Fornecedor(es) de Requisitos
George (george@ficticio.com) - Engenheiro e Investidor

## Descrição do Problema
George tem formação em engenharia civil e também trabalha com investimentos. Atualmente realiza com frequência a análise das diversas criptomoedas (cerca de 388 moedas) por meio de planilhas no excel. A análise manual de criptomoedas é um processo trabalhoso e demorado, que envolve acompanhamento constante do mercado e avaliação de uma grande quantidade de dados. Além disso, mudanças no mercado ocorrem regularmente, tornando difícil e fatigante analisar e acompanhar todas as informações relevantes em tempo real. Dessa forma, acaba realizando análises mais simples, não muito completas quanto gostaria, devido a essa constante oscilação do mercado e ao volume de dados.

## Descrição Geral da Solução (Escopo)
Desenvolver um software que automatize o processo de análise de criptomoedas, facilitando a identificação das moedas com maior potencial de valorização. O software deve ser capaz de analisar as criptomoedas disponíveis em uma corretora específica, aplicar critérios técnicos para selecionar as moedas mais promissoras, gerar relatórios em formato “xlsx” que auxiliem na tomada de decisões de compra e venda.
Além dessa análise principal sobre todas as criptomoedas, o sistema deve apresentar uma interface que mostre informações e acompanhe dados relacionados às moedas que foram compradas. Essa funcionalidade permitirá o registro de dados como data da compra, quantidade adquirida, valor da moeda na data da compra, entre outros. Essa interface de armazenamento de informações irá colaborar no acompanhamento eficiente das transações realizadas, proporcionando uma visão detalhada do histórico de compras e auxiliando o usuário na gestão.


## Fora do Escopo
- Análise de outros tipos de investimentos que não sejam criptomoedas.
- Execução automática de operações de compra e venda de criptomoedas.

## Usuários
Investidores de criptomoedas, tanto iniciantes quanto experientes, buscam uma ferramenta que facilite a análise e o acompanhamento do mercado de criptomoedas utilizando uma técnica específica de análise.

## Requisitos Funcionais
<!-- Use these on the Sprint column -->
<!-- <span style="background-color: green;">Sprint 1</span>
<span style="background-color: brown;">Sprint 2</span>
<span style="background-color: blue;">Sprint 3</span>
<span style="background-color: orange;">Sprint 4</span>
<span style="background-color: grey;">Sprint 5</span> -->

<!-- Use these on Pronto column -->
<!-- Pronto ✅ -->
<!-- Não Pronto ❌ -->

| **ID** | **Descrição do Requisito**                                                                                                                                                            | **Prioridade** | **Complexidade** | **Sprint** | **Pronto** |
| ------ | ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- | -------------- | ---------------- | ---------- | ---------- |
| RF01   | O usuário deve ser capaz de visualizar as criptomoedas com valorização semanal > 10% e a porcentagem de valorização para cada.                                                        | Alta           | Alta             |            |            |
| RF02   | O usuário deve ser capaz de visualizar os setores das criptomoedas filtrados por aqueles que possuem pelo menos 10 moedas.                                                            | Alta           | Alta             |            |            |
| RF03   | O usuário deve ser capaz de visualizar os rankings das criptomoedas.                                                                                                                  | Alta           | Alta             |            |            |
| RF04   | O usuário deve ser capaz de visualizar o valor de mercado das criptomoedas em bilhões de dólares.                                                                                     | Alta           | Alta             |            |            |
| RF05   | O usuário deve ser capaz de visualizar as criptomoedas ordenadas pela porcentagem de  valorização semanal de modo decrescente.                                                        | Alta           | Baixa            |            |            |
| RF06   | O usuário deve ser capaz de visualizar a data e hora da última análise realizada pelo sistema.                                                                                        | Baixa          | Média            |            |            |
| RF07   | O usuário deve ser capaz de visualizar o preço atual da criptomoeda.                                                                                                                  | Alta           | Baixa            |            |            |
| RF08   | O usuário deve ser capaz de visualizar o requisito RF01, RF02, RF03, RF04, RF05, RF06, RF07 no formato xlsl.                                                                          | Alta           | Alta             |            |            |
| RF09   | O usuário deve ser capaz de visualizar quando ocorreu valorização no volume diário, a data e a quantidade nesse dia.                                                                  | Alta           | Alta             |            |            |
| RF10   | O usuário deve ser capaz de visualizar a quantidade de volume diário no dia anterior à valorização de volume.                                                                         | Média          | Média            |            |            |
| RF11   | O usuário deve ser capaz de visualizar a relação percentual entre o volume diário na valorização e o volume diário no dia anterior.                                                   | Média          | Baixa            |            |            |
| RF12   | O usuário deve ser capaz de visualizar se houve superior a 200% nessa relação percentual do RF11.                                                                                     | Baixa          | Baixa            |            |            |
| RF13   | O usuário deve ser capaz de visualizar o requisito RF09, RF10, RF11, RF12 no formato xlsl.                                                                                            | Alta           | Média            |            |            |
| RF14   | O usuário deve ser capaz de visualizar o preço semanal de abertura e de fechamento para o momento atual da análise.                                                                   | Alta           | Alta             |            |            |
| RF15   | O usuário deve ser capaz de visualizar o valor do EMA8 semanal para o momento atual da análise.                                                                                       | ?              | ?                |            |            |
| RF16   | O usuário deve ser capaz de visualizar se o EMA8 é menor que o preço de fechamento e maior que o de abertura.                                                                         | Alta           | Baixa            |            |            |
| RF17   | O usuário deve ser capaz de visualizar médias se as móveis diárias (8,21,50,200) estão alinhadas.                                                                                     | Alta           | Alta             |            |            |
| RF18   | O usuário deve ser capaz de visualizar os requisitos RF14, RF15, RF16, RF17 no formato xlsl.                                                                                          | Alta           | Média            |            |            |
| RF19   | O usuário deve ser capaz de visualizar (xlsl) as variações de preço em períodos específicos de 1 ano, 180 dias, 90 dias, 30 dias e 7 dias.                                            | Baixa          | Média            |            |            |
| RF20   | O usuário deve ser capaz de cadastrar suas criptomoedas e os detalhes de sua aquisição (data, quantidade, moeda, valor de compra).                                                    | Alta           | Média            |            |            |
| RF21   | O usuário deve ser capaz de visualizar seu histórico de moedas ativas em sua carteira e os detalhes da aquisição (data, quantidade, moeda, valor de compra).                          | Alta           | Baixa            |            |            |
| RF22   | O usuário deve ser capaz de converter suas criptomoedas ativas em sua carteira para outras moedas.                                                                                    | Baixa          | Alta             |            |            |
| RF23   | O usuário deve ser capaz de excluir de sua carteira dados da compra de uma moeda.                                                                                                     | Alta           | Baixa            |            |            |
| RF24   | O usuário deve ser capaz de visualizar o requisito RF21 no formato xlsx.                                                                                                              | Alta           | Alta             |            |            |
| RF25   | O usuário deve ser capaz de visualizar(xlsl) para cada criptomoeda ativa em sua carteira os lucros (%) mensais e preço atual para cada cripto para no momento da análise da carteira. | Alta           | Alta             |            |            |
| RF26   | O usuário deve ser capaz de visualizar(xlsl) a data (atual) da análise da carteira ao realizar download.                                                                              | Alta           | Baixa            |            |            |

## Requisitos Não Funcionais

| **ID** | **Descrição do Requisito**                                                                  | **Prioridade** | **Complexidade** | **Sprint** | **Pronto** |
| ------ | ------------------------------------------------------------------------------------------- | -------------- | ---------------- | ---------- | ---------- |
| RNF01  | O sistema deve realizar a análise de todas as criptomoedas em 3 horas.                      | Baixa          | Alta             |            |            |
| RNF02  | O sistema deve ser capaz de ser executado no navegador Chrome.                              | Alta           | Baixa            |            |            |
| RNF03  | O sistema realizar armazenamento de dados no banco de dados.                                | Baixa          | Média            |            |            |
| RNF04  | O sistema deve usar dados disponíveis na API da Binance e da CoinMarketCap.                 | Alta           | Média            |            |            |
| RNF05  | O usuário deve ser capaz de visualizar a análise do Bitcoin sempre fixa no topo da análise. | Alta           | Baixa            |            |            |
