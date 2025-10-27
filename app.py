import streamlit as st
import requests

# --- App Title ---
st.set_page_config(page_title="Qur'an App", page_icon="📖", layout="wide")
st.title("📖 Qur'an App")
st.markdown("Explore the Holy Qur'an with Arabic text, translation, and recitation.")

# --- API Base URL ---
API_BASE = "https://api.alquran.cloud/v1"

# --- Load Surah List ---
@st.cache_data
def get_surah_list():
    response = requests.get(f"{API_BASE}/surah")
    if response.status_code == 200:
        return response.json()["data"]
    else:
        st.error("Failed to load Surah list.")
        return []

surahs = get_surah_list()

# --- Surah Selector ---
surah_names = [f"{s['number']}. {s['englishName']} ({s['englishNameTranslation']})" for s in surahs]
selected_surah = st.selectbox("Select a Surah:", surah_names)

if selected_surah:
    surah_number = int(selected_surah.split(".")[0])
    
    # --- Fetch Surah Data ---
    @st.cache_data
    def get_surah_data(number):
        url = f"{API_BASE}/surah/{number}/en.asad"  # English translation by Muhammad Asad
        response = requests.get(url)
        if response.status_code == 200:
            return response.json()["data"]
        else:
            st.error("Failed to load Surah details.")
            return None

    surah_data = get_surah_data(surah_number)
    
    if surah_data:
        st.subheader(f"{surah_data['englishName']} ({surah_data['englishNameTranslation']})")
        st.markdown(f"**Revelation Place:** {surah_data['revelationType']}")
        st.markdown(f"**Total Ayahs:** {surah_data['numberOfAyahs']}")
        st.divider()
        
        # --- Display Each Ayah ---
        for ayah in surah_data["ayahs"]:
            st.markdown(f"### {ayah['numberInSurah']}. {ayah['text']}")
            if "edition" in ayah and ayah["edition"]["identifier"] == "en.asad":
                st.markdown(f"**Translation:** {ayah['text']}")
            else:
                st.markdown(f"**Arabic:** {ayah['text']}")
            
            # Fetch Arabic text separately for clarity
            arabic_resp = requests.get(f"{API_BASE}/ayah/{ayah['number']}/ar.alafasy")
            if arabic_resp.status_code == 200:
                arabic_data = arabic_resp.json()["data"]
                st.markdown(f"**Arabic:** {arabic_data['text']}")
                if "audio" in arabic_data:
                    st.audio(arabic_data["audio"])
            
            st.divider()
