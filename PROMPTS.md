# Prompts Utilizados

## Prompt 1 — Criação do Simulador SEIR

```
Atue como um Desenvolvedor Python Sênior e Especialista em Modelagem Matemática. > Objetivo: Criar um simulador epidemiológico interativo usando o modelo SEIR (Suscetível, Exposto, Infectado, Recuperado).
Especificações do Código:

1. Linguagem: Python 3.
2. Interface: Use a biblioteca Streamlit para criar uma dashboard moderna.
3. Gráficos: Use Plotly para gráficos interativos (que permitam dar zoom e ver valores ao passar o mouse).
4. Interatividade: Na barra lateral (sidebar), crie sliders para o usuário controlar:
   * População Inicial (N).
   * Taxa de Transmissão (Beta).
   * Período de Incubação em dias (1/Sigma).
   * Período de Infecção em dias (1/Gamma).
   * Tempo de simulação em dias.
5. Cálculo: Resolva as Equações Diferenciais Ordinárias (EDOs) do modelo SEIR usando a função `odeint` da biblioteca `scipy`.
Especificações de Saída:

1. O código deve estar em Português (comentários e interface).
2. Além do código principal (`main.py`), gere o conteúdo de um arquivo chamado `requirements.txt` com as bibliotecas necessárias para que eu possa hospedar o projeto no Streamlit Cloud.
3. Ao final, escreva uma explicação técnica de 2 parágrafos sobre como o modelo SEIR funciona, para que eu possa usar na minha fundamentação.
```

---

## Prompt 2 — Criação do Artigo Científico

```
Agora que o código está pronto, aja como um pesquisador acadêmico. Escreva um artigo científico curto (formato de Paper) em inglês sobre este simulador que você criou. O artigo deve conter:

1. Title: Um título acadêmico profissional.
2. Abstract: Um resumo do que o software faz e sua importância.
3. Introduction: Explique o propósito de modelar doenças como a COVID-19.
4. Methodology: Descreva as equações matemáticas do modelo SEIR que você usou no código Python.
5. Results: Descreva como a interface interativa permite visualizar o achatamento da curva.
6. Conclusion: Uma breve conclusão sobre o uso de simulação computacional na saúde pública.
```
