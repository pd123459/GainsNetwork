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
        
        This dashboard analyses ...
        
        Background paragraph: (why on-chain derivatives platform)
        参考"foreword" - https://foresightnews.pro/article/detail/17593
        
        #### **Key takeaways:**
        
        1. 
        
        2.  
        
        3. 
        
""")
st.markdown(
    f'####  GNS Token Price{gap}{gap}[{icons.setting_icon}](https://app.flipsidecrypto.com/velocity/queries/860f8493-6bad-45a6-98b0-d76d587dc1c3)', unsafe_allow_html=True
)
st.write("""*The price of the $GNS token. Currency in USD.*""")
st.plotly_chart(f.fig_hist_prc, use_container_width=True)


st.markdown(
    """
    
    ---
    # Methodology 
    
    Data is drawn from [Flipside Crypto](https://flipsidecrypto.xyz/)'s Solana tables. 
    
    """
    f'For Flipside data, links to the underlying queries are provided in the wrench icon ({icons.setting_icon})'
   
    """
    next to chart and table tiles.
    
    
    """
    , unsafe_allow_html=True
)

st.markdown(
    """
    ---
    # Gains Network User Key Statistics

    1.1 daily trade vol (by Type: crypto; forex; stock, etc)
        --> add cum vol month & 3 month
        --> may be due to trading comp https://twitter.com/GainsNetwork_io/status/1616468328956022784
        
    1.2 daily traders 
        --> add cum traders month & 3 month
        
    2.1 daily fees （可以偷个懒，按上面的type）
    
    2.2 OI (by Type)
    
    ---
    # Gains Network Liquidity Provider Key Statistics
    
    1. TVL (gDAI) [Poly vs. arbitrum]
    
    2. APR (gDAI) [Poly vs. arbitrum]
    
    3. Collat Ratio (gDAI) [Poly vs. arbitrum]
    
    
    """
)

'''
st.markdown(f'#### Daily Active Whirlpools [{icons.setting_icon}](https://app.flipsidecrypto.com/velocity/queries/860f8493-6bad-45a6-98b0-d76d587dc1c3)', unsafe_allow_html=True)
st.write(
    """*The number of Orca Whirlpools that have active transactions per day.* """)
st.plotly_chart(f.fig_pool_count, use_container_width=True)

st.markdown(
    """
    
    
    """
)
'''

st.markdown(
    """
    ---
    # Competitor Key Statistics
        same as above "User Key statistics"
        
    GMX (Arbitrum)
    
    
    Metavault.trade (Poly)
    
    
    
    Mycelium Perpetual Swaps (Arbitrum)
    
    
    """
)


st.markdown(
    """
    ---
    # A Comparison of Daily Users
    
    ---
    # A Comparison of Transaction Volume
    
    ---
    # A Comparison of Transaction Fees 
    
    
    - Overview (TBD - add to description and analysis)
        1. Chain
        2. Assets --> crypto; forex; stocks
        3. Highest leverage
        4. Functionalities - stop-loss
        
    """
)

st.markdown(
    """
    
    ---
    # About

    This dashboard is designed by [@Phi_Deltalytics](https://twitter.com/phi_deltalytics). 
    I hope it serves as a valuable tool for both newcomers and experienced users 
    to gain insights into the Orca Whirlpools. 
    
    For page source, see [Github](https://github.com/pd123459/Orca-Whirlpools).
    
    
    Any comments and suggestions are welcomed. 
    """
    , unsafe_allow_html=True

    )












