import dash
import dash_core_components as dcc
import dash_html_components as html
import plotly.graph_objs as go
import pandas as pd
import numpy as np
import colorlover as cl
import base64
import re
app = dash.Dash(__name__)
server = app.server
app.config.supress_callback_exceptions = True


#!===========Functions=========================================================
#!=============================================================================

def get_neighbours(dff, threshold = 0.2):
    sample_neighbours = distance[distance[dff.pos.values[0]] < threshold].index
    neighbors = df[df['pos'].isin(sample_neighbours)]
    return(neighbors)

def plot_map(dff):
    return {
        'data': 
            [{
            'lat': df['latitude_deg'],
            'lon': df['longitude_deg'],
            'text': df['envo_biome_2'],
            'marker': {
                'size': df['observations_deblur_90bp']/10000,
                'opacity': 1,
                'color':[color_table_desat[i] for i in df['envo_tmp'].values],
                'line': {'width': 1000, 'color': 'black'}},
            'name': df['envo_tmp'].values,
            'showlegend' : False,
            'customdata': df.index,
            'type': 'scattermapbox'
        }]
            +
            [{
            'lat': dff['latitude_deg'],
            'lon': dff['longitude_deg'],
            'text': dff['envo_biome_2'],
            'marker': {
                'size': dff['observations_deblur_90bp']/10000,
                'opacity': 1,
                'color':[color_table[i] for i in dff['envo_tmp'].values],
                'line': {'width': 1000, 'color': 'black'}},
            'name': dff['envo_tmp'].values,
            'showlegend' : False,
            'customdata': dff.index,
            'type': 'scattermapbox'
        } ],
        'layout': {
            'mapbox': {
                'accesstoken': 'pk.eyJ1IjoicGVybG92YSIsImEiOiJjamN3ZmltYWMxYW1rMnhyeDcyeWt5MnlmIn0.hX0UCxkMYymXgFTvjqG6Zg',
                'style': 'mapbox://styles/perlova/cjd40swkw4tx72rqo2lm262p9',
                'zoom': 1,
            },
            'hovermode': 'closest',
            'dragmode': 'select',
            'margin': {'l': 0, 'r': 0, 'b': 0, 't': 0},
        }
        
    }
            
def plot_map_2(dff):
    return {
        'data': 
            [{
            'lat': dff['latitude_deg'],
            'lon': dff['longitude_deg'],
            'text': dff['biome_labels'],
            'marker': {
                'size': dff['observations_deblur_90bp']/10000,
                'opacity': 1,
                'color': [color_table_desat[i] for i in dff['envo_biome_2'].values]},
            'name': dff['biome_labels'].values,
            'showlegend' : True,
            'customdata': dff.index,
            'type': 'scattermapbox'
        } ],
        'layout': {
            'mapbox': {
                'accesstoken': 'pk.eyJ1IjoicGVybG92YSIsImEiOiJjamN3ZmltYWMxYW1rMnhyeDcyeWt5MnlmIn0.hX0UCxkMYymXgFTvjqG6Zg',
                'style': 'mapbox://styles/perlova/cjd40swkw4tx72rqo2lm262p9',
                'zoom': 1,
            },
            'hovermode': 'closest',
            'dragmode': 'select',
            'margin': {'l': 0, 'r': 0, 'b': 0, 't': 0},
            'legend': {'x': 0.5, 'y': 0.01, 'orientation': 'h'}
        }
        
    }
            
def plot_MDS(dff):
    return {
                'data': 
                      
                      [go.Scatter(
                        x=df[df['envo_tmp'] == i]['t_SNE_x'],
                        y=df[df['envo_tmp'] == i]['t_SNE_y'],
                        text=df[df['envo_tmp'] == i]['envo_biome_2'],
                        showlegend = True,
                        name = [env_re.findall(i)[0] if i != 'other' else i][0],
                        mode = 'markers',
                        customdata = df.index,
                        marker={
                            'opacity':1,
                            'size': 10,
                            'color': color_table_desat[i],
                            'line': {'width': 1, 'color': 'black'},
                        }) for i in df['envo_tmp'].unique()] +
                        
                        [go.Scatter(
                        x=dff['t_SNE_x'],
                        y=dff['t_SNE_y'],
                        text=dff['envo_biome_2'],
                        showlegend = False,
                        name = dff['envo_tmp'],
                        mode = 'markers',
                        hovertext = dff.country,
                        customdata = dff.index,
                        marker={
                            'opacity':1,
                            'size': 10,
                            'color':[color_table[i] for i in dff['envo_tmp'].values],
                            'line': {'width': 1, 'color': 'black'},
                        })],
                'layout': go.Layout(
                    margin={'l': 0, 'b': 0, 't': 0, 'r': 0},
                    hovermode='closest',
                    dragmode= 'select',
                    xaxis=dict(
                    autorange=True,
                    showgrid=False,
                    zeroline=False,
                    showline=False,
                    autotick=True,
                    ticks='',
                    showticklabels=False
                    ),
                    yaxis=dict(
                    autorange=True,
                    showgrid=False,
                    zeroline=False,
                    showline=False,
                    autotick=True,
                    ticks='',
                    showticklabels=False),
                    legend = {'x': 0.56, 'y': 0.01, 'orientation': 'v'},
                    #plot_bgcolor='#029386'
                            ),
                'box': go.Box(visible=True)
            }
            
            
def plot_pieplot(dff):
    return {
        'data':
            [
                go.Pie( 
                     labels=topic_labels, 
                     values=dff.iloc[0][topic_labels].values,
                     customdata = topic_labels,
                     textinfo = 'none',
                     hole=0.5,
                     sort = False,
                     marker=dict(colors=topic_pallette, 
                           line=dict(color='#000000', width=1))
                        )
            ],
        'layout':
                {
        "annotations": [{
                        "font": {"size": 15},
                        "showarrow": False,
                        "text": env_re.findall(dff.iloc[0]['envo_biome_2'])[0],
                        "x": 0.5,
                        "y": 0.5
                        }
                        ],
        'legend': {}
                }
            }

def generate_table(dff, max_rows=2):
    return html.Table(
        # Header
        [html.Tr([html.Th(col) for col in columns])] +

        # Body
        [html.Tr([
            html.Td(dff.iloc[i][col]) for col in dff.columns
        ]) for i in range(min(len(dff), max_rows))]
    )

#!===========Read data==========================================================
#!=============================================================================

df = pd.read_csv('./data/emp_deblur_90bp.qc_filtered_soil.t-SNE_JSD_LDA_topics.by_loc.csv', index_col = 0)
distance = pd.read_csv('./data/emp_deblur_90bp.qc_filtered_soil.JSD_distance_matrix.by_loc.csv', index_col = 0)
df.loc[df.envo_biome_2 == 'anthropogenic terrestrial biome', 
                     'envo_biome_2'] = df[df.envo_biome_2 == 'anthropogenic terrestrial biome'].envo_biome_3

topic_labels = ['Topic{}'.format(i) 
                        for i in range(20)]
dendro = './pictures/dendro.png' # replace with your own image                                                                      
encoded_image = base64.b64encode(open(dendro, 'rb').read())

background = '''
## Background
**Food insecurity.**
Food security is one of the biggest challenges humanity is facing in the 21st century both due to increasing population size and extreme weather conditions brought on by climate change. Right now 3 million children die every year due to undernutrition. And decrease in production in any one of the few major plants that sustain civilization due to drought, soil salinization, temperature extremes or pathogens (harmful microbes) might increase this number even further. Traditional agricultural technologies such as breeding plants with beneficial traits, supplementing soil with fertilizers, spraying crops with pesticides and insecticides, are only effective in a set of defined of conditions and are unable to provide long-term protection or sustain crop productivity in a changing environment. Moreover use and overuse of pesticides and insecticides has harmful side effects such as decline in the population of plant pollinators - another threat to food security. So in recent years a lot of effort and resources have been invested in developing new technologies that would increase crop plants productivity, tolerance to stress and protect them from pathogens. 

**Symbiotic relationships between plants and microbes.**
One of the most promising directions is exploring beneficial interactions between plants and microbes. It turns out that multicellular organisms - plants and animals, can be considered as ecosystems inhabited by many different species of microbes (microbiome). Microbes living on the roots and in the soil around (rhizosphere) can benefit the plant in several ways. Microbes convert nutrients present in the soil thereby make them available for plant intake and protect plant from pathogenic bacteria or stressful environmental conditions, while plants provide carbon source for bacteria to feed on.

**Soil microbiome vs plant microbiome.**
To exploit beneficial interactions between plants and microbes for enhancing agricultural sustainability and food security it is important to understand what are the major factors that define plant microbiome. Microbial composition of the plant rhizosphere is largely determined by the microbial composition of the soil. It is therefore reasonable to assume that effectiveness of the external microbial supplements will depend on the native microbial community structure as well.'''
data_analysis = '''
## Data Insights
**Samples from the same location have similar bacterial composition.**
To see if it makes sense to combine samples from the same locations I did hierarchical clustering of samples based on OTU composition ( I used cosine distance metric to calculate the pairwise distances between each pair of n-dimensional vectors describing each sample, where n number of OTUs). Then I plotted resulting dendrogram on top of the geographical distance matrix (see below). It does look like for the most part samples from the same location are also similar to each other in terms of the composition, at least if you consider the most abundant OTUs.

'''

#!===========Define constants=====================================================
#!=============================================================================
topic_pallette = ['#c9b003', '#77a1b5', '#fffd01', '#34013f', '#d3494e', '#99cc04',
       '#c6f808', '#7e4071', '#062e03', '#3b5b92', '#a2cffe', '#ff028d',
       '#9d5783', '#feb308', '#4a0100', '#8d8468', '#dd85d7', '#748500',
       '#d1b26f', '#fb5581']

color_table = {'cropland biome': '#840000',
 'dense settlement biome': '#960056',
 'desert biome': '#c65102',
 'forest biome': '#002d04',
 'freshwater biome': '#00035b',
 'grassland biome': '#033500',
 'other': '#363737',
 'shrubland biome': '#373e02',
 'tundra biome': '#014d4e'}

color_table_desat = {'cropland biome': '#ff474c',
 'dense settlement biome': '#fa5ff7',
 'desert biome': '#fdaa48',
 'forest biome': '#4f9153',
 'freshwater biome': '#95d0fc',
 'grassland biome': '#96f97b',
 'other': '#d8dcd6',
 'shrubland biome': '#acbf69',
 'tundra biome': '#90e4c1'}

columns = ['envo_biome_2', 'pos']

env_re = re.compile(r'.+(?= biome)')

slider_values = {i: env_re.findall(df['envo_biome_2'].unique()[i])[0] for i in range(len(df['envo_biome_2'].unique()))}
df['biome_labels'] = df.envo_biome_2.apply(lambda x: env_re.findall(x)[0])
slider_values[len(df['envo_biome_2'].unique())] = 'all'
#!===========Set up navbar======================================================
#!=============================================================================

app.layout = html.Div([
    dcc.Location(id='url', refresh=False),
    html.Div([
        html.Div([
            html.Div([
                html.Img(src="https://cdn2.iconfinder.com/data/icons/bacteria/512/bacteria_9-512.png",
                           style={'height': '100px'},className='navbar-brand'),
                dcc.Link('MicrobeX', href='/', className='navbar-brand',style={'padding-top': '40px'}),
                     ], className='navbar-header',
                ),
            html.Ul([
                html.Li([dcc.Link('Biome', href='/')]),
                html.Li([dcc.Link('Latent communities', href='/latent_communities')]),
                html.Li([html.A('About the project', href='/about')])
            ], className='nav navbar-nav',
            style={'padding-top': '25px'})
        ], className='container-fluid')
    ], className='navbar navbar-inverse navbar-fixed-top', style = {'background': '#014d4e'}
            ),
    html.Div(id='page-content', style={'padding-top': '90px', 'line-height': '40px'})
], style={'padding': '0px 10px 80px 10px',
    'marginLeft': 'auto', 'marginRight': 'auto', "width": "98%",
   })

#!============Main tab layout====================================================
main_layout = html.Div([
    html.Div([
        html.H3('Select an environment', style = {'fontsize': '14','textAlign': 'left'}),
        dcc.Slider(
                id = 'biome_slider',
                min=0,
                max=len(slider_values.keys()) - 1,
                marks=slider_values,
                value=5,
            )], 
        style = {'margin-top': '20px', 'margin-bottom': '50px', 'margin-left': '20px', "width": "90%",'textAlign': 'center'}),
    html.Div([
        html.H3('Select points to explore the connection between geography and community structure',
                style = {'fontsize': '14','textAlign': 'left'})
        ],
        style = {'padding': '0px 0px 0px 0px', 'margin-left': '20px'}),
    html.Div([
        html.Div([
            dcc.Graph(id='map', 
                selectedData={'points': [], 'range': None},
                style={'height':'100%'}, 
                animate=True),
            ], className="seven columns",
            style={'padding': '0px 0px 0px 0px', 'margin-left': '30px', 'border': '1px solid black'}),

        html.Div([
            dcc.Graph(id='MDS',
                selectedData={'points': [], 'range': None}, 
                style={'height':'90%','background': '#029386'},
                ),
            ], className="four columns", 
            style={'background': '#029386',
                   'padding': '0px 0px 0px 0px', 'margin-left': '20px', 'margin-right': '20px', 'border': '1px solid black'}),
        #html.Div([
       #generate_table(df)
       #])
        
    ], className="row"),
])

##!============Latent communities layout=======================================
topic_layout = html.Div([
    html.Div([
        html.H3('Hover over points on the map and piechart to explore latent communities composition',
                style = {'fontsize': '14','textAlign': 'left'})
        ],
        style = {'padding': '0px 0px 0px 0px', 'margin-left': '20px', 'margin-top': '10px'}),
    html.Div([
        html.Div([
            dcc.Graph(id='map_2', 
                hoverData={'points': [{'customdata': df.index[0]}], 'range': None},
                style={'height':'100%'}, 
                animate=True),
            ], className="seven columns",
            style={'padding': '0px 0px 0px 0px', 'margin-left': '30px', 'border': '1px solid black'}),
      
        html.Div([
            dcc.Graph(id='pieplot',
                hoverData={'points': [{'customdata':'Topic1'}], 'range': None},
                style={'height':'90%','background': '#029386'},
                ),
            ], className="four columns", 
            style={'background': '#029386',
                   'padding': '0px 0px 0px 0px', 'margin-left': '20px', 'margin-right': '20px'}),       
    ], className="row"),
])

##!============About layout====================================================
slides_layout = html.Div([
    html.Div([
        dcc.Markdown(background, className='col-md-12')], 
    style = {'line-height': '18px', 'margin-right': '30px', 'margin-left': '30px'}),
    html.Div([
        html.Img(src='data:image/png;base64,{}'.format(encoded_image.decode()),
                 style={'height': '300px', 'textAlight': 'center'})
        ], style={'textAlign': 'center'}),
    html.Div([
        dcc.Markdown(data_analysis, className='col-md-12')], 
    style = {'line-height': '18px', 'margin-right': '30px', 'margin-left': '30px'}),
    html.Div([
        html.H2('Find out more about the project', style = {'display': 'block', 'textAlign': 'center', 'margin':'auto', 'margin-top': '25px'})
        ]),
    html.Div([
    html.Iframe(src='https://docs.google.com/presentation/d/e/2PACX-1vT-0AZi8An7IcQJ1Y1H-7P-UvuIzajaVph8A-HANFbcy-nl3KhyCF_9utQ2XzTW2fGc3TOO63Kj8dU6/embed?start=false&loop=false&delayms=3000',
                style = {'width': '960px', 'framborder': '0', 'height': '749px',
                         'textAlign': 'center', 'display': 'block', 'margin': 'auto','margin-top': '20px'})
                ])
    
    ])
          
       
#!===============Callbacks=====================================================
#!=============================================================================

#!Navbar callback
@app.callback(
    dash.dependencies.Output('page-content', 'children'),
    [dash.dependencies.Input('url', 'pathname')])
def display_page(pathname):
   if pathname == '/about':
       return slides_layout
   elif pathname == '/latent_communities':
       return topic_layout
   else:
        return main_layout

#!Hover callback
#@app.callback(
    #dash.dependencies.Output('table', 'children'),
    #[dash.dependencies.Input('map', 'hoverData')])
#def generate_table(hoverData, max_rows=10):
    #selected_points = [p['customdata'] for p in hoverData['points']]
    #dff = df.loc[selected_points]
    #dff_n = get_neighbours(dff)
    
    #return make_dash_table(dff)
    #return html.Table(
        ## Header
        #[html.Tr([html.Th(col) for col in dff.columns])] +

        ## Body
        #[html.Tr([
            #html.Td(dff.iloc[i][col]) for col in dff.columns
        #]) for i in range(min(len(dff), max_rows))]
    #)
    #return html.P(
        #'The sample from {} was collected on {}'.format(
            #dff_n.iloc[0]['env_material'],
            #dff_n.iloc[0]['country']
        #)
    #)
    
    
    #return {'data': go.Table(
    #header=dict(values=columns,
                #fill = dict(color='#C2D4FF'),
                #align = ['left'] * 5),
    #cells=dict(values=[dff[column] for column in columns],
               #fill = dict(color='#F5F8FF'),
               #align = ['left'] * 5))}

@app.callback(
    dash.dependencies.Output('pieplot', 'figure'),
    [dash.dependencies.Input('map_2', 'hoverData')])
def update_pieplot(hoverData, max_rows=10):
    selected_points = [p['customdata'] for p in hoverData['points']]
    dff = df.loc[selected_points]
    return (plot_pieplot(dff))

@app.callback(
    dash.dependencies.Output('map_2', 'figure'),
    [dash.dependencies.Input('pieplot', 'hoverData')])
def update_map_2(hoverData):
    dff = df[df[hoverData['points'][0]['customdata']] > 0.01]
    return (plot_map_2(dff))

#!MDS and slider callback
@app.callback(
    dash.dependencies.Output('map', 'figure'),
    [dash.dependencies.Input('biome_slider', 'value'),
     dash.dependencies.Input('MDS', 'selectedData')
    ])

def update_map(value, selectedData):
    if slider_values[value] != 'all':
        df['envo_tmp'] = 'other'
        df.loc[df.envo_biome_2 == '{} biome'.format(slider_values[value]), 'envo_tmp'] = df.loc[df.envo_biome_2 == '{} biome'.format(slider_values[value]), 'envo_biome_2']
    else:
         df['envo_tmp'] = df['envo_biome_2']
         
    selected_index = list(set([
        p['customdata'] for p in selectedData['points']
    ]))

    dff = df.loc[selected_index]    
    return (plot_map(dff))

#!Map and slider callback
@app.callback(
    dash.dependencies.Output('MDS', 'figure'),
    [dash.dependencies.Input('biome_slider', 'value'),
     dash.dependencies.Input('map', 'selectedData'),
     ])
def update_MDS_plot(value, selectedData):
    
    if slider_values[value] != 'all':
        df['envo_tmp'] = 'other'
        df.loc[df.envo_biome_2 == '{} biome'.format(slider_values[value]), 'envo_tmp'] = df.loc[df.envo_biome_2 == '{} biome'.format(slider_values[value]), 'envo_biome_2']
    else:
         df['envo_tmp'] = df['envo_biome_2']
    selected_index = list(set([
    p['customdata'] for p in selectedData['points']
    ]))

    dff = df.loc[selected_index]
    return (plot_MDS(dff))


app.css.append_css({
    'external_url': 'https://codepen.io/chriddyp/pen/bWLwgP.css'
})

app.css.append_css({
    'external_url': 'https://maxcdn.bootstrapcdn.com/bootstrap/3.3.7/css/bootstrap.min.css'
})
app.scripts.append_script({
    'external_url': 'https://code.jquery.com/jquery-3.2.1.slim.min.js'
})
app.scripts.append_script({
    'external_url': 'https://cdnjs.cloudflare.com/ajax/libs/popper.js/1.11.0/umd/popper.min.js'
})
app.scripts.append_script({
    'external_url': 'https://maxcdn.bootstrapcdn.com/bootstrap/3.3.7/js/bootstrap.min.js'
})

app.scripts.append_script({
    'external_url': "https://maxcdn.bootstrapcdn.com/font-awesome/4.7.0/css/font-awesome.min.css"
})

if __name__ == '__main__':
    app.run_server(debug=True)