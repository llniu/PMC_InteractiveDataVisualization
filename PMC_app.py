import dash
import dash_core_components as dcc
import dash_html_components as html
import plotly.graph_objs as go
import plotly.express as px
import pandas as pd
from dash.dependencies import Input, Output

style_userinput = {'font-size': '120%', 'color': 'darkred'}
template = 'simple_white'
plot_bgcolor = 'whitesmoke'

data = pd.read_csv('data/Dataset_NAFLD_plasma_Cirrhosis.csv')
data['ProteinID_GeneName'] = data['Leading Protein ID'] + \
    "_" + data['Leading Gene name']
options_list = data['ProteinID_GeneName'].dropna().unique().tolist()
options_dict = [{'label': i, 'value': i} for i in options_list]

external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']

app = dash.Dash(__name__, external_stylesheets=external_stylesheets)

app.layout = html.Div(children=[
    html.H1(children='Volcano plot'),
    html.P('Select a protein here:', style=style_userinput),
    dcc.Dropdown(id='User_input',
                 value='P01833_PIGR',
                 options=options_dict,
                 style={'width': '50%'}),
    dcc.Graph(
        id='example-graph',
    )
])

@app.callback(
    Output('example-graph', 'figure'),
    [Input('User_input', 'value')]
)
def update_figure(input_value):
    df = data.copy()
    fig_scatter = px.scatter(
        data_frame=data,
        x='Log2 difference',
        y='P-value [-Log10]',
        color='Sequence coverage [%]',
        hover_name='ProteinID_GeneName',
        width=600,
        height=400,
        template=template)
    data_highlight = data[data['ProteinID_GeneName'] == input_value]
    fig_scatter.add_trace(
        go.Scatter(
            x=data_highlight['Log2 difference'],
            y=data_highlight['P-value [-Log10]'],
            marker_size=20,
            text=input_value,
            mode='markers+text',
            textposition="top center",
            textfont={'size': 12, 'color': 'darkred'},
            marker_color='darkred')
    )
    fig_scatter.update_layout(plot_bgcolor=plot_bgcolor,
                              title='Plasma proteome cirrhosis vs. non-NAFLD',
                              showlegend=False)

    return fig_scatter


if __name__ == '__main__':
    app.run_server(debug=True)
