"""
Meta breakdown di un torneo TopDeck.gg alla classifica corrente.

Uso:
    standings = meta_analysis(api_key, tournament_id, site)
    fig       = meta_pie(standings)
    stats     = archetype_stats(standings)
    players   = players_table(standings)
    top_cards = top_cards_by_archetype(standings)
"""

import io
import re

import pandas as pd
import plotly.express as px

from decknames import deck_archetype
from downloadstandings import download_standings

BASIC_LANDS = {
    'plains', 'island', 'swamp', 'mountain', 'forest', 'wastes',
    'snow-covered plains', 'snow-covered island', 'snow-covered swamp',
    'snow-covered mountain', 'snow-covered forest', 'snow-covered wastes',
}

_SECTION_RE = re.compile(r'~~(?:Mainboard|Sideboard)~~')
_LINE_SPLIT_RE = re.compile(r'\\n|\r?\n')
_QTY_RE = re.compile(r'^(\d+)\s*x?\s+(.+)$', re.IGNORECASE)


def meta_analysis(api_key: str, tournament_id: str, site: str) -> pd.DataFrame:
    """Scarica la classifica corrente e assegna l'archetipo a ogni giocatore."""
    csv_str = download_standings(api_key=api_key, tournament_id=tournament_id, site=site)
    standings = pd.read_csv(io.StringIO(csv_str))

    if 'Decklist' not in standings.columns:
        standings['Decklist'] = None
    standings['Decklist'] = standings['Decklist'].fillna("~~Mainboard~~")

    standings['parsed_decklist'] = standings['Decklist'].apply(parse_decklist)
    standings['played_cards'] = standings['parsed_decklist'].apply(lambda row: [name for _, name in row])
    standings['archetype'] = standings['played_cards'].apply(deck_archetype)
    return standings


def parse_decklist(decklist: str) -> list[tuple[int, str]]:
    """Restituisce [(quantità, nome carta lowercase), ...] da una decklist TopDeck."""
    text = _SECTION_RE.sub('', str(decklist)).replace('~', '')
    cards = []
    for line in _LINE_SPLIT_RE.split(text):
        line = re.sub(r'\s+', ' ', line).strip()
        if len(line) <= 1:
            continue
        m = _QTY_RE.match(line)
        qty, name = (int(m.group(1)), m.group(2)) if m else (1, line)
        cards.append((qty, name.strip().lower()))
    return cards


def _clean_text(s: str) -> str:
    return str(s).replace('\\n', '\n').replace("\\'", "'")


def meta_pie(standings: pd.DataFrame):
    counts_pie = standings['archetype'].value_counts().reset_index()
    counts_pie.columns = ['archetype', 'n']
    counts_pie['label'] = counts_pie['archetype'] + ' (' + counts_pie['n'].astype(str) + ')'

    fig_pie = px.pie(
        counts_pie,
        names='label',
        values='n',
        title='Meta Breakdown',
        hole=0.3,
        color_discrete_sequence=px.colors.qualitative.Pastel,
    )
    fig_pie.update_traces(
        textposition='inside',
        textinfo='percent',
        insidetextorientation='radial',
        textfont_size=10,
    )
    fig_pie.update_layout(
        height=750,
        title=dict(font=dict(size=16)),
        legend=dict(
            orientation='v',
            yanchor='top',
            xanchor='left',
            x=0,
            font=dict(size=11),
        ),
        margin=dict(t=60, b=40, l=20, r=20),
    )
    return fig_pie


def archetype_stats(standings: pd.DataFrame) -> pd.DataFrame:
    """Per archetipo: valore assoluto, percentuale sul totale e winrate medio corrente."""
    df = standings.copy()
    if 'Win Rate %' in df.columns:
        df['win_rate_float'] = pd.to_numeric(
            df['Win Rate %'].astype(str).str.rstrip('%'), errors='coerce'
        )
    else:
        df['win_rate_float'] = float('nan')

    stats = (df
             .groupby('archetype')
             .agg(valore_assoluto=('archetype', 'size'),
                  winrate_medio=('win_rate_float', 'mean'))
             .sort_values('valore_assoluto', ascending=False)
             .reset_index()
             .rename(columns={'archetype': 'archetipo'}))
    stats['percentuale'] = (stats['valore_assoluto'] / stats['valore_assoluto'].sum() * 100).round(2)
    stats['winrate_medio'] = stats['winrate_medio'].round(2)
    return stats[['archetipo', 'valore_assoluto', 'percentuale', 'winrate_medio']]


def players_table(standings: pd.DataFrame) -> pd.DataFrame:
    """Classifica con colonne giocatore, archetipo, decklist, winrate."""
    df = standings.sort_values('Posizione') if 'Posizione' in standings.columns else standings
    winrate = df['Win Rate %'] if 'Win Rate %' in df.columns else ''
    return pd.DataFrame({
        'giocatore': df['Nome giocatore'],
        'archetipo': df['archetype'],
        'decklist': df['Decklist'].apply(_clean_text).str.strip(),
        'winrate': winrate,
    }).reset_index(drop=True)


def top_cards_by_archetype(standings: pd.DataFrame, n: int = 10) -> pd.DataFrame:
    """
    Top n carte per archetipo (main + side, terre base escluse).

    Colonne: archetipo, carta, copie (totale copie giocate), mazzi (n. mazzi che
    la giocano), mazzi_archetipo, pct_mazzi.
    """
    rows = [
        (arch, name, qty, idx)
        for idx, arch, deck in zip(standings.index, standings['archetype'], standings['parsed_decklist'])
        for qty, name in deck
        if name not in BASIC_LANDS
    ]
    cols = ['archetipo', 'carta', 'copie', 'mazzi', 'mazzi_archetipo', 'pct_mazzi']
    if not rows:
        return pd.DataFrame(columns=cols)

    cards = pd.DataFrame(rows, columns=['archetipo', 'carta', 'qty', 'deck_id'])
    agg = (cards
           .groupby(['archetipo', 'carta'])
           .agg(copie=('qty', 'sum'), mazzi=('deck_id', 'nunique'))
           .reset_index())
    agg['mazzi_archetipo'] = agg['archetipo'].map(standings['archetype'].value_counts())
    agg['pct_mazzi'] = (agg['mazzi'] / agg['mazzi_archetipo'] * 100).round(1)
    agg['carta'] = agg['carta'].apply(_clean_text)

    return (agg
            .sort_values(['archetipo', 'copie', 'mazzi'], ascending=[True, False, False])
            .groupby('archetipo')
            .head(n)
            .reset_index(drop=True)[cols])
