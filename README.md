# Projeto Estoque

Este é um projeto de gerenciamento de estoque desenvolvido com Flask, que inclui funcionalidades como login de usuários, cadastro de produtos, registro de saídas de produtos e outras operações relacionadas a estoque.

## Estrutura do Projeto

```
D:.
|   README.md
|   config.py
|   requirements.txt
|   run.py
|   
+---app
|   |   __init__.py        # Inicialização da aplicação Flask
|   |   models.py          # Definição das Models (Banco de Dados)
|   |   routes.py          # Rotas da aplicação
|   |   
|   +---static
|   |   +---js
|   |   |       tabulator.js      # Scripts JavaScript
|   |   |       
|   |   \---css
|   |           style.css         # Estilos CSS
|   |
|   +---__pycache__               # Arquivos gerados automaticamente
|   |
|   \---templates
|           base.html             # Template base para outras páginas
|           login.html            # Página de login
|           dashboard.html        # Dashboard principal
|           registrar.html        # Cadastro de usuários
|           cadastrar_produtos.html # Formulário para cadastro de produtos
|           editar_produto.html   # Edição de produtos
|           editar_usuario.html   # Edição de usuários
|           saida_produto.html    # Registro de saída de produtos
|           403.html              # Página de erro 403 (Acesso negado)
|           401.html              # Página de erro 401 (Não autorizado)
|
+---instance
|       db.sqlite3               # Banco de dados SQLite para fins de estudo apenas
```

## Funcionalidades

### Autenticação de Usuários

- Login e logout com controle de acesso baseado em nível de permissão.
- Página de login estilizada.
- Controle de acessos não autorizados (páginas 401 e 403).

### Gerenciamento de Produtos

- Cadastro, edição e exclusão de produtos.
- Registro de saídas de produtos com histórico.

### Dashboard

- Visão geral do estoque, incluindo alertas de produtos com quantidade abaixo do mínimo.

## Tecnologias Utilizadas

### Backend

- Flask
- Flask-SQLAlchemy
- Flask-Login

### Frontend

- HTML5, CSS3 (com Bootstrap para estilização)
- JavaScript
- Tabulator.js para tabelas dinâmicas.

### Banco de Dados

- SQLite (configuração básica).

## Como Configurar e Rodar

1. **Clone o Repositório**

    ```bash
    git clone https://github.com/estudoalexandre/projeto-estoque-flask.git
    cd projeto-estoque-flask
    ```

2. **Crie o Ambiente Virtual (Opcional)**

    ```bash
    python -m venv venv
    source venv/bin/activate  # Linux/Mac
    venv\Scripts\activate     # Windows
    ```

3. **Instale as Dependências**

    ```bash
    pip install -r requirements.txt
    ```

4. **Configure o Banco de Dados( Opcional o uso de Alembic )**

    Inicialize o sistema de migração e crie as tabelas no banco:

    ```bash
    flask db init
    flask db migrate -m "Inicializando o banco"
    flask db upgrade
    ```

5. **Rode a Aplicação**

    ```bash
    python run.py
    ```

    A aplicação estará disponível em [http://127.0.0.1:5000](http://127.0.0.1:5000).

## Páginas Disponíveis

- **Login:** `/login`
- **Dashboard:** `/dashboard`
- **Cadastrar Produtos:** `/cadastrar_produtos`
- **Editar Produto:** `/editar_produto/<produto_id>`
- **Registrar Saída de Produto:** `/saida_produto/<produto_id>`
- **Registrar Usuário:** `/registrar`
