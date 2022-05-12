import streamlit as st
import json
import pandas as pd
import snowflake.connector
import matplotlib

"""
# Blues Tracker Demo!

This demo pulls data from Snowflake that was routed from [this Notehub project](https://notehub.io/project/app:6e153550-c690-4a7d-ba00-ed6056138574).

The application in question is a Notecard and Notecarrier-F-based asset tracker. In addition to
being configured as a tracker, the Swan-powered host application takes readings from connected
environmental sensors that capture temperature, humidity, altitude, pressure, CO2 and TVOCs.

Raw JSON is routed to Snowflake using the Snowflake SQL API and transformed into
a structured data tables using views, with a view for `_track.qo`, `air.qo`, and `env.qo`
events.

"""

"""
### Options
"""

with st.echo(code_location='below'):
    #num_rows = st.slider('Rows to fetch?', 1, 50, 30)
    #sort = st.selectbox('Sort?',('asc', 'desc'))

    # Initialize connection.
    @st.experimental_singleton
    def init_connection():
        return snowflake.connector.connect(**st.secrets["snowflake"])

    conn = init_connection()

    # Perform query.
    @st.experimental_memo(ttl=600)
    def run_query(query):
        with conn.cursor() as cur:
            cur.execute(query)
            return cur.fetchall()

    """
    ## Notecard `_track.qo` Events
    """

    tracker_rows = run_query(f'SELECT * from tracker_vw ORDER BY created;')

    tracker_data = pd.DataFrame(tracker_rows, columns=("ID", "Device", "When", "Loc", "lat", "lon", "Location", "Location Type", "Timezone", "Country", "Temp", "Voltage"))
    tracker_data[tracker_data.columns[::-1]]

    """
    ## Notecard `air.qo` Events
    """

    air_rows = run_query(f'SELECT * from air_vw ORDER BY created;')

    air_data = pd.DataFrame(air_rows, columns=("Device", "When", "Loc", "Lat", "Lon", "Location", "Location Type", "Timezone", "Country", "CO2", "TVOC"))
    air_data[air_data.columns[::-1]]

    """
    ## Notecard `env.qo` Events
    """

    env_rows = run_query(f'SELECT * from env_vw ORDER BY created;')

    env_data = pd.DataFrame(env_rows, columns=("Device", "When", "Loc", "Lat", "Lon", "Location", "Location Type", "Timezone", "Country", "Temp", "Humidity", "Pressure", "Altitude"))
    env_data[env_data.columns[::-1]]

    """
    ### Environment Charts
    """

    air_group = air_data[["CO2","TVOC"]]

    st.line_chart(air_group)

    env_group = env_data[["Temp", "Humidity", "Pressure", "Altitude"]]

    st.line_chart(env_group)

    """
    ### Tracker Charts
    """

    tracker_locations = tracker_data[["lat", "lon"]]

    st.map(tracker_locations)