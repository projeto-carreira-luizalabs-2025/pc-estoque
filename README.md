# 📦 PC-Estoque

## 📄 Descrição
O PC-Estoque é um sistema de gerenciamento de estoque desenvolvido para oferecer uma solução simples, prática e eficiente no controle de produtos disponíveis em marketplaces. A aplicação permite realizar o cadastro de produtos, controlar entradas e saídas de estoque, atualizar quantidades disponíveis e visualizar informações em tempo real — garantindo maior organização, segurança e agilidade nas operações comerciais.


## 👥 Equipe de Desenvolvimento

- Elbia Simone Buglio

- Fabio Romero

- Laura Gabriely

- Victor Teixeira


## ⚙️ Configuração do Ambiente Local

- Python 3.12
- FastAPI
- Uvicorn
- Make (para automação de tarefas no Linux)
- Outras dependências listadas em requirements

## 📦 Clonando o Repositório

git clone https://github.com/projeto-carreira-luizalabs-2025/pc-estoque/tree/v1

cd pc-estoque

## 📑 Configuração no Linux 🐧

Crie o ambiente virtual:
make build-venv

Ative o ambiente virtual:
source ./venv/bin/activate

Instale as dependências do projeto:
make requirements-dev

⚠️ A partir deste ponto, todos os comandos deverão ser executados dentro do ambiente virtual ativado.

## 📑 Configuração no Windows 🪟

### **📌 1️⃣ Instalar o make via MSYS2 (se ainda não instalado)**

- Baixe o instalador do MSYS2:
  
👉 https://www.msys2.org/
- Após instalar, abra o terminal MSYS2 MSYS e execute:
pacman -Syu

pacman -S make
- Depois de instalado, você poderá usar o make no terminal MSYS2 ou adicionar o caminho do make.exe no PATH para uso em outros terminais.

### **📌 2️⃣ Criar o ambiente virtual:**

python -m venv venv

**Ativar o ambiente virtual:**

venv\Scripts\activate

**Instalar as dependências do projeto:**

pip install -r requirements\develop.txt

📌 Obs: As dependências estão organizadas na pasta requirements

## 📌 Observações
Confirme a versão do Python instalada:

python --version
- No Linux, este projeto utiliza make para automação de tarefas.
- No Windows, os comandos são executados manualmente (a não ser que você instale o make via MSYS2 como descrito acima).
  
⚠️ Certifique-se de ativar o ambiente virtual antes de executar qualquer comando relacionado ao projeto.

## ▶️ Execução

**1️⃣ Configurar as variáveis de ambiente**

Copie o arquivo de variáveis de desenvolvimento:

- **Linux**
cp devtools/dotenv.dev .env
- **Windows**
copy devtools\dotenv.dev .env

**2️⃣ Subir a API**

Com o ambiente virtual ativado e as variáveis configuradas, execute:

make run-dev

ou, se preferir executar manualmente:

uvicorn app.api_main:app --reload

## 📖 Acesse a documentação interativa da API:

- Swagger UI: http://localhost:8000/api/docs
- ReDoc: http://localhost:8000/api/redoc

## 📬 Contribuições e Atualizações  

**Fluxo para contribuição:**

1. Realize um **fork** do repositório.
2. Crie uma **branch descritiva** para a sua feature ou correção.
3. Submeta via **Pull Request**.
4. Aguarde o **Code Review** pela equipe de desenvolvimento.
5. Após aprovação, a alteração será integrada ao código principal.
