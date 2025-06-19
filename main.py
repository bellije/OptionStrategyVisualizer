import dash
from dash import html, dcc, Input, Output, State, dash_table
from dash.dash_table.Format import Format, Scheme
import dash_bootstrap_components as dbc
import plotly.graph_objs as go
import numpy as np

from Models.Portfolio import Portfolio

# App initialization
app = dash.Dash(__name__, external_stylesheets=[dbc.themes.BOOTSTRAP])
app.title = "Option strategy visualizer"

# In portfolio otions data storage
portfolio = Portfolio()
greeks_data=[{"delta": 0, "gamma": 0, "theta": 0, "vega": 0, "rho": 0}]


# Layout
app.layout = dbc.Container([
    html.H2("Option strategy visualizer", className="my-4"),

    dbc.Row([
        dbc.Col([
            html.H5("Common parameters"),
            dbc.Row(children=[dbc.Label('Underlying spot price'), dbc.Input(id="spot", placeholder="Underlying spot price", type="number", value=100, className="mb-2", disabled=False)]),
            dbc.Row(children=[dbc.Label('Annual volatilty'), dbc.Input(id="volatility", placeholder="Annual volatilty", type="number", value=0.2, className="mb-2", disabled=False)]),
            dbc.Row(children=[dbc.Label('Time to maturity (Days)'), dbc.Input(id="timetomaturity", placeholder="Time to maturity (Days)", type="number", value=60, className="mb-2", disabled=False)]),
            dbc.Row(children=[dbc.Label('Annual Risk free rate'), dbc.Input(id="riskfree", placeholder="Annual Risk free rate", type="number", value=0.02, className="mb-2", disabled=False)]),
            html.H5("Add an option"),
            dbc.Row(children=[
                dbc.Label('Option type'),
                dbc.Select(
                    id="type", options=[{"label": "Call", "value": "Call"}, {"label": "Put", "value": "Put"}],
                    value="Call", className="mb-2"
                )
            ]),
            dbc.Row(children=[
                dbc.Label('Direction'),
                dbc.Select(
                    id="direction", options=[{"label": "Long", "value": "Long"}, {"label": "Short", "value": "Short"}],
                    value="Long", className="mb-2"
                )
            ]),
            dbc.Row(children=[dbc.Label('Strike'), dbc.Input(id="strike", placeholder="Strike", type="number", value=100, className="mb-2")]),
            dbc.Row(children=[dbc.Label('Quantity'), dbc.Input(id="quantity", placeholder="Quantity", type="number", value=1, className="mb-2")]),
            dbc.Button("Add", id="add_button", color="primary", className="mb-3"),
            dbc.Button("Reset", id="reset_button", color="primary", className="mb-3"),
            html.Hr(),
            html.Div(id="option_list")
        ], width=3),

        dbc.Col([
            dcc.Graph(id="payoff_graph", config={"displayModeBar": False}),
            dash_table.DataTable(
                id='greeks_table',
                data=greeks_data,
                columns=[{"name": col, "id": col, 'type': 'numeric', 'format': Format(precision=3, scheme=Scheme.fixed)} for col in greeks_data[0].keys()],
                style_cell={'textAlign': 'center'},
                style_header={'fontWeight': 'bold'}
            ),
            dbc.Row(children=[dbc.Label('Time'), dcc.Slider(0, 60, 1, value=60, id='time_slider')])
        ], width=9)
    ])
], fluid=True)

# Callback to add an option
@app.callback(
    Output("option_list", "children"),
    Output("payoff_graph", "figure"),
    Output("greeks_table", "data"),
    Output('spot', 'disabled'),
    Output('volatility', 'disabled'),
    Output('timetomaturity', 'disabled'),
    Output('riskfree', 'disabled'),
    Input("add_button", "n_clicks"),
    State("type", "value"),
    State("direction", "value"),
    State("strike", "value"),
    State("spot", "value"),
    State("volatility", "value"),
    State("timetomaturity", "value"),
    State("riskfree", "value"),
    State("quantity", "value"),
    prevent_initial_call=True
)
def update_options(n_clicks, option_type, direction, strike, spot, volatility, time_to_maturity, risk_free_rate, quantity):
    global portfolio
    
    # Adding the new position to the portfolio
    portfolio.add_position(quantity, direction, option_type, strike, spot, volatility, time_to_maturity/365, risk_free_rate)

    # Plotting the payoff of the portfolio
    figure = go.Figure(data=portfolio.compute_pnl())
    figure.update_layout(title="Maturity PnL", xaxis_title="Underlying price", yaxis_title="PnL",
                         template="plotly_white", showlegend=True)
    
    # Portfolio description
    description = portfolio.get_portfolio_positions()

    # Portfolio greeks
    greeks_data = portfolio.get_greeks_data()

    return html.Ul([html.Li(opt) for opt in description]), figure, greeks_data, True, True, True, True


@app.callback(
    Output("option_list", "children", allow_duplicate=True),
    Output("payoff_graph", "figure", allow_duplicate=True),
    Output("greeks_table", "data", allow_duplicate=True),
    Output('spot', 'disabled', allow_duplicate=True),
    Output('volatility', 'disabled', allow_duplicate=True),
    Output('timetomaturity', 'disabled', allow_duplicate=True),
    Output('riskfree', 'disabled', allow_duplicate=True),
    Input("reset_button", "n_clicks"),
    prevent_initial_call=True
)
def reset_option_list(n_clicks):
    global portfolio
    portfolio.reset_portfolio()
    
    # Plotting the payoff of the portfolio
    figure = go.Figure(data=[])
    figure.update_layout(title="Maturity PnL", xaxis_title="Underlying price", yaxis_title="PnL",
                         template="plotly_white", showlegend=True)
    
    # Portfolio description
    description = portfolio.get_portfolio_positions()

    # Greeks resetting
    greeks_data=[{"delta": 0, "gamma": 0, "theta": 0, "vega": 0, "rho": 0}]

    return html.Ul([html.Li(opt) for opt in description]), figure, greeks_data, False, False, False, False

@app.callback(
    Output('time_slider', 'max'),
    Input('timetomaturity', 'value')
)
def update_slider_max(max_value):
    try:
        val = float(max_value)
        return val if val > 0 else 60
    except:
        return 100


if __name__ == "__main__":
    app.run(debug=True)
