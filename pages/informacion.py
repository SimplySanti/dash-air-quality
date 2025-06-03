import dash
from dash import html, dcc, callback, Output, Input

dash.register_page(__name__)

layout = html.Div(
    [
        html.H1("This is an information page"),
        html.Div(
            [
                "Select something",
                dcc.RadioItems(
                    options=[
                        {"label": "Option 1", "value": "option1"},
                        {"label": "Option 2", "value": "option2"},
                        {"label": "Option 3", "value": "option3"},
                    ],
                    value="option1",
                    id="analytics-input",
                ),
            ]
        ),
        html.Br(),
        html.Div(id="analytics-output"),
    ]
)


@callback(Output("analytics-output", "children"), Input("analytics-input", "value"))
def update_city_selected(input_value):
    return f"You selected: {input_value}"
