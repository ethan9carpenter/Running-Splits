from resourceScrapers.flashResults import getAllLinks, getRace
import dash
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output
from resourceScrapers.flashResults.constants import distance as distanceRaces
import os, json
from raceSettingOptions import dropdownSplitOptions  


def writeAndLoadRaces(url, override=False):
    if os.path.exists('links.json') and not override:
        with open('links.json', 'r') as file:
            raceMaps = json.load(file)
    else:
        extensions = getAllLinks(url, True)
        raceMaps = []
        for ext in extensions:
            scr = getRace(url+ext)['raceInfo']
            if any([distance in scr for distance in distanceRaces]):
                raceMaps.append({'label': scr, 'value': url+ext})
        with open('links.json', 'w') as file:
            json.dump(raceMaps, file)
            
    return raceMaps

def buildGraph(sectionLink, how):
    race = getRace(sectionLink)
    raceName = str(race)
    
    names = race.names
    
    lines = []
    y = race.getTimes(how=how)
    
    for row, name in zip(y.iterrows(), names):
        data = {'x': y.columns, 
                'y': row[1], 
                'name': name}
        lines.append(data)
        #print(i, len(names))
        
    layout = {'title': raceName, 
              'xaxis': {'dtick': 1, 'title': 'Lap Number'},
              'yaxis': {'title': how.replace('-', ' ').title()}}
    graph = dcc.Graph(id='example', figure={'data': lines, 'layout': layout})

    return graph

app = dash.Dash()
app.config['suppress_callback_exceptions']=True

def initViz(dashApp, url, overrideData=False):
    raceMaps = writeAndLoadRaces(url, overrideData)

    # graph div
    graph = html.Div(id='graph')
    # dropdowns
    dropdownRaces = dcc.Dropdown(id='dropdownRaces', options=raceMaps)
    dropdownCumulative = dcc.Dropdown(id='dropdownCumulative', options=dropdownSplitOptions)
    
    children = dropdownRaces, dropdownCumulative, graph 
    dashApp.layout = html.Div(children=children)

@app.callback(Output('graph', 'children'),
              [Input('dropdownRaces', 'value'), Input('dropdownCumulative', 'value')])
def updateGraph(race, cumu):
    if race is not None and cumu is not None:
        return buildGraph(race, cumu)

if __name__ == '__main__':
    url = 'http://www.flashresults.com/2017_Meets/Outdoor/06-29_TTSSFO/'
    initViz(app, url)
    app.run_server(debug=True)

