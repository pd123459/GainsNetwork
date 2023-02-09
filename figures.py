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
UniLP = 'https://node-api.flipsidecrypto.com/api/v2/queries/65d08749-498e-4406-aa54-62ab91b210b5/data/latest'
df_unilp_ttl = pd.read_json(UniLP)
df_unilp_ttl['AVG_LP_ADJ_MA'] = df_unilp_ttl['AVG_LP_ADJ'][::-1].rolling(7).mean()[::-1].replace(np.nan, 'None')

OrcaLPTtl = 'https://node-api.flipsidecrypto.com/api/v2/queries/2ec0ad61-7b05-4a13-82a0-423d39dc0e6f/data/latest'
df_orcalp_ttl = pd.read_json(OrcaLPTtl)
df_orcalp_ttl['AVG_LP_ADJ_MA'] = df_orcalp_ttl['AVG_PRICERANGE_ADJ'][::-1].rolling(7).mean()[::-1].replace(np.nan, 'None')

## ------ PLOTS ----------
# --> LP avg adj (UNI)
fig_lp_adj_uni = px.line(df_unilp_ttl, x='DT', y='AVG_LP_ADJ_MA', labels ={'DT':'Date', 'AVG_LP_ADJ_MA':'7-Day MA'}
                ,color_discrete_sequence=['white']
                ,hover_data={'DT':False,'AVG_LP_ADJ_MA':True} )
fig_lp_adj_uni.add_bar(x=df_unilp_ttl['DT'],y=df_unilp_ttl['AVG_LP_ADJ'], name="# LP Position Adjustment / day"
                     ,marker_color='rgba(255,171,171,255)')
chart_update_layout(fig_lp_adj_uni, "", "Daily LP Position Adjustment on Uniswap")

#--> LP avg adj (ORCA)
fig_lp_adj_orca = px.line(df_orcalp_ttl, x='DT', y='AVG_LP_ADJ_MA', labels ={'DT':'Date', 'AVG_LP_ADJ_MA':'7-Day MA'}
                ,color_discrete_sequence=['white']
                ,hover_data={'DT':False,'AVG_LP_ADJ_MA':True} )
fig_lp_adj_orca.add_bar(x=df_orcalp_ttl['DT'],y=df_orcalp_ttl['AVG_PRICERANGE_ADJ'], name="# LP Position Adjustment / day"
                     ,marker_color='rgba(131,201,255,255)')
chart_update_layout(fig_lp_adj_orca, "", "Daily LP Position Adjustment on Orca")


#------------------ ORCA LP Stats By Pool -----------------------------------------
## Data Frame
OrcaLPSplit = 'https://node-api.flipsidecrypto.com/api/v2/queries/d8efa2d6-ba9c-4610-ae0b-bf2bcbe80b7c/data/latest'
df_orcalp_splitpool = pd.read_json(OrcaLPSplit)
df_orcalp_splitpool['Pool Name'] = df_orcalp_splitpool['POOL_ADDRESS_NAME'].apply(filter_pool)

bonk_index = df_orcalp_splitpool.index[df_orcalp_splitpool['DT'] == '2022-12-15 00:00:00.000'].tolist()
df_orcalp_bonk = df_orcalp_splitpool.loc[:bonk_index[-1]]
df_orcalp_bonk['Pool Name Type'] = df_orcalp_bonk['POOL_ADDRESS_NAME'].apply(filter_bonk)

df_orcalp_apr = df_orcalp_splitpool[df_orcalp_splitpool['DT'].str.contains("2022-04-12")]
df_orcalp_apr['Pool Name'] = df_orcalp_apr['POOL_ADDRESS_NAME'].apply(filter_pool_pie)
df_orcalp_jul = df_orcalp_splitpool[df_orcalp_splitpool['DT'].str.contains("2022-07-18")]
df_orcalp_jul['Pool Name'] = df_orcalp_jul['POOL_ADDRESS_NAME'].apply(filter_pool_pie)
df_orcalp_nov = df_orcalp_splitpool[df_orcalp_splitpool['DT'].str.contains("2022-11-18")]
df_orcalp_nov['Pool Name'] = df_orcalp_nov['POOL_ADDRESS_NAME'].apply(filter_pool_pie)
df_orcalp_jan = df_orcalp_splitpool[df_orcalp_splitpool['DT'].str.contains("2023-01-05")]
df_orcalp_jan['Pool Name'] = df_orcalp_jan['POOL_ADDRESS_NAME'].apply(filter_pool_pie)

#--> Active LP (Orca)
fig_lp_num_pool = px.bar(df_orcalp_splitpool,x='DT',y='NUM_USERS',color='Pool Name'
                           , hover_data={'DT': True, 'NUM_USERS': True}
                           ).update_layout(height=350, margin=dict(l=20, r=20, t=20, b=20), yaxis=dict(title='Number of Active LPs'))
fig_lp_pool_bonk = px.bar(df_orcalp_bonk,x='DT',y='NUM_USERS',color='Pool Name Type'
                          , hover_data={'DT': True, 'NUM_USERS': True}
                           ).update_layout(height=350, margin=dict(l=20, r=20, t=20, b=20), yaxis=dict(title='Number of Active LPs'))

# Pies
fig_pie_lp_apr = px.pie(df_orcalp_apr,names='Pool Name',values='NUM_USERS', title = 'April 2022').update_traces(textposition='inside')
fig_pie_lp_apr.update_layout(height=200, uniformtext_minsize=11,uniformtext_mode='hide',margin=dict(l=20, r=20, t=20, b=20))

fig_pie_lp_jul = px.pie(df_orcalp_jul,names='Pool Name',values='NUM_USERS', title = 'July 2022').update_traces(textposition='inside')
fig_pie_lp_jul.update_layout(height=200, uniformtext_minsize=11,uniformtext_mode='hide',margin=dict(l=20, r=20, t=20, b=20))

fig_pie_lp_nov = px.pie(df_orcalp_nov,names='Pool Name',values='NUM_USERS', title = 'November 2022').update_traces(textposition='inside')
fig_pie_lp_nov.update_layout(height=200, uniformtext_minsize=11,uniformtext_mode='hide',margin=dict(l=20, r=20, t=20, b=20))

fig_pie_lp_jan = px.pie(df_orcalp_jan,names='Pool Name',values='NUM_USERS', title = 'January 2023').update_traces(textposition='inside')
fig_pie_lp_jan.update_layout(height=200, uniformtext_minsize=11,uniformtext_mode='hide',margin=dict(l=20, r=20, t=20, b=20))



#------------------ ORCA Total Stats By Pool -----------------------------------------
## Data Frame
OrcaDailyHist = 'https://node-api.flipsidecrypto.com/api/v2/queries/860f8493-6bad-45a6-98b0-d76d587dc1c3/data/latest'
df_orca_daily = pd.read_json(OrcaDailyHist)
df_orca_daily.loc[df_orca_daily['NUM_TRX'] <= 50, 'POOL NAME'] = 'OTHER'
df_orca_daily.loc[df_orca_daily['NUM_TRX'] > 50, 'POOL NAME'] = df_orca_daily['POOL_ADDRESS_NAME']
df_orca_daily['Pool Name'] = df_orca_daily['POOL_ADDRESS_NAME'].astype(str).apply(filter_pool)

df_orca_count = df_orca_daily.groupby('DT').count()
df_orca_count['POOL_COUNT_MA'] = df_orca_count['POOL_ADDRESS_NAME'][::1].rolling(7).mean()[::1].replace(np.nan, 'None')
df_orca_count['DT']=df_orca_count.index

bonk_index_ttl = df_orca_daily.index[df_orca_daily['DT'] == '2022-12-15 00:00:00.000'].tolist()
df_orca_bonk = df_orca_daily.loc[:bonk_index_ttl[-1]]
df_orca_bonk['Pool Name Type'] = df_orca_bonk['POOL_ADDRESS_NAME'].astype(str).apply(filter_bonk)

df_orca_apr = df_orca_daily[df_orca_daily['DT'].str.contains("2022-04-12")]
df_orca_apr['Pool Name'] = df_orca_apr['POOL_ADDRESS_NAME'].apply(filter_pool_pie)
df_orca_jul = df_orca_daily[df_orca_daily['DT'].str.contains("2022-07-18")]
df_orca_jul['Pool Name'] = df_orca_jul['POOL_ADDRESS_NAME'].apply(filter_pool_pie)
df_orca_nov = df_orca_daily[df_orca_daily['DT'].str.contains("2022-11-18")]
df_orca_nov['Pool Name'] = df_orca_nov['POOL_ADDRESS_NAME'].apply(filter_pool_pie)
df_orca_jan = df_orca_daily[df_orca_daily['DT'].str.contains("2023-01-05")]
df_orca_jan['Pool Name'] = df_orca_jan['POOL_ADDRESS_NAME'].apply(filter_pool_pie)

# --> $ORCA Price
fig_hist_prc = px.line(df_orca_daily, x='DT', y='ORCA_CLOSE', labels ={'DT':'Date', 'ORCA_CLOSE':'$OP Price'}
                ,color_discrete_sequence=['yellow']
                ,hover_data={'DT':True,'ORCA_CLOSE':True})
chart_update_layout(fig_hist_prc, "", "ORCA Token Price (USD)")

# --> Active Pool Count
fig_pool_count = px.line(df_orca_count, x='DT', y='POOL_COUNT_MA', labels ={'DT':'Date', 'POOL_COUNT_MA':'7-Day MA'}
                ,color_discrete_sequence=['white']
                ,hover_data={'DT':False,'POOL_COUNT_MA':True} )
fig_pool_count.add_bar(x=df_orca_count['DT'],y=df_orca_count['POOL_ADDRESS_NAME'], name="# Active Pools / Day"
                    ,marker_color='rgba(125,239,161,255)')
chart_update_layout(fig_pool_count, "", "Number of Active Pools / Day")

#--> daily transaction by pool
fig_trx_pool = px.bar(df_orca_daily,x='DT',y='NUM_TRX',color='Pool Name'
                           , hover_data={'DT': True, 'NUM_TRX': True}
                           ).update_layout(height=350, margin=dict(l=20, r=20, t=20, b=20), yaxis=dict(title='Number of Transactions'))

# Total Swap volume by pool
fig_swap_vol_pool = px.bar(df_orca_daily,x='DT',y='TTL_SWAP_VOLUME',color='Pool Name'
                           , hover_data={'DT': True, 'TTL_SWAP_VOLUME': True}
                           ).update_layout(height=350, margin=dict(l=20, r=20, t=20, b=20), yaxis=dict(title='Total Trading Volume (USD)'))

# Pies
fig_pie_apr = px.pie(df_orca_apr,names='Pool Name',values='TTL_SWAP_VOLUME', title = 'April 2022').update_traces(textposition='inside')
fig_pie_apr.update_layout(height=200, uniformtext_minsize=11,uniformtext_mode='hide',margin=dict(l=20, r=20, t=20, b=20))

fig_pie_jul = px.pie(df_orca_jul,names='Pool Name',values='TTL_SWAP_VOLUME', title = 'July 2022').update_traces(textposition='inside')
fig_pie_jul.update_layout(height=200, uniformtext_minsize=11,uniformtext_mode='hide',margin=dict(l=20, r=20, t=20, b=20))

fig_pie_nov = px.pie(df_orca_nov,names='Pool Name',values='TTL_SWAP_VOLUME', title = 'November 2022').update_traces(textposition='inside')
fig_pie_nov.update_layout(height=200, uniformtext_minsize=11,uniformtext_mode='hide',margin=dict(l=20, r=20, t=20, b=20))

fig_pie_jan = px.pie(df_orca_jan,names='Pool Name',values='TTL_SWAP_VOLUME', title = 'January 2023').update_traces(textposition='inside')
fig_pie_jan.update_layout(height=200, uniformtext_minsize=11,uniformtext_mode='hide',margin=dict(l=20, r=20, t=20, b=20))


# Total Fee by pool
fig_swap_fee_pool = px.bar(df_orca_daily,x='DT',y='TTL_LP_FEE',color='Pool Name'
                           , hover_data={'DT': True, 'TTL_LP_FEE': True}
                           ).update_layout(height=350, margin=dict(l=20, r=20, t=20, b=20), yaxis=dict(title='Total Fee Earned by LP (USD)'))

fig_swap_fee_pool_bonk = px.bar(df_orca_bonk,x='DT',y='TTL_LP_FEE',color='Pool Name Type'
                           , hover_data={'DT': True, 'TTL_LP_FEE': True}
                           ).update_layout(height=350, margin=dict(l=20, r=20, t=20, b=20), yaxis=dict(title='Total Fee Earned by LP (USD)'))

# Fee Pies
fig_pie_fee_apr = px.pie(df_orca_apr,names='Pool Name',values='TTL_LP_FEE', title = 'April 2022').update_traces(textposition='inside')
fig_pie_fee_apr.update_layout(height=200, uniformtext_minsize=11,uniformtext_mode='hide',margin=dict(l=20, r=20, t=20, b=20))

fig_pie_fee_jul = px.pie(df_orca_jul,names='Pool Name',values='TTL_LP_FEE', title = 'July 2022').update_traces(textposition='inside')
fig_pie_fee_jul.update_layout(height=200, uniformtext_minsize=11,uniformtext_mode='hide',margin=dict(l=20, r=20, t=20, b=20))

fig_pie_fee_nov = px.pie(df_orca_nov,names='Pool Name',values='TTL_LP_FEE', title = 'November 2022').update_traces(textposition='inside')
fig_pie_fee_nov.update_layout(height=200, uniformtext_minsize=11,uniformtext_mode='hide',margin=dict(l=20, r=20, t=20, b=20))

fig_pie_fee_jan = px.pie(df_orca_jan,names='Pool Name',values='TTL_LP_FEE', title = 'January 2023').update_traces(textposition='inside')
fig_pie_fee_jan.update_layout(height=200, uniformtext_minsize=11,uniformtext_mode='hide',margin=dict(l=20, r=20, t=20, b=20))


# --> (bonk)
fig_swap_vol_pool_bonk = px.bar(df_orca_bonk,x='DT',y='TTL_SWAP_VOLUME',color='Pool Name Type'
                           , hover_data={'DT': True, 'TTL_SWAP_VOLUME': True}
                           ).update_layout(height=350, margin=dict(l=20, r=20, t=20, b=20), yaxis=dict(title='Total Trading Volume (USD)'))












