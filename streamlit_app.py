import streamlit as st
import requests
import pandas as pd

st.set_page_config(page_title="📋 Kobo Data Viewer", layout="wide")

st.title("📋 Public Kobo Data Viewer")
st.markdown("Live data fetched from a public KoboToolbox form.")

# Hardcoded public Form UID (replace this with your actual public UID)
form_uid = "a7FgXyQPmcAEbZxChPKyWF"  # Example UID — replace as needed

# Construct public data URL
url = f"https://kc.kobotoolbox.org/api/v2/assets/{form_uid}/data.json"

try:
    response = requests.get(url)
    response.raise_for_status()

    data = response.json()
    df = pd.json_normalize(data['results'])

    st.success("✅ Live data fetched successfully!")
    st.dataframe(df)

    # Download button
    csv = df.to_csv(index=False).encode('utf-8')
    st.download_button("📥 Download CSV", data=csv, file_name="kobo_data.csv", mime="text/csv")

except requests.exceptions.HTTPError as e:
    st.error(f"Failed to fetch Kobo data: {e}")
except Exception as e:
    st.error(f"An unexpected error occurred: {e}")
