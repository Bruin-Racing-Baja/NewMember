import pandas as pd
import plotly.express as px
import os
import plotly.offline as pyo

inputFolder = "INPUT"
logName = "log_2023-04-14_19-46-54_paige-drive-to-garage-spinout-error.txt"

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
    ----------
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
    path = "../" + inputFolder + "/" + logname
    df = pd.read_csv(path, skiprows=1, header=None, names=cols)
    df["time(s)"]=df["start_us"]/(10**6)
    
    # create graph of 
    fig = px.line(df, x="time(s)", y=["engine_count"])
    fig.update_layout(hovermode="x unified", title=logname[:-4])
    return fig


figure = CreateFigure(logName)
figures_to_html([figure], "./Data.html")