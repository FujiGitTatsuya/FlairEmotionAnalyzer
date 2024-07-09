from dash import Dash, dcc, html, Input, Output, State
import plotly.graph_objects as go
import pandas as pd
from plotly.subplots import make_subplots
import math
import configparser
import io

import html_upload
import html_graph  # Template of HTML
import parse_contents
import em_label_func_ver2  # Function to calculate values for emotion labels
import value_calc
import eeg_noise_median
import data_cleaning
import event_id

##########################################################################################
# config = configparser.ConfigParser()
# config.read('config.ini', encoding = 'utf-8')
# type(config)

# list_of_stimulation_number = eval(config.get("STIMULATION", "LIST_OF_STIMULATION_NUMBER"))
# list_of_rest_number = eval(config.get("REST", "LIST_OF_REST_NUMBER"))
# # Debug
# print("{0}, {1}, {2}".
#       format(list_of_rest_number, type(list_of_rest_number), type(list_of_rest_number[0])))
# period_of_emotion_label = eval(config.get("PERIOD", "PERIOD_OF_EMOTION_LABEL"))
###########################################################################################

yaxis_max_of_ts_eeg = 0  # Maximum value of EEG axis of time series graph
yaxis_max_of_ts_hrv = 0  # Maximum value of HR axis of time series graph
spec_list_of_ts = []  # List of 'specs' for make_subplots in time-series graph
spec_list_of_em = []  # List of 'specs' for make_subplots in emotion map
ts_image_name = ""  # Image name for time series graph
em_image_name = ""  # Image name for emotion-map

graph_height = 300  # Height of plot area for graphs

# Launch the web application
app = Dash(__name__, suppress_callback_exceptions=True)

app.layout = html.Div([
    dcc.Location(id='url', refresh=False),
    html.Div(id='page-content')
])

h_upload = html_upload.h_upload
upload_page_layout = html.Div(h_upload)
h_plot = html_graph.h
plot_page_layout = html.Div(h_plot)

# Rendering page contents
@app.callback(Output('page-content', 'children'),
              Input('url', 'pathname'))
def display_page(pathname):
    if pathname == '/plot':
        return plot_page_layout
    else:
        return upload_page_layout

# Config file upload
@app.callback(
    Output('output-config-upload', 'children'),
    [Input('upload-config', 'filename')],
    [State('upload-config', 'contents')]
)
def update_output(filename, contents):
    if contents is None:
        return [html.Div(['No file uploaded.'])]
    children, ls, lr, pl = parse_contents.parse_config(contents, filename)
    if (ls is not None) and (lr is not None) and (pl is not None):
        global list_of_stimulation_number
        list_of_stimulation_number = ls

        global list_of_rest_number
        list_of_rest_number = lr

        global period_of_emotion_label
        period_of_emotion_label = pl

        return children
    else:
        return children

# File upload
@app.callback(
    Output('output-data-upload', 'children'),
    Output('go-to-plot', 'style'),
    [Input('upload-data', 'filename')],
    [State('upload-data', 'contents')]
)
def update_output(filename, contents):
    if contents is None:
        return [html.Div(['No file uploaded.'])], {'display': 'none'}
    children, df = parse_contents.parse_csv(contents, filename)
    if df is not None:
        global uploaded_df
        uploaded_df = data_cleaning.data_cleaning(df)

        global subject_name
        subject_name = str(filename).split('.')[0]

        return children, {'display': 'block'}
    else:
        return children, {'display': 'none'}

# Button click action
@app.callback(
    Output('url', 'pathname'),
    Input('go-to-plot', 'n_clicks')
)
def go_to_plot(n_clicks):
    if n_clicks:
        return '/plot'
    return '/'

# Time-series graph
@app.callback(
    Output("time-series-chart", "figure"),
    Input("ticker1", "value"),
    Input("ticker2", "value"),
    Input("ticker3", "value"),
    Input("ticker_stimu", "value"),
    Input('url', 'pathname'))
def display_time_series(ticker1, ticker2, ticker3, ticker_stimu, pathname):

    if pathname == '/plot' and uploaded_df is not None:

        fig = make_subplots(rows = 1, 
                            cols = 1,
                            subplot_titles = subject_name,
                            specs = [[{"secondary_y": True}]]
                            )
        #fig = go.Figure()

        if ticker_stimu != "ALL":
            specific_stimu = str(ticker_stimu).split("_")[1]
        else:
            specific_stimu = "ALL"

        start_index_of_stimulation = 0

        if (ticker1 == ticker2):
            eeg_data_after_cleaning = eeg_noise_median.noise_median(uploaded_df, ticker1, ticker1)
            yaxis_max_of_ts_eeg = eeg_data_after_cleaning['eeg'].max()
        else:
            eeg_data_after_cleaning = eeg_noise_median.noise_median(uploaded_df, ticker1, ticker2)
            yaxis_max_of_ts_eeg = eeg_data_after_cleaning['eeg'].max()

        yaxis_max_of_ts_hrv = uploaded_df[ticker3].max()

        s_flag = 0
        if str(specific_stimu) != "ALL":
            for i, s in enumerate(uploaded_df['stimu_num']):
                if str(s) == str(specific_stimu):
                    if s_flag == 0:
                        start_index_of_stimulation = i
                        s_flag = 1

        # Edit timestamp
        df_t = []
        index_x = []
        for t in uploaded_df['timestamp']:
            t_s = t.split('_')
            df_t.append(t_s[1])

        for i, time_x in enumerate(uploaded_df['timestamp']):
            index_x.append(i)

        # print(index_x)
        # list_for_indexes_of_stimulaton = []
        index_of_stimulation_label = []
        list_for_indexes_of_stimulation_label = []
        # w_i = 0
        for i in range(len(list_of_stimulation_number)):
            list_for_indexes_of_stimulaton = []

            for j, row in uploaded_df.iterrows():
                if (row['stimu_num'] == list_of_stimulation_number[i]):
                    list_for_indexes_of_stimulaton.append(index_x[j])

            # for t in st_i:
            #     w_i = w_i+1
            that_index = int((len(list_for_indexes_of_stimulaton))/2)
            index_of_stimulation_label = list_for_indexes_of_stimulaton[that_index]
            list_for_indexes_of_stimulation_label.append(index_of_stimulation_label)
        # print(list_for_indexes_of_stimulation_label)

        st_temp = 99
        st_series = []
        for st_num in uploaded_df['stimu_num']:
            if st_num in list_of_stimulation_number:
                if st_num != st_temp:
                    st_series.append(st_num)
                st_temp = st_num

        name_s = []
        tx_new = []
        for i in st_series:
            name_s.append(("刺激" + str(i+1)))
            tx_new.append(list_for_indexes_of_stimulation_label[list_of_stimulation_number.index(i)])

        # Create stimulus labels
        name = []
        for i in range(len(list_of_stimulation_number)):
            name.append(("刺激" + str(i+1)))

        index_temp = []
        if ticker_stimu != "ALL":
            for i in range(len(index_x)):
                index_temp.append(index_x[i] - start_index_of_stimulation)

        if ticker_stimu != "ALL":
            for i in range(len(index_x)):
                index_x[i] = index_x[i] - start_index_of_stimulation

        # Time-series graph of EEG
        if (ticker1 == ticker2):  # When using only one EEG indicators
            fig.add_trace(go.Scatter(x=index_x, y=eeg_data_after_cleaning['eeg'], name=ticker1, marker={'color': '#0000ff'}), row=1, col=1)
            fig.update_yaxes(title=ticker1, range=[0, yaxis_max_of_ts_eeg*1.05], row=1, col=1)
            max_t = yaxis_max_of_ts_eeg*1.03
        else:  # When using two EEG indicators
            fig.add_trace(go.Scatter(x=index_x, y=eeg_data_after_cleaning['eeg'], name=ticker1 + '/' + ticker2, marker={'color': '#0000ff'}), row=1, col=1)
            fig.update_yaxes(title=ticker1 + "/" + ticker2,
                            range=[0, yaxis_max_of_ts_eeg*1.05], row=1, col=1)
            max_t = yaxis_max_of_ts_eeg*1.03

        event_list = event_id.event_identify(uploaded_df)
        # print(event_list)

        fig.add_trace(go.Scatter(x=index_x, y=uploaded_df[ticker3], name=ticker3, marker={'color': '#ff0000'}),
                    secondary_y=True, row=1, col=1)  # Time-series graph of HR
        
        fig.add_trace(go.Bar(x=index_x, y=event_list*(yaxis_max_of_ts_hrv/event_list),
                    name='event', width=1.0, marker_color="green"), secondary_y=True, row=1, col=1)  # Plot event

        print(len(index_x))
        # print(len(index_temp))
        # print(index_temp)
        print(len(event_list))

        # Axis labels
        fig.update_yaxes(title=ticker3, secondary_y=True, 
                        range=[0, yaxis_max_of_ts_hrv*1.05], row=1, col=1)

        # Create emotion labels for scenes and insert them into time-series-graph
        count = 0
        c0 = 0
        data_start = 0
        eeg_sum = 0.0
        hr_sum = 0.0
        label_name = []
        stimu_eeg_list = []
        start = None
        end = None
        stimu_data = []

        rest_hr_list = []
        rest_eeg_list = []
        rest_hr_list, rest_eeg_list = value_calc.calc_rest_average_list(uploaded_df, eeg_data_after_cleaning['eeg'], ticker3, list_of_rest_number)

        start_list = []
        end_list = []
        count_s = 0

        for num_stimu in list_of_stimulation_number:
            for i_q, num_q in zip(index_x, uploaded_df['stimu_num']):
                if num_q == num_stimu:
                    end_index = i_q
                    count_s = count_s + 1
            start_list.append((end_index + 1) - count_s)
            end_list.append(end_index)
            count_s = 0

        for stimu_num in list_of_stimulation_number:

            eeg_ave = rest_eeg_list[list_of_stimulation_number.index(stimu_num)]
            hr_ave = rest_hr_list[list_of_stimulation_number.index(stimu_num)]
            print(eeg_ave)

            for h, a, time, e, s_num in zip(uploaded_df[ticker3], eeg_data_after_cleaning['eeg'], index_x, event_list, uploaded_df['stimu_num']):

                if s_num == stimu_num:

                    if start == None:
                        start = time

                    eeg_sum, hr_sum, start, end, count, c0, data_start = em_label_func_ver2.calc_emotionvalue_alpha(h, a, time, c0,
                                                                                                                    eeg_sum, hr_sum,
                                                                                                                    start, end,
                                                                                                                    count, data_start, period_of_emotion_label,
                                                                                                                    end_list[list_of_stimulation_number.index(stimu_num)])

                    if count == period_of_emotion_label:
                        # stimu_eeg_list.append(eeg_sum)
                        n, fc, eeg_sum, hr_sum = em_label_func_ver2.create_emotionlabels(
                            eeg_sum, hr_sum, eeg_ave, hr_ave, c0)

                        line = {"width": 0, }
                        fig.add_trace(go.Scatter(
                            name=n,
                            x=[start, start, end, end],
                            y=[0, yaxis_max_of_ts_hrv*1.05, yaxis_max_of_ts_hrv*1.05, 0],
                            opacity=0.1,
                            fill="toself",
                            fillcolor=fc,
                            mode="lines",
                            line=line,
                            showlegend=False,
                        ), secondary_y=True, row=1, col=1)

                        fig.add_annotation(
                            xref='x',
                            yref='y',
                            x=int((start_list[list_of_stimulation_number.index(stimu_num)] + end_list[list_of_stimulation_number.index(stimu_num)])/2),
                            y=max_t,
                            text="刺激" + str(list_of_stimulation_number.index(stimu_num) + 1),
                            showarrow=False,
                            font=dict(size=11),
                            bgcolor='rgb(243, 243, 243)',
                            row=1, col=1
                        )

                        # print(str(start) + ", " + str(end))

                        count = 0
                        c0 = 0
                        start = None

                        label_name.append(n)

            print(label_name)
            label_name = []

        fig.update_xaxes(title="timestamp", showgrid=False, row=1, col=1)

        # Title of the time-series graph, etc.
        if (ticker1 == ticker2):
            fig.update_layout(
                title="Time series chart  " + "<br>"
                "脳波指標：" + ticker1 + ", "
                "心拍指標：" + ticker3,
            )
        else:
            fig.update_layout(
                title="Time series chart  " + "<br>"
                "脳波指標：" + ticker1 + "/" + ticker2 + ", "
                "心拍指標：" + ticker3,
            )

        fig.update_layout(
            paper_bgcolor='rgb(243, 243, 243)',
            plot_bgcolor='rgb(243, 243, 243)',
            height=graph_height,
        )

        return fig
    return {}

# eeg_noise_detail
@app.callback(
    Output("eeg_noise_detail", "figure"),
    Input("ticker1", "value"),
    Input("ticker2", "value"),
    Input("ticker3", "value"),
    Input('url', 'pathname'))
def display_eeg_noise(ticker1, ticker2, ticker3, pathname):

    if pathname == '/plot' and uploaded_df is not None:

        fig = make_subplots(rows = 1, 
                            cols = 1,
                            subplot_titles = subject_name,
                            specs = [[{"secondary_y": True}]]
                            )

        yaxis_max_of_ts_eeg = 0

        if (ticker1 == ticker2):
            yaxis_max_of_ts_eeg = uploaded_df[ticker1].max()
        else:
            yaxis_max_of_ts_eeg = (uploaded_df[ticker1]/uploaded_df[ticker2]).max()

        index_x = []
        for i, time_x in enumerate(uploaded_df['timestamp']):
            index_x.append(i)

        # Time-series graph of EEG
        if (ticker1 == ticker2):  # When using only one EEG indicators
            fig.add_trace(go.Scatter(x=index_x, y=uploaded_df[ticker1], name=ticker1), row=1, col=1)
            fig.update_yaxes(title=ticker1, 
                            range=[0, yaxis_max_of_ts_eeg*1.05], row=1, col=1)
            max_t = yaxis_max_of_ts_eeg*1.03
        else:  # When using two EEG indicators
            fig.add_trace(go.Scatter(x=index_x, y=(uploaded_df[ticker1]/uploaded_df[ticker2]), name=ticker1 + '/' + ticker2), row=1, col=1)
            fig.update_yaxes(title=ticker1 + "/" + ticker2,
                            range=[0, yaxis_max_of_ts_eeg*1.05], row=1, col=1)
            max_t = yaxis_max_of_ts_eeg*1.03

        x_disc = []
        y_disc = []
        x_disc, y_disc = eeg_noise_median.noise_disc(uploaded_df, ticker1, ticker2)
        fig.add_trace(go.Scatter(x=x_disc, y=y_disc, mode='markers', name='noise'), row=1, col=1)

        fig.update_xaxes(title="timestamp", showgrid=False, row=1, col=1)

        # Title of the time-series graph, etc.
        if (ticker1 == ticker2):
            fig.update_layout(
                title="Noise identification for EEG  " + "<br>"
                "脳波指標：" + ticker1,
            )
        else:
            fig.update_layout(
                title="Noise identification for EEG  " + "<br>"
                "脳波指標：" + ticker1 + "/" + ticker2,
            )

        fig.update_layout(
            paper_bgcolor='rgb(243, 243, 243)',
            plot_bgcolor='rgb(243, 243, 243)',
            height=graph_height,
        )

        return fig
    return {}

# emotion-map


@app.callback(
    Output("emotion-map", "figure"),
    Input("ticker1", "value"),
    Input("ticker2", "value"),
    Input("ticker3", "value"),
    Input("ticker4", "value"),
    Input('url', 'pathname'))
def display_emotion_map(ticker1, ticker2, ticker3, ticker4, pathname):

    if pathname == '/plot' and uploaded_df is not None:

        fig = make_subplots(rows = 1, 
                            cols = 1,
                            subplot_titles = subject_name,
                            specs = [[{}]]
                            )

        eeg_list = []

        if (ticker1 == ticker2):
            eeg_data_after_cleaning = eeg_noise_median.noise_median(uploaded_df, ticker1, ticker1)
            yaxis_max_of_ts_eeg = eeg_data_after_cleaning['eeg'].max()
            #eeg_list.append(y_eeg['eeg'])
        else:
            eeg_data_after_cleaning = eeg_noise_median.noise_median(uploaded_df, ticker1, ticker2)
            yaxis_max_of_ts_eeg = eeg_data_after_cleaning['eeg'].max()
            #eeg_list.append(y_eeg['eeg'])

        stml1_hr = 0
        stml1_eeg = 0
        # c0 = 0
        # c1 = 0
        x_data = []
        y_data = []
        stml_hr_avr = []
        stml_eeg_avr = []
        stml_hr_med = []
        stml_eeg_med = []
        rs_hr = []
        rs_eeg = []

        end_list = []
        for num_stimu in list_of_stimulation_number:
            for i_q, num_q in enumerate(uploaded_df['stimu_num']):
                if num_q == num_stimu:
                    end_index = i_q
            end_list.append(end_index)

        # Calculate values required for normalization
        if (ticker4 == "Average"):  # When normalizing by the mean
            # rest_hr, rest_eeg = value_calc.calc_rest_average_clean(df,eeg_list[index],ticker3)
            rest_hr_list, rest_eeg_list = value_calc.calc_rest_average_list(
                uploaded_df, eeg_data_after_cleaning['eeg'], ticker3, list_of_rest_number)

            # x_data, y_data, stml_hr_avr, stml_eeg_avr = value_calc.calc_stml_average_clean(df,eeg_list[index],case_size,ticker3,rest_hr,rest_eeg,
            #                                                                          stimu_n,x_data,y_data,stml_hr_avr,stml_eeg_avr,stml1_hr,stml1_eeg)
            x_data, y_data, stml_hr_avr, stml_eeg_avr = value_calc.calc_stml_average_list(uploaded_df, eeg_data_after_cleaning['eeg'], len(list_of_stimulation_number), ticker3, rest_hr_list, rest_eeg_list,
                                                                                        list_of_stimulation_number, x_data, y_data, stml_hr_avr, stml_eeg_avr, stml1_hr, stml1_eeg)

            # Save each calculated average
            case = []
            m_size = []
            name = []
            for i, stimu_num in enumerate(uploaded_df['stimu_num']):
                if i in end_list:
                    s_n = list_of_stimulation_number[end_list.index(i)]
                    case.append(("刺激" + str(s_n) + "<br>" + "<br>" +
                                "刺激時心拍平均：" + str(math.floor(stml_hr_avr[end_list.index(i)]*1000)/1000) + "<br>" +
                                    "刺激時脳波平均：" + str(math.floor(stml_eeg_avr[end_list.index(i)]*1000)/1000) + "<br>" + "<br>" +
                                    "安静時心拍平均：" + str(math.floor(rest_hr_list[end_list.index(i)]*1000)/1000) + "<br>" +
                                    "安静時脳波平均：" + str(math.floor(rest_eeg_list[end_list.index(i)]*1000)/1000)
                                ))
                    m_size.append(15)
                    name.append(("刺激" + str(s_n)))

        elif (ticker4 == "Median"):  # When normalizing by median
            # rest_hr, rest_eeg = value_calc.calc_rest_median_clean(df,eeg_list[index],ticker3,rs_hr,rs_eeg)
            rest_hr_list, rest_eeg_list = value_calc.calc_rest_median_list(
                uploaded_df, eeg_data_after_cleaning['eeg'], ticker3, rs_hr, rs_eeg, list_of_rest_number)

            x_data, y_data, stml_hr_med, stml_eeg_med = value_calc.calc_stml_median_list(uploaded_df, eeg_data_after_cleaning['eeg'], len(list_of_stimulation_number), ticker3, rest_hr_list, rest_eeg_list,
                                                                                        list_of_stimulation_number, x_data, y_data, stml_hr_med, stml_eeg_med)

            # Save each calculated median
            case = []
            m_size = []
            name = []
            for i, stimu_num in enumerate(uploaded_df['stimu_num']):
                if i in end_list:
                    s_n = list_of_stimulation_number[end_list.index(i)]
                    case.append(("刺激" + str(s_n) + "<br>" + "<br>" +
                                "刺激時心拍中央値：" + str(math.floor(stml_hr_med[end_list.index(i)]*1000)/1000) + "<br>" +
                                "刺激時脳波中央値：" + str(math.floor(stml_eeg_med[end_list.index(i)]*1000)/1000) + "<br>" + "<br>" +
                                "安静時心拍中央値：" + str(math.floor(rest_hr_list[end_list.index(i)]*1000)/1000) + "<br>" +
                                "安静時脳波中央値：" + str(math.floor(rest_eeg_list[end_list.index(i)]*1000)/1000)
                                ))
                    m_size.append(15)
                    name.append(("刺激" + str(s_n)))

        # Preparation for setting the proper plot size for the emotion-map
        max_x = max(x_data)
        min_x = min(x_data)
        max_y = max(y_data)
        min_y = min(y_data)

        if(max_x < 0):
            max_x = max_x * (-1)
        if(min_x < 0):
            min_x = min_x * (-1)
        if(max_y < 0):
            max_y = max_y * (-1)
        if(min_y < 0):
            min_y = min_y * (-1)

        if(max_x > min_x):
            xr = max_x
        else:
            xr = min_x

        if(max_y > min_y):
            yr = max_y
        else:
            yr = min_y

        # Display of "happy, tense, sorrow, and relax" area
        x_em = [[0, 0, xr*1.1, xr*1.1],
                [0, 0, xr*1.1*(-1), xr*1.1*(-1)],
                [0, 0, xr*1.1*(-1), xr*1.1*(-1)],
                [0, 0, xr*1.1, xr*1.1]]

        y_em = [[0, yr*1.1, yr*1.1, 0],
                [0, yr*1.1, yr*1.1, 0],
                [0, yr*1.1*(-1), yr*1.1*(-1), 0],
                [0, yr*1.1*(-1), yr*1.1*(-1), 0]]

        n_em = ["Happy", "Tense", "Sad", "Relax"]
        c_em = ["rgba(255, 255, 0, 255)", "rgba(255, 0, 0, 255)",
                "rgba(0, 0, 255, 255)", "rgba(0, 255, 0, 255)"]

        line = {"width": 0, }

        for i in range(4):
            fig.add_trace(go.Scatter(
                name=n_em[i],
                x=x_em[i],
                y=y_em[i],
                opacity=0.1,
                fill="toself",
                fillcolor=c_em[i],
                mode="lines",
                line=line,
                showlegend=False,
            ), row=1, col=1)

        fig.add_hline(y=0, row=1, col=1)
        fig.add_vline(x=0, row=1, col=1)

        # Plot each stimulus on a map
        data = pd.DataFrame({
            'X': x_data,
            'Y': y_data,
            'name': name
        })

        stimu_color = ["#ff0000", "#0000ff", "#008000", "#ffff00", "#00ffff",
                        "#ff00ff", "#00ff00", "#000080", "#8a2be2", "#ffa500"]

        for i in range(len(list_of_stimulation_number)):
            fig.add_trace(go.Scatter(
                x=data['X'][data['name'] == name[i]],
                y=data['Y'][data['name'] == name[i]],
                mode='markers',
                name=name[i],
                text=case[i],
                marker_line_color='black',
                marker=dict(
                    size=m_size,
                    showscale=False,
                    color=stimu_color[i]
                )
            ), row=1, col=1)

        if (ticker1 == ticker2):
            fig.update_xaxes(range=[min(x_data)*1.1, max(x_data)*1.1],
                                row=1, col=1)
            fig.update_yaxes(title=ticker1, range=[min(y_data)*1.1, max(y_data)*1.1],
                                row=1, col=1)
        else:
            fig.update_xaxes(range=[xr*1.1*(-1), xr*1.1],
                                row=1, col=1)
            fig.update_yaxes(title=ticker1 + "/" + ticker2, range=[yr*1.1*(-1), yr*1.1],
                                row=1, col=1)

        fig.update_xaxes(title=ticker3, showgrid=False, row=1, col=1)

        # Title of the emotion-map, etc.
        if (ticker1 == ticker2):
            fig.update_layout(
                title="Emotion Map" + "<br>"
                "脳波指標：" + ticker1 + ", "
                "心拍指標：" + ticker3,
            )
        else:
            fig.update_layout(
                title="Emotion Map" + "<br>" +
                "脳波指標：" + ticker1 + "/" + ticker2 + ", "
                "心拍指標：" + ticker3,
            )

        fig.update_layout(
            paper_bgcolor='rgb(243, 243, 243)',
            plot_bgcolor='rgb(243, 243, 243)',
            height=graph_height,
        )

        return fig
    return {}

if __name__ == '__main__':
    uploaded_df = None
    subject_name = None
    app.run_server(debug=True)
