import pandas as pd
import plotly.graph_objects as go
import plotly.offline as pyo

# Create a pandas DataFrame from 2010YumaAZ.csv
df = pd.read_csv("https://raw.githubusercontent.com/Pierian-Data/Plotly-Dashboards-with-Dash/master/Data/2010YumaAZ.csv")
days = ['TUESDAY', 'WEDNESDAY', 'THURSDAY', 'FRIDAY', 'SATURDAY', 'SUNDAY', 'MONDAY']

# Use a for loop (or list comprehension to create traces for the data list)
data = []

for day in days:
    # What should go inside this Scatter call?
    data = df[df['DAY'] == day]
    xdata = data.loc
    trace = go.Scatter()
    data.append(trace)

# Define the layout
