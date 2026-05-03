# 🦠 Simulador Epidemiológico SEIR

<p align="center">
  <img src="https://img.shields.io/badge/Python-3.11-3776AB?style=for-the-badge&logo=python&logoColor=white"/>
  <img src="https://img.shields.io/badge/Streamlit-1.35+-FF4B4B?style=for-the-badge&logo=streamlit&logoColor=white"/>
  <img src="https://img.shields.io/badge/Plotly-5.22+-3F4F75?style=for-the-badge&logo=plotly&logoColor=white"/>
  <img src="https://img.shields.io/badge/SciPy-1.13+-8CAAE6?style=for-the-badge&logo=scipy&logoColor=white"/>
  <img src="https://img.shields.io/badge/License-MIT-22c55e?style=for-the-badge"/>
  <a href="https://calculadoraepidemiologica-sx2fnrkctk5hxat6bdr38c.streamlit.app/" target="_blank">
    <img src="https://img.shields.io/badge/🚀%20Demo%20ao%20Vivo-Streamlit%20Cloud-FF4B4B?style=for-the-badge"/>
  </a>
</p>

<p align="center">
  Uma dashboard interativa para simulação de epidemias baseada no modelo matemático SEIR,
  desenvolvida em Python com interface web moderna, gráficos dinâmicos e controles em tempo real.
</p>

<p align="center">
  <a href="https://calculadoraepidemiologica-sx2fnrkctk5hxat6bdr38c.streamlit.app/" target="_blank">
    <strong>▶️ Acesse a calculadora ao vivo aqui</strong>
  </a>
</p>

---

## 📋 Índice

- [Sobre o Projeto](#-sobre-o-projeto)
- [Demonstração](#-demonstração)
- [O Modelo SEIR](#-o-modelo-seir)
- [Funcionalidades](#-funcionalidades)
- [Tecnologias Utilizadas](#-tecnologias-utilizadas)
- [Como Executar Localmente](#-como-executar-localmente)
- [Deploy no Streamlit Cloud](#-deploy-no-streamlit-cloud)
- [Estrutura do Repositório](#-estrutura-do-repositório)
- [Artigo Científico](#-artigo-científico)
- [Processo de Desenvolvimento](#-processo-de-desenvolvimento)
- [Colaboração com Inteligência Artificial](#-colaboração-com-inteligência-artificial)
- [Referências](#-referências)

---

## 🎯 Sobre o Projeto

Este projeto nasceu da necessidade de tornar a modelagem epidemiológica acessível a estudantes, pesquisadores e formuladores de políticas públicas. Durante a pandemia de COVID-19, modelos matemáticos como o SEIR foram amplamente utilizados por governos e agências de saúde para embasar decisões críticas — mas sua complexidade matemática os mantinha distantes do grande público.

O **Simulador Epidemiológico SEIR** resolve esse problema ao traduzir equações diferenciais em uma interface visual interativa: qualquer pessoa pode mover um controle deslizante e observar imediatamente como a taxa de transmissão, o período de incubação ou o tamanho da população afetam o curso de uma epidemia — incluindo o famoso **achatamento da curva**.

> Este projeto foi desenvolvido como parte de um trabalho acadêmico sobre epidemiologia computacional, combinando rigor matemático com acessibilidade pedagógica.

---

## 🖥️ Demonstração

🔗 **Acesse a calculadora ao vivo:** [calculadoraepidemiologica.streamlit.app](https://calculadoraepidemiologica-sx2fnrkctk5hxat6bdr38c.streamlit.app/)

Ao iniciar a aplicação, você encontrará:

- **Painel lateral** com controles deslizantes para todos os parâmetros
- **Cards de métricas** com pico de infectados, dia do pico, total afetado e nunca infectados
- **Indicador R₀** com código de cores (🟢 controlada / 🟡 limítrofe / 🔴 epidêmica)
- **Gráfico SEIR interativo** com zoom, hover e área sombreada no pico
- **Gráfico de incidência diária** com novos casos por dia
- **Tabela de resumo** a cada 30 dias com percentual da população afetada

---

## 🧮 O Modelo SEIR

O modelo SEIR é um sistema de Equações Diferenciais Ordinárias (EDOs) que divide a população em quatro compartimentos:

| Compartimento | Símbolo | Descrição |
|---|---|---|
| **Suscetível** | S | Indivíduos que podem ser infectados |
| **Exposto** | E | Infectados em período de incubação (não infecciosos) |
| **Infectado** | I | Indivíduos infecciosos ativos |
| **Recuperado** | R | Imunes por recuperação ou óbito |

### Equações do Modelo

$$\frac{dS}{dt} = -\frac{\beta \cdot S \cdot I}{N}$$

$$\frac{dE}{dt} = \frac{\beta \cdot S \cdot I}{N} - \sigma \cdot E$$

$$\frac{dI}{dt} = \sigma \cdot E - \gamma \cdot I$$

$$\frac{dR}{dt} = \gamma \cdot I$$

### Parâmetros

| Parâmetro | Símbolo | Descrição |
|---|---|---|
| Taxa de transmissão | β (beta) | Contatos infecciosos por pessoa por dia |
| Taxa de progressão | σ (sigma) | Inverso do período de incubação |
| Taxa de recuperação | γ (gamma) | Inverso do período infeccioso |
| Reprodução básica | R₀ = β/γ | Secundários gerados por um caso primário |

### Limiar de Imunidade de Rebanho

$$p_c = 1 - \frac{1}{R_0}$$

---

## ✨ Funcionalidades

- 🎛️ **Controles em tempo real** — sliders para 5 parâmetros epidemiológicos
- 📊 **Gráfico SEIR interativo** — zoom, pan e valores ao passar o mouse
- 📈 **Incidência diária** — gráfico de barras com novos casos por dia
- 🔢 **Métricas automáticas** — pico, dia do pico, total afetado e nunca infectados
- 🚦 **Indicador R₀** — semáforo visual com status da epidemia
- 📋 **Tabela por fase** — resumo a cada 30 dias
- 🌐 **Deploy simples** — pronto para o Streamlit Community Cloud

---

## 🛠️ Tecnologias Utilizadas

| Tecnologia | Versão | Uso |
|---|---|---|
| [Python](https://python.org) | 3.11+ | Linguagem principal |
| [Streamlit](https://streamlit.io) | 1.35+ | Interface web interativa |
| [Plotly](https://plotly.com) | 5.22+ | Gráficos dinâmicos |
| [SciPy](https://scipy.org) | 1.13+ | Resolução das EDOs (`odeint`) |
| [NumPy](https://numpy.org) | 1.26+ | Operações numéricas |
| [Pandas](https://pandas.pydata.org) | 2.2+ | Tabela de resumo por fase |

---

## 🚀 Como Executar Localmente

### Pré-requisitos

- Python 3.11 ou superior
- pip

### Passo a passo

```bash
# 1. Clone o repositório
git clone https://github.com/seu-usuario/seu-repositorio.git
cd seu-repositorio

# 2. (Opcional) Crie um ambiente virtual
python -m venv venv
source venv/bin/activate      # Linux/macOS
venv\Scripts\activate         # Windows

# 3. Instale as dependências
pip install -r requirements.txt

# 4. Execute a aplicação
streamlit run main.py
```

A aplicação abrirá automaticamente em `http://localhost:8501`.

---

## ☁️ Deploy no Streamlit Cloud

1. Faça o fork ou push deste repositório para o seu GitHub
2. Acesse [share.streamlit.io](https://share.streamlit.io)
3. Clique em **New app**
4. Selecione o repositório, branch e o arquivo `main.py`
5. Clique em **Deploy** — o Streamlit Cloud detecta o `requirements.txt` automaticamente

---

## 📁 Estrutura do Repositório

```
📦 seu-repositorio/
├── 📄 main.py              # Aplicação principal do simulador
├── 📄 requirements.txt     # Dependências do projeto
├── 📄 artigo.md            # Artigo científico sobre o simulador
├── 📄 prompts.md           # Prompts utilizados no desenvolvimento com IA
└── 📄 README.md            # Este arquivo
```

---

## 📝 Artigo Científico

Este projeto é acompanhado de um artigo científico completo disponível em [`artigo.md`](./artigo.md), contendo:

- **Resumo** — descrição da ferramenta e sua importância
- **Introdução** — contexto histórico e motivação (Kermack & McKendrick, 1927; COVID-19)
- **Metodologia** — equações SEIR, derivação do R₀ e método numérico LSODA
- **Resultados** — análise das visualizações e do fenômeno de achatamento da curva
- **Conclusão** — impacto em políticas públicas e direções futuras
- **Referências** — 7 referências acadêmicas reais

---

## 🔄 Processo de Desenvolvimento

O projeto foi construído em etapas progressivas:

1. **Concepção** — definição dos requisitos técnicos e pedagógicos do simulador
2. **Implementação** — desenvolvimento do `main.py` com modelo SEIR, interface Streamlit e gráficos Plotly
3. **Documentação técnica** — geração do `requirements.txt` e explicação do modelo
4. **Produção acadêmica** — redação do artigo científico no formato de paper
5. **Internacionalização** — tradução do artigo para o português
6. **Versionamento** — organização dos arquivos em Markdown para o repositório Git

Os prompts utilizados em cada etapa estão documentados em [`prompts.md`](./prompts.md).

---

## 🤖 Colaboração com Inteligência Artificial

Este projeto foi desenvolvido em colaboração com o **Claude** (Anthropic), um assistente de inteligência artificial utilizado como par de desenvolvimento ao longo de todo o processo criativo e técnico.

### Como a IA contribuiu

**Como Desenvolvedor Python Sênior**, o Claude foi responsável por:
- Arquitetar a estrutura do simulador em uma única página (`main.py`)
- Implementar o sistema de EDOs com `scipy.integrate.odeint` e o algoritmo LSODA
- Projetar a interface Streamlit com CSS personalizado, paleta de cores coerente e tipografia
- Construir os gráficos Plotly interativos com hover, zoom e preenchimento de área
- Gerar o `requirements.txt` compatível com o Streamlit Community Cloud

**Como Pesquisador Acadêmico**, o Claude foi responsável por:
- Redigir o artigo científico completo em formato de paper acadêmico
- Formalizar as equações do modelo SEIR em notação matemática
- Derivar e contextualizar o número básico de reprodução R₀
- Estruturar as referências bibliográficas com autores e periódicos reais
- Traduzir e adaptar o artigo para o português com terminologia técnica precisa

**Como Assistente de Documentação**, o Claude foi responsável por:
- Organizar os prompts utilizados em `prompts.md`
- Redigir este README completo com badges, tabelas, equações e instruções de uso

### Sobre a abordagem de colaboração humano-IA

A metodologia adotada neste projeto exemplifica o uso de IA generativa como **amplificador de capacidade técnica**: o humano definiu os objetivos, os requisitos pedagógicos e o escopo acadêmico; a IA executou a implementação com rigor técnico e científico. Cada entrega foi revisada e validada antes de ser incorporada ao repositório.

Essa colaboração reduziu significativamente o tempo de desenvolvimento sem comprometer a qualidade do código ou da produção acadêmica — demonstrando que ferramentas de IA podem ser parceiras legítimas em projetos de pesquisa e engenharia de software.

> 💡 Os prompts exatos utilizados para guiar o Claude estão disponíveis em [`prompts.md`](./prompts.md), permitindo total reprodutibilidade do processo.

---

## 📚 Referências

- Harris, C. R. et al. (2020). Array programming with NumPy. *Nature*, 585, 357–362.
- Kermack, W. O., & McKendrick, A. G. (1927). A contribution to the mathematical theory of epidemics. *Proceedings of the Royal Society A*, 115(772), 700–721.
- McKinney, W. (2010). Data structures for statistical computing in Python. *Proceedings of the 9th Python in Science Conference*.
- Organização Mundial da Saúde. (2020). *Report of the WHO-China Joint Mission on Coronavirus Disease 2019*. OMS.
- Virtanen, P. et al. (2020). SciPy 1.0: Fundamental algorithms for scientific computing in Python. *Nature Methods*, 17, 261–272.

---

<p align="center">
  Desenvolvido com 🧠 curiosidade científica e 🤝 colaboração humano-IA
</p>
