import streamlit as st
import streamlit.components.v1 as components
import pandas as pd
import yfinance as yf
import seaborn as sns
import fundamentus as fd
import matplotlib.pyplot as plt
#import plotly.graph_objects as go
import plotly.express as px
from datetime import date
from bcb import sgs




st.set_page_config(page_title="Mapa de Ações", layout="wide")
# Página Home_______________________________________________________________________________
def home():    
    col1, col2,col3 = st.columns([1,3,1])
    with col1:   

        st.image('logo_pa.png')

    with col2:

        st.title('MarketView')


    st.header("Taxas de Câmbio")

    # Código HTML do iframe de Taxas de Câmbio do Investing.com
    iframe_code = """
    <iframe frameborder="0" scrolling="auto" height="400" width="1000" allowtransparency="true" 
        marginwidth="0" marginheight="0" 
        src="https://sslfxrates.investing.com/index_exchange.php?params&inner-border-color=%23d1d1d1&border-color=%23000000&bg1=%23F6F6F6&bg2=%23ffffff&inner-text-color=%23000000&currency-name-color=%23000000&header-text-color=%23FFFFFF&header-bg=%23979797&force_lang=12" 
        align="center"></iframe><br />
    <div style="width:540px">
        <a href="http://br.investing.com" target="_blank">
            <img src="https://wmt-invdn-com.investing.com/forexpros_pt_logo.png" alt="Investing.com" title="Investing.com" style="float:left" />
        </a>
        <span style="float:right">
            <span style="font-size: 11px;color: #333333;text-decoration: none;">
                Taxas de Câmbio fornecidas por 
                <a href="https://br.investing.com/" rel="nofollow" target="_blank" 
                style="font-size: 11px;color: #06529D; font-weight: bold;" class="underline_link">
                Investing.com Brasil
                </a>.
            </span>
        </span>
    </div>
    """

    # Renderizando o HTML no Streamlit
    components.html(iframe_code, height=250)




# Página Calendario_________________________________________________________________________ok
def calendario():    
    st.title("Calendário Econômico")

    # Novo código HTML do iframe do Investing.com
    iframe_code = """
    <iframe src="https://sslecal2.investing.com?columns=exc_flags,exc_currency,exc_importance,exc_actual,exc_forecast,exc_previous&importance=2,3&features=datepicker,timezone,timeselector,filters&countries=17,32,37,5,22,39,35,4,12&calType=day&timeZone=12&lang=12" 
        width="700" height="600" frameborder="0" allowtransparency="true" 
        marginwidth="0" marginheight="0"></iframe>
    <div class="poweredBy" style="font-family: Arial, Helvetica, sans-serif;">
        <span style="font-size: 11px;color: #333333;text-decoration: none;">
            Calendário Econômico fornecido por 
            <a href="https://br.investing.com/" rel="nofollow" target="_blank" 
            style="font-size: 11px;color: #06529D; font-weight: bold;" class="underline_link">
            Investing.com Brasil
            </a>.
        </span>
    </div>
    """

    # Renderizando o HTML no Streamlit
    components.html(iframe_code, height=750)


# Página Panorama___________________________________________________________________________
#st.set_page_config(page_title="Mapa de Ações", layout="wide")
def panorama():
    #st.set_page_config(page_title="Mapa de Ações", layout="wide")
    st.title('Panorama do Mercado')
    st.markdown(date.today().strftime('%d/%m/%Y'))

    st.subheader('Mercados pelo Mundo')

# Criando DataFrame vazio
   # df_info = pd.DataFrame(columns=['Ativo', 'Ticker', 'Ult. Valor', '%'])

# Dicionário de ativos e tickers
    dict_tickers = {
                'Bovespa':'^BVSP', 
                'S&P500':'^GSPC',
                'NASDAQ':'^IXIC', 
                'DAX':'^GDAXI', 
                'FTSE 100':'^FTSE',
                'Cruid Oil': 'CL=F',
                'Gold':'GC=F',
                'BITCOIN':'BTC-USD',
                'ETHEREUM':'ETH-USD'
                }

    df_info = pd.DataFrame({'Ativo': dict_tickers.keys(),'Ticker': dict_tickers.values()})
    
    df_info['Ult. Valor'] = ''
    df_info['%'] = ''
    count =0

    with st.spinner('Baixando cotação...'):
        for ticker in dict_tickers.values():
            cotacoes = yf.download(ticker, period='5d')['Close']
            variacao = (float(cotacoes.iloc[-1]/cotacoes.iloc[-2])-1)*100
            df_info['Ult. Valor'][count] = round(float(cotacoes.iloc[-1]), 2)
            df_info['%'][count] =round(variacao,2)
            count += 1

  #  st.write(df_info)
   
    col1, col2, col3 = st.columns(3)
    with col1:
        st.subheader('Indices')
        st.metric(label=df_info['Ativo'][0], value=df_info['Ult. Valor'][0], delta=str(df_info['%'][0])+ '%')
        st.metric(label=df_info['Ativo'][1], value=df_info['Ult. Valor'][1], delta=str(df_info['%'][1])+ '%')
        st.metric(label=df_info['Ativo'][2], value=df_info['Ult. Valor'][2], delta=str(df_info['%'][2])+ '%')
        st.metric(label=df_info['Ativo'][3], value=df_info['Ult. Valor'][3], delta=str(df_info['%'][3])+ '%')
        st.metric(label=df_info['Ativo'][4], value=df_info['Ult. Valor'][4], delta=str(df_info['%'][4])+ '%')
    
    with col2:
        st.subheader('Commodities')        
        st.metric(label=df_info['Ativo'][5], value=df_info['Ult. Valor'][5], delta=str(df_info['%'][5])+ '%')
        st.metric(label=df_info['Ativo'][6], value=df_info['Ult. Valor'][6], delta=str(df_info['%'][6])+ '%')
    
    with col3:
        st.subheader('Criptos')        
        st.metric(label=df_info['Ativo'][7], value=df_info['Ult. Valor'][7], delta=str(df_info['%'][7])+ '%')
        st.metric(label=df_info['Ativo'][8], value=df_info['Ult. Valor'][8], delta=str(df_info['%'][8])+ '%')
    

    st.markdown('---')
    st.title('')
    # Configuração do Streamlit
   
    st.title("📊 Mapa de Ações do Mercado Financeiro")

    # Lista de ações
    acoes = ['ALOS3', 'ABEV3', 'ASAI3', 'AURE3', 'AMOB3', 'AZUL4', 'AZZA3', 'B3SA3', 'BBSE3', 'BBDC3', 'BBDC4', 'BRAP4', 'BBAS3', 'BRKM5', 'BRAV3', 'BRFS3', 'BPAC11', 'CXSE3', 'CRFB3', 'CCRO3', 'CMIG4', 'COGN3', 'CPLE6', 'CSAN3', 'CPFE3', 'CMIN3', 'CVCB3', 'CYRE3', 'ELET3', 'ELET6', 'EMBR3', 'ENGI11', 'ENEV3', 'EGIE3', 'EQTL3', 'FLRY3', 'GGBR4', 'GOAU4', 'NTCO3', 'HAPV3', 'HYPE3', 'IGTI11', 'IRBR3', 'ISAE4', 'ITSA4', 'ITUB4', 'JBSS3', 'KLBN11', 'RENT3', 'LREN3', 'LWSA3', 'MGLU3', 'POMO4', 'MRFG3', 'BEEF3', 'MRVE3', 'MULT3', 'PCAR3', 'PETR3', 'PETR4', 'RECV3', 'PRIO3', 'PETZ3', 'PSSA3', 'RADL3', 'RAIZ4', 'RDOR3', 'RAIL3', 'SBSP3', 'SANB11', 'STBP3', 'SMTO3', 'CSNA3', 'SLCE3', 'SUZB3', 'TAEE11', 'VIVT3', 'TIMS3', 'TOTS3', 'UGPA3', 'USIM5', 'VALE3', 'VAMO3', 'VBBR3', 'VIVA3', 'WEGE3', 'YDUQ3']
    acoes_dict = {acao: acao + '.SA' for acao in acoes}

    dados = {}
    variacao = {}

    st.info("🔄 Carregando dados... Isso pode levar alguns segundos.")

    # Baixando dados das ações
    for acao, ticker in acoes_dict.items():
        try:
            hist = yf.Ticker(ticker).history(period="2d")["Close"]
            if len(hist) > 1:
                dados[acao] = hist.iloc[-1]  # Último preço de fechamento
                variacao[acao] = ((hist.iloc[-1] / hist.iloc[-2]) - 1) * 100  # Variação diária
        except Exception as e:
            st.warning(f"⚠️ Erro ao obter dados de {acao}: {e}")

    # Criar DataFrame e Treemap
    df = pd.DataFrame(dados.items(), columns=["Ticker", "Último Preço"])
    df["Variação (%)"] = df["Ticker"].map(variacao)
    df["Label"] = df["Ticker"] + " (" + df["Variação (%)"].round(2).astype(str) + "%)"

    # Criando o Treemap
    if not df.empty:
        fig = px.treemap(df,
                         path=["Label"],
                         values="Último Preço",
                         color="Variação (%)",
                         color_continuous_midpoint=0,
                         color_continuous_scale=[(0, "darkred"), (0.5, "white"), (1, "darkgreen")],
                         title="📊 Mapa de Ações - Desempenho Diário")
        st.plotly_chart(fig, use_container_width=True)
    else:
        st.warning("⚠️ Nenhum dado disponível para exibição.")


# Página Mapa Mensal________________________________________________________________________
def retorno_mensal():
    st.title('Retorno Mensal')

    with st.expander('Escolha', expanded=True):
        opcao = st.radio('Selecione', ['Índices', 'Ações', 'Commodities'])

    if opcao == 'Índices':
        indices = {'IBOV': '^BVSP',
                    'S&P500': '^GSPC',     
                    'NASDAQ': '^IXIC',
                    'FTSE100':'^FTSE',
                    'DAX':'^GDAXI',
                    'CAC40':'^FCHI',
                    'SSE Composite':'000001.SS',
                    'Nikkei225':'^N225',
                    'Merval':'^MERV'}
        with st.form(key='form_indice'):
            escolha = st.selectbox('Índice', list(indices.keys()))
            analisar = st.form_submit_button('Analisar')
            ticker = indices[escolha]

    elif opcao == 'Commodities':
        commodities = {'Ouro': 'GC=F',
                    'Prata': 'SI=F',
                    'Platinum': 'PL=F',     
                    'Cobre': 'HG=F',
                    'WTI Oil':'CL=F',
                    'Brent Oil':'BZ=F',
                    'Milho':'ZC=F',
                    'Soja':'ZS=F',
                    'Café':'KC=F'}    
        with st.form(key='form_commodities'):
            escolha = st.selectbox('Commodities', list(commodities.keys()))
            analisar = st.form_submit_button('Analisar')
            ticker = commodities[escolha]

    elif opcao == 'Ações':
        acoes = ['ALOS3', 'ABEV3', 'ASAI3', 'AURE3', 'AMOB3', 'AZUL4', 'AZZA3', 'B3SA3', 'BBSE3', 'BBDC3', 'BBDC4', 
                 'BRAP4', 'BBAS3', 'BRKM5', 'BRAV3', 'BRFS3', 'BPAC11', 'CXSE3', 'CRFB3', 'CCRO3', 'CMIG4', 'COGN3', 
                 'CPLE6', 'CSAN3', 'CPFE3', 'CMIN3', 'CVCB3', 'CYRE3', 'ELET3', 'ELET6', 'EMBR3', 'ENGI11', 'ENEV3', 
                 'EGIE3', 'EQTL3', 'FLRY3', 'GGBR4', 'GOAU4', 'NTCO3', 'HAPV3', 'HYPE3', 'IGTI11', 'IRBR3', 'ISAE4', 
                 'ITSA4', 'ITUB4', 'JBSS3', 'KLBN11', 'RENT3', 'LREN3', 'LWSA3', 'MGLU3', 'POMO4', 'MRFG3', 'BEEF3', 
                 'MRVE3', 'MULT3', 'PCAR3', 'PETR3', 'PETR4', 'RECV3', 'PRIO3', 'PETZ3', 'PSSA3', 'RADL3', 'RAIZ4', 
                 'RDOR3', 'RAIL3', 'SBSP3', 'SANB11', 'STBP3', 'SMTO3', 'CSNA3', 'SLCE3', 'SUZB3', 'TAEE11', 'VIVT3', 
                 'TIMS3', 'TOTS3', 'UGPA3', 'USIM5', 'VALE3', 'VAMO3', 'VBBR3', 'VIVA3', 'WEGE3', 'YDUQ3']

        # Criando um dicionário com chave como o nome da ação e valor como o nome da ação com '.SA'
        acoes_dict = {acao: acao + '.SA' for acao in acoes}

        with st.form(key='form_acoes'):
            escolha = st.selectbox('Ações', list(acoes_dict.keys()))
            analisar = st.form_submit_button('Analisar')
            ticker = acoes_dict[escolha]



    #________________________________________________________________
    
    if analisar:
        data_inicial = ('1999-12-01')
        data_final = ('2030-12-31')

        # Baixa os dados do Yahoo Finance
        dados = yf.download(ticker, start=data_inicial, end=data_final, interval="1mo")

        if not dados.empty:
            retornos = dados['Close'].pct_change().dropna()
            #st.dataframe(retornos)
            # Adiciona colunas de ano e mês para organização
            retornos = retornos.reset_index()
            retornos['Year'] = retornos['Date'].dt.year
            retornos['Month'] = retornos['Date'].dt.month

        # Criar a tabela pivot sem média, apenas reorganizando os dados
            tabela_retornos = retornos.pivot(index='Year', columns='Month', values=ticker)
            tabela_retornos.columns = ['Jan', 'Fev', 'Mar', 'Abr', 'Mai', 'Jun', 
                                            'Jul', 'Ago', 'Set', 'Out', 'Nov', 'Dez']

            #st.write(tabela_retornos_pivot)
            
    # Criando Heatmap
    # Heatmap
            fig, ax = plt.subplots(figsize=(12, 9))
            cmap = sns.color_palette('RdYlGn', 15)
            sns.heatmap(tabela_retornos, cmap=cmap, annot=True, fmt='.2%', center=0, vmax=0.025, vmin=-0.025, cbar=False,
                        linewidths=0.5, xticklabels=True, yticklabels=True, ax=ax)
            ax.set_title(f'Heatmap Retorno Mensal - {escolha}', fontsize=18)
            ax.set_yticklabels(ax.get_yticklabels(), rotation=0, verticalalignment='center', fontsize='12')
            ax.set_xticklabels(ax.get_xticklabels(), fontsize='12')
          #  ax.xaxis.tick_top()  # x axis em cima
            plt.ylabel('')
            st.pyplot(fig)
       
        else:
            st.error("Erro ao buscar os dados. Verifique o ticker ou tente novamente mais tarde.")
    
    #Estatisticas
        stats = pd.DataFrame(tabela_retornos.mean(), columns=['Média'])
        stats['Mediana'] = tabela_retornos.median()
        stats['Maior'] = tabela_retornos.max()
        stats['Menor'] = tabela_retornos.min()
        stats['Positivos'] = tabela_retornos.gt(0).sum()/tabela_retornos.count() # .gt(greater than) = Contagem de números maior que zero
        stats['Negativos'] = tabela_retornos.le(0).sum()/tabela_retornos.count() # .le(less than) = Contagem de nomeros menor que zero

    #Stats_A
        stats_a = stats[['Média','Mediana','Maior','Menor']].transpose()

        fig, ax = plt.subplots(figsize=(12, 2))
        sns.heatmap(stats_a, cmap = cmap, annot=True, fmt='.2%', center=0, vmax=0.025, vmin=-0.025, cbar=False,
                        linewidths=0.5, xticklabels=True, yticklabels=True, ax=ax)
        st.pyplot(fig)

        
    #Stats_B
        stats_b = stats[['Positivos','Negativos']].transpose()

        fig, ax = plt.subplots(figsize=(12, 1))
        sns.heatmap(stats_b,cmap = sns.color_palette("magma", as_cmap=True), annot=True, fmt='.2%', center=0, vmax=0.025, vmin=-0.025, cbar=False,
                        linewidths=0.5, xticklabels=True, yticklabels=True, ax=ax)      
        
 
        st.pyplot(fig)

    # Título do app para gráfico
    st.subheader(f'Evolução do Preço - {escolha}')

    # Entrada de datas
    inicio = st.date_input('Data de Início', value=pd.to_datetime('2010-01-01'), format="DD/MM/YYYY")
    fim = st.date_input('Data de Fim', value=pd.to_datetime('2025-02-01'), format="DD/MM/YYYY")

    # Baixar os dados e gerar o gráfico quando o botão for pressionado
    if st.button('Gerar gráfico de Preço'):
        try:
            # Baixar os dados históricos
            dados = yf.download(ticker, start=inicio, end=fim)['Close']

            # Verificar se os dados foram baixados corretamente
            if dados.empty:
                st.error(f'Nenhum dado foi encontrado para o ativo {escolha} no intervalo de datas selecionado.')
            else:
                # Criar o gráfico de preço
                fig, ax = plt.subplots(figsize=(10, 6))
                ax.plot(dados.index, dados, label=f'Preço de {escolha}', color='b')

                ax.set_title(f'Histórico de Preço - {escolha}')
                ax.set_xlabel('Data')
                ax.set_ylabel('Preço (R$ ou USD)')
                ax.legend()
                ax.grid(True)
                plt.xticks(rotation=45)

                st.pyplot(fig)

        except Exception as e:
            st.error(f'Ocorreu um erro: {e}')

        
# Página Política Monetária_________________________________________________________________
def juros():
    col1, col2, col3 = st.columns([1,3,1])
    with col2:    
        st.title('Política Monetária')
        st.write('')

    # Obtendo a taxa Selic
    selic = sgs.get({'Selic': 432}, start='2000-01-01')
    selic_atual = selic.iloc[-1].values[0]
    
    col1, col2 = st.columns([3, 1])
    with col1:
        # Plotando a série histórica da Selic com grelha
        plt.figure(figsize=(8, 4))
        selic['Selic'].plot(kind='line', title='Taxa de Juros SELIC')
        plt.gca().spines[['top', 'right']].set_visible(False)
        plt.ylabel('Taxa de Juros (%)')

        # Adicionando a grelha apenas no eixo Y (linhas horizontais)
        plt.grid(True, axis='y', linestyle='--', linewidth=0.5, color='gray')

        # Marcando a Selic atual com um ponto vermelho
        plt.scatter(selic.index[-1], selic_atual, color='red', zorder=5, label=f'Atual: {selic_atual:.2f}%')
        #plt.axhline(y=selic_atual, color='red', linestyle='--', zorder=5, label=f'Atual: {selic_atual:.2f}%')

        # Exibindo a legenda
        plt.legend()

        st.pyplot(plt)

    with col2:
        st.write('')
        st.write('')

        # Exibindo o iframe com alinhamento ajustado
        iframe_code = """
        <div style="text-align: center; padding: 10px;">
            <span style="font-size: 16px; font-weight: bold; display: block; margin-bottom: 8px;">Mundo</span>
            <iframe frameborder="0" scrolling="no" height="146" width="108" allowtransparency="true" marginwidth="0" marginheight="0" 
            src="https://sslirates.investing.com/index.php?rows=1&bg1=FFFFFF&bg2=F1F5F8&text_color=333333&enable_border=hide&border_color=0452A1&
            header_bg=ffffff&header_text=FFFFFF&force_lang=12" align="center"></iframe>
        </div>
        """
        st.components.v1.html(iframe_code, height=180)

    ipca = sgs.get({'IPCA':13522}, start='2000-01-01')
    ipca_atual = ipca.iloc[-1].values[0] 
    
    
    with col1:
        st.write('')
        st.write('')
        #Plotando Grafico   
        plt.figure(figsize=(8, 4))
        ipca['IPCA'].plot(kind='line', title='IPCA Acumulado 12M')
        plt.gca().spines[['top', 'right']].set_visible(False)
        plt.ylabel('IPCA acumulado (%)')

        # Adicionando a grelha apenas no eixo Y (linhas horizontais)
        plt.grid(True, axis='y', linestyle='--', linewidth=0.5, color='gray')

        # Marcando a Selic atual com um ponto vermelho
        plt.scatter(ipca.index[-1], ipca_atual, color='red', zorder=5, label=f'Atual: {ipca_atual:.2f}%')
        #plt.axhline(y=selic_atual, color='red', linestyle='--', zorder=5, label=f'Atual: {selic_atual:.2f}%')

        # Exibindo a legenda
        plt.legend()

        st.pyplot(plt)    


    

# Página Fundamentos________________________________________________________________________OK
def fundamentos():
    st.title('Dados Fundamentalistas')

    lista_tickers = ['PETR4', 'VALE3', 'ALOS3', 'ABEV3', 'ASAI3', 'AURE3', 'AMOB3', 'AZUL4', 'AZZA3', 'B3SA3', 'BBSE3', 'BBDC3', 'BBDC4', 
                 'BRAP4', 'BBAS3', 'BRKM5', 'BRAV3', 'BRFS3', 'BPAC11', 'CXSE3', 'CRFB3', 'CCRO3', 'CMIG4', 'COGN3', 
                 'CPLE6', 'CSAN3', 'CPFE3', 'CMIN3', 'CVCB3', 'CYRE3', 'ELET3', 'ELET6', 'EMBR3', 'ENGI11', 'ENEV3', 
                 'EGIE3', 'EQTL3', 'FLRY3', 'GGBR4', 'GOAU4', 'NTCO3', 'HAPV3', 'HYPE3', 'IGTI11', 'IRBR3', 'ISAE4', 
                 'ITSA4', 'ITUB4', 'JBSS3', 'KLBN11', 'RENT3', 'LREN3', 'LWSA3', 'MGLU3', 'POMO4', 'MRFG3', 'BEEF3', 
                 'MRVE3', 'MULT3', 'PCAR3', 'PETR3',  'RECV3', 'PRIO3', 'PETZ3', 'PSSA3', 'RADL3', 'RAIZ4', 
                 'RDOR3', 'RAIL3', 'SBSP3', 'SANB11', 'STBP3', 'SMTO3', 'CSNA3', 'SLCE3', 'SUZB3', 'TAEE11', 'VIVT3', 
                 'TIMS3', 'TOTS3', 'UGPA3', 'USIM5', 'VAMO3', 'VBBR3', 'VIVA3', 'WEGE3', 'YDUQ3']
    #st.write(lista_tickers)

    comparar = st.checkbox('Comparar 2 ativos')
    col1, col2  = st.columns(2)

    with col1:
        with st.expander('Ativo 1', expanded=True):
            papel1 = st.selectbox('Selecione o Papel', lista_tickers)
            st.session_state.papel1 = papel1
            info_papel1 = fd.get_detalhes_papel(papel1)
            #st.write(info_papel1)
            #st.write(info_papel1.columns)

            st.write('**Empresa:**', info_papel1['Empresa'][0])
            st.write('**Setor:**', info_papel1['Setor'][0])
            st.write('**Subsetor:**', info_papel1['Subsetor'][0])
            st.write('**Valor de Mercado:**',f"R$ {float(info_papel1['Valor_de_mercado'][0]):,.2f}".replace(',', 'X').replace('.', ',').replace('X', '.'))
            st.write('**Nº de ações:**', f"{float(info_papel1['Nro_Acoes'][0]):,.2f}".replace(',', 'X').replace('.', ',').replace('X', '.'))

            st.write('')
            
            st.caption(f"Últ. balanço processado: {pd.to_datetime(info_papel1['Ult_balanco_processado'][0]).strftime('%d/%m/%Y')}")
            st.caption('Dados Balanço Patrimonial')
            st.write('**Ativo:**',f"R$ {float(info_papel1['Ativo'][0]):,.2f}".replace(',', 'X').replace('.', ',').replace('X', '.'))
            st.write('**Disponibilidades:**',f"R$ {float(info_papel1['Disponibilidades'][0]):,.2f}".replace(',', 'X').replace('.', ',').replace('X', '.'))
            st.write('**Ativo Circulante:**',f"R$ {float(info_papel1['Ativo_Circulante'][0]):,.2f}".replace(',', 'X').replace('.', ',').replace('X', '.'))
            st.write('**Dívida Bruta:**', f"R$ {float(info_papel1['Div_Bruta'][0]):,.2f}".replace(',', 'X').replace('.', ',').replace('X', '.'))
            st.write('**Dívida Líquida:**', f"R$ {float(info_papel1['Div_Liquida'][0]):,.2f}".replace(',', 'X').replace('.', ',').replace('X', '.'))
            st.write('**Patrimônio Líquido:**', f"R$ {float(info_papel1['Patrim_Liq'][0]):,.2f}".replace(',', 'X').replace('.', ',').replace('X', '.'))
            st.write('')
            st.caption('Dados demonstrativos de resultados')
            st.write('**Receita Liq. 12m:**', f"R$ {float(info_papel1['Receita_Liquida_12m'][0]):,.2f}".replace(',', 'X').replace('.', ',').replace('X', '.'))
            st.write('**EBIT. 12m:**', f"R$ {float(info_papel1['EBIT_12m'][0]):,.2f}".replace(',', 'X').replace('.', ',').replace('X', '.'))
            st.write('**Lucro Liq. 12m:**', f"R$ {float(info_papel1['Lucro_Liquido_12m'][0]):,.2f}".replace(',', 'X').replace('.', ',').replace('X', '.'))
            st.write('')            
            st.caption('Indicadores Fundamentalista')
            st.write('**P/L:**', f"{float(info_papel1['PL'][0]) / 100:,.2f}")            
            st.write('**P/VP:**', f"{float(info_papel1['PVP'][0]) / 100:,.2f}")
            st.write('**P/EBIT:**', f"{float(info_papel1['PEBIT'][0]) / 100:,.2f}")
            st.write('**LPA:**', f"{float(info_papel1['LPA'][0]) / 100:,.2f}")
            st.write('**VPA:**', f"{float(info_papel1['VPA'][0]) / 100:,.2f}")
            st.write('**EV / EBITDA:**', f"{float(info_papel1['EV_EBITDA'][0]) / 100:,.2f}")
            st.write('**EV / EBIT:**', f"{float(info_papel1['EV_EBIT'][0]) / 100:,.2f}")
            st.write('**ROIC:**', f"{(info_papel1['ROIC'][0])}")            
            st.write('**ROE:**', f"{(info_papel1['ROE'][0])}") 
            st.write('**Marg. Bruta:**', f"{(info_papel1['Marg_Bruta'][0])}") 
            st.write('**Marg. EBIT:**', f"{(info_papel1['Marg_EBIT'][0])}") 
            st.write('**Marg. Liquida:**', f"{(info_papel1['Marg_Liquida'][0])}") 
            st.write('**Div. Bruta/ Patrim.:**', f"{float(info_papel1['Div_Br_Patrim'][0])}%") 

            st.write('**Dividend Yield:**', f"{info_papel1['Div_Yield'][0]}")

    if comparar:
        with col2:
            with st.expander('Ativo 2', expanded=True):
                papel2 = st.selectbox('Selecione o 2º Papel', lista_tickers)
                info_papel2 = fd.get_detalhes_papel(papel2)
                st.write('**Empresa:**', info_papel2['Empresa'][0])
                st.write('**Setor:**', info_papel2['Setor'][0])
                st.write('**Subsetor:**', info_papel2['Subsetor'][0])
                st.write('**Valor de Mercado:**',f"R$ {float(info_papel2['Valor_de_mercado'][0]):,.2f}".replace(',', 'X').replace('.', ',').replace('X', '.'))
                st.write('**Nº de ações:**', f"{float(info_papel2['Nro_Acoes'][0]):,.2f}".replace(',', 'X').replace('.', ',').replace('X', '.'))

                st.write('')
                
                st.caption(f"Últ. balanço processado: {pd.to_datetime(info_papel2['Ult_balanco_processado'][0]).strftime('%d/%m/%Y')}")
                st.caption('Dados Balanço Patrimonial')
                st.write('**Ativo:**',f"R$ {float(info_papel2['Ativo'][0]):,.2f}".replace(',', 'X').replace('.', ',').replace('X', '.'))
                st.write('**Disponibilidades:**',f"R$ {float(info_papel2['Disponibilidades'][0]):,.2f}".replace(',', 'X').replace('.', ',').replace('X', '.'))
                st.write('**Ativo Circulante:**',f"R$ {float(info_papel2['Ativo_Circulante'][0]):,.2f}".replace(',', 'X').replace('.', ',').replace('X', '.'))
                st.write('**Dívida Bruta:**', f"R$ {float(info_papel2['Div_Bruta'][0]):,.2f}".replace(',', 'X').replace('.', ',').replace('X', '.'))
                st.write('**Dívida Líquida:**', f"R$ {float(info_papel2['Div_Liquida'][0]):,.2f}".replace(',', 'X').replace('.', ',').replace('X', '.'))
                st.write('**Patrimônio Líquido:**', f"R$ {float(info_papel2['Patrim_Liq'][0]):,.2f}".replace(',', 'X').replace('.', ',').replace('X', '.'))
                st.write('')
                st.caption('Dados demonstrativos de resultados')
                st.write('**Receita Liq. 12m:**', f"R$ {float(info_papel2['Receita_Liquida_12m'][0]):,.2f}".replace(',', 'X').replace('.', ',').replace('X', '.'))
                st.write('**EBIT. 12m:**', f"R$ {float(info_papel2['EBIT_12m'][0]):,.2f}".replace(',', 'X').replace('.', ',').replace('X', '.'))
                st.write('**Lucro Liq. 12m:**', f"R$ {float(info_papel2['Lucro_Liquido_12m'][0]):,.2f}".replace(',', 'X').replace('.', ',').replace('X', '.'))
                st.write('')            
                st.caption('Indicadores Fundamentalista')
                st.write('**P/L:**', f"{float(info_papel2['PL'][0]) / 100:,.2f}")            
                st.write('**P/VP:**', f"{float(info_papel2['PVP'][0]) / 100:,.2f}")
                st.write('**P/EBIT:**', f"{float(info_papel2['PEBIT'][0]) / 100:,.2f}")
                st.write('**LPA:**', f"{float(info_papel2['LPA'][0]) / 100:,.2f}")
                st.write('**VPA:**', f"{float(info_papel2['VPA'][0]) / 100:,.2f}")
                st.write('**EV / EBITDA:**', f"{float(info_papel2['EV_EBITDA'][0]) / 100:,.2f}")
                st.write('**EV / EBIT:**', f"{float(info_papel2['EV_EBIT'][0]) / 100:,.2f}")
                st.write('**ROIC:**', f"{(info_papel2['ROIC'][0])}")            
                st.write('**ROE:**', f"{(info_papel2['ROE'][0])}") 
                st.write('**Marg. Bruta:**', f"{(info_papel2['Marg_Bruta'][0])}") 
                st.write('**Marg. EBIT:**', f"{(info_papel2['Marg_EBIT'][0])}") 
                st.write('**Marg. Liquida:**', f"{(info_papel2['Marg_Liquida'][0])}") 
                st.write('**Div. Bruta/ Patrim.:**', f"{float(info_papel2['Div_Br_Patrim'][0])}%") 

                st.write('**Dividend Yield:**', f"{info_papel2['Div_Yield'][0]}")

  

    # Título do app para gráfico
    st.title('Evolução histórica')

    # Opção para incluir IBOVESPA
    incluir_ibov = st.checkbox('Incluir IBOVESPA (IBOV)')

    # Use os mesmos ativos da selectbox para a construção do gráfico
    ativos = [papel1 + '.SA']
    if comparar:
        ativos.append(papel2 + '.SA')

    # Adicionar IBOVESPA à lista de comparação se a opção estiver ativada
    if incluir_ibov:
        ativos.append('^BVSP')

    # Entrada de datas
    col3, col4, col00, col01 = st.columns(4)
    with col3:
        inicio = st.date_input('Data de Início', value=pd.to_datetime('2010-01-01'), format="DD/MM/YYYY")
    with col4:
        fim = st.date_input('Data de Fim', value=pd.to_datetime('2025-02-01'), format="DD/MM/YYYY")

    # Baixar os dados e gerar o gráfico quando o botão for pressionado
    if st.button('Gerar gráfico'):
        try:
            # Baixar os dados históricos
            dados = yf.download(ativos, start=inicio, end=fim)['Close']
            
            # Verificar se os dados foram baixados corretamente
            if dados.empty:
                st.error(f'Nenhum dado foi encontrado para os ativos: {ativos} no intervalo de datas selecionado.')
            else:
                # Calcular a variação percentual acumulada
                dados_pct_acumulado = (dados / dados.iloc[0] - 1) * 100
                plt.figure(figsize=(10, 6))
                for ativo in ativos:
                    if ativo in dados.columns:
                        plt.plot(dados_pct_acumulado.index, dados_pct_acumulado[ativo], label=f'{ativo}')

                plt.title('Histórico de Variação Percentual Acumulada dos Preços de Ativos')
                plt.xlabel('Data')
                plt.ylabel('Variação Percentual Acumulada (%)')
                plt.legend()
                plt.grid(True)
                plt.tight_layout()

                st.pyplot(plt)

        except Exception as e:
            st.error(f'Ocorreu um erro: {e}')



#___________________________________________________________________________________________OK
def main():

    st.sidebar.image('logo_pa.png',width=150)

    st.sidebar.title('MarketView')
    #st.markdown('---')

    lista_menu = ['Home','Calendário Econômico', 'Panorama do Mercado','Retorno Mensal','Política Monetária','Fundamentos']
    
    escolha = st.sidebar.radio('', lista_menu)
    if escolha == 'Home':
        home()
    if escolha == 'Calendário Econômico':
        calendario()
    if escolha == 'Panorama do Mercado':
        panorama()
    if escolha == 'Retorno Mensal':
        retorno_mensal()
    if escolha == 'Política Monetária':
        juros()   
    if escolha == 'Fundamentos':
        fundamentos()        

main() 


#Preciso formatar os graficos para ter intereçao 
#Juros - talvez adicionar o imab e colocar em selectbox
#Retorno mensal - grafico interativo (candlestick) com caixa de seleçao periodo analisado (D,S,M,A) selectbox com media 20,50,100,200
#Panorama merece atenção - muito lento e preciso definir layout, 5 maiosres alta e baixa do dia
#Home - Adicionar grafico Tradingview

#Talvez adicionar uma pagina cripto com dados do tradingview


#Otimizar performace da aplicaçao inteira 