# 🎯 Auditor de Atendimento

Sistema automatizado para análise de qualidade de atendimento ao cliente baseado em transcrições de conversas.

## 📋 Funcionalidades

- **Análise de Empatia**: Identifica palavras positivas e empáticas
- **Avaliação de Tempo**: Analisa tempo de resposta entre mensagens
- **Relatório Detalhado**: Gera relatório completo com notas e recomendações
- **Fácil Uso**: Interface simples via linha de comando

## 🚀 Como Usar

### Execução Básica
```bash
python main.py
```

### Com arquivo específico
```bash
python main.py exemplos/exemplo_conversa.txt
```

## 📁 Estrutura do Projeto

```
auditor-atendimento/
│
├── main.py                 # Arquivo principal
├── requirements.txt        # Dependências
├── README.md              # Documentação
├── exemplos/
│   └── exemplo_conversa.txt  # Exemplo de conversa
└── auditor/
    ├── __init__.py        # Módulo auditor
    ├── analisador.py      # Lógica de análise
    └── criterios.py       # Critérios de avaliação
```

## 📝 Formato do Arquivo de Conversa

O sistema aceita arquivos `.txt` com o seguinte formato:

```
[HH:MM:SS] Autor: Mensagem
```

### Exemplo:
```
[09:00:15] Cliente: Olá, preciso de ajuda
[09:00:25] Atendente: Olá! Como posso ajudá-lo?
[09:00:45] Cliente: Tenho um problema com meu pedido
[09:01:00] Atendente: Entendo, vou verificar isso para você
```

## 📊 Critérios de Avaliação

### Empatia (60% da nota final)
- **Palavras positivas**: "obrigado", "por favor", "vamos resolver", etc.
- **Nota baseada na proporção** de mensagens com palavras empáticas

### Tempo de Resposta (40% da nota final)
- **Excelente**: ≤ 10 segundos
- **Bom**: ≤ 20 segundos  
- **Regular**: ≤ 30 segundos
- **Ruim**: ≤ 60 segundos
- **Muito ruim**: > 60 segundos

## 🎯 Exemplo de Saída

```
🎯 AUDITOR DE ATENDIMENTO
==================================================
📖 Analisando arquivo: exemplos/exemplo_conversa.txt

==================================================
📊 RELATÓRIO DE AUDITORIA
==================================================
📅 Data/Hora: 15/12/2024 14:30:25
⏱️  Duração total: 00:02:40
💬 Total de mensagens: 10
👤 Mensagens do cliente: 4
👨‍💼 Mensagens do atendente: 6

------------------------------
📈 AVALIAÇÕES
------------------------------
❤️  Empatia: 8.5/10
⏰ Tempo de Resposta: 9.0/10
🏆 Média Final: 8.8/10

------------------------------
🔍 DETALHES
------------------------------
✅ Palavras positivas encontradas: 5
⏱️  Tempo médio de resposta: 15.0 segundos
🚨 Respostas lentas (>30s): 0

------------------------------
💡 RECOMENDAÇÕES
------------------------------
🎉 Excelente atendimento! Continue assim!

==================================================
```

## 🛠️ Instalação

1. Clone o repositório:
```bash
git clone <url-do-repositorio>
cd auditor-atendimento
```

2. Execute o sistema:
```bash
python main.py
```

## 📈 Próximas Funcionalidades

- [ ] Exportação para CSV
- [ ] Interface web
- [ ] API REST com FastAPI
- [ ] Análise de sentimento avançada
- [ ] Relatórios em PDF
- [ ] Dashboard interativo

## 🤝 Contribuição

Contribuições são bem-vindas! Sinta-se à vontade para:

1. Reportar bugs
2. Sugerir novas funcionalidades
3. Enviar pull requests

## 📄 Licença

Este projeto está sob a licença MIT.

---

**Desenvolvido com ❤️ para melhorar a qualidade do atendimento ao cliente** 