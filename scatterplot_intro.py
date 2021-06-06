import plotly
import dash
import numpy as np
import plotly.offline as pyo
import plotly.graph_objs as go


# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    seed = 42
    np.random.seed(seed)

    randx = np.random.randint(1, 101, 100)
    randy = np.random.randint(1, 101, 100)

    data = [go.Scatter(x=randx,
                       y=randy * i,
                       mode='markers',
                       marker=dict(
                           size=12,
                           # color='rgb(51, 204, 153)',
                           symbol='pentagon',
                           line={'width': 2}
                       )) for i in (1, 2)]

    layout = go.Layout(title='Hello plotly',
                       xaxis={'title': 'my x axis'},
                       yaxis=dict(title='my y axis'),
                       hovermode='closest'
                     )

    fig = go.Figure(data=data, layout=layout)
    pyo.plot(data, filename='scatter1.html')


# See PyCharm help at https://www.jetbrains.com/help/pycharm/
