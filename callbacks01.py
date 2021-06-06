import dash
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output


app = dash.Dash()

app.layout = html.Div([
    dcc.Input(id='my-id', value='Initial Text', type='text'),  # this Input is not from dependencies
    html.Div(id='my-div', style={'border': '2px blue solid'})
])


# these Output and Input are from dependencies import
@app.callback(Output('my-div', component_property='children'),
              [Input(component_id='my-id',  # this is the component declared in the layout
                     component_property='value')])  # this is the value of the component, starting as
                                                    # 'Initital Text' but updating as it changes
def updates_output_div(input_value):
    return f'You entered {input_value}'

if __name__ == '__main__':
    app.run_server()