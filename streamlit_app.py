import streamlit as st
import requests
import pandas as pd

st.set_page_config(page_title="Kobo Data Viewer", layout="wide")

st.title("📋 Kobo Data Viewer")
st.markdown("Fetch live form data from KoboCollect (public forms only).")

# User input: Form UID
form_uid = st.text_input("Enter Kobo Form UID", value="", help="You can find this in the form URL or Kobo project settings.")

# Display data when UID is provided
if form_uid:
    # Construct the public URL
    url = f"https://kc.kobotoolbox.org/api/v2/assets/{form_uid}/data.json"

    try:
        response = requests.get(url)
        response.raise_for_status()

        # Convert JSON to DataFrame
        data = response.json()
        df = pd.json_normalize(data['results'])

        st.success("✅ Data fetched successfully!")
        st.dataframe(df)

        # Optional: Download option
        csv = df.to_csv(index=False).encode('utf-8')
        st.download_button("📥 Download CSV", data=csv, file_name="kobo_data.csv", mime="text/csv")

    except requests.exceptions.HTTPError as e:
        st.error(f"Failed to fetch Kobo data: {e}")
    except Exception as e:
        st.error(f"An unexpected error occurred: {e}")
else:
    st.info("👈 Enter a valid Kobo Form UID to view data.")
