
# API Monitoramento de Resíduos

Este repositório contém a implementação de uma API para o monitoramento de resíduos. Siga as instruções abaixo para configurar e executar o projeto.

## Passos para execução do projeto

### 1. Clonar o repositório
Clone o repositório para seu ambiente local com o comando:

```bash
git clone https://github.com/KaiqueVA/API_Monitoramento_de_residuos.git
```

### 2. Criação do ambiente virtual
Navegue até o diretório clonado:

```bash
cd API_Monitoramento_de_residuos
```

Crie um ambiente virtual para isolar as dependências do projeto:

```bash
python -m venv venv
```

Ative o ambiente virtual:
- No Windows:
  ```bash
  venv\Scripts\activate
  ```
- No macOS/Linux:
  ```bash
  source venv/bin/activate
  ```

### 3. Instalar as dependências
Com o ambiente virtual ativado, instale as dependências do projeto:

```bash
pip install -r requiriments.txt
```

### 4. Executar a API
Inicie o servidor da API:

```bash
cd contentor_api
python manage.py runserver
```

### 5. Acessar o Swagger
Para acessar o Swagger, abra o navegador e vá até:

```
http://127.0.0.1:8000/swagger/
```
