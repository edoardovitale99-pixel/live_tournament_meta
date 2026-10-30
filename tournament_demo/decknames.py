"""
Classificazione archetipi MTG Pauper da decklist.

Uso:
    from decknames import deck_archetype
    deck_archetype(['lightning bolt', 'guttersnipe', 'mountain'])  # → 'Red Madness'

Regole in ARCHETYPES: processate in ordine, prima che fa match vince.
  'all': tutte queste carte devono essere presenti
  'any': almeno una di queste deve essere presente
"""

ARCHETYPES = [
    # ── Combo ─────────────────────────────────────────────────────────────────
    {'name': 'Spy Combo',         'all': ['balustrade spy', 'dread return']},
    {'name':'Walls Combo',        'all': ['axebane guardian', 'overgrown battlement']},
    {'name':'Cycle Storm',        'all':['songs of the damned', 'reaping the graves']},
    {'name': 'Poison Storm',      'all': ['infectious inquiry', 'contentious plan']},
    # ── Gates ─────────────────────────────────────────────────────────────────
    {'name': 'Caw-Gate',          'all': ['basilisk gate', 'citadel gate', 'brainstorm']},
    {'name': 'Naya Gates',        'all': ['basilisk gate', 'citadel gate', 'manor gate']},
    # ── Terror ────────────────────────────────────────────────────────────────
    {'name': 'UB Terror',         'all': ['tolarian terror', 'snuff out', 'gurmag angler']},
    {'name': 'UR Terror',         'all': ['tolarian terror', 'skred']},
    {'name': 'U Terror',          'all': ['tolarian terror', 'mental note']},
    # ── Faeries ───────────────────────────────────────────────────────────────
    {'name': 'Dimir Faeries',     'all': ['spellstutter sprite', 'snuff out']},
    {'name': 'Mono U Fate',       'all': ['spellstutter sprite']},
    # ── Affinity ──────────────────────────────────────────────────────────────
    {'name': 'Esper Affinity Ninja',    'all': ['myr enforcer', 'leonardo, big brother', 'moon-circuit hacker']},
    {'name': 'Grixis Affinity',   'all': ['myr enforcer', 'utrom monitor', 'galvanic blast']},
    {'name': 'Esper Affinity',   'all': ['myr enforcer', 'utrom monitor', 'dispatch']},
    {'name': 'Dimir Affinity',   'all': ['myr enforcer', 'utrom monitor', 'thoughtcast', 'baleful strix']},

   

    # ── Familiars ─────────────────────────────────────────────────────────────
    {'name': 'Familiars',         'all': ['sunscape familiar', 'ephemerate']},
    # ── Wildfire ──────────────────────────────────────────────────────────────
    {'name': 'Jeskai Wildfire',   'all': ['cleansing wildfire', 'counterspell', 'ephemerate']},
    {'name': 'Jund Wildfire',     'all': ['cleansing wildfire', 'drossforge bridge', 'slagwoods bridge', 'writhing chrysalis']},
    # ── Pestilence ────────────────────────────────────────────────────────────
    {'name': 'Orzhov Pestilence', 'all': ['pestilence', 'guardian of the guildpact']},
    {'name': 'Food Pestilence',   'all': ['pestilence', 'cauldron familiar']},
    {'name': 'Black Sacrifice',   'all': ['bloodthrone vampire', 'carrion feeder']},
    # ── Infect ────────────────────────────────────────────────────────────────
    {'name': 'Infect',            'any': ['glistener elf', 'ichorclaw myr', 'blight mamba']},
    # ── Cascade ───────────────────────────────────────────────────────────────
    {'name': 'Cascade',           'any': ['boarding party', 'annoyed altisaur']},
    # ── Red ───────────────────────────────────────────────────────────────────
    {'name': 'Goblins',           'all': ['goblin matron', 'mogg war marshal']},
    {'name': 'Red Madness',       'all': ['lightning bolt', 'guttersnipe']},
    {'name': 'Red Rally',         'all': ['lightning bolt', 'rally at the hornburg']},
    {'name': 'Red Aggro',         'all': ['lightning bolt', "inventor\\'s axe"]},
    {'name': 'Rakdos Madness',    'all': ['lightning bolt', 'alms of the vein']},
    {'name': 'Red Pingers',       'all': ['lightning bolt', 'thermo-alchemist']},
    # ── Tron ──────────────────────────────────────────────────────────────────
    {'name': 'Monster Tron',      'all': ["urza\\'s tower", 'maelstrom colossus']},
    {'name': 'Altar Tron',        'all': ["urza\\'s tower", "ashnod\\'s altar"]},
    {'name': 'Flicker Tron',      'all': ["urza\\'s tower", 'mnemonic wall']},
    {'name': 'Pinger Tron',       'all': ["urza\\'s tower", 'ghostly flicker', 'mysidian elder']},
    {'name': 'Urzatron',          'all': ["urza\\'s tower"]},
    # ── Storm / Ramp / LD ─────────────────────────────────────────────────────
    {'name': 'RG Storm',          'all': ['thornscape familiar']},
    {'name': 'Gruul Ponza',       'any': ['mwonvuli acid-moss', 'thermokarst']},
    {'name': 'Golgari Gardens',   'all': ['avenging hunter', 'khalni garden']},
    {'name': 'RG Ramp',           'all': ['avenging hunter']},
    # ── Elves ─────────────────────────────────────────────────────────────────
    {'name': 'Elves',             'all': ['timberwatch elf', 'priest of titania']},
    # ── Tempo / Control ───────────────────────────────────────────────────────
    {'name': 'Esper Ephemerate',  'all': ['ephemerate', 'baleful strix']},
    {'name': 'Jeskai Ephemerate', 'all': ['counterspell', 'ephemerate', 'skred']},
    {'name': 'Dimir Control',    'all': ['counterspell', 'thorn of the black rose', 'baleful strix']},
    {'name': 'Simic Turbo Fog',  'all': ["moment\\'s peace", "stream of thought", "simic growth chamber"]},
    # ── Aura ──────────────────────────────────────────────────────────────────
    {'name': 'Aura Hexproof',     'any': ['slippery bogle', 'gladecover scout', 'silhana ledgewalker']},
    # ── Aggro ─────────────────────────────────────────────────────────────────
    {'name': 'UW Tribe',          'all': ['tireless tribe', 'circular logic']},
    {'name': 'Boros Tribe',       'all': ['tireless tribe', 'pursue the past']},
    {'name': 'Boros Synth',       'all': ['glint hawk', 'lightning bolt', 'experimental synthetizer']},
    {'name': 'Boros Snacker',      'all': ['glint hawk', 'sneaky snacker']},
    {'name': 'Esper Blade',       'all': ['glint hawk', 'kor skyfisher', 'baleful strix']},
    {'name': 'BW Blade',          'all': ['glint hawk', 'refurbished familiar']},
    {'name': 'Mardu Mid',          'all': ['glint hawk', 'refurbished familiar', 'galvanic blast']},
    {'name': 'Boros Aggro',       'all': ['battle screech', 'rally the peasants']},

    {'name': 'White Weenie',      'all': ['thraben inspector', 'kor skyfisher', 'novice inspector', 'battle screech']},
    {'name': 'White Convoke',      'all': ['salt road packbeast', 'ramosian rally']},

]

_FALLBACK = 'Other'


def deck_archetype(decklist: list[str]) -> str:
    """
    Restituisce il nome dell'archetipo del mazzo.

    Args:
        decklist: lista di nomi carta in lowercase (colonna played_cards)

    Returns:
        Nome archetipo. 'Other' se nessuna regola fa match.
    """
    cards = set(decklist)
    for rule in ARCHETYPES:
        all_of = rule.get('all', [])
        any_of = rule.get('any', [])
        if (all(c in cards for c in all_of) and
                (not any_of or any(c in cards for c in any_of))):
            return rule['name']
    return _FALLBACK
