import dash
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output, State
import plotly.graph_objs as go
import Potential as po
from collections import namedtuple
"""
    Dash Application: 
    for graphing the potential of a system using the method of relazation
"""

init_axis = namedtuple("init_axis", ["min", "max", "min_bc", "max_bc", "size"])
init_x = init_axis(1,  10, 1, 2, 50)
init_y = init_axis(-2, 2,  3, 4, 100)

# Make Plot
external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']
app = dash.Dash(__name__)

app.layout = html.Div(children=[

    # Banner
    html.H1("Method of Relaxation", id="banner"),

    # Header Notes
    html.Div([

        # left elements
        html.Div([
            html.H5("Description:", style={"textDecoration": "underline"}),
            html.P("This is a simple tool that uses the method of relaxation to solve " +
                   "for the potential of a rectangular system, given a set of boundary " +
                   "conditions."),
        ], style={"float": "left", "boxSizing": "borderBox","width": "50%"}, className="header-cell"),

        # right elements
        html.Div([
            html.H5("This Tool Can:", style={"textDecoration": "underline"}),
            html.Ul([
               html.Li("Set axis range."),
               html.Li("Set boundary conditions (BCs)."),
               html.Li("Set the plots color-scheme.")
            ])
        ], style={"float": "right", "marginRight": "5%"}, className="header-cell")

    ], id="header"),

    # clear floating elements
    html.Div(style={"clear": "both"}),

    # buttons
    html.Div([

        # minimum
        html.Div([

            # min-x
            html.Div([
                html.P("Minimum X"),
                dcc.Input(
                    id="min-x",
                    placeholder=init_x.min,
                    type='number',
                    value=init_x.min
                )
            ], className="x-button"),

            # min-y
            html.Div([
                html.P("Minimum Y"),
                dcc.Input(
                    id="min-y",
                    placeholder=init_y.min,
                    type='number',
                    value=init_y.min,
                )
            ], className="y-button")

        ], className="xy-buttons"),

        # clear floating elements
        html.Div(style={"clear": "both"}),

        # minimum-bc
        html.Div([

            # min-x
            html.Div([
                html.P("Minimum X (BC)"),
                dcc.Input(
                    id="min-x-bc",
                    placeholder=init_x.min_bc,
                    type='number',
                    value=init_x.min_bc
                )
            ], className="x-button"),

            # min-y
            html.Div([
                html.P("Minimum Y (BC)"),
                dcc.Input(
                    id="min-y-bc",
                    placeholder=init_y.min_bc,
                    type='number',
                    value=init_y.min_bc
                )
            ], className="y-button")

        ], className="xy-buttons"),

        # clear floating elements
        html.Div(style={"clear": "both"}),

        # maximum
        html.Div([

            # max-x
            html.Div([
                html.P("maximum X"),
                dcc.Input(
                    id="max-x",
                    placeholder=init_x.max,
                    type='number',
                    value=init_x.max
                )
            ], className="x-button"),

            # max-y
            html.Div([
                html.P("Maximum Y"),
                dcc.Input(
                    id="max-y",
                    placeholder=init_y.max,
                    type='number',
                    value=init_y.max
                )
            ], className="y-button")

        ], className="xy-buttons"),

        # clear floating elements
        html.Div(style={"clear": "both"}),

        # maximum-bc
        html.Div([

            # max-x-bc
            html.Div([
                html.P("Maximum X (BC)"),
                dcc.Input(
                    id="max-x-bc",
                    placeholder=init_x.max_bc,
                    type='number',
                    value=init_x.max_bc
                )
            ], className="x-button"),

            # max-y-bc
            html.Div([
                html.P("Maximum Y (BC)"),
                dcc.Input(
                    id="max-y-bc",
                    placeholder=init_y.max_bc,
                    type='number',
                    value=init_y.max_bc
                )
            ], className="y-button")

        ], className="xy-buttons"),

        # clear floating elements
        html.Div(style={"clear": "both"}),

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
                value='RdBu',  # default label
                id='style-dropdown',
                style={"float": "left", "width": "200px"}
            ),
            html.Button("Submit", id="submit-button", style={"float": "left"}),
        ], style={'marginTop': "30px"}),

    ], className="all-xy-buttons"),

    # Graph
    html.Div([
        dcc.Graph(id="SurfacePlot")
    ], id="surface-plot")

])


# Submit Button
@app.callback(
    Output('SurfacePlot', 'figure'),
    [Input("submit-button", 'n_clicks')],
    [State('style-dropdown', 'value'),
     State('min-x', 'value'),
     State('min-y', 'value'),
     State('min-x-bc', 'value'),
     State('min-y-bc', 'value'),
     State('max-x', 'value'),
     State('max-y', 'value'),
     State('max-x-bc', 'value'),
     State('max-y-bc', 'value')
    ]
)
def update_graph(n_clicks, style, min_x, min_y, min_x_bc, min_y_bc, max_x, max_y, max_x_bc, max_y_bc):

    # create new grid
    x_axis = po.Axis(minimum=min_x, maximum=max_x, bc_min=min_x_bc, bc_max=max_x_bc, size=50,  num_cells=True)
    y_axis = po.Axis(minimum=min_y, maximum=max_y, bc_min=min_y_bc, bc_max=max_y_bc, size=100, num_cells=True)
    grid = po.Grid(x_axis, y_axis)
    po.relax(grid.Z_cor, 1000)
    return {
        'data': [
            go.Surface(
                z=grid.Z_cor,
                y=grid.Y_cor,
                x=grid.X_cor,
                colorscale=style
            )
        ],
        "layout": go.Layout(
            title='Potential (Method: Relaxation)',
            autosize=True,
            width=700,
            height=700,
            paper_bgcolor='rgba(0,0,0,0)',
            plot_bgcolor='rgba(0,0,0,0)'
        )
    }


if __name__ == '__main__':
    app.run_server(debug=True)
