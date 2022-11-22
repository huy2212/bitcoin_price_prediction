import dash
import dash_bootstrap_components as dbc
import webbrowser
import os
import data_collection
from dash import html, dcc
from dash.dependencies import Input, Output
from threading import Timer
from visualization import trend_plot, box_plot, prediction_plot

#Load the data
raw_data = data_collection.get_raw_data()
df = data_collection.data_processing(raw_data)
past_df = df

#Create a dash application
app = dash.Dash(__name__, external_stylesheets=[dbc.themes.CERULEAN])

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
                                	dbc.Row(
                                        [dbc.Col(
                                            dbc.Card(
                                                dcc.Graph(id='trend_plot',figure= trend_plot(past_data= df))
                                            )
                                        ),
                                        dbc.Col(
                                            dbc.Card(
                                                dcc.Graph(id= 'box_plot', figure= box_plot(past_data= df))
                                            )
                                        )
                                        ]),
                                	html.Br(),
                                    # dcc.D
                                    html.H3('Choose time step:',
                                    style= {'textAlign':'center', 
                                            'color':'#503D36', 
                                            'font-size':'50'}),
                                    html.H6('Time step is the number of previous days used to predict the current day(default 12)',
                                    style= {'textAlign':'center', 
                                            'color':'#503D36', 
                                            'font-size':'50'}),
                                    dcc.Slider(id= 'time_step_slider',
                                            min= 1, max=30, step= 1,
                                            value= 12
                                            ),
                                	dbc.Row(dbc.Card(dbc.CardBody(dcc.Graph(id= "prediction_chart")))),
                                    dcc.RadioItems([
                                            {'label': 'Choose number of days to display:', 'value': 180, 'disabled': True},
                                            {'label': 'Show valid and future', 'value': 89},
                                            {'label': 'Show future only', 'value': 14},
                                            {'label': 'Show all', 'value': 365 + 14}
                                            ],
                                        labelStyle= {"max-width": "3100px", "width": "25%"},
                                        id= "num_day_show"
                                        )
                                	],
                           style= dict(CONTENT_STYLE, justifyContent='center')
                           )

@app.callback(
    [Output(component_id= "prediction_chart", component_property= "figure"),
     Input(component_id= 'num_day_show', component_property= 'value'),
     Input(component_id= "time_step_slider", component_property= 'value')]
)

def display_pred_chart(num_day, time_step):
    return prediction_plot(time_step= time_step, num_day_shown= num_day, data= df)
                  
def open_browser():
    if not os.environ.get("WERKZEUG_RUN_MAIN"):
        webbrowser.open_new('http://127.0.0.1:8050/')

# Run the app
if __name__ == '__main__':
    Timer(1, open_browser).start()
    app.run_server(debug=True)