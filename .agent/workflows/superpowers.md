---
description: Superpowers - Fluxo de Trabalho de Alta Performance para o PREDATOR
---

# 🦸 Superpowers Protocol

Este workflow define a metodologia obrigatória para todas as evoluções do PREDATOR, garantindo robustez, testabilidade e elegância no código.

## 1. Brainstorming (Design First)
- Antes de qualquer alteração, o Agente deve questionar as premissas.
- Explorar alternativas (Trade-offs).
- Definir o "Sucesso" da tarefa (Ex: +5% PnL no Backtest).

## 2. Plano de Implementação (The Blueprint)
- Criar um plano detalhado com:
    - [ ] Arquivos a serem alterados.
    - [ ] Lógica específica de cada alteração.
    - [ ] Passos de verificação (Unit Tests ou Backtests).

// turbo
## 3. Implementação Orientada a Testes (TDD)
- O plano deve ser executado em pequenos lotes.
- Cada mudança de lógica deve ser validada por um comando de backtest ou script de checagem.
- **RED:** O backtest atual falha ou é insuficiente.
- **GREEN:** A nova lógica faz o backtest passar.
- **REFACTOR:** Limpeza do código sem alterar o comportamento.

## 4. Revisão de Código (Quality Guard)
- Após a implementação, o Agente revisa o trabalho contra o Plano.
- Problemas críticos bloqueiam o merge/push.

## 5. Finalização
- Sincronização com GitHub e deploy no Render/Vercel.
- Limpeza de branches e arquivos temporários.

---
*Este protocolo é inspirado no framework 'Superpowers' de Jesse.*
