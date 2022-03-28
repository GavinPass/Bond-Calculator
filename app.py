import numpy
import pandas
import dash
import dash_bootstrap_components as dbc
from dash import dcc
from dash import html
from calculator import *
from dash.dependencies import Input,Output,State
from dash.exceptions import PreventUpdate

app=dash.Dash()
app.title='Bond Calculator'

app.layout=dbc.Container(
    dbc.Row(
        children=[
            dbc.Col(
                children=[
                    html.H3("Bond Risk Metrics Calculator",style={'text-align':'left'}),
                    dbc.FormFloating(
                        children=[
                            dbc.Label('Number of Payments Per Year'),
                            html.Br(),
                            dbc.Input(id='period',placeholder='eg:2',type='number'),
                        ],
                    ),
                    dbc.FormFloating(
                        children=[
                            dbc.Label('Number of Years to Maturity'),
                            html.Br(),
                            dbc.Input(id='maturity',type='number'),
                        ],
                    ),
                    dbc.FormFloating(
                        children=[
                            dbc.Label('Yield to Maturity (YTM)'),
                            html.Br(),
                            dbc.Input(id='ytm',placeholder='eg:2.5',type='number'),
                        ],
                    ),
                    dbc.FormFloating(
                        children=[
                            dbc.Label('Face Value'),
                            html.Br(),
                            dbc.Input(id='fv',placeholder='eg:1000',type='number'),
                        ],
                    ),
                    dbc.FormFloating(
                        children=[
                            dbc.Label('Coupon Rate'),
                            html.Br(),
                            dbc.Input(id='coupon',placeholder='eg:5',type='number'),
                        ],
                    ),
                    html.Br(),
                    dbc.Button('Calculate Bond Duration',id='cal_button'),
                    html.Br(),
                    html.Br(),
                    html.H4('Market Price: '),
                    html.H4(id='fair_price'),
                    html.H4('Macaulay Duration: '),
                    html.H4(id='mac_dur'),
                    html.H4('Modified Duration: '),
                    html.H4(id='mod_dur'),
                    html.H4('Convexity: '),
                    html.H4(id='con'),
                ],
                width=4,
            ),
            dbc.Col(
                children=[
                    html.H3('Yield to Maturity Calculator',style={'text-align':'left'}),
                    dbc.FormFloating(
                        children=[
                            dbc.Label('Market Value'),
                            html.Br(),
                            dbc.Input(id='pv',placeholder='eg:105.00',type='number'),
                        ],
                    ),
                    dbc.FormFloating(
                        children=[
                            dbc.Label('Initial asssume value of YTM'),
                            html.Br(),
                            dbc.Input(id='y-init',placeholder='eg:0.035',type='number'),
                            dbc.FormText('Default Interation time : 10000 \n Default Precision Bound: 1 bp')
                        ],
                    ),

                    html.Br(),
                    dbc.Button('Calculate Bond YTM',id='YTM_button'),
                    html.Br(),
                    html.Br(),
                    html.H4('Yield to Maturity: '),
                    html.H4(id='YTM'),
                ],
                width=4,
            ),
        ],
    )
)

@app.callback(
    [
        Output(component_id='fair_price',component_property='children'),
        Output(component_id='mac_dur',component_property='children'),
        Output(component_id='mod_dur',component_property='children'),
        Output(component_id='con',component_property='children'),
    ],
    [
        Input(component_id='cal_button',component_property='n_clicks')
    ],
    [
        State(component_id='period',component_property='value'),
        State(component_id='maturity',component_property='value'),
        State(component_id='ytm',component_property='value'),
        State(component_id='fv',component_property='value'),
        State(component_id='coupon',component_property='value'),
    ]
)
def duration_cal(n1,N,M,y,fv,c):

    if n1 is None:
        raise PreventUpdate

    PV="{:.2f}".format(np.sum(PV_CF(N,y,fv,c,M)))
    Mac_dur="{:.3f}".format(np.sum(MacDuration(N,y,fv,c,M)))
    Mod_dur="{:.3f}".format(np.sum(MacDuration(N,y,fv,c,M))/(1+y/100/N))

    return PV,Mac_dur,Mod_dur,convexity(N,y,fv,c,M)

@app.callback(
    Output(component_id='YTM',component_property='children'),
    [
        Input(component_id='YTM_button',component_property='n_clicks')
    ],
    [
        State(component_id='period',component_property='value'),
        State(component_id='maturity',component_property='value'),
        State(component_id='pv',component_property='value'),
        State(component_id='fv',component_property='value'),
        State(component_id='coupon',component_property='value'),
        State(component_id='y-init',component_property='value'),
    ]
)
def duration_cal(n1,N,M,pv,fv,c,y_init):

    if n1 is None:
        raise PreventUpdate

    rate=Newton_ytm(N,fv,c,M,pv,y_init,10000,0.0001)
    return rate

if __name__=="__main__":
    app.run_server(debug=True)
