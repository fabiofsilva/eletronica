# Eletrônica

[![Django CI](https://github.com/fabiofsilva/eletronica/actions/workflows/django.yml/badge.svg)](https://github.com/fabiofsilva/eletronica/actions/workflows/django.yml)

## 📌 Descrição do projeto

**Plataforma web para consulta de diagnóstico de defeitos em equipamentos eletrônicos**, desenvolvida em **Django**, com foco em organização, escalabilidade e boas práticas de desenvolvimento.

O projeto foi estruturado para servir tanto como aplicação funcional quanto como base sólida para evolução contínua, adotando padrões modernos de configuração, integração contínua e gerenciamento de dependências.

---

## 🧰 Requisitos

- **Python 3.12**
- Git
- **PostgreSQL 18+**

### Gerenciador de dependências: `uv`

Este projeto utiliza o **uv** como gerenciador de dependências e ambientes virtuais, seguindo uma abordagem moderna e reprodutível.

> **O uv é necessário?**  
> Sim. O uso do `uv` é **recomendado** para garantir consistência entre ambientes de desenvolvimento, CI e produção.

---

## ⚙️ Instalação do uv

Caso ainda não tenha o `uv` instalado, execute:

```bash
curl -LsSf https://astral.sh/uv/install.sh | sh
```

Após a instalação, reinicie o terminal ou garanta que o `uv` esteja disponível no `PATH`:

```bash
uv --version
```

---

## 📥 Clonando o projeto

Clone o repositório a partir do GitHub:

```bash
git clone https://github.com/fabiofsilva/eletronica.git
cd eletronica
```

---

## 📦 Instalando as dependências

Crie o ambiente virtual e instale as dependências do projeto:

```bash
uv sync
```

---

## 🗂️ Arquivos de configuração (.env e settings de desenvolvimento)

O repositório já fornece **arquivos de exemplo** para facilitar a configuração do ambiente de desenvolvimento.

### 1. Arquivo `.env`

Existe um arquivo `env.example` na raiz do projeto. Ele deve ser copiado para `.env`:

```bash
cp env.example .env
```

Edite o arquivo `.env` e ajuste os valores conforme seu ambiente, especialmente as variáveis relacionadas ao PostgreSQL.

### 2. Arquivo de settings de desenvolvimento

O projeto disponibiliza um arquivo `development.example`, que contém uma configuração de settings de desenvolvimento já pré-configurada.

Copie o arquivo para o local correto:

```bash
cp development.example eletronica/settings/development.py
```

Esse arquivo será utilizado como settings de desenvolvimento, facilitando o setup local do projeto.

---

## 🔧 Configurações iniciais

### Banco de dados: PostgreSQL

A conexão com o banco de dados é feita exclusivamente por meio da variável de ambiente **`DATABASE_URL`**, declarada no arquivo `.env`.

#### Configuração via `.env`

No arquivo `.env`, configure a variável no formato:

```bash
DATABASE_URL=postgresql://usuario:senha@host:porta/nome_do_banco
```

Exemplo:

```bash
DATABASE_URL=postgresql://eletronica_user:senha_segura@localhost:5432/eletronica
```

#### Executar as migrações

Após configurar o `.env`, execute as migrações do banco de dados:

```bash
uv run python manage.py migrate
```bash
uv run python manage.py migrate
```

(Opcional) Criar um superusuário para acessar o admin do Django:

```bash
uv run python manage.py createsuperuser
```

---


## ▶️ Executando o servidor de desenvolvimento

Para iniciar o servidor local utilizando os **settings de desenvolvimento**:

```bash
uv run python manage.py runserver --settings=eletronica.settings.development
```

A aplicação estará disponível em:

```
http://127.0.0.1:8000/
```

---

## 🧪 Executando os testes

Para rodar a suíte de testes automatizados:

```bash
uv run python manage.py test --settings=eletronica.settings.test
```

---

## 🚀 Integração Contínua (CI)

O projeto utiliza **GitHub Actions** para garantir qualidade e consistência do código a cada *pull request* para a branch `master`.

O workflow **Django CI** executa automaticamente:

- ✅ **Instalação das dependências** utilizando `uv` e o arquivo `uv.lock`
- 🧹 **Linting do código** com **Ruff**, garantindo padronização e qualidade
- 🧪 **Execução dos testes automatizados** do Django

---

## 📄 Licença

Este projeto é licenciado sob a **GNU Affero General Public License (AGPL) v3**, de 19 de novembro de 2007.

Isso significa que:
- O código-fonte deve permanecer aberto
- Modificações e redistribuições devem manter a mesma licença
- Aplicações que utilizem este projeto via rede também devem disponibilizar o código-fonte correspondente

Consulte o arquivo `LICENSE` para mais detalhes.
