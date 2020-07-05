#dash library
from dash import Dash
import dash_core_components as dcc 
import dash_html_components as html 
from dash.dependencies import Input , Output, State
import  plotly.graph_objects as go 
import plotly.figure_factory as ff 

import pandas as pd 
import numpy as np
import re
import time
import re
from os import path


from textblob import TextBlob
from textblob.sentiments import NaiveBayesAnalyzer


from textblob import TextBlob
from textblob.sentiments import NaiveBayesAnalyzer

from src.tweet_extractor import extractor
from model.text_blob import cleanTxt,getAnalysis,getPolarity,getSubjectivity

colors = {
    'background': '#111111',
    'text': '#5ae8ed'
}

app= Dash()

app.layout = html.Div([
                    html.H1(children= 'Tweeter Sentimental analysis',
                            style= {'textAlign': 'center',
                                    'color': colors['text']
                                    }
                            ),
                    html.Div(dcc.Input(id='input-on-submit', type='text')),
                    html.Button('Submit', id='submit-val', n_clicks=0),
                    dcc.Graph(id='senntimental_graph'),
                    dcc.Graph(id='wc_graph'
            )

])

@app.callback(Output('senntimental_graph', 'figure'),
            [Input('submit-val', 'n_clicks')],
            [State('input-on-submit', 'value')])
def update_output(n_clicks, value):
    # checking for raw file 
    if path.exists(f'./src/raw_data/tweet_{value}.csv'):
        print('file already exist in raw_data')
        df = pd.read_csv(f'./src/raw_data/tweet_{value}.csv')  
    else:
        extractor(value)
        time.sleep(3)
        df = pd.read_csv(f'./src/raw_data/tweet_{value}.csv')
    
    # checking for prediction file
    if path.exists(f'./pred/sentiment_{value}.csv'):
        print('prediction file already exist')
        df_pred= pd.read_csv(f'./pred/sentiment_{value}.csv')
    else: 
        print('performing sentimenatl analysis')
        df['tweet'] = df['tweet'].apply(cleanTxt)
        df['word_count'] =  df['tweet'].apply(lambda x: len(str(x).split()))
        df['char_count'] = df['tweet'].apply(lambda x: len(str(x)))
        # Create two new columns 'Subjectivity' & 'Polarity'
        df['Subjectivity'] = df['tweet'].apply(getSubjectivity)
        df['Polarity'] = df['tweet'].apply(getPolarity)
        df['Analysis'] = df['Polarity'].apply(getAnalysis)
        print('sentimental analaysis has done')
        df.to_csv(f'./pred/sentiment_{value}.csv')
        time.sleep(3)
        df_pred= pd.read_csv(f'./pred/sentiment_{value}.csv')

    #df_pred = pd.read_csv(f'./pred/sentiment_{value}.csv')
    traces= [go.Bar(x=df_pred['Analysis'].value_counts().index, y=df_pred['Analysis'].value_counts().values)]
    return {
        'data': traces,
        'layout': go.Layout(
            xaxis= {'title': 'Sentiment'},
            yaxis = {'title': 'count'},
            height= 400,
            width= 400,
            hovermode= 'closest'
        )
    }

@app.callback(Output('wc_graph', 'figure'),
            [Input('submit-val', 'n_clicks')],
            [State('input-on-submit', 'value')])
def update_output(n_clicks, value):
        # checking for raw file 
    if path.exists(f'./src/raw_data/tweet_{value}.csv'):
        print('file already exist in raw_data')
        df = pd.read_csv(f'./src/raw_data/tweet_{value}.csv')  
    else:
        extractor(value)
        time.sleep(3)
        df = pd.read_csv(f'./src/raw_data/tweet_{value}.csv')
    
    # checking for prediction file
    if path.exists(f'./pred/sentiment_{value}.csv'):
        print('prediction file already exist')
        df_pred= pd.read_csv(f'./pred/sentiment_{value}.csv')
    else: 
        print('performing sentimenatl analysis')
        df['tweet'] = df['tweet'].apply(cleanTxt)
        df['word_count'] =  df['tweet'].apply(lambda x: len(str(x).split()))
        df['char_count'] = df['tweet'].apply(lambda x: len(str(x)))
        # Create two new columns 'Subjectivity' & 'Polarity'
        df['Subjectivity'] = df['tweet'].apply(getSubjectivity)
        df['Polarity'] = df['tweet'].apply(getPolarity)
        df['Analysis'] = df['Polarity'].apply(getAnalysis)
        print('sentimental analaysis has done')
        df.to_csv(f'./pred/sentiment_{value}.csv')
        time.sleep(3)
        df_pred= pd.read_csv(f'./pred/sentiment_{value}.csv')
    #df_pred = pd.read_csv(f'./pred/sentiment_{value}.csv')
    wc = df_pred['word_count']

    hist_data = [wc]

    group_labels = ['word_count distibution']
    fig = ff.create_distplot(hist_data, group_labels)

    return fig


if __name__ == "__main__":
    app.run_server()