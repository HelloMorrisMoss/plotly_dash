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
import dash_bootstrap_components as dbc
from dash.dependencies import Input, Output
import plotly.graph_objs as go
import pandas as pd

# display options for printing out pandas columns wide without ellipses or continuations
pd.set_option('display.max_columns', None)
pd.set_option('max_columns', None)
pd.set_option('display.width', None)

# load the data
# df = pd.read_csv('https://github.com/Pierian-Data/Plotly-Dashboards-with-Dash/raw/master/Data/mpg.csv')
# df = pd.read_excel(r'C:\my documents\nh_plots\working_on_stats\2021-01-03 to 2021-05-23 percent of running speed length meeting target speed e097f566-e009-427d-8202-30ea065080ac.xlsx',
#                    sheet_name='2021-01-03 to 2021-05-23 pe (2)')

fp = r"C:\my documents\nh_plots\working_on_stats\2021-01-03 to 2021-06-12 percent of running speed length meeting target speed 9685949d-0e96-4274-a425-8a40c77ca3e5.csv"

# fp = r'C:\my documents\nh_plots\working_on_stats\2021-01-03 to 2021-05-23 percent of running speed length meeting target speed e097f566-e009-427d-8202-30ea065080ac.csv'
df = pd.read_csv(fp)

# df['total_len_tcs'] = df.groupby(['tabcode', 'coater_num', 'shift', 'week'])['total_length'].transform('sum')
# make sure the data has things the way we want
df = df[df['total_length'] > 0]  # no 0 length
df = df.sort_values(['week'])  # ordered hy length
df['display_length'] = df['total_length'].round(2)

features = df.columns

# app = dash.Dash()
css_sheet = dbc.themes.MATERIA
# app = dash.Dash(__name__, external_stylesheets=[css_sheet])  # this isn't working for me, needed a local copy
app = dash.Dash(__name__,
                meta_tags=[{'name': 'viewport', 'content': 'width=device-width, initial-scale=1.0, maximum-scale=1.2, minimum-scale=0.5' }])
shared_template = 'plotly_dark+presentation+xgridoff'
# shared_template = 'presentation+xgridoff'

# list of divs and components to add to the layout
layout_list = []

# add the components to the list
# ----------------------------------------

# the graph
# layout_list += [dcc.Graph(id='graph')]
layout_list += [dcc.Graph(id='graph')]


def just_ints(the_string):
    """Returns ony the digits from a string as an """
    # print(the_string)
    int_str_list = [character for character in the_string if character.isdigit()]
    # print(int_str_list)
    ret_val = int(''.join(int_str_list))
    return ret_val


targ_pct_list = tuple(hdr for hdr in df.columns if '_of_targ' in hdr)
targ_pct_checklist_list = [{'label': just_ints(targ), 'value': targ} for targ in targ_pct_list]
layout_list += [html.Div(id='pct_selector_label',
                         title='Select percentage met traces to display.',
                         children='Select percentage met traces to display.'), ]
layout_list += [dcc.Checklist(id='pct_selector_checklist',
                              options=targ_pct_checklist_list,
                              value=targ_pct_list
                              ), ]

# the label for and dropdown for tabcode
tc_options = []
for tc in df['tabcode'].unique():
    tc_options.append({'label': str(tc), 'value': tc})

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


# # app.layout = html.Div(layout_list)
# app.layout = dbc.Container([dbc.Row([dbc.Col([comp], width=True)]) for comp in layout_list])
app.layout = html.Div([dbc.Row([dbc.Col([comp], width=True)]) for comp in layout_list])
# app.layout = dbc.Container([dbc.Row([dbc.Col(layout_list, width=True)])])

hvr_template = '''%{hovertext} - %{customdata[total_len]m}'''.replace('total_len', str(df.columns.get_loc('display_length')))
# hvr_template = '''%{x},%{y}'''


@app.callback(Output('graph', 'figure'),
              [Input('tc_picker', 'value'),
               Input('mark_size_form', 'value'),
               Input('coater_selector_checklist', 'value'),
               Input('shift_selector_checklist', 'value'),
               Input('pct_selector_checklist', 'value')])
def update_figure(selected_tc, mark_size_multiplier, selected_coaters, selected_shifts, selected_pcts):
    selected_coaters = tuple(int(n) for n in selected_coaters)

    # filter the data based on inputs
    filtered_df = df[df['tabcode'] == int(selected_tc)]
    filtered_df = filtered_df[filtered_df['coater_num'].isin(selected_coaters)]
    filtered_df = filtered_df[filtered_df['shift'].isin(selected_shifts)]

    length_max = filtered_df['total_length'].max()
    length_min = filtered_df['total_length'].min()
    filtered_df['proportion'] = 1
    proportion = (1 - ((length_max - filtered_df['total_length']) / length_max)) * int(mark_size_multiplier)

    traces = []
    print(selected_tc)

    for grp_mi, grp_df in filtered_df.groupby(['coater_num', 'shift']):
        for pct_targ in selected_pcts:
            print(grp_mi)

            traces.append(go.Scatter(
                x=grp_df['week'],
                y=grp_df[pct_targ],
                mode='lines+markers',
                # mode='markers',
                opacity=0.7,
                # marker={'size': 15},
                marker_size=proportion,
                name='{tc}-{}-{}-{pct}'.format(*grp_mi, tc=selected_tc, pct=pct_targ),
                # hovertemplate=hvr_template,
                customdata=grp_df
                # ,
                # hover_data=['total_length']
            ))

        return {'data': traces, 'layout': go.Layout(title='Achieving Target by Week Plot',
                                                    xaxis={'title': 'Week of Year', 'type': 'linear'},
                                                    yaxis={'title': 'Overall met target speed pct', 'type': 'linear'}
                                                    # , template=shared_template

                                                    # these together along with the darkly bootstrap-theme gives a good
                                                    # dark theme graph
                                                    , template='plotly_dark'
                                                    , plot_bgcolor='rgba(0, 0, 0, 0)'
                                                    , paper_bgcolor='rgba(0, 0, 0, 0)'
                                                    )
                }


app.run_server()
