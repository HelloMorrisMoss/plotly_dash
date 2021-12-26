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

# show all the dataframe columns wider
pd.options.display.max_columns = None
pd.options.display.width = 0

# load the data
# df = pd.read_csv('https://github.com/Pierian-Data/Plotly-Dashboards-with-Dash/raw/master/Data/mpg.csv')
# df = pd.read_excel(r'C:\my documents\nh_plots\working_on_stats\2021-01-03 to 2021-05-23 percent of running speed length meeting target speed e097f566-e009-427d-8202-30ea065080ac.xlsx',
#                    sheet_name='2021-01-03 to 2021-05-23 pe (2)')

# fp = r"C:\my documents\nh_plots\working_on_stats\2021-01-03 to 2021-06-12 percent of running speed length meeting target speed 9685949d-0e96-4274-a425-8a40c77ca3e5.csv"

# fp = r'C:\my documents\nh_plots\working_on_stats\2021-01-03 to 2021-05-23 percent of running speed length meeting target speed e097f566-e009-427d-8202-30ea065080ac.csv'

# increased speed parts, january to mid june
# fp = r"C:\my documents\nh_plots\working_on_stats\2021-01-03 to 2021-06-12 percent of running speed length meeting target speed a1fb1449-115f-4315-9344-b30186160523.csv"
# fp = r"C:\my documents\nh_plots\test_refactoring\by_week\2021-06-23_15-47-05_plot_data.pickle"
# fp = r"C:\my documents\nh_plots\test_refactoring\by_week\2021-06-23_16-40-06_plot_data.pickle"
fp = r"C:\my documents\nh_plots\test_refactoring\by_week\2021-06-25_17-06-09_plot_data.pickle"
df = pd.read_pickle(fp)

# for now, no shift is being provided, so we'll pretend it's 1st
df['shift'] = [1]*len(df)
if 'week' not in df.columns:
    df['week'] = df['end'].apply(lambda x: x.isocalendar()[1])
# if 'tabcode' not in df.columns:
#     df['tabcode'] = df['tcode']
#     df['coater_num'] = df['cnum']
#     df = df.drop(0)

# df['total_len_tcs'] = df.groupby(['tabcode', 'coater_num', 'shift', 'week'])['total_length'].transform('sum')
# make sure the data has things the way we want
# df = df[df['total_length'] > 0]  # no 0 length
# df = df.sort_values(['week'])  # ordered by length
# df['display_length'] = df['total_length'].round(2)

features = df.columns

# app = dash.Dash()
# css_sheet = dbc.themes.MATERIA
# app = dash.Dash(__name__, external_stylesheets=[css_sheet])  # this isn't working for me, needed a local copy
app = dash.Dash(__name__,
                meta_tags=[{'name': 'viewport',
                            'content': 'width=device-width, initial-scale=1.0, maximum-scale=1.2, minimum-scale=0.5'}])
shared_template = 'plotly_dark+presentation+xgridoff'
# shared_template = 'presentation+xgridoff'

# list of divs and components to add to the layout
layout_list = []

# add the components to the list
# ----------------------------------------

# the graph
# layout_list += [dcc.Graph(id='graph')]
graph_list = [dcc.Graph(id='graph')]


# the met target speed % checklist
def just_ints(the_string):
    """Returns only the digits from a string as an integer."""
    # print(the_string)
    int_str_list = [character for character in the_string if character.isdigit()]
    # print(int_str_list)
    ret_val = int(''.join(int_str_list))
    return ret_val


# tabcode to start out on 
default_tc = df['tabcode'].astype(str).min()

# generate a checkbox list for weeks
weeks_list = tuple(wk for wk in df['week'].unique())
week_checklist_list = [{'label': wk_num, 'value': wk_num} for wk_num in weeks_list]
layout_list += [html.Div(id='week_select_label',
                         title='Select weeks to display.',
                         children='Select weeks to display.'), ]
layout_list += [dcc.Checklist(id='week_selector_checklist',
                              options=week_checklist_list,
                              value=weeks_list
                              ), ]

# the label for and dropdown for tabcode
tc_options = []
for tc in df['tabcode'].unique():
    tc_options.append({'label': str(tc), 'value': tc})


layout_list += [html.Div(id='tc_label', title='Select a Tabcode to display from the dropdown menu.',
                         children='Tabcode'),
                dcc.Dropdown(id='tc_picker',
                             options=tc_options,
                             value=default_tc,
                             )]

# the label for and the input box for bubble marker size
layout_list += [html.Div(id='bubble_size_form_label',
                         title='Input a size multiplier for the marker representing proportional length.',
                         children='Marker size multiplier, representing proportional length'),
                dcc.Input(id='mark_size_form',
                          value=50)]


# coater number selector
coater_num_list = (1, 2, 3, 4, 5)
coater_checklist_list = [{'label': f'{num}', 'value': num} for num in coater_num_list]
layout_list += [html.Div(id='coater_selector_label',
                         title='Select coater numbers to display.',
                         children='Select coater numbers to display.'),
                dcc.Checklist(id='coater_selector_checklist',
                              options=coater_checklist_list,
                              value=coater_num_list
                              )]

# shift number checklist
shift_num_list = (1, 2, 3)
shift_checklist_list = [{'label': f'{num}', 'value': num} for num in shift_num_list]
layout_list += [html.Div(id='shift_selector_label',
                         title='Select shift numbers to display.',
                         children='Select shift numbers to display.'),
                dcc.Checklist(id='shift_selector_checklist',
                              options=shift_checklist_list,
                              value=shift_num_list
                              )]

# add everything to the layout
app.layout = html.Div(graph_list + [dbc.Col([dbc.Row([dbc.Col([comp], width=True)]) for comp in layout_list], width=4)])

# totl_len_str = str(df.columns.get_loc('display_length'))
# hvr_template = '''%{hovertext} - %{customdata[total_len]m}'''.replace('total_len', totl_len_str)
# hvr_template = '''%{x},%{y}'''


# update the graph when selections change
@app.callback(Output('graph', 'figure'),
              [Input('tc_picker', 'value'),
               Input('mark_size_form', 'value'),
               Input('coater_selector_checklist', 'value'),
               Input('shift_selector_checklist', 'value'),
               Input('week_selector_checklist', 'value')])
def update_figure(selected_tc, mark_size_multiplier, selected_coaters, selected_shifts, selected_weeks):
    selected_coaters = tuple(int(n) for n in selected_coaters)

    # filter the data based on inputs
    filtered_df = df[df['tabcode'] == selected_tc]
    print(f'rows in filtered_df {filtered_df}')
    filtered_df = filtered_df[filtered_df['coater_num'].isin(selected_coaters)]
    filtered_df = filtered_df[filtered_df['shift'].isin(selected_shifts)]
    filtered_df = filtered_df[filtered_df['week'].isin(selected_weeks)]

    # length_max = filtered_df['total_length'].max()
    # length_min = filtered_df['total_length'].min()
    # filtered_df['proportion'] = 1
    # proportion = (1 - ((length_max - filtered_df['total_length']) / length_max)) * int(mark_size_multiplier)
    proportion = 1 * int(mark_size_multiplier)

    traces = []
    print(selected_tc)

    for grp_mi, grp_df in filtered_df.groupby(['coater_num', 'shift']):
        # for pct_targ in selected_weeks:
        print(grp_mi)

        this_week = grp_df['week'].iloc[0]
        traces.append(go.Scatter(
            x=tuple(x for x in grp_df['x_data'].iloc[0]),
            y=tuple(y for y in grp_df['y_data'].iloc[0]),
            mode='lines+markers',
            # mode='markers',
            opacity=0.7,
            # marker={'size': 15},
            marker_size=proportion,
            name='{tc}-{}-{}-{wk}'.format(*grp_mi, tc=selected_tc, wk=this_week),
            # hovertemplate=hvr_template,
            customdata=grp_df
            # ,
            # hover_data=['total_length']
        ))

    return {'data': traces, 'layout': go.Layout(title='Percentage of time on part at speeds.',
                                                xaxis={'title': 'Speed m/min', 'type': 'linear'},
                                                yaxis={'title': 'Percentage of time on part', 'type': 'linear'}
                                                # , template=shared_template

                                                # these together along with the darkly bootstrap-theme gives a good
                                                # dark theme graph
                                                # , template='plotly_dark'
                                                # , plot_bgcolor='rgba(0, 0, 0, 0)'
                                                # , paper_bgcolor='rgba(0, 0, 0, 0)'
                                                )
            }


app.run_server()
