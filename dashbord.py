#!/usr/bin/python
# -*- coding: utf-8 -*-

import dash
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Output, Input
import dash_bootstrap_components as dbc
import pandas as pd
import plotly.express as px
from datetime import date
import plotly.graph_objs as go
from flask import Flask


server = Flask(__name__)
app = dash.Dash(__name__, server=server)
df_Azure = pd.read_csv('data/Azure-cost-management-today.csv')




def make_lists(df, tag, title):
    radio_list = [html.H4(f'{title}', style={'textAlign':'center'})]
    dic = []
    
    for s ,c in df[f'{tag}'].value_counts().iteritems():
        dic.append({'label': f'{s} : {c}', 'value' : f'{s}'})
    #print(dic)
    radio_list.append(   
        #html.Label(f'{s}', style={'display':'inline', 'fontSize':15}),
        dcc.Dropdown(
            id=f"my-lists-{tag}",
            options=dic,
            value=[],
            multi=True, 
            style={'width': '600px', 'height' : '100%'}
        )    
    )
    return html.Div(radio_list, style={'textAlign':'left'})




def page_html(df, app):
    
    

    today = date.today()

    app.layout = html.Div([
   
    
        dbc.Row([
            dbc.Col(html.H1(f'Cost Managemnet {today}', style={'textAlign':'center'}), width=12)
        ]),
    
        dbc.Row([
            dbc.Col(html.Div(
                                className='ikdrow',
                                style = {'display' : 'flex'},
                                children=[make_lists(df, 'tags', 'Tags'),
                                        make_lists(df, 'resource_group', 'Resource Group'),
                                        dcc.DatePickerRange(
                                                        id='my-date-picker-range',
                                                        min_date_allowed=date(2018, 12, 31),
                                                        max_date_allowed=today,
                                                        initial_visible_month=today,
                                                        end_date=today, 
                                                        start_date = df["date"].min(),
                                                        style={'width': '100%', 'height' : '30%'}
                                                        ),
                                        html.Div(id='output-container-date-picker-range',
                                                 children=[html.P(f'Cost : {df["cost"].sum()} euro')]
                                                 )
                                    ]
                  ), style = {'textAlign': 'center', 'border':'10px'}
             )
        ]),
        dbc.Row([
            dbc.Col(dcc.Graph(id='my-camonbrt', config={'displayModeBar':True} )),
        
            #dbc.Col(dcc.Graph(id='my-bar', figure=fig_AWS, config={'displayModeBar': False}))
            ]), #, style={'width': '100%', 'height' : '100%'} 
        dbc.Row([
            dbc.Col(dcc.Graph(id='my-choropleth', config={'displayModeBar':False}))
        
        ], style={'width': '100%', 'height' : '100%'}) ,  
    ])

def gets_rg(df, lentgh, value):

    prerf = '(df["resource_group"] == value[0])'
    for i in range(1, lentgh):
        prerf += f' & (df["resource_group"] == value[{i}])'
        print(value[i])
    print(prerf)
    mask = eval(prerf)
    print(type(mask))
    return df.loc[mask]



@app.callback(
    dash.dependencies.Output('my-camonbrt', 'figure'),
    [dash.dependencies.Input('my-date-picker-range', 'start_date'),
     dash.dependencies.Input('my-date-picker-range', 'end_date'),
     dash.dependencies.Input('my-lists-resource_group', 'value')])
def update_fig(start_date, end_date, value):
    
    bar_Azure = px.bar(df_Azure, x="date", y="cost", color="resource_group")
    print(value)
    df_tmp = df_Azure
    if len(value) > 0:
        df_tmp = gets_rg(df_Azure, len(value), value)
    print(len(df_tmp))
    if start_date is not None and end_date is not None :
        
        mask = (df_tmp['date'] >= start_date) & (df_tmp['date'] <= end_date) 
        df_now = df_tmp.loc[mask]
        #print(df_now.head())
        bar_Azure = px.bar(df_now, x="date", y="cost", color="resource_group")


        return bar_Azure 
    else :
        return bar_Azure


@app.callback(
    dash.dependencies.Output('my-choropleth', 'figure'),
    [dash.dependencies.Input('my-date-picker-range', 'start_date'),
     dash.dependencies.Input('my-date-picker-range', 'end_date')])
def update_fig(start_date, end_date):
    
    pie_Azure = px.pie(df_Azure, values='cost', names='resource_group')
    if start_date is not None and end_date is not None :

        mask = (df_Azure['date'] >= start_date) & (df_Azure['date'] <= end_date)
        df_now = df_Azure.loc[mask]

        pie_Azure = px.pie(df_now, values='cost', names='resource_group', title='cost by resource group',  hover_data=['resource_group'])
        #pie_Azure = px.pie(df_now, values='cost', names='resource_group')

        return pie_Azure 
    else :
        return pie_Azure


@app.callback(
    dash.dependencies.Output('output-container-date-picker-range', 'children'),
    [dash.dependencies.Input('my-date-picker-range', 'start_date'),
     dash.dependencies.Input('my-date-picker-range', 'end_date')])
def update_output(start_date, end_date):
    
    string_prefix = 'You have selected: '
    if start_date is not None and end_date is not None :

        mask = (df_Azure['date'] >= start_date) & (df_Azure['date'] <= end_date)
        df_now = df_Azure.loc[mask]
        sum_cost = df_now['cost'].sum()
        string_prefix = f'Cost : {sum_cost} euro'

        return string_prefix 
    else :
        return f'Cost : {df_Azure["cost"].sum()} euro'

def main():
    page_html(df_Azure, app)

if __name__ == '__main__':
    main()
    app.run_server()
    













"""
df_AWS = pd.read_csv('data/AWS-cost-management.csv')

fig_AWS = px.histogram(df_AWS, x="lineItem/UsageStartDate", y="lineItem/UnblendedCost", title="AWS : lineItem/UsageStartDate by lineItem/UnblendedCost")
fig_Azure.update_layout(
    title={
        'text': "Azure : Date by Cost",
        'y':0.9,
        'x':0.5,
        'xanchor': 'center',
        'yanchor': 'top'})

"""