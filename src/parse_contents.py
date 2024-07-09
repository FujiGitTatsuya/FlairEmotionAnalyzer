from dash import html, dash_table
import base64
import pandas as pd
import io
import configparser

def parse_csv(contents, filename):
    content_type, content_string = contents.split(',')
    decoded = base64.b64decode(content_string)
    try:
        if 'csv' in filename:
            df = pd.read_csv(io.StringIO(decoded.decode('utf-8')))
        else:
            return html.Div([
                'Unsupported file format. Please upload a CSV file.'
            ]), None
    except Exception as e:
        return html.Div([
            'There was an error processing this file.'
        ]), None

    return html.Div([
        html.H5(filename),
        dash_table.DataTable(
            data=df.to_dict('records'),
            columns=[{'name': i, 'id': i} for i in df.columns],
            page_size=10
        )
    ]), df

def parse_config(contents, filename):
    content_type, content_string = contents.split(',')
    decoded = base64.b64decode(content_string)
    try:
        if 'ini' in filename:
            config = configparser.ConfigParser()
            # config.read(filename, encoding = 'utf-8')
            config.read_string(decoded.decode('utf-8'))
            type(config)

            list_of_stimulation_number = eval(config.get("STIMULATION", "LIST_OF_STIMULATION_NUMBER"))
            list_of_rest_number = eval(config.get("REST", "LIST_OF_REST_NUMBER"))
            period_of_emotion_label = eval(config.get("PERIOD", "PERIOD_OF_EMOTION_LABEL"))
        else:
            return html.Div([
                'Unsupported file format. Please upload a INI file.'
            ]), None
    except Exception as e:
        return html.Div([
            'There was an error processing this file.'
        ]), None

    return html.Div([
        'List of stimulation number: {0}, List of rest number: {1}, Period of emotion label: {2}'.format(
            list_of_stimulation_number, list_of_rest_number, period_of_emotion_label
        )
    ]), list_of_stimulation_number, list_of_rest_number, period_of_emotion_label