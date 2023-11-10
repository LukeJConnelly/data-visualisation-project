from dash import html, dcc

def get_sidebar():
    return html.Div(id='sidebar-contents', children=[
        html.H3('Stats & Filter'),
        html.Div(
            id='sidebar-graphs',
            children=[
                html.H6('Example Graph 1'),
                dcc.Graph(id='example-graph-1'),
                html.H6('Example Graph 2'),
                dcc.Graph(id='example-graph-2')
            ]
        ),
    ])