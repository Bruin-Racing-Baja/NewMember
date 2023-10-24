import pandas as pd
import plotly.express as px
import os
import plotly.offline as pyo

inputFolder = "INPUT"

#Get list of INPUT file names
logName = []
for (dirpath, dirnames, filenames) in os.walk("../INPUT"):
    logName.extend(filenames)
    break
logName.pop(0)

cols = [
    "dt_us",
    "voltage",
    "heartbeat",
    "wheel_rpm",
    "engine_rpm",
    "target_rpm",
    "velocity_command",
    "real_velocity_command",
    "shadow_count",
    "ignore1",
    "ignore2",
    "iq_measured",
    "flushed",
    "wheel_count",
    "engine_count",
    "iq_setpoint",
    "start_us",
    "stop_us",
    "current",
    "axis_error",
    "motor_error",
    "encoder_error",
]

def figures_to_html(figs, filename):
    '''
    Saves a list of plotly figures in an html file.

    Parameters
    figs : list[plotly.graph_objects.Figure]
        List of plotly figures to be saved.
    filename : str
        File name to save in.
    '''
    with open(filename, "w", encoding="utf-8") as f:
        f.write("<html><head></head><body>" + "\n")
        add_js = True
        for fig in figs:
            inner_html = pyo.plot(
                fig, include_plotlyjs=add_js, output_type='div'
            )
            f.write(inner_html)
            add_js = False
        f.write("</body></html>")


def CreateFigure(logname):
    '''
    Creates a plotly figure from a log file.

    Parameters
    logname : str
        Name of the log file to be read.
    '''
    # Create path of input log
    path = "../" + inputFolder + "/" + logname

    # Read log file into pandas dataframe
    df = pd.read_csv(path, skiprows=1, header=None, names=cols)

    #Normalize Data
    df = df[cols]/df[cols].max()
    
    # Convert time to seconds
    df["time(s)"]=df["start_us"]/(10**6)

    # Modify this line: add/remove columns to plot
    fig = px.line(df, x="time(s)", y=cols)

    fig.update_layout(hovermode="x unified", title=logname[:-4])
    return fig

#Create figures and graphs
list_of_figs = []
for log in logName:
    list_of_figs.append(CreateFigure(log))

figures_to_html(list_of_figs, "./Data.html")