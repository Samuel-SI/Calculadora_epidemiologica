# Um Simulador Epidemiológico Interativo Baseado no Modelo SEIR para Educação em Saúde Pública e Análise de Políticas de Intervenção

**Grupo de Pesquisa em Epidemiologia Computacional**  
Departamento de Matemática Aplicada e Informática em Saúde Pública  
*Recebido: maio de 2026 | Publicado: maio de 2026*

---

## Resumo

Este artigo apresenta uma ferramenta de simulação epidemiológica de código aberto, baseada em navegador, construída sobre o modelo compartimental SEIR (Suscetível–Exposto–Infectado–Recuperado). O simulador é implementado em Python 3 utilizando o framework Streamlit para a interface interativa de painel, Plotly para visualizações dinâmicas e o solver `odeint` da SciPy para integração numérica das Equações Diferenciais Ordinárias (EDOs) subjacentes. A ferramenta permite que os usuários manipulem em tempo real cinco parâmetros epidemiológicos centrais — tamanho da população (N), taxa de transmissão (β), período de incubação (1/σ), período infeccioso (1/γ) e horizonte de simulação — e observem imediatamente como cada parâmetro molda as trajetórias da epidemia, o momento do pico de infecção e a fração da população afetada ao final. Um indicador do número básico de reprodução R₀ com esquema de cores semafórico é exibido de forma proeminente. O objetivo principal deste trabalho é diminuir a lacuna entre a epidemiologia matemática e o público não especialista, incluindo estudantes, profissionais de saúde pública e formuladores de políticas, por meio de um ambiente de simulação acessível, visualmente rico e cientificamente rigoroso.

**Palavras-chave:** modelo SEIR; epidemiologia computacional; simulação de epidemias; Python; Streamlit; número básico de reprodução; achatamento da curva.

---

## 1. Introdução

A modelagem matemática constitui um dos pilares da epidemiologia desde o trabalho seminal de Kermack e McKendrick (1927), que formalizou o arcabouço compartimental SIR para explicar a propagação e o declínio de surtos de doenças infecciosas. A extensão subsequente ao modelo SEIR, que introduz um compartimento explícito de Expostos, corrigiu uma limitação crítica da formulação original: a ausência de um período de latência entre a aquisição da infecção e o início da infecciosidade. Essa latência, observada em praticamente todos os patógenos clinicamente relevantes — da influenza A ao SARS-CoV-2 —, altera fundamentalmente a dinâmica temporal de uma epidemia e deve ser considerada em qualquer modelo destinado a apoiar o planejamento de intervenções reais de saúde pública.

A pandemia de COVID-19, que emergiu no final de 2019 e se intensificou até uma crise sanitária global de escala sem precedentes, evidenciou a necessidade urgente de ferramentas epidemiológicas acessíveis, interpretáveis e computacionalmente confiáveis. Governos e agências de saúde em todo o mundo recorreram a modelos compartimentais para orientar decisões críticas sobre o momento de decretar lockdowns, alocação de recursos hospitalares e priorização de campanhas de vacinação. Contudo, a opacidade de muitos desses modelos perante o público em geral contribuiu para o ceticismo generalizado e para dificuldades de comunicação. O desenvolvimento de ferramentas de simulação transparentes e interativas, capazes de transmitir visualmente as consequências das mudanças nos parâmetros epidemiológicos, representa, portanto, não apenas um imperativo educacional, mas também uma estratégia de comunicação em saúde pública.

Este artigo descreve o design, os fundamentos matemáticos, a implementação e o valor pedagógico de um simulador SEIR interativo desenvolvido em Python. A ferramenta se destina a um público duplo: pesquisadores acadêmicos e estudantes de epidemiologia, biomatemática ou saúde pública que necessitam de um ambiente de prototipagem rápida para análises baseadas no modelo SEIR; e tomadores de decisão não especialistas que se beneficiam de um retorno visual intuitivo sem precisar interagir diretamente com as equações diferenciais subjacentes. A Seção 2 detalha o modelo matemático SEIR. A Seção 3 descreve a arquitetura do software e os recursos de interatividade. A Seção 4 discute os principais resultados e visualizações. A Seção 5 conclui com reflexões sobre o papel mais amplo da simulação computacional na saúde pública.

---

## 2. Metodologia

### 2.1 O Modelo Compartimental SEIR

O modelo SEIR particiona uma população fechada de tamanho constante N em quatro compartimentos mutuamente exclusivos e coletivamente exaustivos: Suscetível (S), Exposto (E), Infectado (I) e Recuperado (R), de modo que S(t) + E(t) + I(t) + R(t) = N para todo t ≥ 0. A dinâmica do sistema é governada pelo seguinte sistema de Equações Diferenciais Ordinárias:

$$\frac{dS}{dt} = -\frac{\beta \cdot S \cdot I}{N}$$

$$\frac{dE}{dt} = \frac{\beta \cdot S \cdot I}{N} - \sigma \cdot E$$

$$\frac{dI}{dt} = \sigma \cdot E - \gamma \cdot I$$

$$\frac{dR}{dt} = \gamma \cdot I$$

onde **β** (beta) denota a taxa de contato efetiva, representando o número médio de contatos infecciosos por indivíduo por unidade de tempo; **σ** (sigma) é a taxa de progressão do estado latente para o infeccioso, igual ao inverso do período médio de incubação (1/σ dias); e **γ** (gamma) é a taxa de recuperação, igual ao inverso do período infeccioso médio (1/γ dias). O modelo pressupõe mistura homogênea, população fixa sem nascimentos ou óbitos e um único evento de introdução definido por um indivíduo exposto em t = 0.

### 2.2 Número Básico de Reprodução (R₀)

O número básico de reprodução R₀, definido como o número esperado de infecções secundárias geradas por um único caso infeccioso em uma população totalmente suscetível, é um parâmetro limiar fundamental. Para o modelo SEIR, é analiticamente derivado como:

$$R_0 = \frac{\beta}{\gamma}$$

Quando R₀ < 1, a epidemia não se estabelece e declina monotonicamente. Quando R₀ > 1, a fase de crescimento exponencial inicial persiste até que o esgotamento dos suscetíveis crie um efeito de imunidade de rebanho suficiente para reduzir o número de reprodução efetivo R(t) abaixo de um. O limiar de imunidade de rebanho — a fração da população que deve ser imune para impedir a transmissão sustentada — é dado por:

$$p_c = 1 - \frac{1}{R_0}$$

### 2.3 Integração Numérica

O sistema de EDOs é resolvido numericamente por meio da função `odeint` da biblioteca SciPy (Virtanen et al., 2020), que encapsula o algoritmo LSODA da suíte FORTRAN ODEPACK. O LSODA detecta automaticamente a rigidez do problema e alterna entre o método preditor-corretor de Adams para intervalos não rígidos e a Fórmula de Diferenciação Retroativa (BDF) para intervalos rígidos. A grade temporal é discretizada em quatro pontos por dia para garantir a suavidade das curvas de saída, especialmente na região do pico epidêmico, onde o gradiente de I(t) muda rapidamente.

### 2.4 Pilha Tecnológica

O simulador é escrito em Python 3 e utiliza as seguintes bibliotecas de código aberto:

| Biblioteca | Versão mínima | Função no projeto |
|---|---|---|
| NumPy | 1.26 | Operações matriciais e grade temporal |
| SciPy | 1.13 | Resolução das EDOs via `odeint` |
| Pandas | 2.2 | Geração do resumo tabular por fase |
| Plotly | 5.22 | Gráficos interativos com zoom e hover |
| Streamlit | 1.35 | Framework de aplicação web reativa |

Toda a aplicação está encapsulada em um único arquivo `main.py` acompanhado de um `requirements.txt`, viabilizando a implantação com um único comando no Streamlit Community Cloud.

---

## 3. Resultados

### 3.1 Layout do Painel e Métricas Principais

Ao ser iniciado, o painel exibe quatro cartões de métricas resumidas no topo do painel principal:

1. **Pico de Infectados** — contagem máxima simultânea de infectados e o dia em que ocorre;
2. **Dia do Pico** — reforço temporal do momento crítico da epidemia;
3. **Total de Afetados** — número acumulado de indivíduos que passaram pelo compartimento Infectado, ou seja, R(∞);
4. **Nunca Infectados** — população suscetível residual ao final da simulação.

O valor calculado de R₀ é exibido com um esquema de cores semafórico: 🟢 verde para R₀ < 1 (controlada), 🟡 âmbar para 1 ≤ R₀ < 2 (limítrofe) e 🔴 vermelho para R₀ ≥ 2 (epidêmica).

### 3.2 Visualização das Trajetórias SEIR e Achatamento da Curva

A visualização principal é um gráfico de linhas interativo do Plotly que renderiza os quatro compartimentos SEIR ao longo do horizonte de simulação. Cada série utiliza um estilo de linha distinto — sólido para I, tracejado para S, pontilhado para E, tracejado longo para R — e uma paleta de cores semanticamente escolhida. Uma linha de referência vertical tracejada marca automaticamente o dia do pico de infecção. A curva do compartimento Infectado recebe um preenchimento de área semitransparente para realce visual da região do pico epidêmico.

O fenômeno do **achatamento da curva** — central na comunicação sobre a pandemia de COVID-19 — é direta e intuitivamente observável por meio do controle deslizante de β. Reduzir β de 0,4 para 0,2, simulando o efeito de intervenções de distanciamento físico que reduzem a taxa de contato efetiva em aproximadamente 50%, produz dois efeitos simultâneos:

- **(a)** o pico de I(t) é substancialmente reduzido em magnitude, indicando que o sistema de saúde enfrentaria uma carga máxima menor em qualquer momento;
- **(b)** o pico é deslocado temporalmente para uma data posterior, estendendo a duração da epidemia, mas distribuindo a carga de casos de forma mais homogênea ao longo do tempo.

Essa compensação, qualitativamente consistente com os achados de análises reais da COVID-19, torna-se imediatamente visível sem qualquer conhecimento matemático prévio por parte do usuário.

### 3.3 Gráfico de Incidência Diária

Um gráfico de barras secundário exibe os novos casos diários, aproximados como o incremento diário no compartimento R(t):

$$\text{Novos casos}(t) \approx \frac{\Delta R}{\Delta t} = \gamma \cdot I(t)$$

Uma linha suavizada sobreposta auxilia na identificação de tendências. Essa representação espelha o formato utilizado pelas agências de saúde pública durante a vigilância de surtos, reforçando o alinhamento pedagógico da ferramenta com a prática epidemiológica profissional.

### 3.4 Tabela de Resumo por Fase

Uma seção expansível apresenta um resumo tabular dos quatro compartimentos em intervalos de 30 dias, incluindo o percentual da população cumulativamente afetada. Exemplo de estrutura:

| Dia | Suscetível (S) | Exposto (E) | Infectado (I) | Recuperado (R) | % Afetada |
|-----|----------------|-------------|---------------|----------------|-----------|
| 0   | 999.999        | 1           | 0             | 0              | 0,0%      |
| 30  | ...            | ...         | ...           | ...            | ...       |
| 60  | ...            | ...         | ...           | ...            | ...       |

---

## 4. Conclusão

Este trabalho apresentou um simulador epidemiológico SEIR interativo e de código aberto que integra métodos numéricos rigorosos a uma interface web moderna e acessível. O simulador permite que usuários sem formação em programação ou matemática manipulem parâmetros epidemiológicos centrais e observem, em tempo real, suas consequências sobre as trajetórias da epidemia, a carga máxima sobre o sistema de saúde e a dinâmica de imunidade da população.

A pandemia de COVID-19 demonstrou que a capacidade de comunicar conceitos epidemiológicos de forma clara e interativa não é meramente um exercício acadêmico, mas um imperativo de saúde pública com consequências diretas sobre a adesão às políticas, o planejamento de recursos e a confiança social na ciência. Ferramentas como a descrita neste trabalho possuem um significativo potencial de uso em currículos de epidemiologia, programas de capacitação em saúde pública, campanhas de comunicação científica e briefings rápidos de políticas.

Direções futuras incluem a incorporação de formulações estocásticas para capturar a variabilidade de surtos em populações pequenas, a adição de módulos de modelagem de intervenções — como reduções em degrau de β em momentos especificados pelo usuário para simular lockdowns ou obrigatoriedade de uso de máscaras — e módulos de calibração que permitam ajustar o modelo a dados empíricos de incidência. Essas extensões elevariam a ferramenta de um instrumento pedagógico a um sistema de apoio à decisão leve, porém cientificamente substancial, reforçando o papel transformador que a simulação computacional desempenha na prática moderna da saúde pública baseada em evidências.

---

## Referências

- Harris, C. R., Millman, K. J., van der Walt, S. J., et al. (2020). Array programming with NumPy. *Nature*, 585, 357–362.

- Kermack, W. O., & McKendrick, A. G. (1927). A contribution to the mathematical theory of epidemics. *Proceedings of the Royal Society A*, 115(772), 700–721.

- McKinney, W. (2010). Data structures for statistical computing in Python. *Proceedings of the 9th Python in Science Conference*, 445, 51–56.

- Organização Mundial da Saúde. (2020). *Report of the WHO-China Joint Mission on Coronavirus Disease 2019 (COVID-19)*. OMS.

- Plotly Technologies Inc. (2015). *Collaborative data science*. Plotly Technologies. https://plotly.com

- Streamlit Inc. (2019). *Streamlit: The fastest way to build data apps*. https://streamlit.io

- Virtanen, P., Gommers, R., Oliphant, T. E., et al. (2020). SciPy 1.0: Fundamental algorithms for scientific computing in Python. *Nature Methods*, 17, 261–272.
