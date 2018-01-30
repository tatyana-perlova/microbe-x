import dash
import dash_core_components as dcc
import dash_html_components as html
import plotly.graph_objs as go
import pandas as pd
import numpy as np
import colorlover as cl

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
        'data': [{
            'lat': df['latitude_deg'],
            'lon': df['longitude_deg'],
            'text': df['env_material'],
            'marker': {
                'size': df['observations_deblur_90bp']/10000,
                'opacity': 0,
                'color':[color_table_desat[i] for i in df[value2vary].values],
                },
            'name': df[value2vary].values,
            'showlegend' : False,
            'customdata': df.index,
            'type': 'scattermapbox'
        }] +
            [{
            'lat': df[df[value2vary] == i]['latitude_deg'],
            'lon': df[df[value2vary] == i]['longitude_deg'],
            'text': df[df[value2vary] == i]['env_material'],
            'marker': {
                'size': df[df[value2vary] == i]['observations_deblur_90bp']/10000,
                'opacity': 1,
                'color':color_table_desat[i],
                'line': {'width': 10, 'color': 'white'}},
            'name': i,
            'showlegend' : True,
            'customdata': df[df[value2vary] == i].index,
            'type': 'scattermapbox'
        } for i in df[value2vary].unique()]
            +
            [{
            'lat': dff['latitude_deg'],
            'lon': dff['longitude_deg'],
            'text': dff['env_material'],
            'marker': {
                'size': dff['observations_deblur_90bp']/10000,
                'opacity': 1,
                'color':[color_table[i] for i in dff[value2vary].values],
                'line': {'width': 10, 'color': 'white'}},
            'name': dff[value2vary].values,
            'showlegend' : False,
            'customdata': dff.index,
            'type': 'scattermapbox'
        } ],
        'layout': {
            'mapbox': {
                'accesstoken': 'pk.eyJ1IjoiY2hyaWRkeXAiLCJhIjoiY2ozcGI1MTZ3MDBpcTJ3cXR4b3owdDQwaCJ9.8jpMunbKjdq1anXwU5gxIw',
                'style': 'mapbox://styles/mapbox/light-v9',
                'zoom': 0,
            },
            'hovermode': 'closest',
            'dragmode': 'select',
            'margin': {'l': 40, 'r': 0, 'b': 10, 't': 10}
        }
        
    }
            
def generate_table(dataframe, max_rows=2):
    return html.Table(
        # Header
        [html.Tr([html.Th(col) for col in columns])] +

        # Body
        [html.Tr([
            html.Td(dataframe.iloc[i][col]) for col in dataframe.columns
        ]) for i in range(min(len(dataframe), max_rows))]
    )

#!===========Read data==========================================================
#!=============================================================================

df = pd.read_csv('./data/emp_deblur_90bp.qc_filtered_soil.t-SNE_JSD.by_loc.csv', index_col = 0)
distance = pd.read_csv('./data/emp_deblur_90bp.qc_filtered_soil.JSD_distance_matrix.by_loc.csv', index_col = 0)
columns = ['env_biome_2', 'pos'
       ]

#!===========Define constants=====================================================
#!=============================================================================
value2vary = 'envo_biome_2'

unique_types = df[value2vary].unique()                       
colors = cl.scales['9']['qual']['Set1']
colors_desat = cl.scales['9']['qual']['Pastel1'] 
if len(unique_types) > len(colors):                          
   colors = cl.interp(colors, len(unique_types))
   colors_desat = cl.interp(colors_desat, len(unique_types)) 
else:                                                        
   colors = colors[:len(unique_types)] 
   colors_desat = colors_desat[:len(unique_types)] 
color_table = dict(zip(unique_types, colors)) 
color_table_desat = dict(zip(unique_types, colors_desat)) 

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
                html.Li([dcc.Link('Location', href='/location')]),
                html.Li([html.A('Slides', href='/slides')])
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
    html.H2('Select points to explore the connection between geography and community structure',className="twelve columns",
           style = {'fontsize': '14'}),
    html.Div([
        html.Div([
            dcc.Graph(id='map', 
                selectedData={'points': [], 'range': None},
                style={'height':'80%'}, 
                ),
            ], className="eight columns",
            style={'boxShadow': '5px 5px 5px 5px rgba(204,204,204,0.4)'}),

        html.Div([
            dcc.Graph(id='MDS',
                selectedData={'points': [], 'range': None}, 
                style={'height':'100%'},
                ),
            ], className="four columns", 
            style={'boxShadow': '5px 5px 5px 5px rgba(204,204,204,0.4)',
                   'padding': '0px 0px 0px 0px'}),
        #html.Div([
       #generate_table(df)
       #])
        
    ], className="row"),
])
                
##!============Location explorer layout====================================================
slides_layout = html.Div([
    html.Div([
    html.H2('Find out more about the project', style = {'display': 'block', 'textAlight': 'center', 'margin':'auto', 'margin-top': '25px'})
    ]),
    html.Div([
    html.Iframe(src='https://docs.google.com/presentation/d/e/2PACX-1vT-0AZi8An7IcQJ1Y1H-7P-UvuIzajaVph8A-HANFbcy-nl3KhyCF_9utQ2XzTW2fGc3TOO63Kj8dU6/embed?start=false&loop=false&delayms=3000',
                style = {'width': '960px', 'framborder': '0', 'height': '749px',
                         'textAlight': 'center', 'display': 'block', 'margin': 'auto','margin-top': '20px'})
                ])
    
    ])
          
#!===============Callbacks=====================================================
#!=============================================================================

#!Navbar callback
@app.callback(
    dash.dependencies.Output('page-content', 'children'),
    [dash.dependencies.Input('url', 'pathname')])
def display_page(pathname):
   if pathname == '/slides':
       return slides_layout
   else:
        return main_layout
    
@app.callback(
    dash.dependencies.Output('table', 'children'),
    [dash.dependencies.Input('map', 'hoverData')])
def generate_table(hoverData, max_rows=10):
    selected_points = [p['customdata'] for p in hoverData['points']]
    dff = df.loc[selected_points]
    dff_n = get_neighbours(dff)
    
    return make_dash_table(dff)
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
    dash.dependencies.Output('map', 'figure'),
    [dash.dependencies.Input('MDS', 'selectedData'),
    ])
    
def update_map(*selectedDatas):
    index = df.index
    # filter the dataframe by the selected points
    for i, hover_data in enumerate(selectedDatas):
        selected_index = [
            p['customdata'] for p in selectedDatas[i]['points']
            # the first trace that includes all the data
            if p['curveNumber'] == 0
        ]
        
        index = np.intersect1d(index, selected_index)
   
    dff = df.loc[index]
    return (plot_map(dff))

@app.callback(
    dash.dependencies.Output('MDS', 'figure'),
    [dash.dependencies.Input('map', 'selectedData'),
     ])
def update_MDS_plot(*selectedDatas):
    index = df.index
    # filter the dataframe by the selected points
    for i, hover_data in enumerate(selectedDatas):
        selected_index = [
            p['customdata'] for p in selectedDatas[i]['points']
            # the first trace that includes all the data
            if p['curveNumber'] == 0
        ]
        
        index = np.intersect1d(index, selected_index)
   
    dff = df.loc[index]
    return ({
                'data': 
                      [go.Scatter(
                        x=df['t_SNE_x'],
                        y=df['t_SNE_y'],
                        text=df['env_material'],
                        showlegend = False,
                        name = df[value2vary],
                        mode = 'markers',
                        customdata = df.index,
                        marker={
                            'opacity':1,
                            'size': 10,
                            'color': [color_table_desat[i] for i in df[value2vary].values],
                            'line': {'width': 1, 'color': 'white'},
                        })] +
                        
                        [go.Scatter(
                        x=dff['t_SNE_x'],
                        y=dff['t_SNE_y'],
                        text=dff['env_material'],
                        showlegend = False,
                        name = dff[value2vary],
                        mode = 'markers',
                        customdata = dff.index,
                        marker={
                            'opacity':1,
                            'size': 10,
                            'color':[color_table[i] for i in dff[value2vary].values],
                            'line': {'width': 1, 'color': 'white'},
                        })],
                'layout': go.Layout(
                    margin={'l': 0, 'b': 0, 't': 10, 'r': 0},
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
                    showticklabels=False)
                            ),
                'box': go.Box(visible=True)
            })


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