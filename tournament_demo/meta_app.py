import sys
import streamlit as st

sys.path.insert(0, ".")
from meta_analysis import (
    archetype_stats,
    meta_analysis,
    meta_pie,
    players_table,
    top_cards_by_archetype,
)

st.set_page_config(page_title="Meta Breakdown", layout="wide")
st.title("Meta Breakdown — TopDeck.gg")

# API key da Streamlit Secrets (non visibile nel codice)
api_key = st.secrets["api_key"]

with st.form("params"):
    tournament_id = st.text_input(
        "Tournament ID",
        value="thesideralwolf-tournament-series-pauper-4",
    )
    site = st.text_input("Sito", value="https://topdeck.gg")
    submitted = st.form_submit_button("Aggiorna")


@st.cache_data(show_spinner=False, ttl=60)
def run_analysis(api_key, tournament_id, site):
    return meta_analysis(api_key, tournament_id, site)


if submitted:
    # i parametri restano in sessione, così cambiare archetipo non resetta la pagina
    st.session_state["params"] = (tournament_id, site)
    run_analysis.clear()

if "params" in st.session_state:
    tournament_id, site = st.session_state["params"]
    with st.spinner("Scaricando classifica..."):
        try:
            standings = run_analysis(api_key, tournament_id, site)
        except Exception as e:
            st.error(f"Errore durante il download: {e}")
            st.stop()

    st.plotly_chart(meta_pie(standings), use_container_width=True)

    st.subheader("Statistiche archetipi")
    stats = archetype_stats(standings)
    st.dataframe(stats, use_container_width=True)
    st.download_button(
        "Scarica CSV archetipi",
        data=stats.to_csv(index=False).encode("utf-8-sig"),
        file_name=f"{tournament_id}_archetipi.csv",
        mime="text/csv",
    )

    st.subheader("Classifica")
    players = players_table(standings)
    st.dataframe(players, use_container_width=True)
    st.download_button(
        "Scarica CSV classifica",
        data=players.to_csv(index=False).encode("utf-8-sig"),
        file_name=f"{tournament_id}_classifica.csv",
        mime="text/csv",
    )

    st.subheader("Top 10 carte per archetipo (terre base escluse)")
    top_cards = top_cards_by_archetype(standings, n=10)
    archetypes = standings["archetype"].value_counts().index.tolist()
    archetype = st.selectbox("Archetipo", archetypes)
    st.dataframe(
        top_cards[top_cards["archetipo"] == archetype].drop(columns="archetipo").reset_index(drop=True),
        use_container_width=True,
    )
    st.download_button(
        "Scarica CSV top carte",
        data=top_cards.to_csv(index=False).encode("utf-8-sig"),
        file_name=f"{tournament_id}_top_carte.csv",
        mime="text/csv",
    )
