
import streamlit as st
import requests

st.set_page_config(page_title="📋 Kobo Data Viewer")
st.title("📋 Kobo Data Viewer")
st.markdown("Fetch live form data from KoboCollect.")

form_uid = st.text_input("Form UID", "a7FgXyQPmcAEbZxChPKyWF")
username = st.text_input("Kobo Username", "imad479")
password = st.text_input("Kobo Password", type="password")

@st.cache_data(show_spinner=False)
def fetch_kobo_data(form_uid, username, password):
    url = f"https://kc.kobotoolbox.org/api/v2/assets/{form_uid}/data.json"
    try:
        response = requests.get(url, auth=(username, password))
        response.raise_for_status()
        data = response.json()
        return data
    except requests.exceptions.HTTPError as e:
        st.error(f"HTTP Error: {e}")
    except requests.exceptions.RequestException as e:
        st.error(f"Request Failed: {e}")
    except ValueError as e:
        st.error(f"JSON Decoding Failed: {e}")

if st.button("Fetch Data"):
    if not (form_uid and username and password):
        st.warning("Please fill in all the fields.")
    else:
        st.info("Fetching data from KoboCollect...")
        data = fetch_kobo_data(form_uid, username, password)
        if data and "results" in data:
            st.success(f"Fetched {len(data['results'])} records.")
            st.dataframe(data['results'])
        else:
            st.warning("No data found or invalid credentials.")
            

