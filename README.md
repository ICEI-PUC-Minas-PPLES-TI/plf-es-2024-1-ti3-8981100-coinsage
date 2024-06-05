Here's the updated README with the execution guide for both the deployed API and website:

---

[![CI - Backend Code Quality](https://github.com/ICEI-PUC-Minas-PPLES-TI/plf-es-2024-1-ti3-8981100-coinsage/actions/workflows/ci-backend.yaml/badge.svg)](https://github.com/ICEI-PUC-Minas-PPLES-TI/plf-es-2024-1-ti3-8981100-coinsage/actions/workflows/ci-backend.yaml)

# CoinSage

O CoinSage é um software projetado para automatizar e simplificar a análise de criptomoedas. Utilizando dados da [Binance](https://binance.com/), o CoinSage aplica critérios técnicos para identificar as moedas com maior potencial de valorização, fornecendo relatórios detalhados que orientam decisões de compra e venda.

Além disso, o CoinSage oferece uma interface que permite aos usuários acompanhar suas transações e gerenciar seu portfólio de criptomoedas com facilidade. Com o CoinSage, os investidores podem ter uma visão clara do histórico de suas compras e fazer gestão eficiente de seus investimentos.

## Alunos integrantes da equipe

* [Frederico Martins Rodrigues](https://github.com/fredmrodrigues)
* [João Gabriel Amorim Pádua](https://github.com/jgapadua)
* [José Victor Mendes Dias](https://github.com/zezit)
* [Kimberly Liz Spencer Lourenço](https://github.com/kspencerl)
* [Rubens Marcelo Ramos dos Santos](https://github.com/rubensm33)

## Professores responsáveis

* Eveline Alonso Veloso
* Lucas Henrique Pereira
* Pedro Pongelupe Lopes

## Instruções de utilização

<details>
<summary>Instruções de utilização (Execução Local)</summary>
</br>

**Pré-requisitos**

- Docker: [Windows](https://docs.docker.com/desktop/install/windows-install/) ou [Mac](https://docs.docker.com/desktop/install/mac-install/) ou [Linux](https://docs.docker.com/desktop/install/linux-install/)
- Docker Compose: [Guia de instalação](https://docs.docker.com/compose/install/)

**Obtendo uma Chave de API CoinMarketCap**

1. Visite a documentação da API CoinMarketCap: [CMC Documentação](https://coinmarketcap.com/api/documentation/v1/#section/Quick-Start-Guide)
2. Siga o guia de início rápido para criar uma conta e obter uma chave de API.
3. Depois de fazer login, navegue até o painel da sua chave de API.
4. Copie sua chave de API. Você precisará dela mais tarde para configurar as variáveis de ambiente.

**Clonando o Repositório**

Se você não tiver o código-fonte do CoinSage, clone-o usando Git:

```bash
git clone https://github.com/ICEI-PUC-Minas-PPLES-TI/plf-es-2024-1-ti3-8981100-coinsage/
```

**Configurando o Ambiente**

1. Crie um arquivo `.env` na pasta [Codigo/backend](./Codigo/backend/) do projeto.
2. Adicione as seguintes variáveis de ambiente ao arquivo `.env`, substituindo os marcadores de posição pelos seus valores reais:

   ```
   DATABASE_USER=seu_nome_de_usuario_do_banco_de_dados
   DATABASE_PASSWORD=sua_senha_do_banco_de_dados
   DATABASE_NAME=banco_de_dados_coinsage
   DATABASE_PORT=5432
   SERVER_HOST=localhost  # Ajuste se necessário
   SERVER_PORT=8000
   SERVER_WORKERS=4     # Ajuste com base nos recursos do seu sistema
   DEBUG=true           # Defina como false para produção
   ENVIRONMENT=DEV
   CMC_API_KEY=sua_chave_de_api_coinmarketcap
   ```

**Executando a Aplicação**

1. Abra um terminal no diretório do projeto.
2. Exporte as variáveis de ambiente do arquivo `.env`:
   1. Dentro da pasta [Codigo/backend](./Codigo/backend/), execute o seguinte comando:
      1. No Windows:
         ```bash
         Get-Content .env | ForEach-Object { $_ -replace "`n", "`0" } | ForEach-Object { $_ -replace "`r", "" } | ForEach-Object { $env:$_ }
         ```
      2. No Linux/Mac:
         ```bash
         export $(cat .env | xargs)
         ```
      3. Se você estiver usando um terminal diferente, ajuste o comando conforme necessário.

3. Execute o seguinte comando para iniciar os serviços usando Docker Compose na pasta [Codigo](./Codigo/):

   ```bash
   docker-compose up -d
   ```

   - A flag `-d` desliga os processos, permitindo que eles sejam executados em segundo plano.

**Acessando a Aplicação**

1. Depois que os contêineres estiverem em execução, você poderá acessar o front-end do CoinSage em seu navegador da web em:

   ```
   http://localhost:80
   ```

**Usando a API**

Acessar a documentação da API em:

   ```
   http://localhost:8000/docs
   ```
</details>

<details>
<summary>Instruções de utilização (API e Website Implantados)</summary>
</br>

**Acessando a Aplicação Implantada**

1. Acesse o site CoinSage em seu navegador da web:
> [FrontEnd](https://coinsage-dev.vercel.app/)

**Usando a API Implantada**

A documentação da API implantada pode ser acessada em:
>[API](https://coinsage-dev-api.onrender.com/docs)

</details>
