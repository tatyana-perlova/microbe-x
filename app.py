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

#!===========Read data=========================================================
#!=============================================================================

df = pd.read_csv('./data/emp_deblur_90bp.qc_filtered_soil.t-SNE_JSD_LDA_topics.by_loc.csv', index_col = 0)
distance = pd.read_csv('./data/emp_deblur_90bp.qc_filtered_soil.JSD_distance_matrix.by_loc.csv', index_col = 0)
df.loc[df.envo_biome_2 == 'anthropogenic terrestrial biome', 
                     'envo_biome_2'] = df[df.envo_biome_2 == 'anthropogenic terrestrial biome'].envo_biome_3

df.loc[df.country == 'GAZ:United States of America', 
                     'country'] = 'GAZ:USA'
topic_labels = ['Topic{}'.format(i) 
                        for i in range(20)]

#!===========================Images==============================================
dendro = './pictures/dendro.png'                                                                    
encoded_dendro = base64.b64encode(open(dendro, 'rb').read())
mds_tsne = './pictures/mds_vs_tSNE.png'                                                                    
encoded_mds_tsne = base64.b64encode(open(mds_tsne, 'rb').read())
sim_vs_dist = './pictures/sim_vs_dist.png'                                                                    
encoded_sim_vs_dist = base64.b64encode(open(sim_vs_dist, 'rb').read())
topics_over_biomes = './pictures/topics_over_biomes.png'                                                                    
encoded_topics_over_biomes = base64.b64encode(open(topics_over_biomes, 'rb').read())
biomes_over_topics = './pictures/biomes_over_topics.png'                                                                    
encoded_biomes_over_topics = base64.b64encode(open(biomes_over_topics, 'rb').read())

#!=========================Project description===================================
#!===============================================================================
background = '''
## Background and motivation
**Food insecurity.**
Food security is one of the biggest challenges humanity is facing in the 21st century both due to increasing population size and extreme weather conditions brought on by climate change. Right now 3 million children die every year due to undernutrition. And decrease in production in any one of the few major plants that sustain civilization due to drought, soil salinization, temperature extremes or pathogens (harmful microbes) might increase this number even further. Traditional agricultural technologies such as breeding plants with beneficial traits, supplementing soil with fertilizers, spraying crops with pesticides and insecticides, are only effective in a set of defined of conditions and are unable to provide long-term protection or sustain crop productivity in a changing environment. Moreover use and overuse of pesticides and insecticides has harmful side effects such as decline in the population of plant pollinators - another threat to food security. So in recent years a lot of effort and resources have been invested in developing new technologies that would increase crop plants productivity, tolerance to stress and protect them from pathogens. 

**Symbiotic relationships between plants and microbes.**
One of the most promising directions is exploring beneficial interactions between plants and microbes. It turns out that multicellular organisms - plants and animals, can be considered as ecosystems inhabited by many different species of microbes (microbiome). Microbes living on the roots and in the soil around (rhizosphere) can benefit the plant in several ways. Microbes convert nutrients present in the soil thereby make them available for plant intake and protect plant from pathogenic bacteria or stressful environmental conditions, while plants provide carbon source for bacteria to feed on.

**Project goal.**
To exploit beneficial interactions between plants and microbes for enhancing agricultural sustainability and food security it is important to understand what are the major factors that define plant microbiome. Microbial composition of the plant rhizosphere is largely determined by the microbial composition of the soil. It is therefore reasonable to assume that effectiveness of the external microbial supplements or probiotics will depend on the native microbial community structure as well. Information about soil microbial communities can be used to target plant probiotics to new locations: if the probiotics have been tested and shown successful in one location, their effectiveness in a new location can be inferred based on the similarity between the native microbial communities of the soil from the two locations. The goal of this project was to explore data from [Earth microbiome project](http://www.earthmicrobiome.org/), more specifically to determine which locations are similar to each other in terms of their bacterial compositions and which environmental factors drive this similarity.
'''
data_analysis = '''
## Methods
See [GitHub repository](https://github.com/tatyana-perlova/EMP-analysis) for implementation of the analysis described below.

**Data.**
Data was downloaded from [ftp server](ftp://ftp.microbio.me/emp/release1/otu_tables/). All analysis was done on `emp_deblur_90bp.qc_filtered.biom` biom table, quality-filtered, unrarified table, where OTU assignments were done in a database-independent manner based on sequence similarity. For more details on how the tables were produced see [Thompson et al., 2017, Nature](http://doi.org/10.1038/nature24621). The table was filtered to only leave samples from soil using Qiime command:

`$ filter_samples_from_otu_table.py -i ./emp_deblur_90bp.qc_filtered.biom -o ./emp_deblur_90bp.qc_filtered_soil.biom -m ../../mapping_files/emp_qiime_mapping_qc_filtered.tsv -s 'empo_3:Soil (non-saline)'`

Topic modelling and 2D embedding was performed on the table where samples from the same location were combined by adding correspondent OTU abundances. Latitude and longitude values were rounded to 2 significant figures prior to calculating geographical distance and combining samples from the same location (see below).

**Community similarity metrics.**
Pairwise distance between samples was calculated either using cosine similarity or [Jensen-Shannon divergence](https://en.wikipedia.org/wiki/Jensen%E2%80%93Shannon_divergence) (JSD), both metrics giving comparable results. However all further analysis discussed below was performed using JSD as a measure of similarity. JSD calculation was optimized and parallelized using numba library and took ~8 hours on 40 cores.

**Hierarchical clustering.**
[Hierarchical clustering](https://docs.scipy.org/doc/scipy/reference/generated/scipy.cluster.hierarchy.linkage.html#scipy.cluster.hierarchy.linkage) on the JSD distance matrix was performed using 'centroid' method for calculating distance between clusters (also tried 'single', 'complete', and 'ward' methods).

**Topic Modelling.**
Topic modelling was done using Latent Dirichlet Allocation module of scikit-learn library. Number of latent communities (topics) needed to describe samples was determined based on the values of perplexity, which is essentially a decreasing function of the log-likelihood of the data given the topic matrix and topic over samples distribution. Perplexity changed below 1\% when number of topics changed from 20 to 25 so I set the number of topics to 20. 

**2D embedding with t-SNE and MDS.**
I used both MDS and [t-SNE](https://distill.pub/2016/misread-tsne/) to embed calculated JSD distance matrix in 2 dimensions (see Results for comparison between the two). While t-SNE prioritizes points that are close to each other in high-dimensional space, MDS creates a more faithful representation of the distances between points.
'''

dendro_text = '''
**Samples from the same location have similar bacterial composition**
To see if it makes sense to combine samples from the same locations I did hierarchical clustering of samples based on their pairwise distance according to JSD. Then I plotted resulting dendrogram on top of the geographical distance matrix sorted accordingly (see below). It does look like for the most part samples from the same location are also similar to each other in terms of the composition, i.e. cluster borders also mark geographical clusters, although there are a few location with samples belonging to multiple clusters.'''

two_d_embedding = '''
**Samples from the same type of environment have similar bacterial composition**
Accordingt to the 2d embedding of the samples both with t-SNE and MDS it looks like bacteria cluster together although there is quite a bit of overlap as well.'''

sim_vs_dist_text = '''
**Sample similarity decreases with distance and depends on the environment.**
I also looked at how similarity between samples (1-JSD) changes with geographical distance between them. This analysis was done prior to combining samples from the same location and and point binning was down by geographical distance. While trends is the same for different environments, i.e. similarity decreases with distance as expected, croplands are more similar to each other than deserts even at longer distances. Although this might have to do that both places in Antarctica and South US were labeled as deserts.'''

topics_text = '''
**Different environments have distinct composition in terms of latent communities.**
Based on the distribution of latent communities over different environments (see below), it looks like that some environments are dominated by just a few latent communities, e.g. freshwater and shrubland (see below). And vice versa some topics only have significant abundance in a few environments (see below).'''


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
country_re = re.compile(r'(?<=GAZ:).+')


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
                html.Li([dcc.Link('Geography&Biome', href='/')]),
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
        style = {'margin-top': '20px', 'margin-bottom': '50px', 'margin-left': '15px', "width": "90%",'textAlign': 'center'}),
    html.Div([
        html.H3('Select points to explore the connection between geography and community structure',
                style = {'fontsize': '14','textAlign': 'left'})
        ],
        style = {'padding': '0px 0px 0px 0px', 'margin-left': '15px', 'margin-bottom': '20px'}),
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
            ], className="five columns", 
            style={'background': '#029386',
                   'padding': '0px 0px 0px 0px', 'margin-left': '10px', 'margin-right': '10px', 'border': '1px solid black'}),
        
    ], className="row"),
])

##!============Latent communities layout=======================================
topic_layout = html.Div([
    html.Div([
        html.H3('Hover over points on the map and piechart to explore the composition of latent communities',
                style = {'fontsize': '14','textAlign': 'left'})
        ],
        style = {'padding': '0px 0px 0px 0px', 'margin-left': '15px', 'margin-top': '15px',  'margin-bottom': '15px'}),
    html.Div([
        html.Div([
            html.Div(id = 'topic_info', style = {'line-height': '18px', 'textAlign': 'center'}),
            dcc.Graph(id='map_2', 
                hoverData={'points': [{'customdata': df.index[0]}], 'range': None},
                style={'height':'100%'}, 
                animate=True),
            ], className="seven columns",
            style={'padding': '0px 0px 0px 0px', 'margin-left': '30px'}),
      
        html.Div([
            html.Div(id = 'sample_info', style = {'line-height': '18px', 'textAlign': 'center'}),
            dcc.Graph(id='pieplot',
                hoverData={'points': [{'customdata':'Topic1'}], 'range': None},
                style={'height':'100%'},
                ),
            ], className="five columns", 
            style={
                   'padding': '0px 0px 0px 0px', 'margin-left': '0px', 'margin-right': '20px'}),       
    ], className="row"),
])

##!============About layout====================================================
slides_layout = html.Div([
    html.Div([
        dcc.Markdown(background, className='col-md-12')], 
    style = {'line-height': '18px', 'margin-right': '30px', 'margin-left': '30px'}),
    html.Div([
        dcc.Markdown(data_analysis, className='col-md-12')], 
    style = {'line-height': '18px', 'margin-right': '30px', 'margin-left': '30px'}),
     html.Div([
        dcc.Markdown('''## Results'''),
        dcc.Markdown(dendro_text),
        html.Img(src='data:image/png;base64,{}'.format(encoded_dendro.decode()),
                 style={'height': '300px', 'textAlight': 'center'}),
        dcc.Markdown(sim_vs_dist_text),
        html.Img(src='data:image/png;base64,{}'.format(encoded_sim_vs_dist.decode()),
                 style={'height': '300px', 'textAlight': 'center'}),
        dcc.Markdown(two_d_embedding),
        html.Img(src='data:image/png;base64,{}'.format(encoded_mds_tsne.decode()),
                 style={'height': '300px', 'textAlight': 'center'}),
        dcc.Markdown(topics_text),
        html.Img(src='data:image/png;base64,{}'.format(encoded_topics_over_biomes.decode()),
                 style={'height': '250px', 'textAlight': 'center'}),
        html.Img(src='data:image/png;base64,{}'.format(encoded_biomes_over_topics.decode()),
                 style={'height': '250px', 'textAlight': 'center'})
        ], 
    style = {'line-height': '18px', 'margin-right': '30px', 'margin-left': '30px'}, className='col-md-12'),
    html.Div([
        html.H2('Find out more about the project', style = {'display': 'block', 'textAlign': 'center', 'margin':'auto', 'margin-top': '25px'})
        ]),
    html.Div([
    html.Iframe(src="https://docs.google.com/presentation/d/e/2PACX-1vQuvAYk8nORSR-hNKUTIA_2CAMRFhkRG2EidQWCskLZpS7ItDMWAj6_cTrd59WRQ-bKlEVtjy_tdoR_/embed?start=false&loop=false&delayms=3000",
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

#!====================Latent communities page callbacks========================

#!map callbacks
@app.callback(
    dash.dependencies.Output('pieplot', 'figure'),
    [dash.dependencies.Input('map_2', 'hoverData')])
def update_pieplot(hoverData, max_rows=10):
    selected_points = [p['customdata'] for p in hoverData['points']]
    dff = df.loc[selected_points]
    return (plot_pieplot(dff))

@app.callback(
    dash.dependencies.Output('sample_info', 'children'),
    [dash.dependencies.Input('map_2', 'hoverData')])
def update_sample(hoverData):
    selected_points = [p['customdata'] for p in hoverData['points']]
    dff = df.loc[selected_points]
    return html.P(
        'The sample from {} collected in {}'.format(
            dff.iloc[0]['env_material'],
            country_re.findall(dff.iloc[0]['country'])[0]
                )
        )

#!pieplot callbacks
@app.callback(
    dash.dependencies.Output('map_2', 'figure'),
    [dash.dependencies.Input('pieplot', 'hoverData')])
def update_map_2(hoverData):
    dff = df[df[hoverData['points'][0]['customdata']] > 0.01]
    return (plot_map_2(dff))


@app.callback(
    dash.dependencies.Output('topic_info', 'children'),
    [dash.dependencies.Input('pieplot', 'hoverData')])
def update_topic(hoverData):
    return html.P(
        'Samples that contain {}'.format(
            hoverData['points'][0]['customdata']
                                        )
                )

#!===============Main page callbacks===========================================

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


#!================Styles=========================================================================
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