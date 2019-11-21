import base64
import calendar

import pandas as pd
from IPython.display import SVG, display, HTML


def render(chart=None, filename=None):
    if not any([chart, filename]):
        raise ValueError('Arguments missing')
    if chart:
        b64 = base64.b64encode(chart.render())
    else:
        b64 = base64.b64encode(open(filename, 'rb').read())
    

    src = 'data:image/svg+xml;charset=utf-8;base64,' + b64.decode('utf-8')
    return HTML('<embed src={}></embed>'.format(src))


def read_hn_file(filepath, drop_last_month=True):
    df = pd.read_csv(
        filepath, index_col='Object ID',
        parse_dates=['Created At'],
        dtype={
            'Post Type': 'category'
        })
    
    df['Created At Eastern'] = df['Created At'].dt.tz_localize('UTC').dt.tz_convert('US/Eastern')
    df['Rounded Month'] = df['Created At Eastern'].dt.to_period('m')
    
    day_conversion_table = {k: calendar.day_name[k] for k in range(7)}
    df['Day of Week'] = df['Created At Eastern'].dt.dayofweek.replace(day_conversion_table)
    df['Hour of the Day'] = df['Created At Eastern'].dt.hour
    
    if drop_last_month:
        df.drop(df.loc[df['Rounded Month'] == df['Rounded Month'].iloc[-1]].index, inplace=True)
    return df