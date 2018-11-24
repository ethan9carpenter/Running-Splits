from flashResults import getAllLinks, getRace
import dash
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output
from flashResults.constants import columns as colsToDrop
from flashResults.constants import distance as distanceRaces
import os, json


def writeAndLoadRaces(override=False):
    if os.path.exists('links.json') and not override:
        with open('links.json', 'r') as file:
            raceMaps = json.load(file)
    else:
        url = 'http://flashresults.com/2016_Meets/Indoor/02-26_SEC/'
        url = 'http://www.flashresults.com/2017_Meets/Outdoor/06-29_TTSSFO/'
        extensions = getAllLinks(url)
        raceMaps = []
        for urls in extensions:
            for ext in urls:
                scr = getRace(url+ext)['raceInfo']
                if any([distance in scr for distance in distanceRaces]):
                    raceMaps.append({'label': scr, 'value': url+ext})
        with open('links.json', 'w') as file:
            json.dump(raceMaps, file)
            
    return raceMaps

def buildGraph(sectionLink, how='splits'):
    race = getRace(sectionLink)
    df = race.splitsTable
    info = race.raceName
    
    names = race.names
    
    for col in colsToDrop:
        if col in df.columns:
            df.drop(col, axis=1, inplace=True)
    
    lines = []
    
    y = race.getTimes(how=how)
    
    for i, row in y.iterrows():
        
        data = {'x': list(range(1, 1+len(row))), 'y': row, 'name': names[i]}
        lines.append(data)
        
    layout = {'title': info, 
              'xaxis': {'dtick': 1, 'title': 'Lap Number'},
              'yaxis': {'title': 'Lap Time (Seconds)'}
              }
    graph = dcc.Graph(id='example', figure={'data': lines, 'layout': layout})

    return graph

app = dash.Dash()
app.config['suppress_callback_exceptions']=True

def initViz(dashApp):
    raceMaps = writeAndLoadRaces(False)

    # children
    graph = html.Div(id='graph')
    dropdownRaces = dcc.Dropdown(id='dropdownRaces', options=raceMaps)
    dropdownCumulative = dcc.Dropdown(id='dropdownCumulative', 
                            options=[{'label': 'Cumulative', 'value': 'cumulative'}, 
                                     {'label': 'Split', 'value': 'splits'},
                                     {'label': 'Split Difference', 'value': 'splits-difference'},
                                     {'label': 'Cumulative Difference', 'value': 'cumulative-difference'}])
    
    children = dropdownRaces, dropdownCumulative, graph 
    dashApp.layout = html.Div(children=children)

@app.callback(Output('graph', 'children'),
              [Input('dropdownRaces', 'value'), Input('dropdownCumulative', 'value')])
def updateGraph(race, cumu):
    if race is not None and cumu is not None:
        return buildGraph(race, cumu)

if __name__ == '__main__':
    initViz(app)
    app.run_server(debug=True)

