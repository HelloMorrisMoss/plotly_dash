"""Waiting to update based on a 'state'."""
import dash
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output, State


app = dash.Dash()

app.layout = html.Div([
    dcc.Input(id='number-in', value=1, style={'fontSize': 24}),
    html.H1(id='number-out'),
    html.Button(id='submit-button',
                n_clicks=0,
                children='Submit here',
                style={'fontSize': 24})
])


@app.callback(Output('number-out', 'children'),
              [Input('submit-button', 'n_clicks')],
              [State('number-in', 'value')])
def output(n_clicks, number):
    return f'{number} was typed in and button was clicked {n_clicks} times.'


app.run_server()