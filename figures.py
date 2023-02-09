import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
import json
import requests
import time

# ============================ FUNCTIONS ===============================
# -------- Update chart layout -------------
def chart_update_layout(figure, x_axis, y_axis):
    figure.update_layout(
        font_size=12,
        #width=450,
        height=300,
        autosize=True,
        paper_bgcolor='rgba(0,0,0,0)',
        plot_bgcolor='rgba(14,17,23,255)',
        margin=dict(l=20, r=20, t=20, b=20),
        hovermode='x unified',
        hoverlabel=dict(
            bgcolor="rgba(100,100,100,0.3)",
            font_size=14,
            #font_family="Rockwell"
        ),

        legend_title_text='',
        legend=dict(
            orientation='h',
            yanchor='top',
            y=1.2,
            xanchor='left',
            x=0.01,
            font=dict(
                size=12,
                color="white"
            ),
            bgcolor="rgba(0,0,0,0)",
            bordercolor="rgba(0,0,0,0)",
            borderwidth=2
        ),
        legend_font=dict(size=12),  # legend location


        xaxis=dict(
            title=x_axis,
            title_font=dict(size=14, color='rgba(170,170,170,0.7)'), #, family='Arial Black'
            gridcolor='rgba(100,100,100,0.3)',
            linecolor='rgba(100,100,100,0.7)',
            tickfont=dict(color='rgba(100,100,100,1)')
            # rangeslider=dict(bgcolor='rgba(0,0,0,0)',yaxis_rangemode='auto')
        ),

        yaxis=dict(
            title=y_axis,
            title_font=dict(size=14, color='rgba(171,171,171,0.7)'), #, family='Arial Black'
            title_standoff=3,
            gridcolor='rgba(100,100,100,0.3)',
            linecolor='rgba(100,100,100,0.7)',
            tickfont=dict(color='rgba(100,100,100,1)')
        )
    )


# ============================ HISTORICAL DAILY TIME SERIES ===============================
## ------ DATA ----------

'''
def filter_pool(x):
    if 'SOL-USDC' in x:
        return ('Known Pool')
    elif 'mSOL-USDC' in x:
        return ('Known pool')
    elif 'BTC-USDC' in x:
        return ('Known pool')
    elif 'stSOL' in x:
        return ('stSOL pools')
    elif 'UST-USDC' in x:
        return ('Known pool')
    elif 'SOL-mSOL' in x:
        return ('Known pool')
    elif 'mSOL-USDT' in x:
        return ('Known pool')
    elif 'KI-USDC' in x:
        return ('Known pool')
    elif 'CAVE-USDC' in x:
        return ('Known pool')
    elif 'ORCA-USDC' in x:
        return ('Known pool')
    elif 'ETH-USDC' in x:
        return ('Known pool')
    elif ('USDC-MEDIA' in x) or ('MEDIA-USDC' in x):
        return ('Known pool')
    elif ('bonk-sol' in x) or ('SOL-BONK' in x):
        return ('Known pool')
    elif ('bonk-usdc' in x) or ('BONK-USDC' in x):
        return ('Known pool')
    elif 'pool' in x:
        return(x)
    else:
        return ('Other pool')
        
'''

def filter_pool_pie(x):
    if 'pool' in x:
        return(x)
    else:
        return ('Other pool')

def filter_pool(x):
    if 'SOL-USDC' in x:
        return ('SOL-USDC Pool')
    elif 'mSOL-USDC' in x:
        return ('mSOL-USDC pool')
    elif 'BTC-USDC' in x:
        return ('BTC-USDC pool')
    elif 'USDC-MEDIA' in x:
        return ('USDC-MEDIA pool')
    elif 'stSOL' in x:
        return ('stSOL pools')
    elif 'UST-USDC' in x:
        return ('UST-USDC pool')
    elif 'SOL-mSOL' in x:
        return ('SOL-mSOL pool')
    elif 'mSOL-USDT' in x:
        return ('mSOL-USDT pool')
    elif 'ORCA-USDC' in x:
        return ('ORCA-USDC pool')
    elif 'ETH-USDC' in x:
        return ('ETH-USDC pool')
    elif ('bonk-sol' in x) or ('SOL-BONK' in x):
        return ('BONK-SOL pool')
    elif ('bonk-usdc' in x) or ('BONK-USDC' in x):
        return ('BONK-USDC pool')
    #elif 'pool' in x:
        #return(x)
    else:
        return ('Other pool')


def filter_bonk(x):
    if ('bonk-sol' in x) or ('SOL-BONK' in x):
        return ('BONK-SOL pool')
    elif ('bonk-usdc' in x) or ('BONK-USDC' in x):
        return ('BONK-USDC pool')
    elif 'SOL-USDC' in x:
        return ('SOL-USDC Pool')
    else:
        return('Other pool')

# ------------------------ LP Daily Position Adj. ------------------------------------
## Data Frame
dailyUrl = 'https://api.flipsidecrypto.com/api/v2/queries/3f52b4f5-28c8-4a43-bfe8-684169762005/data/latest'
df_daily_ttl = pd.read_json(dailyUrl)

df_gains = df_daily_ttl[df_daily_ttl['PLATFORM'].isin(['gains_arbitrum','gains_poly'])]

df_gmx = df_daily_ttl[df_daily_ttl['PLATFORM'] == 'gmx']
df_gmx['volMA7'] = df_gmx['TOTAL_VOLUME'][::-1].rolling(7).mean()[::-1].replace(np.nan, 'None')
df_gmx['userMA7'] = df_gmx['USERS_COUNT'][::-1].rolling(7).mean()[::-1].replace(np.nan, 'None')
df_gmx['trxMA7'] = df_gmx['TX_COUNT'][::-1].rolling(7).mean()[::-1].replace(np.nan, 'None')


# Plots (Gain)
fig_gains_vol = px.bar(df_gains,x='DATE',y='TOTAL_VOLUME',color='PLATFORM'
                           , hover_data={'DATE': True, 'TOTAL_VOLUME': True}
                           ).update_layout(height=350, margin=dict(l=20, r=20, t=20, b=20), yaxis=dict(title='Total Volume'))
fig_gains_user = px.bar(df_gains,x='DATE',y='USERS_COUNT',color='PLATFORM'
                           , hover_data={'DATE': True, 'USERS_COUNT': True}
                           ).update_layout(height=350, margin=dict(l=20, r=20, t=20, b=20), yaxis=dict(title='Total Number of Users'))
fig_gains_trx = px.bar(df_gains,x='DATE',y='TX_COUNT',color='PLATFORM'
                           , hover_data={'DATE': True, 'TX_COUNT': True}
                           ).update_layout(height=350, margin=dict(l=20, r=20, t=20, b=20), yaxis=dict(title='Total Number of Transactions'))

# Plots (GMX)
fig_gmx_vol = px.line(df_gmx, x='DATE', y='volMA7', labels ={'DATE':'Date', 'volMA7':'7-Day MA'}
                ,color_discrete_sequence=['white']
                ,hover_data={'DATE':False,'volMA7':True} )
fig_gmx_vol.add_bar(x=df_gmx['DATE'],y=df_gmx['TOTAL_VOLUME'], name="Total Volume"
                     ,marker_color='rgba(255,171,171,255)')
chart_update_layout(fig_gmx_vol, "", "Total Daily Volume on GMX")


fig_gmx_user = px.line(df_gmx, x='DATE', y='userMA7', labels ={'DATE':'Date', 'userMA7':'7-Day MA'}
                ,color_discrete_sequence=['white']
                ,hover_data={'DATE':False,'userMA7':True} )
fig_gmx_user.add_bar(x=df_gmx['DATE'],y=df_gmx['USERS_COUNT'], name="Total Number of Users"
                     ,marker_color='rgba(255,171,171,255)')
chart_update_layout(fig_gmx_user, "", "Total User Count on GMX")


fig_gmx_trx = px.line(df_gmx, x='DATE', y='trxMA7', labels ={'DATE':'Date', 'trxMA7':'7-Day MA'}
                ,color_discrete_sequence=['white']
                ,hover_data={'DATE':False,'trxMA7':True} )
fig_gmx_trx.add_bar(x=df_gmx['DATE'],y=df_gmx['TX_COUNT'], name="Total Number of Transactions"
                     ,marker_color='rgba(255,171,171,255)')
chart_update_layout(fig_gmx_trx, "", "Total Transaction Count on GMX")


