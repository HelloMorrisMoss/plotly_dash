"""Multiple component imputs


                                        PLANNING

                    will want a drop down for:
                        tabcode

                        loop for:
                            coater
                            shift



"""
#######
# Here we'll use the mpg.csv dataset to demonstrate
# how multiple inputs can affect the same graph.
######
import dash
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output
import plotly.graph_objs as go
import pandas as pd

# display options for printing out pandas columns wide without ellipses or continuations
pd.set_option('display.max_columns', None)
pd.set_option('max_columns', None)
pd.set_option('display.width', None)

# dash instance
app = dash.Dash()

# load the data
# df = pd.read_csv('https://github.com/Pierian-Data/Plotly-Dashboards-with-Dash/raw/master/Data/mpg.csv')
# df = pd.read_excel(r'C:\my documents\nh_plots\working_on_stats\2021-01-03 to 2021-05-23 percent of running speed length meeting target speed e097f566-e009-427d-8202-30ea065080ac.xlsx',
#                    sheet_name='2021-01-03 to 2021-05-23 pe (2)')
df = pd.read_csv(
    r'C:\my documents\nh_plots\working_on_stats\2021-01-03 to 2021-05-23 percent of running speed length meeting target speed e097f566-e009-427d-8202-30ea065080ac.csv')

# df['total_len_tcs'] = df.groupby(['tabcode', 'coater_num', 'shift', 'week'])['total_length'].transform('sum')
# make sure the data has things the way we want
df = df[df['total_length'] > 0]  # no 0 length
df = df.sort_values(['week'])  # ordered hy length

features = df.columns

app = dash.Dash()

tc_options = []

for tc in df['tabcode'].unique():
    tc_options.append({'label': str(tc), 'value': tc})

# list of divs and components to add to the layout
layout_list = []

# add the components to the list

# the graph
layout_list += [dcc.Graph(id='graph')]

# the label for and dropdown for tabcode
layout_list += [html.Div(id='tc_label', title='Select a Tabcode to display from the dropdown menu.',
                         children='Tabcode'),
                dcc.Dropdown(id='tc_picker',
                             options=tc_options,
                             value=df['tabcode'].min(),
                             )]

# the label for and the input box for bubble marker size
layout_list += [html.Div(id='bubble_size_form_label',
                         title='Input a size multiplier for the marker representing proportional length.',
                         children='Marker size multiplier, representing proportional length'),
                dcc.Input(id='mark_size_form',
                          value=50)]


coater_num_list = (1, 2, 3, 4, 5)
coater_checklist_list = [{'label': f'{num}', 'value': num} for num in coater_num_list]
layout_list += [html.Div(id='coater_selector_label',
                         title='Select coater numbers to display.',
                         children='Select coater numbers to display.'),
                dcc.Checklist(id='coater_selector_checklist',
                              options=coater_checklist_list,
                              value=coater_num_list
                              )]

shift_num_list = (1, 2, 3)
shift_checklist_list = [{'label': f'{num}', 'value': num} for num in shift_num_list]
layout_list += [html.Div(id='shift_selector_label',
                         title='Select shift numbers to display.',
                         children='Select shift numbers to display.'),
                dcc.Checklist(id='shift_selector_checklist',
                              options=shift_checklist_list,
                              value=shift_num_list
                              )]

app.layout = html.Div(layout_list)

hvr_template = '''%{customdata[total_len]}'''.replace('total_len', str(df.columns.get_loc('total_length')))
# hvr_template = '''%{x},%{y}'''


@app.callback(Output('graph', 'figure'),
              [Input('tc_picker', 'value'),
               Input('mark_size_form', 'value'),
               Input('coater_selector_checklist', 'value'),
               Input('shift_selector_checklist', 'value')])
def update_figure(selected_tc, mark_size_multiplier, selected_coaters, selected_shifts):
    selected_coaters = tuple(int(n) for n in selected_coaters)

    # filter the data based on inputs
    filtered_df = df[df['tabcode'] == int(selected_tc)]
    filtered_df = filtered_df[filtered_df['coater_num'].isin(selected_coaters)]
    filtered_df = filtered_df[filtered_df['shift'].isin(selected_shifts)]

    # length_max = filtered_df['total_length'].max()
    length_min = filtered_df['total_length'].min()
    proportion = (filtered_df['total_length'] - length_min) * int(mark_size_multiplier) / 1000

    traces = []
    print(selected_tc)

    for grp_mi, grp_df in filtered_df.groupby(['coater_num', 'shift']):
        print(grp_mi)

        traces.append(go.Scatter(
            x=grp_df['week'],
            y=grp_df['pct_met_target'],
            mode='lines+markers',
            # mode='markers',
            opacity=0.7,
            # marker={'size': 15},
            marker_size=proportion,
            name='{tc}-{}-{}'.format(*grp_mi, tc=selected_tc),
            hovertemplate=hvr_template,
            customdata=grp_df
            # ,
            # hover_data=['total_length']
        ))


    return {'data': traces, 'layout': go.Layout(title='My Plot',
                                                xaxis={'title': 'Week of Year', 'type': 'linear'},
                                                yaxis={'title': 'Overall met target speed pct', 'type': 'linear'},
                                                template='plotly_dark'
                                                )
            }


app.run_server()
