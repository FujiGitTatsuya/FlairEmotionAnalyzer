from dash import dcc, html

h = [
    #Page Title & Dropbox Name
    html.H4('EEG & HR analysis'),
    html.P("note: EEG-axis value = (One of the EEG indexes) / (One of the EEG indexes)"),
    html.Div([
        html.Div(
            html.P("EEG Index(numerator) stock:"),
            style={
                'width':'25%',
                'display':'inline-block',
                'margin-right':10
            }
        ),
        html.Div(
            html.P(" "),
            style={
                'width':'10%',
                'display':'inline-block',
                'margin-right':10
            }
        ),
        html.Div(
            html.P("EEG Index(denominator) stock:"),
            style={
                'width':'25%',
                'display':'inline-block',
                'margin-right':10
            }
        )
    ]),
    html.Div([
        html.Div(
            dcc.Dropdown(
                #Drop box of EEG index (numerator)
                id="ticker1",
                options=["theta", "delta", "low_alpha", "high_alpha",
                         "low_beta", "high_beta", "low_gamma", "mid_gamma"],
                value="low_beta",
                clearable=False,
            ),
            style={
                'width':'25%',
                'display':'inline-block',
                'margin-right':10
            }
        ),
        html.Div(
            html.P(" "),
            style={
                'width':'10%',
                'display':'inline-block',
                'margin-right':10
            }
        ),
        html.Div(
            dcc.Dropdown(
                #Drop box of EEG index (denominator)
                id="ticker2",
                options=["theta", "delta", "low_alpha", "high_alpha",
                         "low_beta", "high_beta", "low_gamma", "mid_gamma"],
                value="low_alpha",
                clearable=False,
            ),
            style={
                'width':'25%',
                'display':'inline-block',
                'margin-right':10
            }
        )
    ]),
    html.P("HR stock:"),
    html.Div([
        html.Div(
            dcc.Dropdown(
                #Drop box of HR index
                id="ticker3",
                options=["IBI", "BPM", "SDNN_over_RMSSD", "CVNN", "SDNN", "RMSSD",
                         "pNN10", "pNN20", "pNN30", "pNN40", "pNN50", "LF", "HF",
                         "LF_over_HF"],
                value="RMSSD",
                clearable=False,
            ),
            style={
                'width':'25%',
                'margin-right':10
            }
        )
    ]),
    # html.P("Noise identification method stock:"),
    # html.Div([
    #     html.Div(
    #         dcc.Dropdown(
    #             #Drop box of HR index
    #             id="ticker5",
    #             options=["MAD (Median Absolute Deviation)", "STD (Standard Deviation)"],
    #             value="MAD (Median Absolute Deviation)",
    #             clearable=False,
    #         ),
    #         style={
    #             'width':'25%',
    #             'margin-right':10
    #         }
    #     )
    # ]),
    html.P("Stimulation stock:"),
    html.Div([
        html.Div(
            dcc.Dropdown(
                #Drop box of HR index
                id="ticker_stimu",
                options=["ALL", "Stimu_1", "Stimu_2", "Stimu_3", "Stimu_4", "Stimu_5"],
                value="ALL",
                clearable=False,
            ),
            style={
                'width':'25%',
                'margin-right':10
            }
        )
    ]),
    html.H4(' '),
    dcc.Graph(id="time-series-chart"),
    html.H4(' '),
    dcc.Graph(id="eeg_noise_detail"),
    html.H4(' '),
    dcc.Graph(id="emotion-map"),
    html.P("Emotion Map's Index stock:"),
    dcc.Dropdown(
        id="ticker4",
        options=["Average", "Median"], #average or median
        value="Average",
        clearable=False,
    ),
    html.H4(' '),
    dcc.Link('Go to Upload Page', href='/'),
]