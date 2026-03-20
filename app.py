import streamlit as st
import pandas as pd
import plotly.express as px
import joblib

# ==========================================
# 1. CONFIGURAÇÃO DA PÁGINA E DADOS BASE
# ==========================================
st.set_page_config(page_title="Dashboard - Passos Mágicos", page_icon="📊", layout="wide")

# ---> CARREGANDO O MODELO <---
@st.cache_resource
def carregar_modelo():    
    return joblib.load('modelo_passos_magicos.pkl')

try:
    modelo = carregar_modelo()
    modelo_pronto = True
except Exception as e:
    modelo_pronto = False
    erro_modelo = e

@st.cache_data
def carregar_dados():
    df = pd.read_csv('pede_completo.csv', sep=';')

    # Tratando colunas numéricas (substituindo vírgula por ponto)
    cols_numericas = ['inde', 'iaa', 'ieg', 'ips', 'ida', 'ipv', 'ian', 'ipp', 'risco_defasagem']
    for col in cols_numericas:
        if df[col].dtype == 'object':
            df[col] = df[col].str.replace(',', '.').astype(float)
    return df

df_analise = carregar_dados()

# Vinculando o df_analise ao df_tratado para não quebrar os códigos do modelo que usam df_tratado
df_tratado = df_analise 

# ==========================================
# 2. MENU LATERAL (NAVEGAÇÃO)
# ==========================================
st.sidebar.image("logo.png", width=200)
st.sidebar.title("Navegação")

pagina = st.sidebar.radio(
    "Selecione a página:",
    ["🏠 Página Inicial", "📈 Análises e Descobertas", "💡Modelo Preditivo (Risco Defasagem)"]
)

# ==========================================
# GAVETA 1: PÁGINA INICIAL
# ==========================================
if pagina == "🏠 Página Inicial":
    st.title("🎩 Bem-vindo ao Dashboard - Associação Passos Mágicos")
    st.markdown("""
    Este painel analítico foi desenvolvido para entender a jornada educacional dos alunos da **Associação Passos Mágicos**.
    
    **O que você vai encontrar aqui:**
    * 📈 **Análises e Insights:** Respostas diretas baseadas em dados sobre defasagem, engajamento e evolução.
    * 💡 **Modelo Preditivo:** Ferramenta que utilza recurso de Inteligênia Artificial (IA) para prever o risco de defasagem de alunos do programa.
    
    👈 *Utilize o menu lateral para navegar.*
    """)
    
    st.divider()
    col1, col2, col3 = st.columns(3)
    col1.metric("Total de Alunos (Histórico)", len(df_analise['ra'].unique()))
    col2.metric("Média Geral INDE", round(df_analise['inde'].mean(), 2))
    col3.metric("Taxa Média de Risco", f"{round(df_analise['risco_defasagem'].mean() * 100, 1)}%")

# ==========================================
# GAVETA 2: ANÁLISES E DESCOBERTAS
# ==========================================
elif pagina == "📈 Análises e Descobertas":
    st.title("📈 Análises e Descobertas")
    
    # Menu suspenso para escolher o gráfico
    opcao_grafico = st.selectbox(
        "Selecione a análise/resposta que deseja visualizar:",
        [
            "1. Adequação do Nível (IAN)",
            "2. Evolução do Desempenho (IDA)",
            "3. Relação IEG vs IDA vs IPV",
            "4. Coerência IAA vs IDA",
            "5. Aspectos Psicossociais (IPS)",
            "6. Aspectos Psicopedagógicos (IPP)",
            "7. Fatores do Ponto de Virada (IPV)",
            "8. Multidimensionalidade (INDE)",
            "9. Padrões de Risco (Previsão de Defasagem)",
            "10. Efetifidade do Programa (Evolução das Pedras)",
            "11. Termômetro de Risco por Fase",
            "12. Comparativo de desempenho (Escola Pública vs Privada)"
        ]
    )
    st.divider()

    # -----------------------------------------
    # GRÁFICO 1
    # -----------------------------------------
    if opcao_grafico == "1. Adequação do Nível (IAN)":

        # ---> PERGUNTA 1 <---
        st.markdown("#### **Pergunta 1:** Qual é o perfil geral de defasagem dos dos alunos (IAN) ao longo dos anos?")

        def categorizar_ian_oficial(nota_ian):
            if nota_ian >= 9.0: return 'Adequado (Nota 10)'
            elif nota_ian >= 4.0: return 'Defasagem Moderada (Nota 5)'
            else: return 'Defasagem Severa (Nota 2.5 ou 0)'

        df_analise['status_ian'] = df_analise['ian'].apply(categorizar_ian_oficial)
        df_q1 = df_analise.groupby(['ano', 'status_ian']).size().reset_index(name='contagem')
        totais_por_ano = df_q1.groupby('ano')['contagem'].transform('sum')
        df_q1['percentual'] = (df_q1['contagem'] / totais_por_ano) * 100
        df_q1['rotulo'] = df_q1.apply(lambda x: f"{int(x['contagem'])} ({x['percentual']:.1f}%)", axis=1)

        fig1 = px.bar(df_q1, x='ano', y='contagem', color='status_ian',
                      title="1. Adequação de Nível (IAN): Perfil de Defasagem ao Longo dos Anos",
                      barmode='group', text='rotulo',
                      color_discrete_map={'Adequado (Nota 10)': 'green', 'Defasagem Moderada (Nota 5)': 'orange', 'Defasagem Severa (Nota 2.5 ou 0)': 'red'},
                      category_orders={'status_ian': ['Adequado (Nota 10)', 'Defasagem Moderada (Nota 5)', 'Defasagem Severa (Nota 2.5 ou 0)']},
                      labels={'ano': 'Ano', 'status_ian': 'Status IAN'})
        fig1.update_traces(textposition='outside')
        fig1.update_layout(yaxis=dict(title='Quantidade de Alunos'), margin=dict(t=60))
        
        st.plotly_chart(fig1, use_container_width=True)

        # <-- Resumo da análise do gráfico -->
        st.info("**Insight analítico:** O gráfico evidencia a evolução do programa ao longo dos anos. Em 2022 havia um número significativo de alunos em defasagem moderada e severa. " \
        "Em 2023 e 2024 houve grande migração de alunos para o nível 'Adequado', demonstrando a eficácia da intervenção pedagógica da Passos Mágiocos.")


    # -----------------------------------------
    # GRÁFICO 2
    # -----------------------------------------
    elif opcao_grafico == "2. Evolução do Desempenho (IDA)":

        # ---> PERGUNTA 2 <---
        st.markdown("#### **Pergunta 2:** O desempenho acadêmico médio (IDA) está melhorando, estagnado ou caindo ao longo das fases e anos?")

        df_q2 = df_analise.groupby(['ano', 'fase'])['ida'].mean().reset_index()
        df_q2['ida_medio'] = df_q2['ida'].round(2)
        df_q2 = df_q2.sort_values(by='fase')
        df_q2['Nome da Fase'] = df_q2['fase'].apply(lambda x: 'Alfa' if x == 0 else f'Fase {x}')
        df_q2['ano'] = df_q2['ano'].astype(str)

        min_y, max_y = df_q2['ida_medio'].min() - 0.5, df_q2['ida_medio'].max() + 0.5

        fig2 = px.line(df_q2, x='Nome da Fase', y='ida_medio', color='ano', markers=True, text='ida_medio',
                       title="2. Desempenho Acadêmico Médio (IDA) por Fase (Comparativo Anual)",
                       category_orders={"Nome da Fase": ["Alfa", "Fase 1", "Fase 2", "Fase 3", "Fase 4", "Fase 5", "Fase 6", "Fase 7", "Fase 8"], "ano": ["2022", "2023", "2024"]},
                       color_discrete_sequence=['#9ecae1', '#3182bd', '#08519c'], height=500,
                       labels={'ano': 'Ano', 'ida_medio': 'Média IDA', 'Nome da Fase': 'Fase'})
        fig2.update_traces(textposition='top center', textfont=dict(size=13))
        fig2.update_layout(yaxis=dict(range=[min_y, max_y]), margin=dict(t=50))
        
        st.plotly_chart(fig2, use_container_width=True)

        # <-- Resumo da análise do gráfico -->        
        st.info("**Insight Analítico:** Observa-se que as Fase 6 consolida o maior Desempenho Acadêmico histórico (destaque para a média 7,23 em 2024)." \
        " Nota-se também uma oscilação interessante: enquanto as Fase 2 e 3 apresentaram uma ligeira queda em 2024 face a 2023," \
        " as fases intermédias (3 a 5) mostram uma recuperação, sugerindo diferentes níveis de desafio pedagógico à medida que o aluno avança no programa.")

    # -----------------------------------------
    # GRÁFICO 3
    # -----------------------------------------
    elif opcao_grafico == "3. Relação IEG vs IDA vs IPV":

        # ---> PERGUNTA 3 <---
        st.markdown("#### **Pergunta 3:**  O grau de engajamento dos alunos (IEG) tem relação direta com seus indicadores de desempenho (IDA) e do ponto de virada (IPV)?")

        fig3 = px.scatter(df_analise, x='ieg', y='ida', color='ipv', size='ipv', hover_data=['ano', 'fase'],
                          title="3. O impacto do Engajamento (IEG) no Desempenho (IDA) e Ponto de Virada (IPV)",
                          color_continuous_scale='Inferno', height=500,
                          labels={'ieg': 'Engajamento (IEG)', 'ida': 'Desempenho Acadêmico (IDA)', 'ipv': 'Ponto de Virada (IPV)'})
        fig3.update_layout(xaxis=dict(range=[0, 11]), yaxis=dict(range=[0, 11]), margin=dict(t=50))
        
        st.plotly_chart(fig3, use_container_width=True)

        # <-- Resumo da análise do gráfico -->
        st.info("**Insight Analítico:** O gráfico de dispersão revela uma forte correlação entre os indicadores IEG, IDA e IPV. A alta concentração de 'bolhas amarelas'" \
        " encontra-se no quadrante superior direito. Isso demonstra que a 'virada de chave' na vida do aluno ocorre quando há uma combinação simultânea de" \
        " elevado engajamento (IEG acima de 8) e bom desempenho acadêmico (IDA acima de 7). " \
        "Alunos desengajados tendem a apresentar baixos índices de IPV, representados pelos pontos mais escuros no gráfico.")

    # -----------------------------------------
    # GRÁFICO 4
    # -----------------------------------------
    elif opcao_grafico == "4. Coerência IAA vs IDA":

        # ---> PERGUNTA 4 <---
        st.markdown("#### **Pergunta 4:**  As percepções dos alunos sobre si mesmos (IAA) são coerentes com seu desempenho real (IDA) e engajamento (IEG)?")

        fig4 = px.scatter(df_analise, x='iaa', y='ida', color='ieg', size='ieg', hover_data=['ano', 'fase'], opacity=0.8,
                          title="4. Coerência: A percepção do aluno (IAA) vs Realidade (IDA) e (IEG)",
                          color_continuous_scale='Viridis', height=600,
                          labels={'iaa': 'Autoavaliação (IAA)', 'ida': 'Desempenho Acadêmico (IDA)', 'ieg': 'Engajamento (IEG)'})
        fig4.update_layout(xaxis=dict(range=[-0.5, 11]), yaxis=dict(range=[-0.5, 11]), margin=dict(t=50))
        
        st.plotly_chart(fig4, use_container_width=True)

        # <-- Resumo da análise do gráfico -->
        st.info("**Insight Analítico:** Existe uma coerência geral entre o que o aluno percebe de si mesmo (IAA) e o seu desempenho real (IDA)," \
        " Contudo, há casos de alunos com alta autoavaliação (IAA: 8-10) e desempenho mediano (IDA 5-6)." \
        " Como esses alunos mantêm um alto nível de engajamento (cores claras no IEG), infere-se que o esforço não está a ser traduzido em notas, " \
        "o que exige um acompanhamento pedagógico focado nas metodologias de estudo")

    # -----------------------------------------
    # GRÁFICO 5
    # -----------------------------------------
    elif opcao_grafico == "5. Aspectos Psicossociais (IPS)":

        # ---> PERGUNTA 5 <---
        st.markdown("#### **Pergunta 5:**  Há padrões psicossociais (IPS) que antecedem quedas de desempenho acadêmico ou de engajamento?")

        df_q5 = df_analise.sort_values(by=['ra', 'ano']).copy()
        
        # Cria colunas com as notas do ano anterior do mesmo aluno
        df_q5['ida_anterior'] = df_q5.groupby('ra')['ida'].shift(1)
        df_q5['ieg_anterior'] = df_q5.groupby('ra')['ieg'].shift(1)
        
        def classificar_queda_simples(row):
            # Excluindo alunos sem notas no ano anterior
            if pd.isna(row['ida_anterior']) or pd.isna(row['ieg_anterior']): return 'Sem Histórico Anterior'
            if row['ida'] < row['ida_anterior'] or row['ieg'] < row['ieg_anterior']: return 'Teve Queda (IDA ou IEG)'
            return 'Manteve ou Evoluiu'

        df_q5['Status de Evolução'] = df_q5.apply(classificar_queda_simples, axis=1)
        
        # Filtro: apenas 2023 e 2024, e removendo os alunos "Sem Histórico Anterior"
        df_q5 = df_q5[(df_q5['ano'].astype(str).isin(['2023', '2024'])) & (df_q5['Status de Evolução'] != 'Sem Histórico Anterior')]
        
        # Contagem para o "n="
        contagens = df_q5.groupby(['ano', 'Status de Evolução']).size().reset_index(name='qtd')
        df_q5 = df_q5.merge(contagens, on=['ano', 'Status de Evolução'])
        df_q5['Eixo X Dinamico'] = df_q5['Status de Evolução'] + "<br>(Alunos Avaliados: " + df_q5['qtd'].astype(str) + ")"
        
        # Ordenando as caixas: Queda primeiro, Manteve ou Evoluiu depois
        ordem_status = ['Teve Queda (IDA ou IEG)', 'Manteve ou Evoluiu']
        df_q5['Ordem'] = df_q5['Status de Evolução'].map({k: i for i, k in enumerate(ordem_status)})
        df_q5 = df_q5.sort_values(['ano', 'Ordem'])

        fig5 = px.box(df_q5, x='Eixo X Dinamico', y='ips', color='Status de Evolução', facet_col='ano',
                      title="5. Aspectos Psicossociais (IPS) x Desempenho (IDA) ou Engajamento (IEG)?",
                      color_discrete_map={'Manteve ou Evoluiu': '#3182bd', 'Teve Queda (IDA ou IEG)': '#de2d26'}, height=650,
                      labels={'ips': 'Saúde Psicológica (IPS)', 'Eixo X Dinamico': 'Comparativo de Desempenho'})
        
        # Ajustes de Layout e Eixos
        fig5.update_layout(
            yaxis=dict(range=[0, 11], title="Nota IPS"), 
            yaxis2=dict(range=[0, 11]), 
            showlegend=False, 
            margin=dict(t=100, b=120)
        )
        
        # Melhorando o alinhamento das legendas inferiores
        fig5.update_xaxes(matches=None, tickangle=0, title_text="") 
                
        fig5.for_each_annotation(lambda a: a.update(
            text=f"<b>ANO: {a.text.split('=')[-1]}</b>", 
            font=dict(size=20, color="black")
        ))
        
        st.plotly_chart(fig5, use_container_width=True)
        
        # <-- Resumo da análise do gráfico -->
        st.info("**Insight Analítico:** O gráfico compara os Índices Psicossociais (IPS) dos alunos que tiveram queda nas notas acadêmicas ou de engajamento (caixas vermelhas)" \
        " com aqueles que mantiveram ou melhoraram suas notas (caixas azuis). A análise visual das 'caixas' demonstra que a mediana do (IPS) é estatisticamente semelhante" \
        " tanto para os alunos que tiveram queda no desempenho quanto para os demais. Isso sugere que o indicador IPS, isoladamente, não possui correlação direta com a queda de Desempenho (IDA)" \
        " ou Engajamento (IEG) de um ano para o outro, indicando que a raiz das quedas acadêmicas provém de outros fatores.")
        st.info (" **Nota:** *O número de 'Alunos Avaliados' refere-se exclusivamente aos alunos que possuíam notas registradas no ano imediatamente anterior para fins de comparação).*")

    # -----------------------------------------
    # GRÁFICO 6
    # -----------------------------------------
    elif opcao_grafico == "6. Aspectos Psicopedagógicos (IPP)":

        # ---> PERGUNTA 6 <---
        st.markdown("#### **Pergunta 6:**  As avaliações psicopedagógicas (IPP) confirmam ou contradizem a defasagem identificada pelo IAN?")

        df_q6 = df_analise.copy()
        def categorizar_ian(nota):
            if pd.isna(nota): return 'Sem nota'
            elif nota >= 9.0: return 'Adequado'
            elif nota >= 4.0: return 'Defasagem Moderada'
            else: return 'Defasagem Severa'

        df_q6['Perfil IAN'] = df_q6['ian'].apply(categorizar_ian)

        # Filtrando os quem tem nota no IAN e no IPP
        df_q6 = df_q6[(df_q6['Perfil IAN'] != 'Sem nota') & (df_q6['ipp'].notna())]
        
        # Contagem para o Eixo X
        contagens_q6 = df_q6.groupby('Perfil IAN').size().reset_index(name='qtd')
        df_q6 = df_q6.merge(contagens_q6, on='Perfil IAN')
        df_q6['Eixo X'] = df_q6['Perfil IAN'] + "<br>(n=" + df_q6['qtd'].astype(str) + ")"

        fig6 = px.box(df_q6, x='Eixo X', y='ipp', color='Perfil IAN',
                      title="6. Coerência: Avaliação Psicopedagógica (IPP) x Defasagem (IAN)",
                      color_discrete_map={'Adequado': 'green', 'Defasagem Moderada': 'orange', 'Defasagem Severa': 'red'},
                      category_orders={'Perfil IAN': ['Adequado', 'Defasagem Moderada', 'Defasagem Severa']}, height=500,
                      labels={'ipp': 'Nota Psicopedagógica (IPP)', 'Eixo X': 'Status de Defasagem (IAN)'})
        fig6.update_layout(yaxis=dict(range=[0, 11]), showlegend=False, margin=dict(b=80))
        
        st.plotly_chart(fig6, use_container_width=True)

        # <-- Resumo da análise do gráfico -->
        st.info("**Insight Analítico:** O gráfico indica elevada coerência. Alunos com Nível Adequado (IAN sem defasagem) recebem " \
        " notas maiores na avaliação psicopedagógica (IPP) em comparação aos alunos com defasagem 'moderada' ou 'severa'. Isso valida a metodologia de avaliação"
        " psicopedagógica aplicada pelos profissionais da Associação Passos Mágicos.")

    # -----------------------------------------
    # GRÁFICO 7 (Possui 2 gráficos: Correlação e Regressão)
    # -----------------------------------------
    elif opcao_grafico == "7. Fatores do Ponto de Virada (IPV)":
        
        from sklearn.linear_model import LinearRegression
        from sklearn.preprocessing import StandardScaler
        import numpy as np
        
        st.subheader(" Pergunta 7: O que mais influencia o aluno a 'virar a chave' (IPV)?")
        
        # Gráfico 7.1 - Correlações
        colunas_comportamento = ['ida', 'ieg', 'ips', 'ipp', 'iaa']
        df_corr = df_analise[colunas_comportamento + ['ipv']].dropna()
        correlacoes = df_corr.corr()['ipv'].drop('ipv').sort_values(ascending=True).reset_index()
        correlacoes.columns = ['Comportamento', 'Força da Influência']
        nomes_amigaveis = {'ida': 'Desempenho Acadêmico (IDA)', 'ieg': 'Engajamento (IEG)', 'ips': 'Saúde Psicossocial (IPS)', 'ipp': 'Avaliação Psicopedagógica (IPP)', 'iaa': 'Autoavaliação (IAA)'}
        correlacoes['Comportamento'] = correlacoes['Comportamento'].map(nomes_amigaveis)
        
        fig7_1 = px.bar(correlacoes, x='Força da Influência', y='Comportamento', orientation='h', title="Correlação Histórica com o IPV", text_auto='.2f', color='Força da Influência', color_continuous_scale='Blues', height=400)
        fig7_1.update_layout(xaxis_title="Grau de Influência (Pearson)", yaxis_title="", coloraxis_showscale=False)
        st.plotly_chart(fig7_1, use_container_width=True)
        
        # <-- Resumo - análise do gráfico 7.1 -->
        st.info("**Insight Analítico (Visão Geral):** Numa perspetiva histórica dos anos (2022 a 2024) somados, a Avaliação Pscicopedagógica (IPP), o Desempenho Acadêmico (IDA) e o Engajamento (IEG) " \
        "aparecem como os fatores mais fortemente correlacionados com o Ponto de Virada (IPV). Isto indica que a perfomance e a participação ativa dos alunos são a base para a transformação" \
        " de mentalidade, o que tem sido capturado pela equipe psicopedagógica. Por outro lado, os resultados de autoavaliação e os fatores psicossociais dos alunos apontam não haver correlação direta com o IPV.")

        st.divider()
        
        # Gráfico 7.2 - Regressão (Evolução da influência)
        indicadores = ['ida', 'ieg', 'ips', 'ipp', 'iaa']
        anos = [2022, 2023, 2024]
        dados_influencia = []

        for ano in anos:
            df_ano = df_analise[df_analise['ano'] == ano].dropna(subset=indicadores + ['ipv'])
            if len(df_ano) > 10:
                indicadores_validos = [ind for ind in indicadores if df_ano[ind].std() > 0]
                X = df_ano[indicadores_validos]
                y = df_ano['ipv']
                scaler = StandardScaler()
                X_scaled = scaler.fit_transform(X)
                y_scaled = (y - y.mean()) / y.std()
                modelo = LinearRegression()
                modelo.fit(X_scaled, y_scaled)
                for i, ind in enumerate(indicadores_validos):
                    if ano == 2022 and ind in ['ipp']: continue
                    dados_influencia.append({'Ano': str(ano), 'Indicador': ind, 'Grau de Influência': round(modelo.coef_[i], 3)})

        df_influencia = pd.DataFrame(dados_influencia)
        nomes_map = {'ida': 'Desempenho (IDA)', 'ieg': 'Engajamento (IEG)', 'ips': 'Psicossocial (IPS)', 'ipp': 'Psicopedagógico (IPP)', 'iaa': 'Autoavaliação (IAA)'}
        df_influencia['Indicador'] = df_influencia['Indicador'].map(nomes_map)

        fig7_2 = px.line(df_influencia, x='Ano', y='Grau de Influência', color='Indicador', markers=True, text='Grau de Influência', title="Evolução da Influência no Ponto de Virada (IPV)", height=500)
        fig7_2.update_layout(yaxis=dict(range=[-0.2, 1.2], zeroline=True, zerolinewidth=2, zerolinecolor='lightgray'), margin=dict(t=50, b=50), legend_title_text='Indicadores')
        fig7_2.update_traces(textposition='top center', textfont=dict(size=11))
        st.plotly_chart(fig7_2, use_container_width=True)

        # <-- Resumo - Análise do Gráfico 7.2 -->
        st.info("**Insight Analítico (Visão Evolutiva):** A quebra temporal através da regressão revela que o Desempenho acadêmico (IDA) e o Engajamento (IEG), este mais fortemente a partir de 2023," \
        " são os fatores preponderantes de correlação com o ponto de virada (IPV). Essa correlação passou a ser melhor capturada pela avaliação psicopedagógica (IPP), que pasou a ser realizada a partir de 2023.")

    # -----------------------------------------
    # GRÁFICO 8
    # -----------------------------------------
    elif opcao_grafico == "8. Multidimensionalidade (INDE)":

        # ---> PERGUNTA 8 <---
        st.markdown("#### **Pergunta 8:**  Quais combinações de indicadores (IDA + IEG + IPS + IPP) elevam mais a nota global do aluno (INDE)?")

        df_q8 = df_analise[df_analise['ano'].astype(str).isin(['2023', '2024'])].copy()
        c_ida = df_q8['ida'] >= 8
        c_ieg = df_q8['ieg'] >= 8
        c_ips = df_q8['ips'] >= 8
        c_ipp = df_q8['ipp'] >= 8

        combos = [
            {'Nome': 'Super combo (IDA + IEG+ IPS + IPP)', 'Media': df_q8[c_ida & c_ieg & c_ips & c_ipp]['inde'].mean()},
            {'Nome': 'IDA + IPS (Acadêmico + Psicosso)', 'Media': df_q8[c_ida & c_ips]['inde'].mean()},
            {'Nome': 'IEG + IPS (Engajam + Psicosso)', 'Media': df_q8[c_ieg & c_ips]['inde'].mean()},
            {'Nome': 'IDA + IPP (Acadêmico + Psicoped)', 'Media': df_q8[c_ida & c_ipp]['inde'].mean()},
            {'Nome': 'IPS + IPP (Psicosso + Psicoped)', 'Media': df_q8[c_ips & c_ipp]['inde'].mean()},
            {'Nome': 'IDA + IEG (Acadêmico + Engajam)', 'Media': df_q8[c_ida & c_ieg]['inde'].mean()},
            {'Nome': 'IEG + IPP (Engajam + Psicoped)', 'Media': df_q8[c_ieg & c_ipp]['inde'].mean()}
        ]
        df_combos = pd.DataFrame(combos).dropna().sort_values(by='Media', ascending=True)

        fig8 = px.bar(df_combos, x='Media', y='Nome', orientation='h',
                      title="8. Quais combinações elevam mais o INDE?",
                      text_auto='.2f', color='Media', color_continuous_scale='RdPu', height=500,
                      labels={'Media': 'INDE Médio Resultante', 'Nome': 'Melhores Combinações (Notas >= 8)'})
        
        fig8.update_layout(xaxis=dict(range=[0, 10.5], title="Nota Global Média Resultante (INDE)"), yaxis=dict(title=""), coloraxis_showscale=False)
        st.plotly_chart(fig8, use_container_width=True)

        # <-- Resumo análise do Gráfico -->
        st.info("**Insight Analítico:*** Como esperado o 'Super Combo' (quatro fatores, com valores acima de 8) resulta no maior Índice Global de Desenvolvimento Educacional (INDE). " \
        "No entanto, a grande descoberta é a combinação do **IDA + IPS** (Desempenho Académico + Avaliação Psicossocial), que isoladamente apresentou um INDE médio (8.71), muito próximo" \
        " ao Super Combo (8.93), provando que um ótimo desempenho acadêmico aliado a uma base psicossocial sólida possibilita ao aluno um resultado global de excelência no programa," \
        " mesmo que o engajamento ou o IPP oscilem.")
        
    # -----------------------------------------
    # GRÁFICO 9
    # -----------------------------------------
    elif opcao_grafico == "9. Padrões de Risco (Previsão de Defasagem)":

        # ---> PERGUNTA 9 <---
        st.markdown("#### **Pergunta 9:**  Quais padrões nos indicadores permitem identificar alunos em risco antes de queda no desempenho ou aumento da defasagem?")

        df_importancia = pd.DataFrame({
            'Indicador': [
                'Fase Ideal',
                'Ano de Ingresso',
                'Idade do Aluno', 
                'Instituição de Ensino Privada',
                'Fase no Programa', 
                'Ano',
                'Psicopedagógico (IPP)', 
                'Saúde Psicossocial (IPS)',
                'Defasagem',
                'Adequação de Nível (IAN)',
                'Autoavaliação (IAA)',
                'Ponto de Virada (IPV)', 
                'Engajamento (IEG)', 
                'Desempenho (IDA)'
            ],
            'Peso': [
                0.0001, 0.0003, 0.0007, 0.0009, 0.001, 0.002, 0.006, 0.029, 0.042, 0.052, 0.113, 0.131, 0.189, 0.433
            ]
        })

        # Transformando o peso em formato de Percentual (%)
        df_importancia['Percentual (%)'] = df_importancia['Peso'] * 100

        fig9 = px.bar(df_importancia, 
                      x='Percentual (%)', 
                      y='Indicador', 
                      orientation='h', 
                      title="9. Padrões de Risco: Qual a influência de cada indicador na decisão da IA?", 
                      color='Percentual (%)', 
                      color_continuous_scale='Viridis', 
                      height=600)
                      
        # Adicionando o símbolo de % diretamente no texto das barras
        fig9.update_traces(texttemplate='%{x:.2f}%', textposition='outside')
                      
        fig9.update_layout(
            coloraxis_showscale=False, 
            xaxis_title="Grau de Influência (%)", 
            yaxis_title="",
            margin=dict(l=50, r=50, t=80, b=50),
            xaxis=dict(range=[0, 50]) # Dá um respiro de espaço para a barra de 43%
        )
        
        st.plotly_chart(fig9, use_container_width=True)

        # <-- resumo da análise-->
        st.info("**Insight Analítico:** Observa-se que o algoritmo do modelo de previsão do risco de defasagem não pondera todas as variáveis de forma igual." \
        " O **Desempenho Acadêmico (IDA)** é o fator de maior criticidade (43.30%), seguido pelo Engajamento (IEG), com apenas (18,9%) de influência. " \
        "Isso significa que, do ponto de vista preditivo, quedas contínuas nestes dois pilares são os maiores alertas de que o aluno pode não atingir os objetivos" \
        " da sua 'Pedra' atual, exigindo ação imediata da tutoria do programa.")

    # -----------------------------------------
    # GRÁFICO 10
    # -----------------------------------------
    elif opcao_grafico == "10. Efetifidade do Programa (Evolução das Pedras)":

        # ---> PERGUNTA 10 <---
        st.markdown("#### **Pergunta 10:**  Os indicadores mostram melhora consistente ao longo do ciclo nas diferentes fases (Quartzo, Ágata, Ametista e Topázio), confirmando o impacto real do programa?")

        ordem_pedras = ['Quartzo', 'Ágata', 'Ametista', 'Topázio']
        df_jornada = df_tratado.groupby('pedra')[['inde', 'ida', 'ieg', 'ipv']].mean().reset_index()
        df_jornada['pedra'] = pd.Categorical(df_jornada['pedra'], categories=ordem_pedras, ordered=True)
        df_jornada = df_jornada.sort_values('pedra')
        df_plot_jornada = df_jornada.melt(id_vars='pedra', var_name='Indicador', value_name='Media')
        nomes_map = {'inde': 'Índice Geral (INDE)', 'ida': 'Desempenho (IDA)', 'ieg': 'Engajamento (IEG)', 'ipv': 'Ponto de Virada (IPV)'}
        df_plot_jornada['Indicador'] = df_plot_jornada['Indicador'].map(nomes_map)

        fig10 = px.line(df_plot_jornada, x='pedra', y='Media', color='Indicador', markers=True, text=df_plot_jornada['Media'].round(1),
                        title="10. O programa é efetivo e produz impacto na Melhoria dos Indicadores? (Evolução das Pedras)",
                        color_discrete_sequence=['#2ca02c', '#d62728', '#ff7f0e', '#1f77b4'], height=600,
                        labels={'pedra': 'Classificação do Aluno (Pedra)', 'Media': 'Nota Média Resultante'})
        
        fig10.update_traces(textposition='top center', line=dict(width=4), marker=dict(size=12))
        fig10.update_layout(yaxis=dict(range=[0, 11]), legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1))
        st.plotly_chart(fig10, use_container_width=True)

        # <-- Resumo da análise -->
        st.info("**Insight Analítico:** SIM, o gráfico comprova a efetividade do programa. À medida que o aluno progride na sua jornada de transformação "
        "(da base 'Quartzo' até ao nível de excelência 'Topázio'), todos os pilares avaliados — Desempenho, Engajamento e Ponto de Virada — apresentam um crescimento expressivo e linear. "
        "Isso demonstra que as réguas de progressão não são apenas burocráticas, mas refletem um amadurecimento real, sólido e multidimensional do estudante.")

    # -----------------------------------------
    # GRÁFICO 11
    # -----------------------------------------
    elif opcao_grafico == "11. Termômetro de Risco por Fase":

        # ---> Insights e Criatividade 1 <---
        st.markdown("#### **Pergunta 11 (Insights):**  Quais as fases do programa apresentam maiores indicativos de risco de defasagem?")
        
        df_fase_risco = df_tratado.groupby('fase')['risco_defasagem'].mean().reset_index()
        df_fase_risco['taxa_risco'] = (df_fase_risco['risco_defasagem'] * 100).round(1)

        # Ajustando a nomenclatura das Fase: 0 == 'Alpha' e as demais 'Fase X'
        df_fase_risco['Nome da Fase'] = df_fase_risco['fase'].apply(lambda x: 'Alpha' if x == 0 else f'Fase {x}')

        fig11 = px.bar(df_fase_risco, x='Nome da Fase', y='taxa_risco', color='taxa_risco', color_continuous_scale='Reds', text_auto='.1f', 
                       title="11. Termômetro de Vulnerabilidade (% de Risco por Fase)", height=500,
                       labels={'taxa_risco': 'Alunos em Risco (%)', 'Nome da Fase': 'Fases do Programa'})
                
        fig11.update_layout(yaxis=dict(range=[0, 70]), coloraxis_showscale=False, template="plotly_white", margin=dict(l=50, r=50, t=80, b=50))
        fig11.update_traces(textfont_size=12, textposition='outside', marker_line_color='rgb(255,255,255)', marker_line_width=1.5)
        
        st.plotly_chart(fig11, use_container_width=True)

        # <-- Adicionando o resumo/insight -->
        st.info("**Insight Analítico:** O mapeamento revela um padrão de risco muito específico, concentrado nas fase intermediárias do programa (2 a 5). Enquanto as fases iniciais (Alpha e 1)" \
        " e finais (6 e 7) apresentam risco de defasagem em patamares inferiores. Logo, as **Fases 2 e 3** acendem um alerta ao programa, indicando que a transição pedagógica" \
        " que ocorre nestas fases exige um plano de contenção robusto e urgente por parte da Associação Passos Mágicos.")

    # -----------------------------------------
    # GRÁFICO 12
    # -----------------------------------------
    elif opcao_grafico == "12. Comparativo de desempenho (Escola Pública vs Privada)":

        # ---> Insights e Criatividade 2 <---
        st.markdown("#### **Pergunta 12 (Insights):** Existe diferença no resultado médio dos indicadores de desempenho entre alunos de Escolas Públicas e Privadas?")

        # Filtra os dados apenas para escola Pública ou Privada nos anos desejados
        df_inst = df_tratado[(df_tratado['ano'].astype(str).isin(['2022', '2023', '2024'])) & 
                             (df_tratado['instituicao_ensino'].isin(['Pública', 'Privada']))].copy()
        
        # Calcula a média dos indicadores por tipo de instituição
        df_comparativo = df_inst.groupby('instituicao_ensino')[['inde', 'ida', 'ieg']].mean().reset_index()
        
        df_melted_inst = df_comparativo.melt(id_vars='instituicao_ensino', var_name='Indicador', value_name='Media')
        
        # Mapeia para nomes amigáveis nas legendas
        nomes_inst = {'inde': 'Índice Global (INDE)', 'ida': 'Desempenho Acadêmico (IDA)', 'ieg': 'Engajamento (IEG)'}
        df_melted_inst['Indicador'] = df_melted_inst['Indicador'].map(nomes_inst)

        # Cria o gráfico de barras agrupadas
        fig12 = px.bar(df_melted_inst, 
                       x='instituicao_ensino', y='Media', color='Indicador', barmode='group', text_auto='.1f', 
                       title="12. Comparativo: Média de desempenho dos alunos (Escola Pública vs Privada)", 
                       color_discrete_sequence=['#85C1E9', '#82E0AA', '#F9E79F'], 
                       height=550,
                       labels={'instituicao_ensino': 'Tipo de Escola', 'Media': 'Média Resultante'})
        
        # --- Ajustes de visualização ---
                
        fig12.update_layout(
            yaxis=dict(range=[0, 10]), 
            xaxis=dict(title=""),
            bargap=0.45,      
            bargroupgap=0.05,
            legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1, title=""),
            margin=dict(l=50, r=50, t=100, b=50),
            template="plotly_white"
        )
        
        st.plotly_chart(fig12, use_container_width=True)
        
        # <-- Resumo/insight -->
        st.info("**Insight Analítico:** Os gráfico demonstram que as médias dos indices Globais (INDE), Acadêmico (IDA) e de Engamento (IEG) dos alunos da **Rede Privada**, dentro do programa, " \
        "são superiores às dos alunos de **Escola Pública**. A maior diferença está no IDA (0.9 pontos), já no IEG a diferença na média reduz para (0.5 pontos).")
        
# ==========================================
# GAVETA 3: MODELO PREDITIVO DE RISCO
# ==========================================

elif pagina == "💡Modelo Preditivo (Risco Defasagem)":
        st.title("💡 Passos Mágicos: IA Educacional")
        st.markdown("""
        <div style="font-size: 1.3rem; line-height: 1.6;">
            <b>Sistema de Diagnóstico e Prevenção de Risco.</b><br>
            Simule os indicadores do aluno para avaliar a probabilidade de queda de desempenho 
            e receba recomendações para intervenção pedagógica direcionada.
        </div>
        """, unsafe_allow_html=True)
        st.divider()

        if not modelo_pronto:
            st.error(f"🚨 O arquivo do modelo ('modelo_passos_magicos.pkl') não foi encontrado ou deu erro. Detalhe: {erro_modelo}")
        else:
            # --- FORMULÁRIO NO MENU LATERAL (Aparece só nesta página) ---
            st.sidebar.header("🧑‍🎓 Perfil do Aluno")
            idade = st.sidebar.number_input("Idade", min_value=7, max_value=25, value=14)
            ano = st.sidebar.number_input("Ano da Avaliação", min_value=2020, max_value=2026, value=2024)
            ano_ingresso = st.sidebar.number_input("Ano de Ingresso no Programa", min_value=2010, max_value=2026, value=2022)
            
            mapa_fase_atual = {
                "Alfa": 0, "Fase 1": 1, "Fase 2": 2, "Fase 3": 3,
                "Fase 4": 4, "Fase 5": 5, "Fase 6": 6, "Fase 7": 7, "Fase 8": 8
            }
            selecao_fase_atual = st.sidebar.selectbox("Fase Atual no Programa", list(mapa_fase_atual.keys()))
            fase = mapa_fase_atual[selecao_fase_atual] 

            mapa_series = {
                "1º ano do Fundamental": 0, "2º ano do Fundamental": 0, "3º ano do Fundamental": 1,
                "4º ano do Fundamental": 1, "5º ano do Fundamental": 2, "6º ano do Fundamental": 2,
                "7º ano do Fundamental": 3, "8º ano do Fundamental": 3, "9º ano do Fundamental": 4,
                "1º ano do Ensino Médio": 5, "2º ano do Ensino Médio": 6, "3º ano do Ensino Médio": 7, "Universitário": 8
            }
            serie_escolar = st.sidebar.selectbox("Série Escolar do Aluno", list(mapa_series.keys()))
            
            # --- CÁLCULOS ---
            fase_ideal = mapa_series[serie_escolar]
            defasagem_valor = fase - fase_ideal 
            nome_fase_ideal = "Alfa" if fase_ideal == 0 else f"Fase {fase_ideal}"
            
            if defasagem_valor >= 0:
                texto_defasagem = ":green[Sem Defasagem]"
                ian = 10.0
            elif defasagem_valor in [-1, -2]:
                texto_defasagem = f":orange[Defasagem Moderada ({defasagem_valor})]"
                ian = 5.0
            else: # Menor ou igual a -3
                texto_defasagem = f":red[Defasagem Severa ({defasagem_valor})]" 
                ian = 2.5 
            
            st.sidebar.info(f"📌 **Fase Ideal:** {nome_fase_ideal} | **Status:** {texto_defasagem}")
            instituicao = st.sidebar.selectbox("Instituição de Ensino", ["Pública", "Privada"])
            
            st.sidebar.header("📊 Indicadores Passos Mágicos")
            ida = st.sidebar.slider("Desempenho Acadêmico (IDA)", 0.0, 10.0, 5.0, 0.1)
            ieg = st.sidebar.slider("Engajamento (IEG)", 0.0, 10.0, 5.0, 0.1)
            iaa = st.sidebar.slider("Autoavaliação (IAA)", 0.0, 10.0, 5.0, 0.1)
            ips = st.sidebar.slider("Indicador Psicossocial (IPS)", 0.0, 10.0, 5.0, 0.1)
            ipp = st.sidebar.slider("Avaliação Psicopedagógica (IPP)", 0.0, 10.0, 5.0, 0.1)
            ipv = st.sidebar.slider("Ponto de Virada (IPV)", 0.0, 10.0, 5.0, 0.1)
                        
            st.sidebar.markdown("---")
            analisar_botao = st.sidebar.button("Gerar Diagnóstico 🔍", use_container_width=True, type="primary")
            
            # --- LÓGICA DE PREVISÃO E RESULTADOS ---
            if analisar_botao:
                dados_entrada = {
                    'idade': [idade], 'ano': [ano], 'ano_ingresso': [ano_ingresso],
                    'fase': [fase], 'fase_ideal': [fase_ideal],
                    'defasagem': [defasagem_valor], 'instituicao_ensino': [instituicao],
                    'ida': [ida], 'ieg': [ieg], 'iaa': [iaa], 'ips': [ips], 
                    'ipp': [ipp], 'ipv': [ipv], 'ian': [ian] # O IAN (apenas valor calculado implícito)
                }
                
                df_novo_aluno = pd.DataFrame(dados_entrada)
                
                try:
                    df_novo_aluno['instituicao_ensino'] = df_novo_aluno['instituicao_ensino'].astype(str)
                    df_novo_aluno = df_novo_aluno[modelo.feature_names_in_]
                    
                    with st.spinner('O modelo está processando os dados inseridos com com o histórico de indicadores do programa...'):
                        previsao = modelo.predict(df_novo_aluno)[0]
                        probabilidade = modelo.predict_proba(df_novo_aluno)[0][1] * 100 
                        
                        # Veredito
                        st.subheader("1. Resultado Calculado do Risco")
                        if previsao == 1:
                            st.error(f"### ⚠️ ALTO RISCO DE QUEDA DE DESEMPENHO")
                            st.markdown(f"#### **Probabilidade de Risco:** `{probabilidade:.1f}%`")
                            st.markdown("###### O modelo detectou uma forte tendência de que este aluno sofra regressão nos seus resultados (risco de rebaixamento de Pedra ou evasão).")
                        else:
                            st.success(f"### ✅ ALUNO FORA DE RISCO (ESTÁVEL)")
                            st.markdown(f"**Probabilidade de Risco:** `{probabilidade:.1f}%` (Controlada)")
                            st.markdown("###### Os indicadores atuais sustentam um desenvolvimento saudável. A probabilidade de queda de Pedra é baixa.")
                        
                        # Raio-X
                        st.subheader("2. Raio-X dos Indicadores (Onde Direcionar os Esforços?)")
                        dic_indicadores = {
                            "IDA (Desempenho Acadêmico)": ida, "IEG (Engajamento)": ieg, "IAA (Autoavaliação)": iaa,
                            "IPS (Psicossocial)": ips, "IPP (Psicopedagógica)": ipp, "IPV (Ponto de Virada)": ipv
                        }
                        
                        indicadores_ordenados = sorted(dic_indicadores.items(), key=lambda x: x[1])
                        pontos_criticos = [item for item in indicadores_ordenados if item[1] <= 6.0]
                        
                        col_a, col_b = st.columns(2)
                        with col_a:
                            st.markdown("#### 🚨 Focos de Alerta (Prioridades)")
                            if len(pontos_criticos) > 0:
                                st.markdown("##### O programa deve direcionar esforços imediatos para:")
                                for nome, nota in pontos_criticos[:3]: 
                                    st.warning(f"**{nome}:** Nota {nota:.1f}")
                                if defasagem_valor < 0:
                                    st.warning(f"**Defasagem de Série:** Aluno está {abs(defasagem_valor)} fase(s) atrás do ideal.")
                            else:
                                st.success("Não há indicadores em nível crítico (< 6.0) no momento.")
                                
                        with col_b:
                            st.markdown("#### 🏅 Pontos Fortes (Apoio)")
                            melhores = indicadores_ordenados[-3:] 
                            melhores.reverse()
                            st.write("##### Utilize estes pontos para alavancar a confiança do aluno:")
                            for nome, nota in melhores:
                                st.info(f"**{nome}:** Nota {nota:.1f}")
                        
                        st.divider()
                        st.markdown("###### **Nota:** Este diagnóstico orienta a equipe do Programa Passos Mágico sobre quais dimensões focar para garantir a evolução do aluno na metodologia" \
                        " das Pedras.")
                        st.markdown("###### ***⚠️ Esta é uma ferramenta de suporte à decisão. A análise final deve sempre considerar a avaliação de profissionais especializados***")
                
                except Exception as e:
                    st.error(f"Erro ao processar o modelo: {e}. Verifique se não há inconsistência nos dados inseridos.")
            
            else:
                st.info("👈 Preencha as notas e a série do aluno no menu lateral e clique em 'Gerar Diagnóstico' para avaliar o risco.")