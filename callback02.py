import dash
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output
import plotly.graph_objs as go
import pandas as pd

df = pd.read_csv('https://github.com/Pierian-Data/Plotly-Dashboards-with-Dash/raw/master/Data/gapminderDataFiveYear.csv')

app = dash.Dash()


year_options = []

for year in df['year'].unique():
    year_options.append({'label': str(year), 'value': year})

app.layout = html.Div([
    dcc.Graph(id='graph'),
    dcc.Dropdown(id='year-picker',
                 options=year_options,
                 value=df['year'].min())
])


@app.callback(Output('graph', 'figure'),
              [Input('year-picker', 'value')])
def update_figure(selected_year):
    filttered_df = df[df['year'] == selected_year]

    traces = []

    # add a scatter for each continent for the selected year
    for continent_name in filttered_df['continent'].unique():
        df_by_continent = filttered_df[filttered_df['continent'] == continent_name]
        traces.append(go.Scatter(
            x=df_by_continent['gdpPercap'],
            y=df_by_continent['lifeExp'],
            mode='markers',
            opacity=0.7,
            marker={'size': 15},
            name=continent_name
        ))

    return {'data': traces, 'layout': go.Layout(title='My Plot',
            xaxis={'title': 'GDP Per Cap', 'type': 'log'},
            yaxis={'title': 'Life Expectency'}
                                                )
            }

app.run_server()