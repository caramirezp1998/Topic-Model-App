#!/usr/bin/env python
# coding: utf-8

# # DASH APP
# 
# 1) Virtual enviroment de la app se llama, app_env ya podemos acceder a él a traves de jupyter notebook
# 
# Pasos para crear un virtual enviroment:
# 
#     - en conda prompt correr:
#     
#         - conda create -n __name__ python=3.6
#         
#         - conda activate __name__
#         
#         - Seguir los otros pasos del blog<https://janakiev.com/blog/jupyter-virtual-envs/>
#         
# 2) Implementar eficientemente los requirimientos del proyecto
# 
# 3) Creación de la aplicación web
# 
# 4) Crear conexión con servidores para que se abastezca de información (files_lemmatized)
# 
# 5) Desplegación de la aplicación en Heroku

#Para revisar como se realiza el deployment de la app en heroku una vez se tiene listo el virtual enviroment a traves de venv
#Usa https://dash.plotly.com/deployment



# In[15]:


#get_ipython().system(' conda activate app_env')
#get_ipython().system('pip install dash ')
#get_ipython().system('pip install dash-html-components ')
#get_ipython().system('pip install dash-core-components ')
#get_ipython().system('pip install dash-table  ')
#get_ipython().system('pip install dash-daq  ')


# In[ ]:





# ## Tutorial Part 2 App Layout
# 
# 

# In[21]:


# -*- coding: utf-8 -*-
import dash
import dash_core_components as dcc
import dash_html_components as html
import plotly.graph_objects as go
import os 
import json as js
import pandas as pd
import re # El paquete para tratar texto. Expresiones regulares
import matplotlib.pyplot as plt
import numpy as np
import time
# LDA, tSNE
# Visualization
import matplotlib.patches as mpatches
import matplotlib
import dash_bootstrap_components as dbc






def link_construsctor(date_1,date_2,num_topics,csv):
    first_date=["2020-04-13","2020-04-27","2020-05-11","2020-05-25","2020-06-08","2020-06-22","2020-07-06","2020-07-20"]
    second_date=["2020-04-26","2020-05-10","2020-05-24","2020-06-07","2020-06-21","2020-07-05","2020-07-19","2020-08-02"]
    print(first_date[date_1])
    print(second_date[date_2-1])
    link="https://raw.githubusercontent.com/caramirezp1998/Proyectos-Personales/master/Dash%20App/Escenarios/"+str(first_date[date_1])+"__"+str(second_date[date_2-1])+"/"+num_topics+"/"+csv
    return link


    
#lda_output=pd.read_csv("https://raw.githubusercontent.com/caramirezp1998/Proyectos-Personales/master/Dash%20App/Escenarios/2020-04-13__2020-04-26/12/lda_output.csv",
               #encoding="utf-8", index_col=0)
#topic_word_df=pd.read_csv("https://raw.githubusercontent.com/caramirezp1998/Proyectos-Personales/master/Dash%20App/Escenarios/2020-04-13__2020-04-26/12/topic_word_df.csv",
              # encoding="utf-8", index_col=0)

def tsne_traces(tsnedf):
    traces=[]
    a=0
    for i in range(0,len(tsnedf["topico_dominante"].unique())):
        trace = go.Scatter(
            x = tsnedf.loc[tsnedf["topico_dominante"]==i,"x_tsne"],
            y =  tsnedf.loc[tsnedf["topico_dominante"]==i,"y_tsne"],
            mode = "markers",
            opacity=0.65,
            name = "Topic: "+str(1+i),
            marker ={
                'size': 12,
                'line': {'width': 0.35, 'color': 'white'}
            },
            hovertext=tsnedf.loc[tsnedf["topico_dominante"]==i,"titulo"],
            hoverinfo=None)
        traces.append(trace)
    return traces

def pca_traces(tsnedf):
    traces=[]
    a=0
    for i in range(0,len(tsnedf["topico_dominante"].unique())):
        trace = go.Scatter(
            x = tsnedf.loc[tsnedf["topico_dominante"]==i,"x_pca"],
            y =  tsnedf.loc[tsnedf["topico_dominante"]==i,"y_pca"],
            mode = "markers",
            opacity=0.65,
            name = "Topic: "+str(1+i),
            marker ={
                'size': 12,
                'line': {'width': 0.35, 'color': 'white'}
            },
            hovertext=tsnedf.loc[tsnedf["topico_dominante"]==i,"titulo"],
            hoverinfo=None)
        traces.append(trace)
    return traces

def tsne_spider_trace(lda_output_row,num_doc,num_topics):
    trace=[go.Scatterpolar(
        name="Doc: "+str(num_doc),
        opacity=0.9,
        r=lda_output_row,
        fill='toself',
        theta=["Topic: "+str(i+1) for i in range(0,num_topics)])]
    return trace



def topic_doc_distribution(lda_output):
    trace=[go.Histogram(
    x=lda_output['dominant_topic'],
    histnorm="",
    name='control', # name used in legend and hover labels
    marker_color='#EB89B5',
    opacity=0.75
)]
    return trace


df=pd.DataFrame()
external_stylesheets = ['https://codepen.io/chriddyp/pen/dZVMbK.css', dbc.themes.FLATLY]
#"https://stackpath.bootstrapcdn.com/bootswatch/4.4.1/lux/bootstrap.min.css"
#,
 #                       "https://stackpath.bootstrapcdn.com/bootswatch/4.4.1/simplex/bootstrap.min.css"
##PReguntarle a Checho como ponga una linea bonita divisoria

navbar = dbc.Navbar(
    children=[
        dbc.NavbarBrand("Topic Modeling Project",
                       style={'fontSize':30})        
    ],
    sticky=True,
    color="primary",
    dark=True,
    
)



init= html.Div([
    dbc.Container([
        dbc.Row([
            dbc.Col(html.H1("Welcome to the Topic-Modelling dashboard", className="text-center")
                    , className="mb-5 mt-5")
        ]),
        dbc.Row([
            dbc.Col(html.H3(children='This dash app marks my first attempt at creating an interactive visualization of an statistical text model output.  '
                                     )
                    , className="mb-4")
            ]),

        dbc.Row([
            dbc.Col(html.H3(children='This project had 4 phases: Data collecting, Text Processing, Creating the LDA model and creating this dashboard to visualize the results.')
                    , className="mb-5")
        ]),

        dbc.Row([
            dbc.Col(dbc.Card(children=[html.H3(children='If you want grab a peek at the code of the project and learn more about me.',
                                               className="text-center"),
                                       dbc.Row([dbc.Col(dbc.Button(dcc.Markdown(''' Git-Hub''', style={'display': 'inline-block',
             'marginTop': '10px',
             'marginBottom':'10px',
             'fontSize': 15}), href="https://github.com/caramirezp1998/Topic-Model-App",
                                                                   color="primary"),
                                                        className="mt-3"),
                                                dbc.Col(dbc.Button(dcc.Markdown(''' Linkedin''', style={'display': 'inline-block',
             'marginTop': '10px',
             'marginBottom':'10px',
             'fontSize': 15}), href="https://www.linkedin.com/in/caramirezp98"),
                                                        className="mt-3")], justify="center")
                                       ],
                             body=True, color="dark", outline=True)
                    , width=6, className="mb-5"),

            dbc.Col(dbc.Card(children=[html.H4(children='I will be posting an article soon, where I will discuss the details of the project',
                                               className="text-center"),
                                       dbc.Button(" Future Article Link",
                                                  href=".",
                                                  color="primary",
                                                  className="mt-4"),

                                       ],
                             body=True, color="dark", outline=True)
                    , width=6, className="mb-3")
        ], className="mb-4", justify="center"),

    ])

])



#If I needed to run the page individually
app = dash.Dash(__name__, external_stylesheets=external_stylesheets)
server = app.server
#app.layout instead of layout
app.layout =html.Div([navbar, init, html.Div([
    html.Div([
    html.H1("The LDA Model"),
    html.H1(children="Interpretating the Results"),
    html.Div(
    [dbc.Col(dcc.Markdown(''' The output of the LDA model is a matrix with k-topics as dimension, we can map the output to get the estimated probability that an article belongs to a certain topic based on the words it contains. In the following plot, I try to reproduce the distribution of articles by mapping from a K dimensional space to a 2 dimension plot with the tsne function. We can appreciate how one topic may be "far" or "closer" from the other and what words the algorithm thought were relevant to make the distintion between them. 
    ''', style={'display': 'inline-block',
             'marginTop': '10px',
             'marginBottom':'10px',
             'fontSize': 15}),width=10),
    html.Div([
        dbc.Row(
        [
            dbc.Col(
                html.Div([
                    dcc.Graph(
                        id='tsne-graph',
                        animate=True,
                        animation_options=dict(transition={"duration":750})), 
                    html.Div([
                    dcc.RangeSlider(
                        id="range-slider_tsne",
                        min=0,
                        max=8,
                        step=None,
                        allowCross=False,
                        marks={
                    0: "13-04-2020",
                    1: "27-04-2020",
                    2: "11-05-2020",
                    3: "25-05-2020",
                    4: "08-06-2020",
                    5: "21-06-2020",
                    6: "06-07-2020",
                    7: "20-07-2020",
                    8: "02-08-2020"
                            
                },
                value=[0, 2]
                    )],style={'width':'85%'})
                ])
            , width= 10),
            dbc.Col(
                html.Div([ html.H4("Number of Topics"),html.Br(),
                    dcc.Dropdown(
                        id='topic-dropdown_tsne',
                        options=[
                            {'label': '4', 'value': '4'},
                            {'label': '6', 'value': '6'},
                            {'label': '8', 'value': '8'},
                            {'label': '10', 'value': '10'},
                            {'label': '12', 'value': '12'}
                        ],
                        value='10'
                    )
                ],style={'width': '80%', 'display': 'inline-block'})
            , width=3.5, align="start", className="pt-2")
        ]
        , justify="start", className="mt-3 mb-3 pl-3"), html.Br(), html.Br(),
           html.Div([dbc.Row([html.Div(dbc.Row([
                        dbc.Col( dbc.Card(
                            dbc.ListGroup([
                                dbc.ListGroupItem([
                                    dbc.ListGroupItemHeading("Title:"
                                    )
                                ]),
                                dbc.ListGroupItem([
                                    dbc.ListGroupItemHeading("Topic"
                                    )
                                ]),
                                dbc.ListGroupItem([
                                    dbc.ListGroupItemHeading("Category:"
                                    )
                                ]),
                                dbc.ListGroupItem([
                                    dbc.ListGroupItemHeading("Link:")
                                ]),
                                dbc.ListGroupItem([
                                    dbc.ListGroupItemHeading("Words related to the Topic:"
                                    )
                                ])
                            ])
                        ), width=5, align="start"),
                        dbc.Col( dbc.Card(
                            dbc.ListGroup([
                                dbc.ListGroupItem(id="titulo-tsne",
                                                  className="font-size-16px"
                                    
                                ),
                                dbc.ListGroupItem(id="topico-tsne",
                                                  className="font-size-16px"
                                    ),
                                dbc.ListGroupItem(id="category-tsne",
                                                  className="font-size-16px"
                                    ), 
                                dbc.ListGroupItem(id="link-tsne",
                                                  className="font-size-16px"
                                   ),
                                dbc.ListGroupItem(id="topic-words-tsne",
                                                  className="font-size-16px"
                                   )
                            ])
                        )
                        , className="m-1")
                   ], className='m-2 p-1')
                       ),dbc.Row([dbc.Col([dcc.Graph(
                            id="tsne_spider_graph",
                            animate=True,
                            animation_options=dict(transition={"duration":750})

    )],width=5)], className="m-2 p-1")
              ])
                    ] ,style={'width': '90%', 'display': 'inline-grid'}),
        
    html.Div([dbc.Row([dbc.Col(html.Img(id="word-cloud-tsne", style={"height":'250', 'width':"250"}),width=5), 
            dbc.Col(dcc.Graph(
            id="tsne_histogram_topics",
            animate=True,
            animation_options=dict(transition={'duration':750})),width=7)])],style={'width': '80%', 'display': 'inline-grid',
         'marginRight': '10px',
         'marginLeft': '50px',
         'marginTop': '30px',
         'marginBottom':'30px'})
    ])
    ]
    )
    ]
    )
    ,
    html.H2("Principal Component Analysis"
    ),
    html.Div(
    [
        dcc.Markdown(''' Another way of visualizing the results is through the Principal Component Analysis  dimensionality reduction technique.
    ''', style={'display': 'inline-block',
             'marginTop': '10px',
             'marginBottom':'10px',
             'fontSize': 15}),
     html.Div(
    [
        dbc.Container( dbc.Row(
        [
            dbc.Col(
                html.Div([
                    dcc.Graph(
                        id='pca-graph',
                        animate=True,
                        animation_options=dict(transition={"duration":800}),


                    ),
                        html.Div([
                            dcc.RangeSlider(
                                id="range-slider_pca",
                                min=0,
                                max=8,
                                step=None,
                                allowCross=False,
                                marks={
                            0: "13-04-2020",
                            1: "27-04-2020",
                            2: "11-05-2020",
                            3: "25-05-2020",
                            4: "08-06-2020",
                            5: "21-06-2020" ,
                            6: "06-07-2020",
                            7: "20-07-2020",
                            8: "02-08-2020"
                        },
                        value=[0, 2]
                            )]  
                        )]), width= 7),
            dbc.Col(
               html.Div([
                    dcc.Dropdown(
                        id='topic-dropdown_pca',
                        options=[
                            {'label': '4', 'value': '4'},
                            {'label': '6', 'value': '6'},
                            {'label': '8', 'value': '8'},
                            {'label': '10', 'value': '10'},
                            {'label': '12', 'value': '12'}
                        ],
                        value='10'
                    ),
                   dbc.Row([
                        dbc.Col(
                            dbc.ListGroup([
                                dbc.ListGroupItem([
                                    dbc.ListGroupItemHeading("Title:"
                                    )
                                ]),
                                dbc.ListGroupItem([
                                    dbc.ListGroupItemHeading("Topic"
                                    )
                                ]),
                                dbc.ListGroupItem([
                                    dbc.ListGroupItemHeading("Category:"
                                    )
                                ]),
                                dbc.ListGroupItem([
                                    dbc.ListGroupItemHeading("Link:")
                                ]),
                                dbc.ListGroupItem([
                                    dbc.ListGroupItemHeading("Words related to the Topic:"
                                    )
                                ])
                            ])
                        ),
                        dbc.Col(
                            dbc.ListGroup([
                                dbc.ListGroupItem([
                                    dbc.ListGroupItemHeading(id="titulo-pca"
                                    )
                                ]),
                                dbc.ListGroupItem([
                                    dbc.ListGroupItemHeading(id="topico-pca"
                                    )
                                ]),
                                dbc.ListGroupItem([
                                    dbc.ListGroupItemHeading(id="category-pca"
                                    )
                                ]), 
                                dbc.ListGroupItem([
                                    dbc.ListGroupItemHeading(id="link-pca"
                                    )
                                ]),
                                dbc.ListGroupItem([
                                    dbc.ListGroupItemHeading(id="topic-words-pca"
                                    )
                                ])
                            ])
                        )
                    ], className="mt-4 mb-4"
                    )
                ])
            )
        ]
        ))
    ]
    )
    ]
    ),
    html.Div(id="intermediate-value-tsne", style={'display':'none'}),
    html.Div(id='intermediate-topic-word-tsne', style={'display':'none'}),
    html.Div(id='intermediate-value-pca', style={'display':'none'}),
    html.Div(id='intermediate-topic-word-pca', style={'display':'none'}),
    html.Div(id="intermediate-lda-output-tsne", style={'display':'none'})
],style={'width': '95%', 'display': 'inline-block',
         'marginRight': '80px',
         'marginLeft': '80px',
         'marginTop': '80px',
         'marginBottom':'80px'})])



    
    
    
    
    
    
###############################################################################3
################################################################################33
####################################################################################3
#### CALLBACKS
######################################################################################

@app.callback(
[dash.dependencies.Output('intermediate-value-tsne','children'),
 dash.dependencies.Output('intermediate-topic-word-tsne','children'),
 dash.dependencies.Output('word-cloud-tsne','src'),
dash.dependencies.Output('intermediate-lda-output-tsne','children')],
[dash.dependencies.Input('range-slider_tsne', 'value'),
    dash.dependencies.Input("topic-dropdown_tsne","value")])
def update_intermediate_value_tsne(dates, num_topic):
    print(dates)
    print(link_construsctor(dates[0],dates[1],num_topic,"df_tot.csv"))
    df=pd.read_csv(link_construsctor(dates[0],dates[1],num_topic,"df_tot.csv"),
               encoding="utf-8", index_col=0)
    topic_word=pd.read_csv(link_construsctor(dates[0],dates[1],num_topic,"topic_word_df.csv"),
               encoding="utf-8", index_col=0)
    src=link_construsctor(dates[0],dates[1],num_topic,"word_cloud.jpg")
    lda_output=pd.read_csv(link_construsctor(dates[0],dates[1],num_topic,"lda_output.csv"),
                          encoding='utf-8',index_col=0)
    
    return [js.dumps(df.to_dict()), js.dumps(topic_word.to_dict()),src,js.dumps(lda_output.to_dict())]


@app.callback(
[dash.dependencies.Output('intermediate-value-pca','children'),
 dash.dependencies.Output('intermediate-topic-word-pca','children')],
[dash.dependencies.Input('range-slider_pca', 'value'),
    dash.dependencies.Input("topic-dropdown_pca","value")])
def update_intermediate_value_pca(dates, num_topic):
    df=pd.read_csv(link_construsctor(dates[0],dates[1],num_topic,"df_tot.csv"),
               encoding="utf-8", index_col=0)
    
    topic_word=pd.read_csv(link_construsctor(dates[0],dates[1],num_topic,"topic_word_df.csv"),
               encoding="utf-8", index_col=0)
    
    return [js.dumps(df.to_dict()), js.dumps(topic_word.to_dict())]

@app.callback(
dash.dependencies.Output('tsne-graph','figure'),
[dash.dependencies.Input('intermediate-value-tsne','children')])
def update_tsne_plot(obj):
    df=pd.DataFrame(js.loads(obj))
    traces=tsne_traces(df)
    figure={
            'data': traces,
            'layout': {
                "title": 'TSNE-Model',
                "yaxis": dict(title="",zeroline = False),
                "xaxis": dict(zeroline = False),
                "hovermode": "closest"
            }
    }
    
    
    return figure


@app.callback(
dash.dependencies.Output('tsne_spider_graph','figure'),
[dash.dependencies.Input('intermediate-lda-output-tsne','children'),
dash.dependencies.Input('tsne-graph','hoverData')])
def update_tsne_spider_graph(lda_output,hover_Data):
    if hover_Data is not None:
        print("hoverData is not None")
        lda_output=pd.DataFrame(js.loads(lda_output))
        data=np.array(lda_output.iloc[:,:])
        lda_output['dominant_topic']=np.argmax(data, axis=1)
        temp_df=lda_output.loc[lda_output['dominant_topic']==int(hover_Data['points'][0]['curveNumber']),:]
        output_row=temp_df.iloc[int(hover_Data["points"][0]["pointNumber"]),0:-1]
        trace=tsne_spider_trace(output_row,len(output_row),int(hover_Data["points"][0]["pointNumber"]))
        figure={
            'data': trace,
            'layout': {
                "title": 'Article Topic Distribution',
                  'polar':{
                      'radialaxis':{
                  'visible':True,
                  'range':[0,1]}},
                  'showlegend':False,
                "hovermode": "closest",
                'autosize':False,
                'width':400,
                'height':400
            }
        }
        
        return figure
    
    else:
        print("hoverData is not None")
        trace=[go.Scatterpolar(
            name="No Document",
            opacity=0.9,
            r=[10 for i in range(0,10)],
            fill='toself',
            theta=["topic: "+str(i+1) for i in range(0,10)])]
        figure={
            'data': trace,
            'layout': {
                "title": 'Article Topic - Distribution',
                  'polar':{
                      'radialaxis':{
                      'visible':True,
                      'range':[0,1]}},
                  'showlegend':False,
                "hovermode": "closest",
                'autosize': False,
                'width': 400,
                'height': 400
            }
        }
        
        return figure
    

@app.callback(
dash.dependencies.Output('tsne_histogram_topics','figure'),
[dash.dependencies.Input('intermediate-lda-output-tsne','children')])
def update_tsne_histogram_topics(lda_output):
    lda_output=pd.DataFrame(js.loads(lda_output))
    data=np.array(lda_output.iloc[:,:])
    lda_output['dominant_topic']=np.argmax(data, axis=1)
    trace= topic_doc_distribution(lda_output)
    figure={
            'data': trace,
            'layout': {
                "title": 'Documents Topic Distribution',
                  'polar':{
                      'radialaxis':{
                  'visible':True,
                  'range':[0,1]}},
                  'showlegend':False,
                "hovermode": "closest"
            }
        }
    return figure
    
    

# @app.callback(
#     dash.dependencies.Output('tsne-graph', 'figure'),
#     [dash.dependencies.Input('range-slider_tsne', 'value'),
#     dash.dependencies.Input("topic-dropdown_tsne","value")])
# def update_output_tsne(dates,num_topic):
#     df=pd.read_csv(link_construsctor(dates[0],dates[1],num_topic,"df_tot.csv"),
#                encoding="utf-8", index_col=0)
#     traces=tsne_traces(df)
#     figure={
#             'data': traces,
#             'layout': {
#                 "title": 'TSNE-Model',
#                 "yaxis": dict(title="",zeroline = False),
#                 "xaxis": dict(zeroline = False),
#                 "hovermode": "closest"
#             }
#     }
    
    
#     return figure
    
    
@app.callback(
dash.dependencies.Output('pca-graph', 'figure'),
[dash.dependencies.Input('range-slider_pca', 'value'),
dash.dependencies.Input("topic-dropdown_pca","value")])
def update_output_pca(dates,num_topic):
    df=pd.read_csv(link_construsctor(dates[0],dates[1],num_topic,"df_tot.csv"),
               encoding="utf-8", index_col=0)
    traces=pca_traces(df)
    figure={
            'data': traces,
            'layout': {
                "title": 'PCA-Model',
                "yaxis": dict(title="",zeroline = False),
                "xaxis": dict(zeroline = False),
                "hovermode": "closest"
            }
    }
    
    
    return figure


@app.callback(
[dash.dependencies.Output('titulo-tsne', 'children'),
dash.dependencies.Output('topico-tsne','children'),
dash.dependencies.Output('category-tsne', 'children'),
dash.dependencies.Output('topic-words-tsne','children'),
dash.dependencies.Output('link-tsne', 'children')],
   [dash.dependencies.Input('tsne-graph','hoverData'),
    dash.dependencies.Input('intermediate-value-tsne', 'children'),
    dash.dependencies.Input("intermediate-topic-word-tsne","children")]
)
def update_cards_tsne(hover_data,df_js,topic_word_js):
    if hover_data is not None:
        df=pd.DataFrame(js.loads(df_js))
        df=df.loc[df["topico_dominante"]==int(hover_data["points"][0]["curveNumber"]),:]
        df.reset_index(drop=True,inplace=True)
        topic_word=pd.DataFrame(js.loads(topic_word_js))
        npa=np.array(topic_word)
        pre=npa.argsort()[hover_data["points"][0]["curveNumber"],-11:-1]
        palab=[list(topic_word.columns)[i] for i in pre]
        palabras=", ".join(palab)        
        return [hover_data["points"][0]["hovertext"],hover_data["points"][0]["curveNumber"]+1,df.loc[int(hover_data["points"][0]["pointNumber"]),'categoria'],palabras,html.A("Article",href=df.loc[int(hover_data["points"][0]["pointNumber"]),"link"])]
    else:
        return ["","","","",""]

    
@app.callback(
[dash.dependencies.Output('titulo-pca', 'children'),
dash.dependencies.Output('topico-pca','children'),
dash.dependencies.Output('category-pca', 'children'),
dash.dependencies.Output('topic-words-pca','children'),
dash.dependencies.Output('link-pca', 'children')],
   [dash.dependencies.Input('pca-graph','hoverData'),
    dash.dependencies.Input('intermediate-value-pca', 'children'),
    dash.dependencies.Input("intermediate-topic-word-pca","children")]
)
def update_cards_pca(hover_data,df_js,topic_word_js):
    if hover_data is not None:
        df=pd.DataFrame(js.loads(df_js))
        df=df.loc[df["topico_dominante"]==int(hover_data["points"][0]["curveNumber"]),:]
        df.reset_index(drop=True,inplace=True)
        topic_word=pd.DataFrame(js.loads(topic_word_js))
        npa=np.array(topic_word)
        pre=npa.argsort()[hover_data["points"][0]["curveNumber"],-11:-1]
        palab=[list(topic_word.columns)[i] for i in pre]
        palabras=", ".join(palab)        
        return [hover_data["points"][0]["hovertext"],hover_data["points"][0]["curveNumber"]+1,df.loc[int(hover_data["points"][0]["pointNumber"]),'categoria'],palabras,df.loc[int(hover_data["points"][0]["pointNumber"]),"link"]]
    else:
        return ["","","","",""]    
    
    
#If I needed to run the page individually

if __name__ == '__main__':
    app.run_server(debug=True)