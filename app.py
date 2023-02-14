import streamlit as st
import pandas as pd
from streamlit_option_menu import option_menu
import time
import plotly.express as px
import plotly.graph_objects as go
import figures as f
import icons as icons

st.set_page_config(page_title='Gains Network',  layout='wide', page_icon='images/logo.png')

proj_title = '<p style="font-family:sans-serif; color:white; font-size: 50px;"><b>Gains Network</b></p>'
gap = '<span>&nbsp;&nbsp;</span>'

t1, t2 = st.columns((1,5))
t1.image('images/logo.png', width = 120)
t2.markdown(proj_title, unsafe_allow_html=True)
t2.markdown(f'[{icons.link_icon}](https://gainsnetwork.io/){gap}'
            f'{gap}[{icons.twitter_icon}](https://twitter.com/GainsNetwork_io){gap}'
            f'{gap}[{icons.discord_icon}](https://discord.com/invite/gains-network){gap}'
            f'{gap}[{icons.medium_icon}](https://medium.com/gains-network){gap}', unsafe_allow_html=True)

#=========================== OVERVIEW ==============================
st.markdown(
    """
        # Overview 
        
        This dashboard analyses trading activities on gTrade, the impact of its recent Arbitrum deployment 
        and comparisons between Gains Network and its largest competitor GMX.
        Gains Network develops gTrade, a liquidity-efficient, powerful, and user-friendly decentralized leveraged trading platform.
        The platform uses an uniquely designed synthetic architecture that targets low trading fees, and a wide range of leverages and pairs
        : up to 150x on cryptos, 1000x on forex, 100x on stocks, and 35x on indices. [More](https://gains-network.gitbook.io/docs-home/gtrade-leveraged-trading/overview)

        
        Key takeaways:
        
        1. Recent growth for the gains network is contributed by its deployment on Arbitrum on December 31, 2022. Since the launch, the trading activities on gTrade Arbitrum soon outran its activities on Polygon, contributed by L2's high speed and low gas fees. 
        
        2. gTrade traders tend to take larger position sizes and higher leverages on Arbitrum compared to Polygon. 
        
        3. While the total trading volume on gTrade is smaller than that on GMX, the volume gap between the two platforms is shrinking. With the trading fee on gTrade (0.08% for crypto) lower than that on GMX (0.1% for crypto), and benefits from Layer2 trading now enabled, gTrade could potentially rival with GMX in the near future. 
        
        4. gTrade is a more institutional focused platform compared to GMX.
        
""")



st.markdown(
    """
    
    ---
    # Methodology 
    
    Data for the Gains network is identified using topics information in the arbitrum.core.fact_event_logs and polygon.core.fact_event_logs
    tables. Trade specific data is pulled from the data field and then converted from hex code to integers. These include trader address, 
    open price, current price, leverage, original position size, whether the trade is long or short, etc. The locations of these trade specific information
    in data differs for each code update, and are identified with different indexes in the underlying query. Profit and loss is then calculated
    for each closed trade. Below is a list of topics used:
    
    - Gains Polygon v5 (marketExecuted): 0xc74e5bdf3e3b91b5cda39fb8ee72fb93dbb735b9cbbaddc7eef34178ffbaf555
    - Gains Polygon v5 (limitExecuted): 0x15f192ad872076db7d7571711429e445b0eabf30dc598ab77f02cacf622eec83
    - Gains Polygon v6 (marketExecuted): 0x2343a1f0e076656e179f7fb23a0cb40efbb9cfaa668dd58344a840eb0306fec6
    - Gains Polygon v6 (limitExecuted): 0x9d894746ec0e0f1ac0599e4fdb9b9a250d21e0e23a6b9cf8c62bb8f5908bb40b
    - Gains Arbitrum & Polygon v6_1 & Polygon v6_2 (marketExecuted): 0x2739a12dffae5d66bd9e126a286078ed771840f2288f0afa5709ce38c3330997
    - Gains Arbitrum & Polygon v6_1 & Polygon v6_2 (limitExecuted): 0x165b0f8d6347f7ebe92729625b03ace41aeea8fd7ebf640f89f2593ab0db63d1
    
    Similar to data for the Gains Network, data for perpetual trading on GMX platform is identified using topics information 
    in arbitrum.core.fact_event_logs and avalanche.core.fact_event_logs tables:
    
    - GMX AVAX & Arbitrum Perpetual Trading: 0x2fe68525253654c21998f35787a8d0f361905ef647c854092430ab65f2f15022, 0x93d75d64d1f84fc6f430a64fc578bdd4c1e090e90ea2d51773e626d19de56d30
    - GMX AVAX & Arbitrum Swaps: 0xcd3829a3813dc3cdd188fd3d01dcf3268c16be2fdd2dd21d0665418816e46062
        
    Swap volume is then calculated using token price information from the ethereum.core.fact_hourly_token_prices table, 
    identified by contract address information in the event_inputs field. 
    
    The following data are then aggregated and used for analysis below: 
    
    - Daily Total Trading Volume: volume calculated uses post-leverage position size (leverage * positionsizeDai)
    - Daily Total Traders: the aggregated number of unique trader addresses on the platform
    - Daily Total Trading Fees: 0.1% per trade for GMX and 0.08% per trade for Gains network. This is not the gas fee paid for transfers. The fees for Gains network is simplified using fees charged for cryptocurrency trading as the most volume on gains network currently is from crypto trading. For the full Gains network fee schedule, see [Gains Fees and Spread](https://gains-network.gitbook.io/docs-home/gtrade-leveraged-trading/fees-and-spread).  
    - Average Position Size: the average post-leverage position size per trade
    - Leverage: aggregated leverage calculated using aggregated post-leverage volume divided by pre-leverage volume. This is only calculated for the Gains network.
    - Profitable Trader%: calculated using the total number of profitable closed trades divided by the total number of closed trades. This is only calculated for the Gains network.
        
    All of the data is drawn from [Flipside Crypto](https://flipsidecrypto.xyz/),
    """
    f'and the underlying queries are provided in the wrench icon ({icons.setting_icon})'
   
    """
    next to chart and table tiles.
    
    """
    , unsafe_allow_html=True
)

st.markdown(
    f"""
    ---
    # gTrade User Key Statistics
    
    With the Arbitrum deployment on December 31st, 2022, Gains Network has experienced a surge in trading activities, and the price
    of its native token GNS increased from 3.06USD on January 1st to more than 7USD in February. Faster speed and lower fee, along 
    with a [trading competition](https://twitter.com/GainsNetwork_io/status/1616468328956022784), attracted traders into the
    gTrade platform, and pushed the 7-day average of daily trading volume on the platform above 150 million (USD), an 650% increase from
    its low of 20 million (USD) in late December 2022. Daily number of traders on the platform also increased from below 300 in late December
    to more than 800 in January. 
    
    """
    , unsafe_allow_html=True
)


st.markdown(f'#### Total Trading Volume on gTrade [{icons.setting_icon}](https://flipsidecrypto.xyz/edit/queries/42de9e27-af83-4af3-ab82-dad0bc0d8d3c)', unsafe_allow_html=True)
st.write(
    """*Total derivative trading volume on gTrade per day, per month and per 3 months.* """)

a1, a2 = st.columns((1,1))
a1.plotly_chart(f.fig_gains_vol_daily, use_container_width=True)
a2.plotly_chart(f.fig_gains_vol_monthly, use_container_width=True)


st.markdown(f'#### Total Traders on gTrade [{icons.setting_icon}](https://flipsidecrypto.xyz/edit/queries/42de9e27-af83-4af3-ab82-dad0bc0d8d3c)', unsafe_allow_html=True)
st.write(
    """*Total number of unique users who traded on gTrade per day, per month and per 3 months.* """)

b1, b2 = st.columns((1,1))
b1.plotly_chart(f.fig_gains_user_daily, use_container_width=True)
b2.plotly_chart(f.fig_gains_user_monthly, use_container_width=True)


st.markdown(f'#### Total Trading Fees on gTrade [{icons.setting_icon}](https://flipsidecrypto.xyz/edit/queries/42de9e27-af83-4af3-ab82-dad0bc0d8d3c)', unsafe_allow_html=True)
st.write(
    """*Total fees collected on gTrade per day/month/3 months due to trading activities.* """)

c1, c2 = st.columns((1,1))
c1.plotly_chart(f.fig_gains_fee_daily, use_container_width=True)
c2.plotly_chart(f.fig_gains_fee_monthly, use_container_width=True)

st.markdown(
    f"""
    ---
    # gTrade Detailed Statistics 
    
    This section shows the detailed statistics for user activities on the Gains network. The metrics for activities on Polygon and Arbitrum 
    are also shown separately to identify the difference in user behaviors on both chains. With the short history of gTrade on
    Arbitrum, the metrics for Polygon vs. Arbitrum activities only use 2023 data.
    
    Since the Arbitrum deployment, total trading volume on gTrade Arbitrum soon exceeds that on gTrade Polygon.
    In late January, the 7-day average of daily trading volume on Arbitrum hovers around 100 million (USD), while that of Polygon 
    is only around 50 million (USD). 
    
    Interestingly, traders on Arbitrum take much larger positions compared to traders on Polygon. On average, an Arbitrum trade ranges
    from 50-100k (USD), while a Polygon trade ranges from 20-25k (USD). Arbitrum traders also tend to take higher leverages compared to Polygon 
    traders. These could potentially indicate more institutional trading on Arbitrum. 
    
    """, unsafe_allow_html=True)

st.markdown(f'#### Average Position Size [{icons.setting_icon}](https://flipsidecrypto.xyz/edit/queries/42de9e27-af83-4af3-ab82-dad0bc0d8d3c)', unsafe_allow_html=True)
st.write(
    """*The average position size per trade on gTrade per day. With high levels of leverage used on both exchanges,
    position size uses the post leverage trading position.* """)

st.plotly_chart(f.fig_gains_avg_size, use_container_width=True)
h1, h2 = st.columns((1,1))
h1.plotly_chart(f.fig_poly_avg_size, use_container_width=True)
h2.plotly_chart(f.fig_arbitrum_avg_size, use_container_width=True)

st.markdown(f'#### Leverage & Daily Number of Trades  [{icons.setting_icon}](https://flipsidecrypto.xyz/edit/queries/42de9e27-af83-4af3-ab82-dad0bc0d8d3c)', unsafe_allow_html=True)
st.write(
    """*The average leverage used per trade and the average number of trades executed per user per day on gTrade.* """)

st.plotly_chart(f.fig_gains_lvg, use_container_width=True)
i1, i2 = st.columns((1,1))
i1.plotly_chart(f.fig_poly_lvg, use_container_width=True)
i2.plotly_chart(f.fig_arbitrum_lvg, use_container_width=True)


st.markdown(f'#### Trader Profit and Loss [{icons.setting_icon}](https://flipsidecrypto.xyz/edit/queries/42de9e27-af83-4af3-ab82-dad0bc0d8d3c)', unsafe_allow_html=True)
st.write(
    """*The average percentage of profitable trades and the aggregated amount of profit and loss on gTrade per day. 
    The percentage of profitable trades is weighted by the number of close trades, rather than trading volume.* """)

st.plotly_chart(f.fig_gains_pnl, use_container_width=True)
k1, k2 = st.columns((1,1))
k1.plotly_chart(f.fig_poly_pnl, use_container_width=True)
k2.plotly_chart(f.fig_arbitrum_pnl, use_container_width=True)


st.markdown(
    """
    ---
    # Competitor Key Statistics
    
    This section shows the key statistics for Gains network's largest competitor GMX. GMX is a decentralized spot and perpetual exchange that supports low swap fees and zero price impact trades. Trading 
    is supported by a unique multi-asset pool that earns liquidity providers fees from market making, swap fees and leverage trading.
    
    Similar to gTrade, the majority of trading volume comes from GMX's perpetual trading on Arbitrum. 
    
    """
)

st.markdown(f'#### Daily Trading Volume on GMX [{icons.setting_icon}](https://flipsidecrypto.xyz/edit/queries/3f52b4f5-28c8-4a43-bfe8-684169762005)', unsafe_allow_html=True)
st.write(
    """*Total trading volume on the GMX per day, per month and per 3 months. The volume includes both GMX swap and GMX perpetual
    trading on AVAX and Arbitrum.* """)
d1, d2 = st.columns((1,1))
d1.plotly_chart(f.fig_gmx_vol_daily, use_container_width=True)
d2.plotly_chart(f.fig_gmx_vol_monthly, use_container_width=True)

st.markdown(f'#### Daily Unique Users on GMX [{icons.setting_icon}](https://flipsidecrypto.xyz/edit/queries/3f52b4f5-28c8-4a43-bfe8-684169762005)', unsafe_allow_html=True)
st.write(
    """*Total number of unique traders on GMX per day, per month and per 3 months. The statistics include both GMX swap and GMX perpetual
    trading on AVAX and Arbitrum.* """)
e1, e2 = st.columns((1,1))
e1.plotly_chart(f.fig_gmx_user_daily, use_container_width=True)
e2.plotly_chart(f.fig_gmx_user_monthly, use_container_width=True)

st.markdown(f'#### Daily Trading Fees on GMX Network [{icons.setting_icon}](https://flipsidecrypto.xyz/edit/queries/3f52b4f5-28c8-4a43-bfe8-684169762005)', unsafe_allow_html=True)
st.write(
    """*Total fees collected on GMX per day/month/3 months due to trading activities. The statistics include both GMX swap and GMX perpetual
    trading on AVAX and Arbitrum.* """)

f1, f2 = st.columns((1,1))
f1.plotly_chart(f.fig_gmx_fee_daily, use_container_width=True)
f2.plotly_chart(f.fig_gmx_fee_monthly, use_container_width=True)

st.markdown(
    """
    ---
    # A Comparison of gTrade & GMX

    This section compares trading activities on gTrade and GMX.
    
    While the total trading volume on gTrade is smaller than that on GMX, the volume gap between the two platforms is shrinking
    rapidly since gTrade's Arbitrum deployment. In the second half of 2022, the trading volume on gTrade is roughly 15-20% of 
    GMX trading volume. However, since the Arbitrum deployment, the trading volume on gTrade rises to around 50% of GMX trading volume.
    Interestingly, the trading volume gap between gTrade and GMX started to increase in April 2022, with GMX's Arbitrum adoption. 
    Prior to GMX's Arbitrum tradings, gTrade trading volume was more than 50% of GMX's trading volume.
    With the trading fee on gTrade (0.08% for crypto) lower than that on GMX (0.1% for crypto), and benefits from Layer2 trading now
    enabled, gTrade could potentially rival with GMX in the near future. 
    
    gTrade is a more institutional focused platform compared to GMX. With a minimum position size of 1,500 DAI, average 
    position size on gTrade is much larger than average position size on GMX. We also isolated GMX's perpetual trading data on 
    Arbitrum, and compared that to gTrade's Arbitrum trading data (as GMX data could be biased by spot trading). Similar conclusion is reached.
    Traders on gTrade are also more active compared to traders on GMX. An average GMX trader executes 4-5 trades per day, while 
    an average gTrade trader executes 6-8 trades per day in 2023. 
    
    """
)

st.markdown(f'#### Trading Volume and Fees [{icons.setting_icon}](https://flipsidecrypto.xyz/edit/queries/3f52b4f5-28c8-4a43-bfe8-684169762005)', unsafe_allow_html=True)
st.write(
    """*Total derivative trading volume and trading fee on the platform per day.* """)
l1, l2 = st.columns((1,1))
l1.plotly_chart(f.fig_comp_vol, use_container_width=True)
l2.plotly_chart(f.fig_comp_fee, use_container_width=True)

st.markdown(f'#### Total Number of Trades and Traders [{icons.setting_icon}](https://flipsidecrypto.xyz/edit/queries/3f52b4f5-28c8-4a43-bfe8-684169762005)', unsafe_allow_html=True)
st.write(
    """*Total number of trades and traders on the platform per day.* """)
m1, m2 = st.columns((1,1))
m1.plotly_chart(f.fig_comp_user, use_container_width=True)
m2.plotly_chart(f.fig_comp_trades, use_container_width=True)

st.markdown(f'#### Average Position Size and Trades per User [{icons.setting_icon}](https://flipsidecrypto.xyz/edit/queries/3f52b4f5-28c8-4a43-bfe8-684169762005)', unsafe_allow_html=True)
st.write(
    """*The average position size (post leverage) per trade per day, and the average number of trades executed per user per day.* """)
n1, n2 = st.columns((1,1))
n1.plotly_chart(f.fig_comp_avgsize, use_container_width=True)
n2.plotly_chart(f.fig_comp_numtrades, use_container_width=True)

n1.plotly_chart(f.fig_comp_arbitrum_avgsize, use_container_width=True)
n2.plotly_chart(f.fig_comp_arbitrum_numtrades, use_container_width=True)



st.markdown(
    """
    
    ---
    # About

    This dashboard is designed by [@Phi_Deltalytics](https://twitter.com/phi_deltalytics). 
    I hope it serves as a valuable tool for both newcomers and experienced users 
    to gain insights into the Gains Network and other derivative trading platforms on Arbitrum. 
    
    For page source, see [Github](https://github.com/pd123459/GainsNetwork).
    
    
    Any comments and suggestions are welcomed. 
    """
    , unsafe_allow_html=True

    )












