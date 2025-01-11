from dash import Dash, dcc, html, Input, Output
import plotly.express as px
import pandas as pd
import numpy as np

# Carregar os dados
df = pd.read_csv('ecommerce_estatistica (1).csv')

# Tratamento dos dados
df['Qtd_Vendidos'] = pd.to_numeric(df['Qtd_Vendidos_Cod'], errors='coerce')  # Converter para numérico caso necessário

# Lista de opções para dropdown e checklist
lista_temporada = df['Temporada'].unique()
options_temporada = [{'label': temporada, 'value': temporada} for temporada in lista_temporada]

# Função para criar gráficos
def cria_graficos(selecao_temporada):
    filtro_df = df[df['Temporada'].isin(selecao_temporada)]

    # Gráfico de barras: Quantidade de produtos vendidos por temporada
    fig1 = px.bar(filtro_df, x='Temporada', y='Qtd_Vendidos', color='Temporada',
                  title='Quantidade de Produtos Vendidos por Temporada',
                  labels={'Qtd_Vendidos': 'Quantidade Vendida', 'Temporada': 'Temporada'},
                  color_discrete_sequence=px.colors.qualitative.Set3)

    # Gráfico de dispersão: Preço vs Nota
    fig2 = px.scatter(filtro_df, x='Preço', y='Nota', color='Gênero',
                      title='Preço vs Nota',
                      labels={'Preço': 'Preço', 'Nota': 'Nota'},
                      color_discrete_sequence=px.colors.qualitative.Plotly)

    # Histograma: Distribuição de preços
    fig3 = px.histogram(filtro_df, x='Preço', nbins=20, color_discrete_sequence=['green'],
                        title='Distribuição de Preços',
                        labels={'Preço': 'Preço'})

    # Mapa de calor: Correlação entre variáveis
    corr = filtro_df[['Preço', 'Desconto']].corr()
    fig4 = px.imshow(corr, text_auto=True, color_continuous_scale='RdBu',
                     title='Mapa de Calor - Correlação Preço e Desconto')

    # Gráfico de pizza: Proporção por temporada
    temporada_count = filtro_df['Temporada'].value_counts()
    fig5 = px.pie(values=temporada_count.values, names=temporada_count.index, title='Proporção por Temporada')

    return fig1, fig2, fig3, fig4, fig5

# Criar App
app = Dash(__name__)

app.layout = html.Div([
    html.H1('Dashboard Interativo - E-commerce'),

    html.Div('''Selecione as temporadas para filtrar os dados e visualizar os gráficos.'''),
    dcc.Checklist(
        id='id_selecao_temporada',
        options=options_temporada,
        value=[lista_temporada[0]],  # Valor inicial
        inline=True
    ),

    dcc.Graph(id='grafico_barras'),
    dcc.Graph(id='grafico_dispersao'),
    dcc.Graph(id='grafico_histograma'),
    dcc.Graph(id='grafico_calor'),
    dcc.Graph(id='grafico_pizza')
])

@app.callback(
    [
        Output('grafico_barras', 'figure'),
        Output('grafico_dispersao', 'figure'),
        Output('grafico_histograma', 'figure'),
        Output('grafico_calor', 'figure'),
        Output('grafico_pizza', 'figure'),
    ],
    [Input('id_selecao_temporada', 'value')]
)
def atualiza_graficos(selecao_temporada):
    return cria_graficos(selecao_temporada)

if __name__ == '__main__':
    app.run_server(debug=True, port=8050)
