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
        
        L2’s high speed and low gas provide an excellent venue for on-chain derivatives trading, and now L2 has become the main battlefield for trading derivatives.
        
        This dashboard analyses the decentralized derivative trading platform Gains Network, the impact of its Arbitrum launch,
        and comparisons between Gains Network and its competitors.         
        
        
""")



st.markdown(
    """
    
    ---
    # Methodology 
    
    Data is drawn from [Flipside Crypto](https://flipsidecrypto.xyz/). 
    
    """
    f'For Flipside data, links to the underlying queries are provided in the wrench icon ({icons.setting_icon})'
   
    """
    next to chart and table tiles.
    
    
    """
    , unsafe_allow_html=True
)

st.markdown(
    f"""
    ---
    # Gains Network User Key Statistics
    
    With the Arbitrum launch, Gains Network experienced a surge in trading activities, and exceeded daily 
    post leverage trading volume of $200mil. The recent [trading competition](https://twitter.com/GainsNetwork_io/status/1616468328956022784)
    on Gains Arbitrum chain could also be a potential driver of the increase in trading activities. 
    
    
    """
    , unsafe_allow_html=True
)


st.markdown(f'#### Daily Trading Volume on Gains Network [{icons.setting_icon}](https://next.flipsidecrypto.xyz/edit/queries/3f52b4f5-28c8-4a43-bfe8-684169762005/visualizations/0d283bac-2601-469f-ad93-705e0dfefbc2)', unsafe_allow_html=True)
st.write(
    """*Total derivative trading volume on the Gains Network per day. Split by chain used.* """)
st.plotly_chart(f.fig_gains_vol, use_container_width=True)

st.markdown(f'#### Daily Unique Users on Gains Network [{icons.setting_icon}](https://next.flipsidecrypto.xyz/edit/queries/3f52b4f5-28c8-4a43-bfe8-684169762005/visualizations/0d283bac-2601-469f-ad93-705e0dfefbc2)', unsafe_allow_html=True)
st.write(
    """*Total number of unique users who traded on the Gains Network per day. Split by chain used.* """)
st.plotly_chart(f.fig_gains_user, use_container_width=True)

st.markdown(f'#### Daily Number of trades on Gains Network [{icons.setting_icon}](https://next.flipsidecrypto.xyz/edit/queries/3f52b4f5-28c8-4a43-bfe8-684169762005/visualizations/0d283bac-2601-469f-ad93-705e0dfefbc2)', unsafe_allow_html=True)
st.write(
    """*Total number of trades that use the Gains Network per day. Split by chain used.* """)
st.plotly_chart(f.fig_gains_trx, use_container_width=True)


st.markdown(
    """
    ---
    # Competitor Key Statistics
    
    """
)

st.markdown(f'#### Daily Trading Volume on GMX [{icons.setting_icon}](https://next.flipsidecrypto.xyz/edit/queries/3f52b4f5-28c8-4a43-bfe8-684169762005/visualizations/0d283bac-2601-469f-ad93-705e0dfefbc2)', unsafe_allow_html=True)
st.write(
    """*Total derivative trading volume on GMX per day. Split by chain used.* """)
st.plotly_chart(f.fig_gmx_vol, use_container_width=True)

st.markdown(f'#### Daily Unique Users on GMX [{icons.setting_icon}](https://next.flipsidecrypto.xyz/edit/queries/3f52b4f5-28c8-4a43-bfe8-684169762005/visualizations/0d283bac-2601-469f-ad93-705e0dfefbc2)', unsafe_allow_html=True)
st.write(
    """*Total number of unique users who traded on GMX per day. Split by chain used.* """)
st.plotly_chart(f.fig_gmx_user, use_container_width=True)

st.markdown(f'#### Daily Number of trades on Gains Network [{icons.setting_icon}](https://next.flipsidecrypto.xyz/edit/queries/3f52b4f5-28c8-4a43-bfe8-684169762005/visualizations/0d283bac-2601-469f-ad93-705e0dfefbc2)', unsafe_allow_html=True)
st.write(
    """*Total number of trades that use the GMX per day. Split by chain used.* """)
st.plotly_chart(f.fig_gmx_trx, use_container_width=True)


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












