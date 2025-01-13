import streamlit as st
import requests
import pandas as pd

# App Title and Custom Theme
st.set_page_config(
    page_title="Meme Coin Analyzer",
    page_icon="💎",
    layout="centered",
    initial_sidebar_state="collapsed",
)
st.markdown(
    """
    <style>
    body {
        background-color: #0d1117;
        color: #c9d1d9;
    }
    h1, h2, h3, h4, h5, h6 {
        color: #58a6ff;
    }
    .stButton > button {
        background-color: #161b22;
        color: #58a6ff;
        border: 2px solid #58a6ff;
        border-radius: 5px;
        padding: 5px 10px;
    }
    .stButton > button:hover {
        background-color: #58a6ff;
        color: #0d1117;
    }
    .reminder {
        background-color: #161b22;
        border-radius: 5px;
        padding: 10px;
        margin: 20px 0;
        color: #f85149;
    }
    </style>
    """,
    unsafe_allow_html=True,
)

# App Header
st.title("💎 Meme Coin Analyzer")
st.subheader("Analyze meme coins and make smarter decisions!")
st.markdown("<div class='reminder'>⚠️ Don't risk more than 30% of your net worth on a meme coin!</div>", unsafe_allow_html=True)

# Function to get data from Dexscreener
def fetch_data(pair_address):
    url = f"https://api.dexscreener.com/latest/dex/tokens/{pair_address}"
    response = requests.get(url)
    if response.status_code == 200:
        return response.json()
    else:
        st.error("Failed to fetch data. Please check the address or try again.")
        return None

# Input Section
pair_address = st.text_input("Enter the Solana token pair address:", placeholder="Example: 9k5p...")

if st.button("Analyze Token"):
    if pair_address:
        data = fetch_data(pair_address)
        if data:
            token_data = data.get("pair", {})
            if token_data:
                # Token Metrics
                st.subheader("📊 Token Metrics")
                st.write(f"**Token Name:** {token_data.get('baseToken', {}).get('name', 'N/A')}")
                st.write(f"**Market Cap (MC):** ${token_data.get('marketCap', 'N/A'):,}")
                st.write(f"**Fully Diluted Valuation (FDV):** ${token_data.get('fdv', 'N/A'):,}")
                st.write(f"**Circulating Supply:** {token_data.get('circulatingSupply', 'N/A'):,}")
                st.write(f"**Liquidity:** ${token_data.get('liquidity', 'N/A'):,}")

                # Sentiment Analysis Placeholder
                st.subheader("📈 Sentiment Analysis (Coming Soon!)")
                st.write("Sentiment analysis and community trends will be integrated in future updates.")

                # Advanced Insights
                st.subheader("🤔 Is This a Good Buy?")
                if token_data.get("marketCap") and token_data.get("fdv"):
                    mc = token_data.get("marketCap")
                    fdv = token_data.get("fdv")
                    ratio = mc / fdv if fdv > 0 else 0
                    if ratio > 0.7:
                        st.write("💎 **Bullish:** High percentage of tokens are in circulation.")
                    elif ratio > 0.3:
                        st.write("⚠️ **Neutral:** Significant tokens remain locked.")
                    else:
                        st.write("🔻 **Bearish:** High dilution risk; approach with caution.")
                else:
                    st.write("Insufficient data to provide an analysis.")

                # Trading Insights
                st.subheader("📉 Trading Insights")
                st.write(f"**Buyers:** {token_data.get('buyers', 'N/A')}")
                st.write(f"**Sellers:** {token_data.get('sellers', 'N/A')}")

                # Price Action Chart (Mock)
                st.subheader("📊 Price Action Chart")
                st.line_chart(
                    pd.DataFrame(
                        {
                            "Time": ["T-3", "T-2", "T-1", "Now"],
                            "Price": [
                                token_data.get("price", 0.001) * (1 + x / 10)
                                for x in range(-3, 1)
                            ],
                        }
                    )
                )
            else:
                st.warning("No token data found for the provided address.")
        else:
            st.error("Failed to fetch token data.")
    else:
        st.warning("Please enter a valid token pair address.")

# Footer
st.markdown("<div class='reminder'>⚡ Built for meme coin enthusiasts!</div>", unsafe_allow_html=True)
