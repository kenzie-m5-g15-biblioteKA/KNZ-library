# KNZ Library

O objetivo desse desafio é construir uma aplicação que faz a gestão de uma biblioteca.

## 🚀 Começando

Essas instruções permitirão que você obtenha uma cópia do projeto em operação na sua máquina local para fins de desenvolvimento e teste.

Consulte **[Implantação](#-implanta%C3%A7%C3%A3o)** para saber como implantar o projeto.

### 📋 Pré-requisitos

De que coisas você precisa para instalar o software e como instalá-lo?

```
Editor de texto (IDE) preferencialmente VScode pois foi nele que a aplicação foi desenvolvida
Uma ferramenta de teste e depuração de APIs para testes (Opicional)
```

### 🔧 Instalação

Uma série de exemplos passo-a-passo que informam o que você deve executar para ter um ambiente de desenvolvimento em execução.

Clonar o Repositório :

```
Clique no botão (<>code) e copie e chave SSH
```

Salvar uma copia do projeto em sua máquina:

```
Abra o diretorio onde será salvo o projeto e abra o terminal nesse diretório
Rode o comando git clone (chave SSH copiada)
Após isso você terá uma copia totalmente editavel de todo o projeto em sua maquina
```

## 📦 Implantação

Procedimentos para rodar o projeto localmente 

Criando o ambiente virtual

```
Na raiz do projeto abra o terminal e crie o ambiente virtual com o comando python -m venv venv
Em seguida entre nesse ambiente com um dos comandos:
.\venv\Scripts\activate # windows
source ./venv/bin/activate # linux
```

Instalando as dependências necessárias

```
Na raiz do projeto abra o terminal e instale as dependências do projeto com o comando make install
```
Manipulando o arquivo .env

```
Na raiz do projeto crie um arquivo chamado .env e dentro dele crie as variáveis de ambiente seguindo o padrão do arquivo .env.example

Configure suas variáveis de ambiente com suas credenciais do PostgresSQL e um novo banco de dados para estar utilizando no projeto.
```

executando as migrates

```
Na raiz do projeto abra o terminal e execute as migrações com o comando make migrate
```

## 🛠️ Construído com

Ferramentas e tecnologias usadas na criação do projeto

* [Django](https://www.djangoproject.com) - O framework web usado
* [Python](https://www.python.org) - Linguagem de programação
* [PostgreSQL](https://www.postgresql.org) - Gerenciador de banco de dados
* [Render](https://www.render.com) - Serviço de hospedagem
* [Insomnia](https://insomnia.rest) - Software para debug de requisições HTTP
* [VScode](https://code.visualstudio.com) - Editor de texto (IDE)






## ✒️ Autores

A API de gestão de biblioteca foi desenvolvida por uma equipe de desenvolvedores altamente qualificados. Aqui estão os desenvolvedores responsáveis pelo projeto:

*  [Rafael Rocha](https://github.com/Rafaelgot10)
*  [Hanna Boppe](https://github.com/hboppe)
*  [Maksuel Nascimento](https://github.com/mk-nascimento)
*  [Diego Carvalho](https://github.com/Diegaum87)
  
Se você tiver alguma dúvida, sugestão ou feedback sobre a API,
sinta-se à vontade para entrar em contato com qualquer um dos desenvolvedores mencionados acima.
Eles terão prazer em ajudar e ouvir suas opiniões.
