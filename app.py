import dash
import dash_bootstrap_components as dbc
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output, State
import plotly.graph_objs as go
import numpy as np
from collections import namedtuple
import time

import Potential as po

# initialize application
app = dash.Dash(__name__, external_stylesheets=[dbc.themes.BOOTSTRAP])

# initial values
fields = ["min", "max", "min_bc", "max_bc", "size"]
init_axis = namedtuple("init_axis", fields)
init_x = init_axis(1, 10, 1, 2, 50)
init_y = init_axis(-2, 2, 3, 4, 100)

# create fields
input_fields = []
text_headers = ["Minimum", "Maximum", "Minimum (BC)", "Maximum (BC)"]
for i in range(len(text_headers)):

    # X input fields
    x_col = dbc.Col([

        html.P(text_headers[i] + " X", className="field-text"),

        dcc.Input(
            id=fields[i] + "_x",
            type='number',
            value=getattr(init_x, fields[i]),
            className="input-field"
        )

    ], width=6, className="x-field")

    # Y input fields
    y_col = dbc.Col([

        html.P(text_headers[i] + " Y", className="field-text"),

        dcc.Input(
            id=fields[i] + "_y",
            type='number',
            value=getattr(init_y, fields[i]),
            className="input-field"
        )

    ], width=6, className="y-field")

    row = dbc.Row([x_col, y_col], className="field-combo")
    input_fields.append(row)

# Append Drop Down / Submit Button
input_fields.extend([
    dbc.Row([
        dbc.Col(html.P("Set Color-Scheme"), width=6),
        dbc.Col(html.P(""), width=6)
    ]),
    dbc.Row([
            dbc.Col(
                dcc.Dropdown(
                    options=[
                                 {'label': 'RdBu', 'value': 'RdBu'},
                                 {'label': 'Picnic', 'value': 'Picnic'},
                                 {'label': 'Rainbow', 'value': 'Rainbow'},
                                 {'label': 'Hot', 'value': 'Hot'},
                                 {'label': 'Earth', 'value': 'Earth'}
                                    ],
                    value='Earth',
                    id='style-dropdown',
                    style={"width": "120px"}
                )
            ),
        dbc.Col(dbc.Button("Submit", id="submit-button", color="primary", className="mr-1"), width=6)
    ])
])


# used for converting slider values to #-iterations
def transform_slider_value(value):
    return 10 ** int(value)


app.layout = html.Div([

    # Banner
    html.H1("Method of Relaxation", id="banner"),

    # Header Notes
    html.Div([

        dbc.Button(
            "Description",
            id="button-description",
            className="mb-3",
            color="info",
            style={"marginRight": "10px"}
        ),

        dbc.Button(
            "Usage",
            id="button-usage",
            className="mb-3",
            color="info",
            style={"marginRight": "10px"}
        ),

        dbc.Button(
            "Author",
            id="button-author",
            className="mb-3",
            color="info",
        ),

        # collapse: description
        dbc.Collapse(
            dbc.Card(dbc.CardBody([
                html.H4("Description", className="card-title"),
                html.P("This dashboard uses the method of relaxation to solve " +
                        "for the potential of a rectangular system given a set of four constant boundary " +
                        "conditions. This tool is meant to be a visual aid for people who are interested " +
                        "in understanding how the method of relaxation works."),

            ]), color="info", inverse=True),
            id="collapse-description"
        ),

        # collapse: usage
        dbc.Collapse(
            dbc.Card(dbc.CardBody([
                html.H4("Usage", className="card-title"),
                html.H6("Input Fields"),
                html.Ul([
                    html.Li("Minimum / Maximum: Set the size of the rectangle for the x/y axis."),
                    html.Li("Minimum / Maximum (BC): Set the boundary conditions along the minimum / maximum axis values."),
                    html.Li("Submit Button: Uses all of the input parameters to start a new relaxation calculation.")
                ]),
                html.H6("Sum of Square Errors"),
                html.Ul([
                    html.Li("Each point on the graph represents the sum of the difference between the non-relaxed" +
                            " grid, and the relaxed grid, squared."),
                    html.Li("Equation: sum((initial-grid - relaxed-grid)^2)"),
                    html.Li("This graph serves as an indicator as to when you" +
                            " have used enough relaxation iterations to converge on a solution."+
                            " When the error flattens out, you have converged on a solution.")
                ])
            ]), color="info", inverse=True),
            id="collapse-usage",
        ),

        # collapse: Author
        dbc.Collapse(
            dbc.Card([
                html.Div(
                    dbc.CardImg(src="/assets/images/jim.png", top=True,
                                style={"maxWidth": "100%", "height": "auto"}),
                    style={"width": "150px", "height": "250px"}
                ),
                dbc.CardBody([
                    html.H4("Author: James Shaddix", className="card-title"),
                    html.P("I am an aspiring data scientist who just graduated from Colorado State University" +
                           " with B.S. degrees in Applied Physics and Computer Science.")
                    ]
                )
            ], color="info", inverse=True),

        id="collapse-author"),

    ], id="header-cell", className="left-element"),

    # Container
    html.Div([

        dbc.Row([

            # column-1 (LEFT)
            dbc.Col([

                # Fields for input values
                *input_fields,

                # Error Plot
                html.Div([
                    #dcc.Loading(id="loading-2", children=[html.Div(id="loading-output-2")], type="default"),
                    dcc.Graph(id="error-plot")
                ], className="error")

            ], width=4, id="left-elements"),

            # column-2 (RIGHT)
            dbc.Col([


                # Time
                dbc.Row([

                    # header text
                    dbc.Col(html.P("Time to Calculate (s)"), width=8),

                    # field displaying iteration value
                    dbc.Col(
                        dcc.Input(
                            id="time-field",
                            type='text',
                            value="0",
                            readOnly=True,
                            style={"textAlign": "right", "backgroundColor": "#C6CCC5"},
                            className="input-field"
                        ), width=4)
                ]),

                # iteration headers
                dbc.Row([

                    # header text
                    dbc.Col(html.P("Number of Relaxation Iterations"), width=8),

                    # field displaying iteration value
                    dbc.Col(
                        dcc.Input(
                            id="iteration-field",
                            type='number',
                            value="0",
                            readOnly=True,
                            style={"textAlign": "right","backgroundColor": "#C6CCC5"},
                            className="input-field"
                        ), width=4)
                ]),

                # iteration slider
                html.Div(
                    dcc.Slider(
                        min=1,
                        max=6,
                        value=3,
                        id="iteration-slider",
                        marks={
                            i: {"label": str(transform_slider_value(i)),
                                "style": {'writing-mode': 'vertical-lr'}}
                            for i in range(1, 7)
                        },
                    ), className="slider"
                ),

                html.Div([
                    dcc.Loading(id="loading-1", children=[html.Div(id="loading-output-1")], type="default"),
                    dcc.Graph(id="SurfacePlot")
                ], className="surface")


            ], width=8)
        ])
    ], className="container-fluid"),

])

# Submit Button
@app.callback(
    [Output('SurfacePlot', 'figure'),
     Output('error-plot', 'figure'),
     Output("time-field", "value"),
     Output("loading-output-1", "children")],
    [Input("submit-button", 'n_clicks')],
    [State('style-dropdown', 'value'),
     State('min_x', 'value'),
     State('min_y', 'value'),
     State('min_bc_x', 'value'),
     State('min_bc_y', 'value'),
     State('max_x', 'value'),
     State('max_y', 'value'),
     State('max_bc_x', 'value'),
     State('max_bc_y', 'value'),
     State('iteration-slider', 'value')
     ]
)
def update_graph(n_clicks, style, min_x, min_y, min_bc_x, min_bc_y, max_x, max_y, max_bc_x, max_bc_y, iterations):

    # create new grid
    start_time = time.time()
    x_axis = po.Axis(minimum=min_x, maximum=max_x, bc_min=min_bc_x, bc_max=max_bc_x, size=50,  num_cells=True)
    y_axis = po.Axis(minimum=min_y, maximum=max_y, bc_min=min_bc_y, bc_max=max_bc_y, size=100, num_cells=True)
    grid = po.Grid(x_axis, y_axis)
    iters = transform_slider_value(iterations)
    x_error_values, y_error_values = po.relax(grid.Z_cor, iters)
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
            #autosize=True,
            width=700,
            height=700,
            paper_bgcolor='rgba(0,0,0,0)',
            plot_bgcolor='rgba(0,0,0,0)',
        )
    }, {
       'data' : [
           go.Scatter(
               x=x_error_values,
               y=y_error_values,
           )
       ],

       "layout": go.Layout(
           title='Sum of Squared Errors',
           paper_bgcolor='rgba(0,0,0,0)',
           plot_bgcolor='rgba(0,0,0,0)',
           xaxis={"title": "Iterations"},
           yaxis={"title": "Error"}
       )
    }, "{:.2f}".format(time.time() - start_time), None


# iteration-slider updates iteration-field
@app.callback(
    Output('iteration-field', 'value'),
    [Input('iteration-slider', 'value')]
)
def update_output(value):
    return transform_slider_value(value)

# toggle description
@app.callback(
    Output("collapse-description", "is_open"),
    [Input("button-description", "n_clicks")],
    [State("collapse-description", "is_open")],
)
def toggle_collapse(n, is_open):
    if n:
        return not is_open
    return is_open

# toggle usage
@app.callback(
    Output("collapse-usage", "is_open"),
    [Input("button-usage", "n_clicks")],
    [State("collapse-usage", "is_open")],
)
def toggle_collapse(n, is_open):
    if n:
        return not is_open
    return is_open

# toggle author
@app.callback(
    Output("collapse-author", "is_open"),
    [Input("button-author", "n_clicks")],
    [State("collapse-author", "is_open")],
)
def toggle_collapse(n, is_open):
    if n:
        return not is_open
    return is_open


if __name__ == '__main__':
    app.run_server(debug=True)
