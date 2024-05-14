# Caso de uso: **RF20 - Cadastrar compra de criptomoedas**

## Precondições

1. O sistema deve ter coletado e armazenado informações das criptomoedas da binance.


## Fluxo principal

1. O usuário acessa a tela de cadastro de compra de criptomoedas.
2. O usuário seleciona a criptomoeda que deseja registrar a compra.
4. O usuário informa a data, hora e minuto da aquisição.
5. O sistema busca a cotação da criptomoeda na data e hora informada.
6. O usuário informa a quantidade de criptomoedas adquiridas.
7. O usuário clica no botão "Cadastrar compra".
8. O sistema armazena a transação de compra.

## Fluxo alternativos

### FLA01 - Usuário informa a cotação da criptomoeda no momento da compra

#### Passos

1. O usuário acessa a tela de cadastro de compra de criptomoedas.
2. O usuário seleciona a criptomoeda que deseja registrar a compra.
4. O usuário informa a data, hora e minuto da aquisição.
5. O sistema busca a cotação da criptomoeda na data e hora informada.
6. O usuário informa a cotação da criptomoeda no momento da compra (substituindo a cotação obtida pelo sistema).
7. O usuário informa a quantidade de criptomoedas adquiridas.
8. O usuário clica no botão "Cadastrar compra".
9. O sistema armazena a transação de compra.


### FLA02 - Usuário retoma a cotação da criptomoeda no momento da compra

#### Passos

1. O usuário acessa a tela de cadastro de compra de criptomoedas.
2. O usuário seleciona a criptomoeda que deseja registrar a compra.
3. O usuário informa a data, hora e minuto da aquisição.
4. O sistema busca a cotação da criptomoeda na data e hora informada.
5. O usuário informa a cotação da criptomoeda no momento da compra (substituindo a cotação obtida pelo sistema).
6. O usuário clica no botão "Retomar preço automático".
7. O sistema retoma a cotação da criptomoeda na data e hora informada.
8. O usuário informa a quantidade de criptomoedas adquiridas.
9. O usuário clica no botão "Cadastrar compra".
10. O sistema armazena a transação de compra.


### FLA03 - Cadastrar compra pelo valor e não pela quantidade comprada

#### Passos

1. O usuário acessa a tela de cadastro de compra de criptomoedas.
2. O usuário seleciona a criptomoeda que deseja registrar a compra.
4. O usuário informa a data, hora e minuto da aquisição.
5. O sistema busca a cotação da criptomoeda na data e hora informada.
6. O usuário seleciona a opção "Valor Comprado"
7. O usuário informa o valor comprado em dólares.
8. O usuário clica no botão "Cadastrar compra".
9. O sistema armazena a transação de compra.
