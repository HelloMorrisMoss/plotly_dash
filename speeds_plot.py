
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


pd.set_option('display.max_columns', None)
pd.set_option('max_columns', None)
pd.set_option('display.width', None)

app = dash.Dash()

# df = pd.read_csv('https://github.com/Pierian-Data/Plotly-Dashboards-with-Dash/raw/master/Data/mpg.csv')
# df = pd.read_excel(r'C:\my documents\nh_plots\working_on_stats\2021-01-03 to 2021-05-23 percent of running speed length meeting target speed e097f566-e009-427d-8202-30ea065080ac.xlsx',
#                    sheet_name='2021-01-03 to 2021-05-23 pe (2)')
df = pd.read_csv(r'C:\my documents\nh_plots\working_on_stats\2021-01-03 to 2021-05-23 percent of running speed length meeting target speed e097f566-e009-427d-8202-30ea065080ac.csv')

# df['total_len_tcs'] = df.groupby(['tabcode', 'coater_num', 'shift', 'week'])['total_length'].transform('sum')

df = df[df['total_length'] > 0]

# tcode_bools = df['tabcode'] == '91688'
# cnum_bools = df['coater_num'] == 4
# df = df[cnum_bools]
# df = df[tcode_bools & cnum_bools]

features = df.columns


app = dash.Dash()


tc_options = []

for tc in df['tabcode'].unique():
    tc_options.append({'label': str(tc), 'value': tc})

app.layout = html.Div([
    dcc.Graph(id='graph'),
    dcc.Dropdown(id='tc_picker',
                 options=tc_options,
                 value=df['tabcode'].min())
])


@app.callback(Output('graph', 'figure'),
              [Input('tc_picker', 'value')])
def update_figure(selected_tc):
    filtered_df = df[df['tabcode'] == selected_tc]
    proportion = (filtered_df['total_length'] / filtered_df['total_length'].max()) * 100

    traces = []
    print(selected_tc)

    for grp_mi, grp_df in filtered_df.groupby(['coater_num', 'shift']):
        print(grp_mi)
        # grp_df['overall_met_pct']

        # df_by_shift = df_by_cnum[df_by_cnum['shift'] == shift]
        # df_this_shift = df_by_shift.groupby(['week'])['overall_met_pct'].mean().reset_index()
        traces.append(go.Scatter(
            x=grp_df['week'],
            y=grp_df['pct_met_target'],
            mode='lines+markers',
            # mode='markers',
            opacity=0.7,
            # marker={'size': 15},
            marker_size=proportion,
            # name=f'{selected_tc}-{cnum}-{shift}'
            name='{tc}-{}-{}'.format(*grp_mi, tc=selected_tc)
        ))


    # # add a scatter for each continent for the selected year
    # for cnum in filtered_df['coater_num'].unique():
    #
    #     # adding another loop for shift, make a trace for each coater/shift in lists, the lists should later be
    #     # from parameters for callback components
    #
    #     df_by_cnum = filtered_df[filtered_df['coater_num'] == cnum]
    #     # df.groupby(["SINID", "EXTRA"]).MONTREGL.sum().reset_index()
    #     # df_by_cnum = df_by_cnum.groupby(['week', 'shift'])['overall_met_pct'].mean().reset_index()
    #
    #     for shift in (1, 2, 3):
    #         df_by_shift = df_by_cnum[df_by_cnum['shift'] == shift]
    #         df_this_shift = df_by_shift.groupby(['week'])['overall_met_pct'].mean().reset_index()
    #         traces.append(go.Scatter(
    #             x=df_this_shift['week'],
    #             y=df_this_shift['overall_met_pct'],
    #             mode='lines+markers',
    #             opacity=0.7,
    #             marker={'size': 15},
    #             name=f'{selected_tc}-{cnum}-{shift}'
    #         ))

    return {'data': traces, 'layout': go.Layout(title='My Plot',
            xaxis={'title': 'Week of Year', 'type': 'log'},
            yaxis={'title': 'Overall met target speed pct'}
                                                )
            }


app.run_server()

# app.layout = html.Div([
#
#         html.Div([
#             dcc.Dropdown(
#                 id='xaxis',
#                 options=[{'label': i.title(), 'value': i} for i in features],
#                 value=features[0]
#             )
#         ],
#         style={'width': '48%', 'display': 'inline-block'}),
#
#         html.Div([
#             dcc.Dropdown(
#                 id='yaxis',
#                 options=[{'label': i.title(), 'value': i} for i in features],
#                 value=features[1]
#             )
#         ],style={'width': '48%', 'float': 'right', 'display': 'inline-block'}),
#
#     dcc.Graph(id='feature-graphic')
# ], style={'padding': 10})
#
#
# def group_df(grp_df: pd.DataFrame, grp_cols: list):
#     return grp_df.groupby(grp_cols)
#
#
# @app.callback(
#     Output('feature-graphic', 'figure'),
#     [Input('xaxis', 'value'),
#      Input('yaxis', 'value')])
# def update_graph(xaxis_name, yaxis_name):
#     return {
#         'data': [go.Scatter(
#             x=df[xaxis_name],
#             y=df[yaxis_name],
#             text=df['name'],
#             mode='markers',
#             marker={
#                 'size': 15,
#                 'opacity': 0.5,
#                 'line': {'width': 0.5, 'color': 'white'}
#             }
#         )],
#         'layout': go.Layout(
#             xaxis={'title': xaxis_name.title()},
#             yaxis={'title': yaxis_name.title()},
#             margin={'l': 40, 'b': 40, 't': 10, 'r': 0},
#             hovermode='closest'
#         )
#     }
#
# if __name__ == '__main__':
#     app.run_server()


# import pandas as pd
# import plotly.graph_objects as go
# import plotly.offline as pyo
#
# # Create a pandas DataFrame from 2010YumaAZ.csv
# # df = pd.read_csv("https://raw.githubusercontent.com/Pierian-Data/Plotly-Dashboards-with-Dash/master/Data/2010YumaAZ.csv")
# df = pd.read_excel(r'C:\my documents\nh_plots\working_on_stats\2021-01-03 to 2021-05-23 percent of running speed length meeting target speed e097f566-e009-427d-8202-30ea065080ac.xlsx',
#                    sheet_name='2021-01-03 to 2021-05-23 pe (2)')
# days = ['TUESDAY', 'WEDNESDAY', 'THURSDAY', 'FRIDAY', 'SATURDAY', 'SUNDAY', 'MONDAY']
# tcodes = df.tabcode.unique()
#
# data = [go.Scatter(x=randx,
#                    y=randy * i,
#                    mode='markers',
#                    marker=dict(
#                        size=12,
#                        # color='rgb(51, 204, 153)',
#                        symbol='pentagon',
#                        line={'width': 2}
#                    )) for i in (1, 2)]
#
#
#
# # Use a for loop (or list comprehension to create traces for the data list)
# # data = []
#
#
# # for tc in tcodes:
# #     # What should go inside this Scatter call?
# #     # data = df[df['DAY'] == day]
# #
# #
# #     xdata = data.loc
# #     trace = go.Scatter()
# #     data.append(trace)
#
# # Define the layout
