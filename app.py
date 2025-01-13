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

st.title("💎 Meme Coin Analyzer")
st.markdown("<div style='color: #f85149;'>⚠️ Don't risk more than 30% of your net worth on a meme coin!</div>", unsafe_allow_html=True)

# Function to get data from Dexscreener
def fetch_data(pair_address):
    url = f"https://api.dexscreener.com/latest/dex/tokens/{pair_address}"
    response = requests.get(url)
    if response.status_code == 200:
        return response.json()
    else:
        return None

# Input Section
pair_address = st.text_input("Enter the Solana token contract address:", placeholder="Example: 9k5p...")

if st.button("Analyze Token"):
    if pair_address:
        # Fetch data from API
        data = fetch_data(pair_address)
        
        if data and "pairs" in data and len(data["pairs"]) > 0:
            # Extract the first pair data
            token_data = data["pairs"][0]

            # Display Token Metrics
            st.subheader("📊 Token Metrics")
            st.write(f"**Token Name:** {token_data.get('baseToken', {}).get('name', 'N/A')}")
            st.write(f"**Market Cap (MC):** ${token_data.get('marketCap', 'N/A')}")
            st.write(f"**Fully Diluted Valuation (FDV):** ${token_data.get('fdv', 'N/A')}")
            st.write(f"**Price:** ${token_data.get('priceUsd', 'N/A')}")
            st.write(f"**Liquidity:** ${token_data.get('liquidity', {}).get('usd', 'N/A')}")
            
            # Buyers and Sellers
            st.subheader("📉 Trading Activity")
            st.write(f"**Buyers:** {token_data.get('txns', {}).get('h24', {}).get('buys', 'N/A')}")
            st.write(f"**Sellers:** {token_data.get('txns', {}).get('h24', {}).get('sells', 'N/A')}")

            # Display Chart
            st.subheader("📊 Price Action Chart")
            st.line_chart(
                pd.DataFrame(
                    {
                        "Time": ["T-3", "T-2", "T-1", "Now"],
                        "Price": [
                            token_data.get("priceUsd", 0.001) * (1 + x / 10)
                            for x in range(-3, 1)
                        ],
                    }
                )
            )
        else:
            st.error("No token data found for the provided address. Ensure the address is correct and belongs to a supported Solana token.")
    else:
        st.warning("Please enter a valid token pair address.")
