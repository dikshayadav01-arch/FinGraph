import requests
import streamlit as st
import pandas as pd


API_URL = "http://127.0.0.1:8000"


st.set_page_config(
    page_title="FinGraph | Fraud Intelligence",
    page_icon="🔎",
    layout="wide",
)


st.title("🔎 FinGraph")
st.subheader("Real-Time Fraud Syndicate Analytics")

if st.button("🔄 Refresh Detection Results"):
    st.rerun()

st.markdown(
    """
    **FinTech & AML Investigation Dashboard**

    Detect suspicious transaction networks using Starburst,
    Smurfing, and Circular transaction patterns.
    """
)


def fetch_data(endpoint):
    try:
        response = requests.get(
            f"{API_URL}{endpoint}",
            timeout=10
        )
        response.raise_for_status()
        return response.json()
    except requests.exceptions.RequestException as error:
        st.error(f"API connection failed: {error}")
        return []


# Fetch fraud detection results
starburst = fetch_data("/fraud/starburst")
smurfing = fetch_data("/fraud/smurfing")
circular = fetch_data("/fraud/circular")


# -----------------------------
# KPI SECTION
# -----------------------------

starburst_count = len(starburst)
smurfing_count = len(smurfing)
circular_count = len(circular)

total_alerts = (
    starburst_count +
    smurfing_count +
    circular_count
)

starburst_amount = sum(
    item.get("totalAmount", 0)
    for item in starburst
)

smurfing_amount = sum(
    item.get("totalAmount", 0)
    for item in smurfing
)

total_detected_exposure = (
    starburst_amount +
    smurfing_amount
)

col1, col2, col3, col4, col5 = st.columns(5)

with col1:
    st.metric(
        "Total Alerts",
        total_alerts,
        icon="🚨",
        border=True,
    )

with col2:
    st.metric(
        "Starburst",
        starburst_count,
        icon="⭐",
        border=True,
    )

with col3:
    st.metric(
        "Smurfing",
        smurfing_count,
        icon="💰",
        border=True,
    )

with col4:
    st.metric(
        "Circular",
        circular_count,
        icon="🔄",
        border=True,
    )

with col5:
    st.metric(
        "Detected Exposure",
        f"₹{total_detected_exposure:,.2f}",
        icon="💰",
        border=True,)

st.divider()

st.header("📊 Fraud Pattern Overview")

pattern_data = pd.DataFrame(
    {
        "Fraud Pattern": [
            "Starburst",
            "Smurfing",
            "Circular",
        ],
        "Alerts": [
            starburst_count,
            smurfing_count,
            circular_count,
        ],
    }
)

st.bar_chart(
    pattern_data.set_index("Fraud Pattern")
)

# -----------------------------
# DETECTION TABS
# -----------------------------

tab1, tab2, tab3 = st.tabs(
    [
        "⭐ Starburst Detection",
        "💰 Smurfing Detection",
        "🔄 Circular Detection",
    ]
)


with tab1:

    st.header("Starburst Fraud Detection")

    if starburst:

        df = pd.DataFrame(starburst)

        df = df.rename(
            columns={
                "suspiciousReceiver": "Suspicious Receiver",
                "uniqueSenders": "Unique Senders",
                "totalAmount": "Total Amount (₹)",
            }
        )

        st.dataframe(
            df,
            width="stretch",
            hide_index=True,
        )

        st.bar_chart(
            df.set_index("Suspicious Receiver")[
                "Unique Senders"
            ]
        )

    else:
        st.success("No Starburst patterns detected.")


with tab2:

    st.header("Smurfing Fraud Detection")

    if smurfing:

        df = pd.DataFrame(smurfing)

        df = df.rename(
            columns={
                "targetAccount": "Target Account",
                "uniqueSenders": "Unique Senders",
                "transactionCount": "Transaction Count",
                "totalAmount": "Total Amount (₹)",
            }
        )

        st.dataframe(
            df,
            width="stretch",
            hide_index=True,
        )

        st.bar_chart(
            df.set_index("Target Account")[
                "Transaction Count"
            ]
        )

    else:
        st.success("No Smurfing patterns detected.")


with tab3:

    st.header("Circular Fraud Detection")

    if circular:

        for index, cycle in enumerate(circular, start=1):

            st.markdown(f"### 🔄 Circular Pattern {index}")

            accounts = cycle.get("accounts", [])
            amounts = cycle.get("amounts", [])

            st.write(
                " → ".join(accounts)
            )

            cycle_df = pd.DataFrame(
                {
                    "Account": accounts[:-1],
                    "Amount (₹)": amounts,
                }
            )

            st.dataframe(
                cycle_df,
                width="stretch",
                hide_index=True,
            )

    else:
        st.success("No Circular patterns detected.")


st.divider()


# -----------------------------
# SYSTEM STATUS
# -----------------------------

st.header("System Status")

st.header("🕵️ Investigation Summary")

st.info(
    f"""
    FinGraph detected **{total_alerts} suspicious patterns** across
    Starburst, Smurfing, and Circular transaction activity.

    The investigation engine identified **{starburst_count} Starburst**,
    **{smurfing_count} Smurfing**, and **{circular_count} Circular**
    patterns.

    Current detected exposure across the available detection results:
    **₹{total_detected_exposure:,.2f}**
    """
)

status_col1, status_col2 = st.columns(2)

with status_col1:
    try:
        health_response = requests.get(
            f"{API_URL}/health",
            timeout=5
        )

        if health_response.ok:
            st.success("🟢 Investigation API: Connected")
        else:
            st.error("🔴 Investigation API: Unavailable")

    except requests.exceptions.RequestException:
        st.error("🔴 Investigation API: Unavailable")


with status_col2:
    if starburst or smurfing or circular:
        st.success("🟢 Neo4j Detection Engine: Connected")
    else:
        st.warning("🟡 Neo4j Detection Engine: No detections")


st.caption(
    "FinGraph — Real-Time Fraud Syndicate Analytics | "
    "Kafka → Flink → Neo4j → FastAPI → Streamlit"
)