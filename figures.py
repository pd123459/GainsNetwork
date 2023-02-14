import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots
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
            y=1.05,
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


def chart_update_layout_y2(figure, y2_axis, y2_range):
    figure.update_layout(

        yaxis2=dict(
            title=y2_axis,
            title_font=dict(size=14, color='rgba(171,171,171,0.7)'),  # , family='Arial Black'
            title_standoff=3,
            gridcolor='rgba(100,100,100,0)',
            linecolor='rgba(100,100,100,0.7)',
            tickfont=dict(color='rgba(100,100,100,1)'),
            overlaying="y", side="right", range=y2_range
        )

    )

def chart_update_legend(figure, names):
    series_names = names

    for idx, name in enumerate(series_names):
        figure.data[idx].name = name




# ============================ HISTORICAL DAILY TIME SERIES ===============================

# ------------------------ DATA ------------------------------------
## ----------- Gains Data Frame ---------------
gainDailyUrl = 'https://node-api.flipsidecrypto.com/api/v2/queries/42de9e27-af83-4af3-ab82-dad0bc0d8d3c/data/latest'
df_gains_initial = pd.read_json(gainDailyUrl).sort_values(by="DATE").reset_index(drop=True)
df_gains_start_index = df_gains_initial.index[df_gains_initial['DATE'] == '2022-01-01'].tolist()
df_gains = df_gains_initial.loc[df_gains_start_index[0]:]

df_gains_ttl = df_gains.groupby('DATE')[['TX_COUNT','USERS_COUNT','TOTAL_VOLUME','TOTAL_VOLUME_NOLVG','TOTAL_TRADEFEE','TOTAL_CLOSE_TRADES','TOTAL_PROFIT_TRADES','TOTAL_PNL']].sum().reset_index()
df_gains_ttl['TOTAL_VOLUME_1MONTH'] = df_gains_ttl['TOTAL_VOLUME'][::1].rolling(30).sum()[::1].replace(np.nan, 'None')
df_gains_ttl['TOTAL_VOLUME_3MONTH'] = df_gains_ttl['TOTAL_VOLUME'][::1].rolling(90).sum()[::1].replace(np.nan, 'None')
df_gains_ttl['TOTAL_TRADER_1MONTH'] = df_gains_ttl['USERS_COUNT'][::1].rolling(30).sum()[::1].replace(np.nan, 'None')
df_gains_ttl['TOTAL_TRADER_3MONTH'] = df_gains_ttl['USERS_COUNT'][::1].rolling(90).sum()[::1].replace(np.nan, 'None')
df_gains_ttl['TOTAL_FEE_1MONTH'] = df_gains_ttl['TOTAL_TRADEFEE'][::1].rolling(30).sum()[::1].replace(np.nan, 'None')
df_gains_ttl['TOTAL_FEE_3MONTH'] = df_gains_ttl['TOTAL_TRADEFEE'][::1].rolling(90).sum()[::1].replace(np.nan, 'None')
df_gains_ttl['PROFIT_PCT'] = df_gains_ttl['TOTAL_PROFIT_TRADES'] / df_gains_ttl['TOTAL_CLOSE_TRADES']
df_gains_ttl['PROFIT_PCT_MA'] = df_gains_ttl['PROFIT_PCT'][::1].rolling(7).mean()[::1].replace(np.nan, 'None')
df_gains_ttl['TX_COUNT_MA'] = df_gains_ttl['TX_COUNT'][::1].rolling(7).mean()[::1].replace(np.nan, 'None')
df_gains_ttl['TOTAL_VOLUME_MA'] = df_gains_ttl['TOTAL_VOLUME'][::1].rolling(7).mean()[::1].replace(np.nan, 'None')
df_gains_ttl['TOTAL_TRADEFEE_MA'] = df_gains_ttl['TOTAL_TRADEFEE'][::1].rolling(7).mean()[::1].replace(np.nan, 'None')
df_gains_ttl['USERS_COUNT_MA'] = df_gains_ttl['USERS_COUNT'][::1].rolling(7).mean()[::1].replace(np.nan, 'None')
df_gains_ttl['AVG_NUM_TRADES'] = df_gains_ttl['TX_COUNT'] / df_gains_ttl['USERS_COUNT']
df_gains_ttl['AVG_TRADE_SIZE'] = df_gains_ttl['TOTAL_VOLUME'] / df_gains_ttl['TX_COUNT']
df_gains_ttl['AVG_LEVERAGE'] = df_gains_ttl['TOTAL_VOLUME']/ df_gains_ttl['TOTAL_VOLUME_NOLVG']
df_gains_ttl['AVG_LEVERAGE_MA'] = df_gains_ttl['AVG_LEVERAGE'][::1].rolling(7).mean()[::1].replace(np.nan, 'None')
df_gains_ttl['AVG_TRADE_SIZE_MA'] = df_gains_ttl['AVG_TRADE_SIZE'][::1].rolling(7).mean()[::1].replace(np.nan, 'None')
df_gains_ttl['AVG_NUM_TRADES_MA'] = df_gains_ttl['AVG_NUM_TRADES'][::1].rolling(7).mean()[::1].replace(np.nan, 'None')

df_gains_chain_index = df_gains.index[df_gains['DATE'] == '2023-01-01'].tolist()
df_gains_chain_initial = df_gains
df_gains_chain_initial = df_gains_chain_initial.loc[df_gains_chain_index[0]:]
df_gains_chain = df_gains_chain_initial.groupby(['DATE','CHAIN'])[['TX_COUNT','USERS_COUNT','TOTAL_VOLUME','TOTAL_VOLUME_NOLVG','TOTAL_TRADEFEE','TOTAL_CLOSE_TRADES','TOTAL_PROFIT_TRADES','TOTAL_PNL']].sum().reset_index()
df_gains_poly_initial = df_gains.groupby(['DATE','CHAIN'])[['TX_COUNT','USERS_COUNT','TOTAL_VOLUME','TOTAL_VOLUME_NOLVG','TOTAL_TRADEFEE','TOTAL_CLOSE_TRADES','TOTAL_PROFIT_TRADES','TOTAL_PNL']].sum().reset_index()
#all poly data: df_gains_poly = df_gains_poly_initial[(df_gains_poly_initial['CHAIN'] == 'poly')].reset_index(drop=True)
df_gains_poly = df_gains_chain[(df_gains_chain['CHAIN'] == 'poly')].reset_index(drop=True) #2023 poly data
df_gains_arbitrum = df_gains_chain[(df_gains_chain['CHAIN'] == 'arbitrum')].reset_index(drop=True)

df_gains_poly['PROFIT_PCT'] = df_gains_poly['TOTAL_PROFIT_TRADES'] / df_gains_poly['TOTAL_CLOSE_TRADES']
df_gains_poly['PROFIT_PCT_MA'] = df_gains_poly['PROFIT_PCT'][::1].rolling(7).mean()[::1].replace(np.nan, 'None')
df_gains_poly['AVG_NUM_TRADES'] = df_gains_poly['TX_COUNT'] / df_gains_poly['USERS_COUNT']
df_gains_poly['TX_COUNT_MA'] = df_gains_poly['TX_COUNT'][::1].rolling(7).mean()[::1].replace(np.nan, 'None')
df_gains_poly['USERS_COUNT_MA'] = df_gains_poly['USERS_COUNT'][::1].rolling(7).mean()[::1].replace(np.nan, 'None')
df_gains_poly['TOTAL_VOLUME_MA'] = df_gains_poly['TOTAL_VOLUME'][::1].rolling(7).mean()[::1].replace(np.nan, 'None')
df_gains_poly['TOTAL_VOLUME_NOLVG_MA'] = df_gains_poly['TOTAL_VOLUME_NOLVG'][::1].rolling(7).mean()[::1].replace(np.nan, 'None')
df_gains_poly['AVG_LEVERAGE'] = df_gains_poly['TOTAL_VOLUME']/ df_gains_poly['TOTAL_VOLUME_NOLVG']
df_gains_poly['AVG_LEVERAGE_MA'] = df_gains_poly['AVG_LEVERAGE'][::1].rolling(7).mean()[::1].replace(np.nan, 'None')
df_gains_poly['AVG_TRADE_SIZE'] = df_gains_poly['TOTAL_VOLUME'] / df_gains_poly['TX_COUNT']
df_gains_poly['AVG_TRADE_SIZE_MA'] = df_gains_poly['AVG_TRADE_SIZE'][::1].rolling(7).mean()[::1].replace(np.nan, 'None')
df_gains_poly['AVG_NUM_TRADES_MA'] = df_gains_poly['AVG_NUM_TRADES'][::1].rolling(7).mean()[::1].replace(np.nan, 'None')
#df_gains_poly_mkt_limit = df_gains_chain_initial[(df_gains_chain_initial['CHAIN'] == 'poly')].reset_index(drop=True)

df_gains_arbitrum['PROFIT_PCT'] = df_gains_arbitrum['TOTAL_PROFIT_TRADES'] / df_gains_arbitrum['TOTAL_CLOSE_TRADES']
df_gains_arbitrum['PROFIT_PCT_MA'] = df_gains_arbitrum['PROFIT_PCT'][::1].rolling(7).mean()[::1].replace(np.nan, 'None')
df_gains_arbitrum['AVG_NUM_TRADES'] = df_gains_arbitrum['TX_COUNT'] / df_gains_arbitrum['USERS_COUNT']
df_gains_arbitrum['TX_COUNT_MA'] = df_gains_arbitrum['TX_COUNT'][::1].rolling(7).mean()[::1].replace(np.nan, 'None')
df_gains_arbitrum['USERS_COUNT_MA'] = df_gains_arbitrum['USERS_COUNT'][::1].rolling(7).mean()[::1].replace(np.nan, 'None')
df_gains_arbitrum['TOTAL_VOLUME_MA'] = df_gains_arbitrum['TOTAL_VOLUME'][::1].rolling(7).mean()[::1].replace(np.nan, 'None')
df_gains_arbitrum['TOTAL_VOLUME_NOLVG_MA'] = df_gains_arbitrum['TOTAL_VOLUME_NOLVG'][::1].rolling(7).mean()[::1].replace(np.nan, 'None')
df_gains_arbitrum['AVG_LEVERAGE'] = df_gains_arbitrum['TOTAL_VOLUME']/ df_gains_arbitrum['TOTAL_VOLUME_NOLVG']
df_gains_arbitrum['AVG_LEVERAGE_MA'] = df_gains_arbitrum['AVG_LEVERAGE'][::1].rolling(7).mean()[::1].replace(np.nan, 'None')
df_gains_arbitrum['AVG_TRADE_SIZE'] = df_gains_arbitrum['TOTAL_VOLUME'] / df_gains_arbitrum['TX_COUNT']
df_gains_arbitrum['AVG_TRADE_SIZE_MA'] = df_gains_arbitrum['AVG_TRADE_SIZE'][::1].rolling(7).mean()[::1].replace(np.nan, 'None')
df_gains_arbitrum['AVG_NUM_TRADES_MA'] = df_gains_arbitrum['AVG_NUM_TRADES'][::1].rolling(7).mean()[::1].replace(np.nan, 'None')
#df_gains_arbitrum_mkt_limit = df_gains_chain_initial[(df_gains_chain_initial['CHAIN'] == 'arbitrum')].reset_index(drop=True)

# ## ----------- GMX Data Frame ---------------
gmxDailyUrl = 'https://node-api.flipsidecrypto.com/api/v2/queries/3f52b4f5-28c8-4a43-bfe8-684169762005/data/latest'
df_gmx_initial = pd.read_json(gmxDailyUrl).sort_values(by="DATE").reset_index(drop=True)
df_gmx_initial['CHAIN: TRADE TYPE'] = df_gmx_initial['CHAIN'] + ': ' + df_gmx_initial['ORDERTYPE']
df_gmx_start_index = df_gmx_initial.index[df_gmx_initial['DATE'] == '2022-01-01'].tolist()
df_gmx = df_gmx_initial.loc[df_gmx_start_index[0]:]

df_gmx_ttl = df_gmx.groupby('DATE')[['TX_COUNT','USERS_COUNT','TOTAL_VOLUME','TOTAL_TRADEFEE']].sum().reset_index()
df_gmx_ttl['TOTAL_VOLUME_1MONTH'] = df_gmx_ttl['TOTAL_VOLUME'][::1].rolling(30).sum()[::1].replace(np.nan, 'None')
df_gmx_ttl['TOTAL_VOLUME_3MONTH'] = df_gmx_ttl['TOTAL_VOLUME'][::1].rolling(90).sum()[::1].replace(np.nan, 'None')
df_gmx_ttl['TOTAL_TRADER_1MONTH'] = df_gmx_ttl['USERS_COUNT'][::1].rolling(30).sum()[::1].replace(np.nan, 'None')
df_gmx_ttl['TOTAL_TRADER_3MONTH'] = df_gmx_ttl['USERS_COUNT'][::1].rolling(90).sum()[::1].replace(np.nan, 'None')
df_gmx_ttl['TOTAL_FEE_1MONTH'] = df_gmx_ttl['TOTAL_TRADEFEE'][::1].rolling(30).sum()[::1].replace(np.nan, 'None')
df_gmx_ttl['TOTAL_FEE_3MONTH'] = df_gmx_ttl['TOTAL_TRADEFEE'][::1].rolling(90).sum()[::1].replace(np.nan, 'None')
df_gmx_ttl['TX_COUNT_MA'] = df_gmx_ttl['TX_COUNT'][::1].rolling(7).mean()[::1].replace(np.nan, 'None')
df_gmx_ttl['TOTAL_VOLUME_MA'] = df_gmx_ttl['TOTAL_VOLUME'][::1].rolling(7).mean()[::1].replace(np.nan, 'None')
df_gmx_ttl['TOTAL_TRADEFEE_MA'] = df_gmx_ttl['TOTAL_TRADEFEE'][::1].rolling(7).mean()[::1].replace(np.nan, 'None')
df_gmx_ttl['USERS_COUNT_MA'] = df_gmx_ttl['USERS_COUNT'][::1].rolling(7).mean()[::1].replace(np.nan, 'None')
df_gmx_ttl['AVG_NUM_TRADES'] = df_gmx_ttl['TX_COUNT'] / df_gmx_ttl['USERS_COUNT']
df_gmx_ttl['AVG_TRADE_SIZE'] = df_gmx_ttl['TOTAL_VOLUME'] / df_gmx_ttl['TX_COUNT']
df_gmx_ttl['AVG_TRADE_SIZE_MA'] = df_gmx_ttl['AVG_TRADE_SIZE'][::1].rolling(7).mean()[::1].replace(np.nan, 'None')
df_gmx_ttl['AVG_NUM_TRADES_MA'] = df_gmx_ttl['AVG_NUM_TRADES'][::1].rolling(7).mean()[::1].replace(np.nan, 'None')


df_gmx_arbitrum_index = df_gmx_initial.index[df_gmx_initial['DATE'] == '2023-01-01'].tolist()
df_gmx_arbitrum_perp_initial = df_gmx_initial.loc[df_gmx_arbitrum_index[0]:]
df_gmx_arbitrum_perp = df_gmx_arbitrum_perp_initial[(df_gmx_arbitrum_perp_initial['CHAIN: TRADE TYPE'] == 'arbitrum: perp')].reset_index(drop=True)
df_gmx_arbitrum_perp['TX_COUNT_MA'] = df_gmx_arbitrum_perp['TX_COUNT'][::1].rolling(7).mean()[::1].replace(np.nan, 'None')
df_gmx_arbitrum_perp['TOTAL_VOLUME_MA'] = df_gmx_arbitrum_perp['TOTAL_VOLUME'][::1].rolling(7).mean()[::1].replace(np.nan, 'None')
df_gmx_arbitrum_perp['TOTAL_TRADEFEE_MA'] = df_gmx_arbitrum_perp['TOTAL_TRADEFEE'][::1].rolling(7).mean()[::1].replace(np.nan, 'None')
df_gmx_arbitrum_perp['USERS_COUNT_MA'] = df_gmx_arbitrum_perp['USERS_COUNT'][::1].rolling(7).mean()[::1].replace(np.nan, 'None')
df_gmx_arbitrum_perp['AVG_NUM_TRADES'] = df_gmx_arbitrum_perp['TX_COUNT'] / df_gmx_arbitrum_perp['USERS_COUNT']
df_gmx_arbitrum_perp['AVG_TRADE_SIZE'] = df_gmx_arbitrum_perp['TOTAL_VOLUME'] / df_gmx_arbitrum_perp['TX_COUNT']
df_gmx_arbitrum_perp['AVG_TRADE_SIZE_MA'] = df_gmx_arbitrum_perp['AVG_TRADE_SIZE'][::1].rolling(7).mean()[::1].replace(np.nan, 'None')
df_gmx_arbitrum_perp['AVG_NUM_TRADES_MA'] = df_gmx_arbitrum_perp['AVG_NUM_TRADES'][::1].rolling(7).mean()[::1].replace(np.nan, 'None')


# ------------------------ PLOTS ------------------------------------
# Plots (Gain - Key Statistics)
# ttl volume
fig_gains_vol_daily = px.line(df_gains_ttl, x='DATE', y='TOTAL_VOLUME_MA', labels ={'DATE':'Date', 'TOTAL_VOLUME_MA':'7-Day MA'}
                ,color_discrete_sequence=['white']
                ,hover_data={'DATE':False,'TOTAL_VOLUME_MA':True} )
fig_gains_vol_daily.add_bar(x=df_gains_ttl['DATE'],y=df_gains_ttl['TOTAL_VOLUME'], name="Daily Trading Volume"
                     ,marker_color='Aquamarine')
chart_update_layout(fig_gains_vol_daily, "", "Daily Gains Trading Volume")

fig_gains_vol_monthly = px.area(df_gains_ttl,x='DATE',y=['TOTAL_VOLUME_1MONTH', 'TOTAL_VOLUME_3MONTH']
                           , hover_data={'DATE': False})
chart_update_layout(fig_gains_vol_monthly, "", "Monthly Gains Trading Volume")

# ttl users
fig_gains_user_daily = px.line(df_gains_ttl, x='DATE', y='USERS_COUNT_MA', labels ={'DATE':'Date', 'USERS_COUNT_MA':'7-Day MA'}
                ,color_discrete_sequence=['white']
                ,hover_data={'DATE':False,'USERS_COUNT_MA':True} )
fig_gains_user_daily.add_bar(x=df_gains_ttl['DATE'],y=df_gains_ttl['USERS_COUNT'], name="Daily Traders"
                     ,marker_color='Aquamarine')
chart_update_layout(fig_gains_user_daily, "", "Daily Number of Traders")

fig_gains_user_monthly = px.area(df_gains_ttl,x='DATE',y=['TOTAL_TRADER_1MONTH', 'TOTAL_TRADER_3MONTH']
                           , hover_data={'DATE': False})
chart_update_layout(fig_gains_user_monthly, "", "Monthly Number of Traders")

# ttl fee
fig_gains_fee_daily = px.line(df_gains_ttl, x='DATE', y='TOTAL_TRADEFEE_MA', labels ={'DATE':'Date', 'TOTAL_TRADEFEE_MA':'7-Day MA'}
                ,color_discrete_sequence=['white']
                ,hover_data={'DATE':False,'TOTAL_TRADEFEE_MA':True} )
fig_gains_fee_daily.add_bar(x=df_gains_ttl['DATE'],y=df_gains_ttl['TOTAL_TRADEFEE'], name="Daily Fees"
                     ,marker_color='Aquamarine')
chart_update_layout(fig_gains_fee_daily, "", "Daily Trading Fees")

fig_gains_fee_monthly = px.area(df_gains_ttl,x='DATE',y=['TOTAL_FEE_1MONTH', 'TOTAL_FEE_3MONTH']
                           , hover_data={'DATE': False})
chart_update_layout(fig_gains_fee_monthly, "", "Monthly Trading Fees")


# Plots (Gain - ttl details)
fig_gains_avg_size = make_subplots(specs=[[{"secondary_y": True}]]).update_layout(title = 'Total', yaxis_range=[0,150000])
fig_gains_avg_size.add_trace(go.Scatter(x=df_gains_ttl['DATE'], y=df_gains_ttl['AVG_TRADE_SIZE_MA'], name='Trading Size',
                                       fill='tozeroy', fillcolor='rgba(255,209,106,1)', mode='none'), secondary_y=False)
fig_gains_avg_size.add_bar(x=df_gains_ttl['DATE'],y=df_gains_ttl['TOTAL_VOLUME'], name="Total Volume", secondary_y=True)
fig_gains_avg_size.add_trace(go.Scatter(x=df_gains_ttl['DATE'], y=df_gains_ttl['TOTAL_VOLUME_MA'],
                          name='7-Day Vol MA', marker=dict(color="white")), secondary_y=True)
chart_update_layout(fig_gains_avg_size, "", "Position Size / Trade")
chart_update_layout_y2(fig_gains_avg_size, "Total Volume", [0,600000000])

fig_gains_lvg = make_subplots(specs=[[{"secondary_y": True}]]).update_layout(title = 'Total', yaxis_range=[0,70])
fig_gains_lvg.add_trace(go.Scatter(x=df_gains_ttl['DATE'], y=df_gains_ttl['AVG_LEVERAGE_MA'], name='Leverage (7-Day MA)',
                                       fill='tozeroy', fillcolor='rgba(255,209,106,1)', mode='none'), secondary_y=False)
fig_gains_lvg.add_bar(x=df_gains_ttl['DATE'],y=df_gains_ttl['AVG_NUM_TRADES'], name="# Trades / Day", secondary_y=True) #,marker_color='rgba(131,201,255,0.8)'
fig_gains_lvg.add_trace(go.Scatter(x=df_gains_ttl['DATE'], y=df_gains_ttl['AVG_NUM_TRADES_MA'],
                          name='# Trades / Day (7-Day MA)', marker=dict(color="white")), secondary_y=True)
chart_update_layout(fig_gains_lvg, "", "Average Leverage Taken")
chart_update_layout_y2(fig_gains_lvg, "Daily Number of Trades", [0,20])

fig_gains_pnl = make_subplots(specs=[[{"secondary_y": True}]]).update_layout(title = 'Total', yaxis_range=[0,0.7])
fig_gains_pnl.add_trace(go.Scatter(x=df_gains_ttl['DATE'], y=df_gains_ttl['PROFIT_PCT_MA'], name='Profitable Trades% (7-Day MA)',
                                       fill='tozeroy', fillcolor='rgba(255,209,106,1)', mode='none'), secondary_y=False)
fig_gains_pnl.add_bar(x=df_gains_ttl['DATE'],y=df_gains_ttl['TOTAL_PNL'], name="PnL", secondary_y=True) #,marker_color='rgba(131,201,255,0.8)'
chart_update_layout(fig_gains_pnl, "", "Profitable Trades Percentage")
chart_update_layout_y2(fig_gains_pnl, "Profit and Loss / Day", [-500000,500000])

# Plots (Gain - Poly)
fig_poly_avg_size = make_subplots(specs=[[{"secondary_y": True}]]).update_layout(title = 'On Polygon (2023)', yaxis_range=[0,150000])
fig_poly_avg_size.add_trace(go.Scatter(x=df_gains_poly['DATE'], y=df_gains_poly['AVG_TRADE_SIZE_MA'], name='Trading Size',
                                       fill='tozeroy', fillcolor='rgba(255,209,106,1)', mode='none'), secondary_y=False)
fig_poly_avg_size.add_bar(x=df_gains_poly['DATE'],y=df_gains_poly['TOTAL_VOLUME'], name="Total Volume", secondary_y=True)
fig_poly_avg_size.add_trace(go.Scatter(x=df_gains_poly['DATE'], y=df_gains_poly['TOTAL_VOLUME_MA'],
                          name='7-Day Vol MA', marker=dict(color="white")), secondary_y=True)
chart_update_layout(fig_poly_avg_size, "", "Position Size / Trade")
chart_update_layout_y2(fig_poly_avg_size, "Total Volume", [0,600000000])

fig_poly_lvg = make_subplots(specs=[[{"secondary_y": True}]]).update_layout(title = 'On Polygon (2023)', yaxis_range=[0,50])
fig_poly_lvg.add_trace(go.Scatter(x=df_gains_poly['DATE'], y=df_gains_poly['AVG_LEVERAGE_MA'], name='Leverage (7-Day MA)',
                                       fill='tozeroy', fillcolor='rgba(255,209,106,1)', mode='none'), secondary_y=False)
fig_poly_lvg.add_bar(x=df_gains_poly['DATE'],y=df_gains_poly['AVG_NUM_TRADES'], name="# Trades / Day", secondary_y=True) #,marker_color='rgba(131,201,255,0.8)'
fig_poly_lvg.add_trace(go.Scatter(x=df_gains_poly['DATE'], y=df_gains_poly['AVG_NUM_TRADES_MA'],
                          name='# Trades / Day (7-Day MA)', marker=dict(color="white")), secondary_y=True)
chart_update_layout(fig_poly_lvg, "", "Average Leverage Taken")
chart_update_layout_y2(fig_poly_lvg, "Daily Number of Trades", [0,20])

fig_poly_pnl = make_subplots(specs=[[{"secondary_y": True}]]).update_layout(title = 'On Polygon (2023)', yaxis_range=[0,0.7])
fig_poly_pnl.add_trace(go.Scatter(x=df_gains_poly['DATE'], y=df_gains_poly['PROFIT_PCT_MA'], name='Profitable Trades% (7-Day MA)',
                                       fill='tozeroy', fillcolor='rgba(255,209,106,1)', mode='none'), secondary_y=False)
fig_poly_pnl.add_bar(x=df_gains_poly['DATE'],y=df_gains_poly['TOTAL_PNL'], name="PnL", secondary_y=True) #,marker_color='rgba(131,201,255,0.8)'
chart_update_layout(fig_poly_pnl, "", "Profitable Trades Percentage")
chart_update_layout_y2(fig_poly_pnl, "Profit and Loss / Day", [-500000,500000])

# Plots (Gain - Arbitrum)

fig_arbitrum_avg_size = make_subplots(specs=[[{"secondary_y": True}]]).update_layout(title = 'On Arbitrum (2023)')
fig_arbitrum_avg_size.add_trace(go.Scatter(x=df_gains_arbitrum['DATE'], y=df_gains_arbitrum['AVG_TRADE_SIZE_MA'], name='Trading Size',
                                       fill='tozeroy', fillcolor='rgba(255,209,106,255)', opacity=0.9, mode='none'), secondary_y=False)
fig_arbitrum_avg_size.add_bar(x=df_gains_arbitrum['DATE'],y=df_gains_arbitrum['TOTAL_VOLUME'], name="Total Volume", secondary_y=True)
fig_arbitrum_avg_size.add_trace(go.Scatter(x=df_gains_arbitrum['DATE'], y=df_gains_arbitrum['TOTAL_VOLUME_MA'],
                          name='7-Day Vol MA', marker=dict(color="white")), secondary_y=True)
chart_update_layout(fig_arbitrum_avg_size, "", "Position Size / Trade")
chart_update_layout_y2(fig_arbitrum_avg_size, "Total Volume", [0,600000000])

fig_arbitrum_lvg = make_subplots(specs=[[{"secondary_y": True}]]).update_layout(title = 'On Arbitrum (2023)')
fig_arbitrum_lvg.add_trace(go.Scatter(x=df_gains_arbitrum['DATE'], y=df_gains_arbitrum['AVG_LEVERAGE_MA'], name='Leverage (7-Day MA)',
                                       fill='tozeroy', fillcolor='rgba(255,209,106,1)', mode='none'), secondary_y=False)
fig_arbitrum_lvg.add_bar(x=df_gains_arbitrum['DATE'],y=df_gains_arbitrum['AVG_NUM_TRADES'], name="# Trades / Day", secondary_y=True) #,marker_color='rgba(131,201,255,0.8)'
fig_arbitrum_lvg.add_trace(go.Scatter(x=df_gains_arbitrum['DATE'], y=df_gains_arbitrum['AVG_NUM_TRADES_MA'],
                          name='# Trades / Day (7-Day MA)', marker=dict(color="white")), secondary_y=True)
chart_update_layout(fig_arbitrum_lvg, "", "Average Leverage Taken")
chart_update_layout_y2(fig_arbitrum_lvg, "Daily Number of Trades", [0,20])

fig_arbitrum_pnl = make_subplots(specs=[[{"secondary_y": True}]]).update_layout(title = 'On Arbitrum (2023)', yaxis_range=[0,0.7])
fig_arbitrum_pnl.add_trace(go.Scatter(x=df_gains_arbitrum['DATE'], y=df_gains_arbitrum['PROFIT_PCT_MA'], name='Profitable Trades% (7-Day MA)',
                                       fill='tozeroy', fillcolor='rgba(255,209,106,1)', mode='none'), secondary_y=False)
fig_arbitrum_pnl.add_bar(x=df_gains_arbitrum['DATE'],y=df_gains_arbitrum['TOTAL_PNL'], name="PnL", secondary_y=True) #,marker_color='rgba(131,201,255,0.8)'
chart_update_layout(fig_arbitrum_pnl, "", "Profitable Trades Percentage")
chart_update_layout_y2(fig_arbitrum_pnl, "Profit and Loss / Day", [-500000,500000])

# Plots (GMX)
# ttl volume
fig_gmx_vol_daily = px.bar(df_gmx, x='DATE', y='TOTAL_VOLUME', color='CHAIN: TRADE TYPE', hover_data={'DATE':False,'TOTAL_VOLUME':True})
fig_gmx_vol_daily.add_trace(go.Scatter(x=df_gmx_ttl['DATE'], y=df_gmx_ttl['TOTAL_VOLUME_MA']
                                       , name='7-Day Total Volume MA', marker=dict(color="white")))
chart_update_layout(fig_gmx_vol_daily, "", "Daily Trading Volume")

fig_gmx_vol_monthly = px.area(df_gmx_ttl,x='DATE',y=['TOTAL_VOLUME_1MONTH', 'TOTAL_VOLUME_3MONTH']
                           , hover_data={'DATE': False})
chart_update_layout(fig_gmx_vol_monthly, "", "Monthly Trading Volume")

# ttl users
fig_gmx_user_daily = px.bar(df_gmx, x='DATE', y='USERS_COUNT', color='CHAIN: TRADE TYPE', hover_data={'DATE':False,'USERS_COUNT':True})
fig_gmx_user_daily.add_trace(go.Scatter(x=df_gmx_ttl['DATE'], y=df_gmx_ttl['USERS_COUNT_MA']
                                       , name='7-Day Total Trader MA', marker=dict(color="white")))
chart_update_layout(fig_gmx_user_daily, "", "Daily Number of Traders")

fig_gmx_user_monthly = px.area(df_gmx_ttl,x='DATE',y=['TOTAL_TRADER_1MONTH', 'TOTAL_TRADER_3MONTH']
                           , hover_data={'DATE': False})
chart_update_layout(fig_gmx_user_monthly, "", "Monthly Number of Traders")

# ttl fee
fig_gmx_fee_daily = px.bar(df_gmx, x='DATE', y='TOTAL_TRADEFEE', color='CHAIN: TRADE TYPE', hover_data={'DATE':False,'TOTAL_TRADEFEE':True})
fig_gmx_fee_daily.add_trace(go.Scatter(x=df_gmx_ttl['DATE'], y=df_gmx_ttl['TOTAL_TRADEFEE_MA']
                                       , name='7-Day Total Fee MA', marker=dict(color="white")))
chart_update_layout(fig_gmx_fee_daily, "", "Daily Trading Fees")

fig_gmx_fee_monthly = px.area(df_gmx_ttl,x='DATE',y=['TOTAL_FEE_1MONTH', 'TOTAL_FEE_3MONTH']
                           , hover_data={'DATE': False})
chart_update_layout(fig_gmx_fee_monthly, "", "Monthly Trading Fees")


# Plots (Gains vs. GMX)
fig_comp_vol = px.area(x=df_gains_ttl['DATE'],y=[df_gains_ttl['TOTAL_VOLUME_MA'],df_gmx_ttl['TOTAL_VOLUME_MA']]
                       , color_discrete_sequence = ['Gold','LightGreen']).update_layout(title = 'Volume Comparison')
chart_update_legend(fig_comp_vol, ['Gains (7-Day MA)', 'GMX (7-Day MA)'])
chart_update_layout(fig_comp_vol, "", "Daily Trading Volume")

fig_comp_fee = px.area(x=df_gains_ttl['DATE'],y=[df_gains_ttl['TOTAL_TRADEFEE_MA'],df_gmx_ttl['TOTAL_TRADEFEE_MA']]
                       , color_discrete_sequence = ['Gold','LightGreen']).update_layout(title = 'Fees Comparison')
chart_update_legend(fig_comp_fee, ['Gains (7-Day MA)', 'GMX (7-Day MA)'])
chart_update_layout(fig_comp_fee, "", "Daily Trading Fees")

fig_comp_user = px.area(x=df_gains_ttl['DATE'],y=[df_gains_ttl['USERS_COUNT_MA'],df_gmx_ttl['USERS_COUNT_MA']]
                       , color_discrete_sequence = ['Gold','LightGreen']).update_layout(title = '#Traders Comparison')
chart_update_legend(fig_comp_user, ['Gains (7-Day MA)', 'GMX (7-Day MA)'])
chart_update_layout(fig_comp_user, "", "Number of Traders")

fig_comp_trades = px.area(x=df_gains_ttl['DATE'],y=[df_gains_ttl['TX_COUNT_MA'],df_gmx_ttl['TX_COUNT_MA']]
                       , color_discrete_sequence = ['Gold','LightGreen']).update_layout(title = '#Trades Comparison')
chart_update_legend(fig_comp_trades, ['Gains (7-Day MA)', 'GMX (7-Day MA)'])
chart_update_layout(fig_comp_trades, "", "Number of Trades")

fig_comp_avgsize = px.area(x=df_gains_ttl['DATE'],y=[df_gains_ttl['AVG_TRADE_SIZE_MA'],df_gmx_ttl['AVG_TRADE_SIZE_MA']]
                       , color_discrete_sequence = ['Gold','LightGreen']).update_layout(title = 'Average Position Size Comparison')
chart_update_legend(fig_comp_avgsize, ['Gains (7-Day MA)', 'GMX (7-Day MA)'])
chart_update_layout(fig_comp_avgsize, "", "Average Position Size")

fig_comp_numtrades = px.area(x=df_gains_ttl['DATE'],y=[df_gains_ttl['AVG_NUM_TRADES_MA'],df_gmx_ttl['AVG_NUM_TRADES_MA']]
                       , color_discrete_sequence = ['Gold','LightGreen']).update_layout(title = 'Daily Trades per User Comparison')
chart_update_legend(fig_comp_numtrades, ['Gains (7-Day MA)', 'GMX (7-Day MA)'])
chart_update_layout(fig_comp_numtrades, "", "Daily Trades / User")


# Plots (Gains Arbitrun vs. GMX Arbitrum)

fig_comp_arbitrum_avgsize = px.area(x=df_gains_arbitrum['DATE'],y=[df_gains_arbitrum['AVG_TRADE_SIZE_MA'],df_gmx_arbitrum_perp['AVG_TRADE_SIZE_MA']]
                       , color_discrete_sequence = ['LightSalmon','PaleTurquoise']).update_layout(title = 'Average Position Size Comparison')
chart_update_legend(fig_comp_arbitrum_avgsize, ['Gains Arbitrum (7-Day MA)', 'GMX Arbitrum (7-Day MA)'])
chart_update_layout(fig_comp_arbitrum_avgsize, "", "Average Position Size")

fig_comp_arbitrum_numtrades = px.area(x=df_gains_arbitrum['DATE'],y=[df_gains_arbitrum['AVG_NUM_TRADES_MA'],df_gmx_arbitrum_perp['AVG_NUM_TRADES_MA']]
                       , color_discrete_sequence = ['LightSalmon','PaleTurquoise']).update_layout(title = 'Daily Trades per User Comparison')
chart_update_legend(fig_comp_arbitrum_numtrades, ['Gains Arbitrum (7-Day MA)', 'GMX Arbitrum (7-Day MA)'])
chart_update_layout(fig_comp_arbitrum_numtrades, "", "Daily Trades / User")