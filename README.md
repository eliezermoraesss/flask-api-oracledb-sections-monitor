
# 🧠 Oracle Kill Sessions Monitor

![Python](https://img.shields.io/badge/Python-3.11-blue?logo=python)
![Flask](https://img.shields.io/badge/Flask-2.3-black?logo=flask)
![Bootstrap](https.md.io/badge/Bootstrap-5.3-purple?logo=bootstrap)
![Oracle](https://img.shields.io/badge/Oracle-Database-red?logo=oracle)
![License](https://img.shields.io/badge/License-MIT-green)

---

## 📘 Sobre o Projeto

O **Oracle Kill Sessions Monitor** é uma aplicação web desenvolvida em **Python (Flask)** para **monitorar e gerenciar sessões ativas do banco de dados Oracle em tempo real**.

A ferramenta exibe todas as sessões de usuários conectados, mostrando informações como:
- SID, SERIAL, USERNAME, MACHINE, EVENT, TEMPO DE EXECUÇÃO, entre outras colunas;
- Possibilidade de **matar sessões individuais** ou **todas de uma vez**;
- Monitoramento automático a cada segundo via **APS Scheduler**, com **auto kill** quando o limite configurado é ultrapastado (por padrão, 20 sessões).

É ideal para **DBAs e equipes de suporte** que precisam visualizar e controlar sessões em tempo real sem depender de scripts SQL manuais.

---

## ⚙️ Funcionalidades Principais

✅ Monitoramento em tempo real das sessões ativas no Oracle  
✅ Ação manual para matar uma sessão específica  
✅ Ação global para matar todas as sessões  
✅ Atualização automática da tela (refresh a cada 3 segundos)  
✅ Auto Kill automático ao atingir 20 sessões ativas  
✅ Visualização amigável com **Bootstrap 5.3**  
✅ Separação de camadas entre aplicação Flask e camada de banco de dados (`db.py`)

---

## 🧩 Estrutura do Projeto

```
OracleKillSessionsMonitor/
│
├── app.py                  # Aplicação Flask principal
├── db.py                   # Módulo para conexão e execução de queries Oracle
├── requirements.txt        # Dependências do projeto
├── .env                    # Variáveis de ambiente (usuário, senha, host, etc)
├── .venv/                  # Ambiente virtual Python
│
├── templates/
│   └── index.html          # Interface web responsiva
│
└── README.md               # Este arquivo
```

---

## 🧰 Tecnologias Utilizadas

| Categoria | Tecnologias |
|------------|--------------|
| Linguagem  | **Python 3.11+** |
| Framework Web | **Flask 2.3** |
| Banco de Dados | **Oracle Database (cx_Oracle / oracledb)** |
| Interface | **Bootstrap 5.3** |
| Scheduler | **APScheduler** |
| Template Engine | **Jinja2** |

---

## 🚀 Como Executar o Projeto

### 1️⃣ Clonar o repositão
```bash
git clone https://github.com/SEU_USUARIO/OracleKillSessionsMonitor.git
cd OracleKillSessionsMonitor
```

### 2️⃣ Criar e ativar ambiente virtual
```bash
python -m venv .venv
# Windows
.venv\Scriptsctivate
# Linux / Mac
source .venv/bin/activate
```

### 3️⃣ Instalar dependências
```bash
pip install -r requirements.txt
```

### 4️⃣ Configurar variáveis de ambiente
Crie um arquivo **.env** na raiz com os dados da conexão Oracle:
```env
ORACLE_USER=system
ORACLE_PASSWORD=senha123
ORACLE_DSN=192.168.0.100:1521/xe
```

### 5️⃣ Executar o servidor Flask
```bash
python app.py
```

Acesse no navegador:  
👉 [http://localhost/5000](http://localhost/5000)

---

## 🖥️ Interface Web

A aplicação apresenta uma interface limpa e responsiva, com:
- Tabela de sessões Oracle
- Botão vermelho para matar todas as sessões
- Badge dinâmica mostrando o número de sessões (verde, amarela, vermelha conforme o volume)
- Auto refresh a cada 3 segundos

---

## 🧠 Lógica de Funcionamento

1. A cada segundo, o **APS Scheduler** executa a query em `gv$session` e `gv$process`;
2. Os resultados são atualizados em cache (`last_result`);
3. O template `index.html` renderiza esses dados;
4. O botão **Kill** executa o comando `ALTER SYSTEM KILL SESSION '<sid>,<serial>' IMMEDIATE`;
5. Se o total de sessões ≥ 20, o sistema executa o **auto kill** automaticamente.

---

## 🧾 Exemplo de Query Usada

```sql
SELECT 'ALTER SYSTEM KILL SESSION '|| ''''||s.sid||','||s.serial#||'''' ||' immediate;' AS KILL,
       s.username, s.machine, s.event, s.status, s.program
FROM gv$session s, gv$process p
WHERE s.paddr = p.addr
  AND s.status = 'ACTIVE'
  AND s.username IS NOT NULL
  AND TYPE <> 'BACKGROUND';
```

---

## 🧑‍💻 Autor

**Eliezer Moraes**  
Desenvolvedor de Software & Analista de Sistemas  

[![GitHub](https://img.shields.io/badge/GitHub-EliezerMoraes-black?logo=github)](https://github.com/SEU_USUARIO)
[![LinkedIn](https://img.shields.io/badge/LinkedIn-EliezerMoraes-blue?logo=linkedin)](https://www.linkedin.com/in/SEU_PERFIL)

---

## 📜 Licença

Este projeto está licenciado sob a **MIT License** – veja o arquivo [LICENSE](LICENSE) para mais detalhes.

---

## 🧩 Próximos Passas (Roadmap)

- [ ] Adicionar filtro de sessões por usuário  
- [ ] Implementar gráficos de consumo de recursos  
- [ ] Adicionar logs e auditoria das sessões mortas  
- [ ] Notificações automáticas via e-mail ou Telegram  
- [ ] Containerização com Docker  

---

⭐ Se este projeto te ajudou, **deixa uma estrela no repositão**!
