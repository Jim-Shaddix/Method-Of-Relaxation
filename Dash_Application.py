import dash
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output
import plotly.graph_objs as go
import Potential as po
"""
    Dash Application: 
    for graphing the potential of a system using the method of relazation
"""

# Get Data
x_axis = po.Axis(minimum=1, maximum=10, bc_min=1, bc_max=2, size=50, num_cells=True)
y_axis = po.Axis(minimum=-2, maximum=2, bc_min=3, bc_max=4, size=100, num_cells=True)
grid = po.Grid(x_axis, y_axis)
po.relax(grid.Z_cor, 1000)


# Make Plot
external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']
app = dash.Dash(__name__)

colors = {
    'background': '#111111',
    'text': 'black'
}

app.layout = html.Div(children=[

    # Banner
    html.H1("Method of Relaxation", id="banner"),

    # Header Notes
    html.Div([

        # left elements
        html.Div([
            html.H5("Description:", style={"textDecoration":"underline"}),
            html.P("This is a simple tool that uses the method of relaxation to solve "  +
                   "for the potential of a rectangular system, given a set of boundary " +
                   "conditions."),
        ], style={"float":"left", "boxSizing":"borderBox","width":"50%"}, className="header-cell"),

        # right elements
        html.Div([
            html.H5("This Tool Can:",style={"textDecoration": "underline"}),
            html.Ul([
               html.Li("Set axis range."),
               html.Li("Set boundary conditions (BCs)."),
               html.Li("Set the plots color-scheme.")
            ])
        ], style={"float": "right","marginRight": "15%"}, className="header-cell")

    ], id="header"),

    # clear floating elements
    html.Div(style={"clear":"both"}),

    # buttons
    html.Div([

        # minimum
        html.Div([

            # min-x
            html.Div([
                html.P("Minimum X"),
                dcc.Input(
                    id="min-x",
                    placeholder='1',
                    type='number',
                    value=''
                )
            ], className="x-button"),

            # min-y
            html.Div([
                html.P("Minimum Y"),
                dcc.Input(
                    id="min-y",
                    placeholder='0',
                    type='number',
                    value='',
                )
            ], className="y-button")

        ], className="xy-buttons"),

        # clear floating elements
        html.Div(style={"clear":"both"}),

        # minimum-bc
        html.Div([

            # min-x
            html.Div([
                html.P("Minimum X (BC)"),
                dcc.Input(
                    id="min-x-bc",
                    placeholder='1',
                    type='number',
                    value=''
                )
            ], className="x-button"),

            # min-y
            html.Div([
                html.P("Minimum Y (BC)"),
                dcc.Input(
                    id="min-y-bc",
                    placeholder='0',
                    type='number',
                    value=''
                )
            ], className="y-button")

        ], className="xy-buttons"),

        # clear floating elements
        html.Div(style={"clear":"both"}),

        # maximum
        html.Div([

            # max-x
            html.Div([
                html.P("maximum X"),
                dcc.Input(
                    id="max-x",
                    placeholder='1',
                    type='number',
                    value=''
                )
            ], className="x-button"),

            # max-y
            html.Div([
                html.P("Maximum Y"),
                dcc.Input(
                    id="max-y",
                    placeholder='0',
                    type='number',
                    value=''
                )
            ], className="y-button")

        ], className="xy-buttons"),

        # clear floating elements
        html.Div(style={"clear":"both"}),

        # maximum-bc
        html.Div([

            # max-x-bc
            html.Div([
                html.P("Maximum X (BC)"),
                dcc.Input(
                    id="max-x-bc",
                    placeholder='1',
                    type='number',
                    value=''
                )
            ], className="x-button"),

            # max-y-bc
            html.Div([
                html.P("Maximum Y (BC)"),
                dcc.Input(
                    id="max-y-bc",
                    placeholder='0',
                    type='number',
                    value=''
                )
            ], className="y-button")

        ], className="xy-buttons"),

        # clear floating elements
        html.Div(style={"clear":"both"}),

        # Drop Down
        html.Div([
            html.P("Set Color-Scheme"),
            dcc.Dropdown(
                options=[
                    {'label': 'RdBu',    'value': 'RdBu'},
                    {'label': 'Picnic',  'value': 'Picnic'},
                    {'label': 'Rainbow', 'value': 'Rainbow'},
                    {'label': 'Hot',     'value': 'Hot'},
                    {'label': 'Earth',   'value': 'Earth'}
                ],
                value='RdBu', # default label
                id='id',
                style={"float": "left", "width": "200px"}
            ),
            html.Button("Submit", id="submit", style={"float": "left"}),
        ], style={'marginTop': "30px"}),

    ], className="all-xy-buttons"),

    # Graph
    html.Div([
        dcc.Graph(
            id="SurfacePlot",
            figure={
                'data': [
                    go.Surface(
                        z=grid.Z_cor,
                        y=grid.Y_cor,
                        x=grid.X_cor,
                        colorscale='Rainbow'
                    )
                ],
                "layout": go.Layout(
                    title='Potential (Method: Relaxation)',
                    autosize=True,
                    width=700,
                    height=700
                )
            }
        )
    ], id="surface-plot")

])


if __name__ == '__main__':
    app.run_server(debug=True)
