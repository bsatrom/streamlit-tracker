import streamlit as st
import json
import pandas as pd
import snowflake.connector
import matplotlib

"""
# Blues Tracker Demo!

This demo pulls data from Snowflake that was routed from [this Notehub project](https://notehub.io/project/app:7580945e-58ae-424c-b254-5ec55ee2eeff/).

Each button press on a connected host is sent to the Notecard as a `note.add` with
the OS running on the Host MCU and a count of presses since last restart.

```json
{"req":"note.add","sync":true,"body":{"os":"zephyr","button_count":16}}
```

Raw JSON is routed to Snowflake using the Snowflake SQL API and transformed into
a structured data table using a view.

"""