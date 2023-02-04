import dash
import dash_bootstrap_components as dbc
# import webbrowser
from assets import data_collection
from dash import html, dcc
from dash.dependencies import Input, Output
from assets.visualization import trend_plot, box_plot, prediction_plot, acf_pacf_plot

#Load the data
raw_data = data_collection.get_raw_data()
df = data_collection.data_processing(raw_data)
past_df = df

#Create a dash application
app = dash.Dash(__name__, external_stylesheets=[dbc.themes.CERULEAN])
server = app.server

#Create app layout
CONTENT_STYLE = {
    "padding": "2rem 1rem",
    'background-color' : '#f0f3f7'
}

app.layout = dbc.Container(children=[html.H1('Bitcoin Price Dashboard',
                                	style= {'textAlign':'center', 
                                            'color':'#503D36', 
                                            'font-size':'50',
                                            }),
                                    html.Br(),
                                    dcc.Dropdown(options= [
                                            {'label': 'Overall', 'value': 'overall'},
                                            {'label': 'Statistic', 'value': 'statistic'}
                                        ],
                                        value= 'overall',
                                        id= 'overall_or_stats',
                                        ),
                                	dbc.Row(
                                        [dbc.Col(
                                            dbc.Card(
                                                dcc.Graph(id= 'trend_or_acf')
                                            )
                                        ),
                                        dbc.Col(
                                            dbc.Card(
                                                dcc.Graph(id= 'box_or_pacf')
                                            )
                                        )
                                        ]),
                                	html.Br(),
                                    # dcc.D
                                    html.H3('Choose time step:',
                                    style= {'textAlign':'center', 
                                            'color':'#503D36', 
                                            'font-size':'50'}),
                                    html.H6('Time step is the number of previous days used to predict the current day(default 8)',
                                    style= {'textAlign':'center', 
                                            'color':'#503D36', 
                                            'font-size':'50'}),
                                    dcc.Slider(id= 'time_step_slider',
                                            min= 1, max= 15, step= 1,
                                            value= 8
                                            ),
                                	dbc.Row(dbc.Card(dbc.CardBody(dcc.Graph(id= "prediction_chart")))),
                                    dcc.RadioItems([
                                            {'label': 'Choose number of days to display:', 'value': 180, 'disabled': True},
                                            {'label': 'Show valid and future', 'value': 73 + 15},
                                            {'label': 'Show future only', 'value': 15},
                                            {'label': 'Show all', 'value': 365 + 15}
                                            ],
                                        labelStyle= {"max-width": "3100px", "width": "25%"},
                                        id= "num_day_show"
                                        )
                                	],
                           style= dict(CONTENT_STYLE, justifyContent='center')
                           )
                           
@app.callback(
    [Output(component_id= 'trend_or_acf', component_property= 'figure'),
    Output(component_id= 'box_or_pacf', component_property= 'figure'),
    Input(component_id= 'overall_or_stats', component_property= 'value')]
)

def overall_stats_plot(value):
    if value == 'overall':
        return trend_plot(past_data= past_df), box_plot(past_data= past_df)
    else:
        return acf_pacf_plot(past_data= past_df, plot_pacf= False), acf_pacf_plot(past_data= past_df, plot_pacf= True) 

@app.callback(
    [Output(component_id= "prediction_chart", component_property= "figure"),
     Input(component_id= 'num_day_show', component_property= 'value'),
     Input(component_id= "time_step_slider", component_property= 'value')]
)

def display_pred_chart(num_day, time_step):
    return prediction_plot(time_step= time_step, num_day_shown= num_day, data= df)


# def open_browser():
#     if not os.environ.get("WERKZEUG_RUN_MAIN"):
#         webbrowser.open_new('http://127.0.0.1:8050/')

# Run the app
if __name__ == '__main__':
    # Timer(0.5, open_browser).start()
    app.run_server(debug= True)
