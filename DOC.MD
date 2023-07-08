<h2>Descrição</h2><br>
<p>
A API de gestão de biblioteca é um conjunto de endpoints que permite o empréstimo, devolução e controle de livros.
Os estudantes podem visualizar seu histórico de empréstimos e receber notificações sobre a disponibilidade dos livros.
Os colaboradores podem cadastrar novos livros, emprestá-los e verificar o histórico de empréstimos dos estudantes.
A API também oferece recursos adicionais, como avaliações de livros, feed de livros recentes e envio de lembretes e cobranças.
Ela pode ser adaptada para ser utilizada por várias bibliotecas simultaneamente.
</p><br>

# Documentação da API

URL da aplicação:
http://localhost:8000

Alguma das tecnologias utilizadas.

- [Django Rest Framework:](https://) Uma extensão do Django que simplifica a criação de APIs RESTful.
- [Django ORM:](https://) Uma camada de abstração de banco de dados que permite interagir com o banco de dados usando código Python.
- [djangorestframework-simplejwt ](https://)Biblioteca para autenticação JWT
- [drf-spectacular ](https://)Biblioteca para gerar automaticamente documentação Swagger/OpenAPI para APIs Django Rest Framework.
- [gunicorn](https://)Um servidor HTTP Python WSGI para implantar aplicativos Django.
- [whitenoise](https://)Biblioteca para servir arquivos estáticos de forma eficiente em aplicativos Django.
- [sqlparse](https://)Analisador de SQL em Python.
- [PyYAML](https://)Biblioteca para análise e emissão de dados YAML em Python.
- [pytz](https://)Biblioteca para trabalhar com fusos horários em Python.
- [Swagger](https://)OpenAPI para APIs Django Rest Framework.
- [psycopg2-binary](https://yarnpkg.com/package/zod) Adaptador de banco de dados PostgreSQL para Python.<br><br>

## Diagrama de Entidade de Relacionamentos (DER)<br>

<img src="der KNZ.PNG" alt="Descrição da imagem" width="750px" height="450px" /><br><br>

### Instalando Dependências

Clone o projeto em sua máquina e instale as dependências utilizando o comando:

```
pip install
```

### Variáveis de Ambiente

crie um arquivo **.env**, copiando o formato do arquivo **.env.example**:

```
.env.example .env
```

Configure suas variáveis de ambiente com suas credenciais do PostgresSQL e um novo banco de dados para estar utilizando no projeto.

### Migrations

Execute as migrations com o comando:

```
python manage.py makemigrations
python manage.py migrate

```

## **Usuário**

## Endpoints users

| Método | Rota       | Descrição                                          |
| ------ | ---------- | -------------------------------------------------- |
| POST   | /users     | Criação de um usuário.                             |
| GET    | /users     | Lista todos os usuários.                           |
| GET    | /users/:id | Lista um usuário, usando seu ID como parâmetro.    |
| PATCH  | /users/:id | Atualiza um usuário, usando seu ID como parâmetro. |
| DELETE | /users/:id | Deleta um usuário, usando seu ID como parâmetro.   |

---

## **Books**

## Endpoints books

| Método | Rota         | Descrição                                        |
| ------ | ------------ | ------------------------------------------------ |
| POST   | /books       | Criação de um livro.                             |
| GET    | /books       | Lista todos os livros.                           |
| GET    | /books/:id   | Lista um livro, usando seu ID como parâmetro.    |
| PATCH  | /books/:id   | Atualiza um livro, usando seu ID como parâmetro. |
| DELETE | /books/:id   | Deleta um livro, usando seu ID como parâmetro.   |
| POST   | /books/login | Deleta um livro, usando username e password.     |

---

### **Criar Usuário**

### Exemplo de Request:

```
POST /users
Host: localhost:8000/api/users/
Authorization: None
Content-type: application/json
```

### Corpo da Requisição:

```json
{
  "username": "Diego",
  "password": "12345",
  "type_user": "Staff"
}
```

### Resposta da Requisição:

```json
{
	"id": 1,
	"type_user": "Staff",
	"username": "Diego",
	"email": "",
	"status": "Active",
	"Books": [],
	"Created_at": "2023-07-05T20:17:53.866213Z"
}

OBS: Não tem retorno de senha na resposta.
```

### **Listar todos Usuários**

```
GET /users
Host: http://localhost:3000
Authorization: necessita do token do cliente para acesso
Content-type: application/json
```

### Corpo da Requisição:

```
Não possui corpo na requisição.
```

### Resposta da Requisição:

```json
[
  {
    "count": 2,
    "next": null,
    "previous": null,
    "results": [
      {
        "id": 1,
        "type_user": "Staff",
        "username": "Diego",
        "email": "diego@mail.com",
        "status": "Active",
        "Books": [],
        "lending": [],
        "Created_at": "2023-07-08T14:45:24.011341Z",
        "unblocked_date": null
      },
      {
        "id": 2,
        "type_user": "Staff",
        "username": "Rafael",
        "email": "rafaelgot@mail.com",
        "status": "Active",
        "Books": [],
        "lending": [],
        "Created_at": "2023-07-08T14:53:13.548696Z",
        "unblocked_date": null
      }
    ]
  }
]
```

### 1.3. **Listar Usuários por id**

### Exemplo de Request:

```
GET /users/:id
Host: http://localhost:8000
Authorization: necessita do token do cliente para acesso
Content-type: application/json
```

### Corpo da Requisição:

```
Não possui corpo na requisição.
```

### Resposta da Requisição:

```json
{
	"id": 1,
	"type_user": "Staff",
	"username": "Diego",
	"email": "diego@mail.com",
	"Books": [],
	"lending": [],
	"Created_at": "2023-07-08T14:45:24.011341Z",
	"assessments": []
}
".
```

### **Atualizar Usuários por id**

### Exemplo de Request:

```
PATCH /users/:id
Host: http://localhost:8000
Authorization: necessita do token do usuário para acesso
Content-type: application/json
```

### Corpo da Requisição:

```json
{
  "type_user": "Student"
}
```

### Resposta da Requisição:

```json
{
  "id": 1,
  "type_user": "Student",
  "username": "Diego",
  "email": "diego@mail.com",
  "Books": [],
  "lending": [],
  "Created_at": "2023-07-08T14:45:24.011341Z",
  "assessments": []
}
```

### **Deletar Usuários por id**

### Exemplo de Request:

```
DELETE /users/:id
Host: http://localhost:8000
Authorization: necessita do token do usuário para acesso
Content-type: application/json
```

### Corpo da Requisição:

```
Não possui corpo na requisição.
```

### Resposta da Requisição:

```
204 no Content "nenhum corpo retornou para resposta"
```

### **Login**

### Exemplo de Request:

```
POST /login
Host: http://localhost:8000
Authorization: None
Content-type: application/json
```

### Corpo da Requisição:

```json
{
  "email": "rafael@mail.com",
  "password": "1234"
}
```

### Resposta da Requisição:

```json
{
  "token": "eyJlbWFpbCI6ImpvbmFzQG1haWwuY29tIiwiaWF0IjoxNjg2MjU2NTUzLCJleHAiOjE2ODYzNDI5NTMsInN1YiI6IjcifQ.tKRxiYJCPTaqaF--YjFlGDHoiDVdvJmkU1DC2l_zuBk"
}
```

## \*books\*\*

### Endpoints

| Método | Rota       | Descrição                                       |
| ------ | ---------- | ----------------------------------------------- |
| POST   | /books     | Criação de um livro.                            |
| GET    | /books     | Lista todos os livros.                          |
| GET    | /books/:id | Lista um livro, usando seu ID como parâmetro    |
| PATCH  | /books/:id | Atualiza um livro, usando seu ID como parâmetro |
| DELETE | /books/:id | Deleta um livro, usando seu ID como parâmetro   |

---

### **Criar Livro**

### Exemplo de Request:

```
POST /books
Host: http://localhost:8000
Authorization: necessita do token do cliente para acesso
Content-type: application/json
```

### Corpo da Requisição:

```json
{
  "title": "Aprendendo Programação do Zero",
  "author": "John Smith",
  "publishing_company": "Tech Publishing",
  "published_date": "2022-05-15"
}
```

### Resposta da Requisição:

```json
{
  "id": 1,
  "title": "Aprendendo Programação do Zero",
  "author": "John Smith",
  "published_date": "2022-05-15",
  "publishing_company": "Tech Publishing",
  "availability": "avaliable",
  "ranking": "0.00",
  "assessments": [],
  "followers": []
}
```

### **Listar todos Livros**

```
GET /books
Host: http://localhost:8000
Authorization: necessita do token do cliente para acesso
Content-type: application/json
```

### Corpo da Requisição:

```
Não possui corpo na requisição.
```

### Resposta da Requisição:

```json
[
  {
    "count": 2,
    "next": null,
    "previous": null,
    "results": [
      {
        "id": 1,
        "title": "Aprendendo Programação do Zero",
        "author": "John Smith",
        "published_date": "2022-05-15",
        "publishing_company": "Tech Publishing",
        "availability": "avaliable",
        "ranking": "0.00",
        "assessments": [],
        "followers": []
      },
      {
        "id": 2,
        "title": "Algoritmos e Estruturas de Dados em Python",
        "author": "Maria Garcia",
        "published_date": "2023-02-28",
        "publishing_company": "CodeBooks",
        "availability": "avaliable",
        "ranking": "0.00",
        "assessments": [],
        "followers": []
      }
    ]
  }
]
```

### **Listar Livros por id**

### Exemplo de Request:

```
GET /books/:id
Host: http://localhost:8000
Authorization: necessita do token do livro  para acesso
Content-type: application/json
```

### Corpo da Requisição:

```
Não possui corpo na requisição.
```

### Resposta da Requisição:

```json
{
		"id": 1,
		"title": "Aprendendo Programação do Zero",
		"author": "John Smith",
		"published_date": "2022-05-15",
		"publishing_company": "Tech Publishing",
		"availability": "avaliable",
		"ranking": "0.00",
		"assessments": [],
		"followers": []
},

```

### **Atualizar Livros por id**

### Exemplo de Request:

```
PATCH /books/:id
Host: http://localhost:8000
Authorization: necessita do token do livro para acesso
Content-type: application/json
```

### Corpo da Requisição:

```json
{
   "title": "Python",
}
```

### Resposta da Requisição:

```json
{
		"id": 1,
		"title": "Python",
		"author": "John Smith",
		"published_date": "2022-05-15",
		"publishing_company": "Tech Publishing",
		"availability": "avaliable",
		"ranking": "0.00",
		"assessments": [],
		"followers": []
},
```

### **Deletar Livro por id**

### Exemplo de Request:

```
DELETE /books/:id
Host: http://localhost:3000
Authorization: necessita do token do livro para acesso
Content-type: application/json
```

### Corpo da Requisição:

```
Não possui corpo na requisição.
```

### Resposta da Requisição:

```
204 no Content "nenhum corpo retornou para resposta"
```

### Possíveis Erros:

| 401 "detail": "No active account found with the given credentials"

| 401 "detail": "You do not have permission to perform this action."


## Desenvolvedores: 


A API de gestão de biblioteca foi desenvolvida por uma equipe de desenvolvedores altamente qualificados. Aqui estão os desenvolvedores responsáveis pelo projeto:

- https://github.com/Rafaelgot10
- https://github.com/hboppe
- https://github.com/mk-nascimento
- https://github.com/Diegaum87

Esses desenvolvedores trabalharam em estreita colaboração para projetar, implementar e testar todos os recursos da API de gestão de biblioteca.
Eles são apaixonados por desenvolvimento de software e estão comprometidos em oferecer uma solução eficiente e de alta qualidade para atender às necessidades das bibliotecas e usuários.

