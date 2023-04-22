
import streamlit as st

import pandas as pd 
import numpy as np
import requests
import warnings
warnings.filterwarnings('ignore')

st.set_page_config(
    page_title='Akku-Option Chain',
    layout='wide'
)

st.title("Option Chain")

col1,col2,col3=st.columns(3)
with col1:
    nam=st.selectbox('Symbol',('NIFTY','BANKNIFTY','FINNIFTY'))
with col2:
    date=st.text_input("ExpiryDate")
with col3:
    sprice=st.number_input("Strike Price")
if st.button("Get Chain"):
    sesi=requests.Session()
    headers={}
    headers['User-agent']='Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/112.0.0.0 Safari/537.36'
    a=sesi.get("https://www.nseindia.com/",headers=headers)

    indices=['BANKNIFTY','FINNIFTY','NIFTY']

    def Fetchoptionchain(scrip):
        if scrip in indices:
            url=f"https://www.nseindia.com/api/option-chain-indices?symbol={scrip}"
        a=sesi.get(url,headers=headers)
        return a.json()['records']
        
    q=Fetchoptionchain(nam)


    def getoptionchain(name,expiry):
        option_chain = pd.DataFrame()
        option_chain_record = name
        option_chain_data = option_chain_record["data"]
        
        optionchain_data_df = pd.DataFrame(option_chain_data)
        option_chain_data_df = optionchain_data_df[optionchain_data_df['expiryDate']==expiry]

        
        OptionChain_CE = pd.DataFrame()
        OptionChain_CE['CE'] = option_chain_data_df['CE']
        
        OptionChain_CE_expand = pd.concat([OptionChain_CE.drop(['CE'],axis=1),
                                            OptionChain_CE['CE'].apply(pd.Series)],axis=1)
        
        OptionChain_PE = pd.DataFrame()
        OptionChain_PE['PE'] = option_chain_data_df['PE']
        
        
        OptionChain_PE_expand = pd.concat([OptionChain_PE.drop(['PE'],axis=1),
                                            OptionChain_PE['PE'].apply(pd.Series)],axis=1)

        
        option_chain['CE_OI'] = OptionChain_CE_expand['openInterest']
    
        option_chain['CE_CHNG_IN_OI'] = OptionChain_CE_expand['changeinOpenInterest']
        
        option_chain['CE_VOLUME'] = OptionChain_CE_expand['totalTradedVolume']

        option_chain['CE_IV'] = OptionChain_CE_expand['impliedVolatility']
    
        option_chain['CE_LTP'] = OptionChain_CE_expand['lastPrice']

        option_chain['CE_CHNG'] = OptionChain_CE_expand['change'] 
        
        option_chain['CE_BID_QTY'] = OptionChain_CE_expand['bidQty']

        option_chain['strikePrice'] = option_chain_data_df['strikePrice']

        option_chain['PE_BID_OTY'] = OptionChain_PE_expand['bidQty']

        option_chain['EPE_CHING'] = OptionChain_PE_expand['change']

        option_chain['PE_LTP'] = OptionChain_PE_expand['lastPrice']

        option_chain['PE_IV'] = OptionChain_PE_expand['impliedVolatility'] 
        
        option_chain['PE_VOLUME'] = OptionChain_PE_expand['totalTradedVolume']

        option_chain['PE_CHNG_IN_OI'] = OptionChain_PE_expand['changeinOpenInterest']
        
        option_chain['PE_OI'] = OptionChain_PE_expand['openInterest']
        
        return option_chain


    option_chain1 = getoptionchain(q,date)


    option_chain1.reset_index(inplace = True)

    a=list(option_chain1['strikePrice'])
    b=pd.DataFrame(columns=['index','CE_OI','CE_CHNG_IN_OI','CE_VOLUME','CE_IV','CE_LTP','CE_CHNG','CE_BID_QTY','strikePrice','PE_BID_OTY',
                        'EPE_CHING','PE_LTP','PE_IV','PE_VOLUME','PE_CHNG_IN_OI','PE_OI'])
    for i in a:
        if (i % 500) == 0:
            dff = int(option_chain1[option_chain1['strikePrice']==i].index[0])
            c=option_chain1.iloc[dff,]
            b = b.append(c,ignore_index = True)


    sp=sprice

    ind_lower= int(b[b['strikePrice']==sp].index[0])
    q=b.iloc[ind_lower-6:ind_lower-1]

    df = int(option_chain1[option_chain1['strikePrice']==sp].index[0])
    r=option_chain1.iloc[df-5:df+6]

    ind_upper= int(b[b['strikePrice']==sp].index[0])
    s=b.iloc[ind_upper+2:ind_upper+7]

    t=q.append(r,ignore_index = True)
    Final_chain=t.append(s,ignore_index = True)

    pd.set_option('display.max_rows', None)
    # st.write(Final_chain,200,800,)
    st.dataframe(Final_chain,12000,800)
