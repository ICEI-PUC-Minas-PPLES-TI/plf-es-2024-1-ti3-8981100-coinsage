# Caso de uso: **RF20 - Cadastrar compra de criptomoedas**

## Precondições

O sistema deve ter coletado e armazenado informações das criptomoedas da binance.


## Fluxo principal

> No caso de uso "Cadastro de Compra de Criptomoedas", inicialmente o usuário acessa a tela específica para este fim. Em seguida, ele seleciona a criptomoeda que deseja registrar a compra. Posteriormente, o usuário é solicitado a informar a data, hora e minuto da aquisição da criptomoeda. Além disso, ele deve informar a quantidade de criptomoedas que foram adquiridas. Por fim, para concluir o processo, o usuário clica no botão "Cadastrar compra".

#### Passos

1. O usuário acessa a tela de cadastro de compra de criptomoedas.
2. O usuário seleciona a criptomoeda que deseja registrar a compra.
3. O usuário informa a data, hora e minuto da aquisição.
4. O usuário informa a quantidade de criptomoedas adquiridas.
5. O usuário clica no botão "Cadastrar compra".

## Fluxo alternativos

### FLA01 - Usuário informa a cotação da criptomoeda no momento da compra

>No fluxo alternativo "Usuário informa a cotação da criptomoeda no momento da compra", entre os passos 3 e 4, após o sistema buscar a cotação da criptomoeda na data e hora informada, o usuário tem a opção de informar manualmente a cotação da criptomoeda em dólares no momento da compra, substituindo a cotação que foi obtida pelo sistema. O restante do processo segue conforme o fluxo principal.


### FLA02 - Usuário retoma a cotação da criptomoeda no momento da compra

>No fluxo alternativo "Usuário retoma a cotação da criptomoeda no momento da compra", entre os passos 3 e 4, após o usuário ter informado manualmente a cotação da criptomoeda no momento da compra, ele tem a opção de clicar no botão "Retomar preço automático". Ao fazer isso, o sistema retoma a cotação da criptomoeda que havia sido buscada inicialmente na data e hora informada. O restante do processo segue conforme o fluxo principal.


### FLA03 - Cadastrar compra pelo valor e não pela quantidade comprada

>No fluxo alternativo "Cadastrar compra pelo valor e não pela quantidade comprada", no passo 4, o usuário tem a opção de selecionar "Valor Comprado" em vez de informar a quantidade de criptomoedas adquiridas. Nesse caso, o usuário informa o valor comprado em dólares. O restante do processo segue conforme o fluxo principal.
