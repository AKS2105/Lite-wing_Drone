import streamlit as st
import pandas as pd
import plotly.express as px
from streamlit_autorefresh import st_autorefresh
from streamlit_option_menu import option_menu

st.set_page_config(
    page_title="LiteWing Fire Detection System",
    page_icon="🚁",
    layout="wide"
)

st_autorefresh(interval=1000, key="refresh")

with st.sidebar:
    selected = option_menu(
        "LiteWing",
        ["Dashboard", "Telemetry", "Smoke Analytics"],
        icons=["speedometer2", "broadcast", "fire"],
        default_index=0,
    )

st.title("🚁 LiteWing Fire Detection Dashboard")

data = {}
if "smoke_history" not in st.session_state:
    st.session_state.smoke_history = []


try:
    with open("data.txt", "r") as f:
        lines = f.readlines()

    for line in lines:
        line = line.strip()

        if "=" not in line:
            continue

        key, value = line.split("=", 1)

        if key == "SMOKE":
            st.session_state.smoke_history.append(float(value))
            data["SMOKE"] = float(value)

        elif key == "BAT":
            pass

        else:
            data[key] = value

except Exception:
    pass

if selected == "Dashboard":

    st.subheader("Live Flight Status")

    c1, c2, c3, c4 = st.columns(4)

    c1.metric("Roll", data.get("ROLL", "--"))
    c2.metric("Pitch", data.get("PITCH", "--"))
    c3.metric("Yaw", data.get("YAW", "--"))
    c4.metric("Thrust", data.get("THRUST", "--"))

    c5, c6, c7, c8 = st.columns(4)

    c5.metric("Battery", "3.7 V")
    c6.metric("Smoke", data.get("SMOKE", "--"))
    c7.metric("Altitude", data.get("ALTITUDE", "--"))
    c8.metric("Mode", data.get("FLIGHT_MODE", "MANUAL"))

    st.divider()

    
    st.subheader("🔥 Smoke Trend")

    

    if st.session_state.smoke_history:
      smoke_df = pd.DataFrame(
        {"Smoke": st.session_state.smoke_history[-100:]}
    )

    fig = px.line(
        smoke_df,
        y="Smoke",
        title="Smoke Level"
    )

    st.plotly_chart(
        fig,
        use_container_width=True
    )


    st.divider()

    smoke = float(data.get("SMOKE", 0))

    if smoke > 0.40:
        st.error("🚨 FIRE / SMOKE DETECTED")
    else:
        st.success("✅ ENVIRONMENT NORMAL")

elif selected == "Telemetry":

    st.subheader("Raw Telemetry")
    st.json(data)

elif selected == "Smoke Analytics":

    st.subheader("Smoke Analysis")

    if st.session_state.smoke_history:

        avg_smoke = (
            sum(st.session_state.smoke_history)
            / len(st.session_state.smoke_history)
        )

        st.metric(
            "Average Smoke Level",
            f"{avg_smoke:.2f}"
        )

        st.metric(
            "Maximum Smoke Level",
            max(st.session_state.smoke_history)
        )

        st.metric(
            "Current Smoke Level",
            st.session_state.smoke_history[-1]
        )

        