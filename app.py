import re
import streamlit as st
from datetime import date


st.set_page_config(
    page_title="The Signal",
    page_icon="◈",
    layout="wide",
    initial_sidebar_state="collapsed"
)


# ==================================================
# DESIGN
# ==================================================

st.markdown("""
<style>

.stApp {
    background: #f4f0df;
    color: #10233f;
}

.block-container {
    max-width: 980px;
    padding: 42px 52px 80px;
}

[data-testid="stSidebar"] {
    background: #f4f0df;
    border-right: 1px solid #d8d2bd;
}

[data-testid="stSidebar"] * {
    color: #10233f;
}

[data-testid="stSidebar"] .stRadio label {
    font-family: Arial, Helvetica, sans-serif;
    font-size: 13px;
    font-weight: 700;
    letter-spacing: 1.5px;
}

.kicker {
    color: #667083;
    font-family: Arial, Helvetica, sans-serif;
    font-size: 11px;
    font-weight: 700;
    letter-spacing: 3px;
}

.title {
    color: #10233f;
    font-family: Georgia, serif;
    font-size: 64px;
    font-weight: 700;
    line-height: 1;
    margin-top: 10px;
}

.subtitle {
    color: #667083;
    font-family: Arial, Helvetica, sans-serif;
    font-size: 17px;
    margin-top: 12px;
}

.rule {
    border-top: 1px solid #cfc8b1;
    margin: 28px 0 18px;
}

.date {
    color: #667083;
    font-family: Arial, Helvetica, sans-serif;
    font-size: 11px;
    font-weight: 700;
    letter-spacing: 2px;
}

.section {
    color: #667083;
    font-family: Arial, Helvetica, sans-serif;
    font-size: 12px;
    font-weight: 700;
    letter-spacing: 3px;
    margin: 50px 0 20px;
}

.story {
    border-top: 1px solid #cfc8b1;
    padding: 30px 0 42px;
}

.meta {
    color: #7b8492;
    font-family: Arial, Helvetica, sans-serif;
    font-size: 11px;
    font-weight: 700;
    letter-spacing: 2px;
}

.category {
    color: #10233f;
    margin-left: 14px;
}

.headline {
    color: #10233f;
    font-family: Georgia, serif;
    font-size: 32px;
    font-weight: 700;
    line-height: 1.22;
    margin: 10px 0 27px;
}

.label {
    color: #667083;
    font-family: Arial, Helvetica, sans-serif;
    font-size: 10px;
    font-weight: 700;
    letter-spacing: 2px;
    margin: 22px 0 8px;
}

.body {
    color: #26364d;
    font-family: Arial, Helvetica, sans-serif;
    font-size: 16px;
    line-height: 1.7;
}

.effect {
    color: #26364d;
    font-family: Arial, Helvetica, sans-serif;
    font-size: 15px;
    line-height: 1.6;
    margin: 7px 0;
}

.market {
    display: inline-block;
    background: #ebe5d2;
    border: 1px solid #d2cbb6;
    border-radius: 3px;
    color: #10233f;
    padding: 7px 10px;
    margin: 3px 6px 3px 0;
    font-family: Arial, Helvetica, sans-serif;
    font-size: 11px;
    font-weight: 700;
}

.footer {
    border-top: 1px solid #cfc8b1;
    margin-top: 55px;
    padding-top: 20px;
    color: #7b8492;
    font-family: Arial, Helvetica, sans-serif;
    font-size: 10px;
    letter-spacing: 1px;
}

@media (max-width: 700px) {

    .block-container {
        padding: 30px 22px 60px;
    }

    .title {
        font-size: 48px;
    }

    .subtitle {
        font-size: 16px;
    }

    .headline {
        font-size: 27px;
    }

    .body {
        font-size: 16px;
        line-height: 1.65;
    }

    .effect {
        font-size: 15px;
    }

}

</style>
""", unsafe_allow_html=True)


# ==================================================
# MENU
# ==================================================

with st.sidebar:

    st.markdown(
        '<div class="kicker">THE SIGNAL</div>',
        unsafe_allow_html=True
    )

    st.markdown(
        '<div style="height:18px"></div>',
        unsafe_allow_html=True
    )

    page = st.radio(
        "Navigation",
        [
            "THE DAILY SIGNAL",
            "EQUITIES",
            "FX",
            "FIXED INCOME",
            "COMMODITIES",
            "MACRO",
            "CREDIT"
        ],
        label_visibility="collapsed"
    )


# ==================================================
# HEADER
# ==================================================

st.markdown(
    '<div class="kicker">GLOBAL MARKETS · MACRO · INVESTING</div>',
    unsafe_allow_html=True
)

st.markdown(
    '<div class="title">THE SIGNAL</div>',
    unsafe_allow_html=True
)

st.markdown(
    '<div class="subtitle">Financial intelligence, without the noise.</div>',
    unsafe_allow_html=True
)

st.markdown(
    '<div class="rule"></div>',
    unsafe_allow_html=True
)

st.markdown(
    f'<div class="date">'
    f'{date.today().strftime("%A · %d %B %Y").upper()}'
    f'</div>',
    unsafe_allow_html=True
)


# ==================================================
# READ SIGNAL
# ==================================================

try:

    with open("signal.txt", "r", encoding="utf-8") as f:
        result = f.read()

except FileNotFoundError:

    st.error("signal.txt could not be found.")
    st.stop()


# ==================================================
# EXTRACT DAILY SIGNAL RANKING
# ==================================================

daily_signal_numbers = []

ranking_match = re.search(
    r"DAILY SIGNAL\s*(.*?)\s*END DAILY SIGNAL",
    result,
    re.DOTALL
)

if ranking_match:

    ranking_block = ranking_match.group(1)

    for line in ranking_block.splitlines():

        match = re.search(
            r"^\s*(\d+)\s*:\s*(\d+)",
            line
        )

        if match:
            daily_signal_numbers.append(
                int(match.group(2))
            )


# ==================================================
# REMOVE RANKING FROM STORIES
# ==================================================

stories_text = result

if ranking_match:

    stories_text = (
        result[:ranking_match.start()]
        + result[ranking_match.end():]
    )


# ==================================================
# PARSE STORIES
# ==================================================

raw_stories = stories_text.split("STORY")

parsed_stories = []

for raw_story in raw_stories:

    story = raw_story.strip()

    if not story:
        continue

    story = story.split("END STORY")[0].strip()

    category = ""
    headline = ""
    happened = ""
    matters = ""
    effects = []
    markets = []

    current_section = ""

    for raw_line in story.splitlines():

        line = raw_line.strip()

        if not line:
            continue

        if line.startswith("Category:"):

            category = line.replace(
                "Category:", "", 1
            ).strip().upper()

        elif line.startswith("Headline:"):

            headline = line.replace(
                "Headline:", "", 1
            ).strip()

        elif line.startswith("What happened:"):

            current_section = "happened"

            happened = line.replace(
                "What happened:", "", 1
            ).strip()

        elif line.startswith("Why it matters:"):

            current_section = "matters"

            matters = line.replace(
                "Why it matters:", "", 1
            ).strip()

        elif line.startswith("Second-order effects:"):

            current_section = "effects"

        elif line.startswith("Markets to watch:"):

            current_section = "markets"

            text = line.replace(
                "Markets to watch:", "", 1
            ).strip()

            markets.extend(
                item.strip()
                for item in text.split(",")
                if item.strip()
            )

        elif current_section == "happened":

            happened += " " + line

        elif current_section == "matters":

            matters += " " + line

        elif current_section == "effects":

            if line.startswith("-"):

                effects.append(
                    line[1:].strip()
                )

        elif current_section == "markets":

            markets.extend(
                item.strip()
                for item in line.split(",")
                if item.strip()
            )

    if headline:

        parsed_stories.append({
            "category": category,
            "headline": headline,
            "happened": happened,
            "matters": matters,
            "effects": effects,
            "markets": markets
        })


# ==================================================
# SELECT STORIES
# ==================================================

if page == "THE DAILY SIGNAL":

    visible_stories = []

    for number in daily_signal_numbers:

        index = number - 1

        if 0 <= index < len(parsed_stories):

            visible_stories.append(
                parsed_stories[index]
            )

    # Fallback if ranking is missing
    if not visible_stories:

        visible_stories = parsed_stories[:5]

else:

    visible_stories = [
        story
        for story in parsed_stories
        if story["category"] == page
    ]


# ==================================================
# SECTION TITLE
# ==================================================

st.markdown(
    f'<div class="section">{page}</div>',
    unsafe_allow_html=True
)


# ==================================================
# DISPLAY STORIES
# ==================================================

for story_number, story in enumerate(
    visible_stories,
    start=1
):

    st.markdown(
        '<div class="story">',
        unsafe_allow_html=True
    )

    st.markdown(
        f'<span class="meta">'
        f'{story_number:02d}'
        f'</span>'
        f'<span class="meta category">'
        f'{story["category"]}'
        f'</span>',
        unsafe_allow_html=True
    )

    st.markdown(
        f'<div class="headline">'
        f'{story["headline"]}'
        f'</div>',
        unsafe_allow_html=True
    )

    st.markdown(
        '<div class="label">WHAT HAPPENED</div>',
        unsafe_allow_html=True
    )

    st.markdown(
        f'<div class="body">'
        f'{story["happened"]}'
        f'</div>',
        unsafe_allow_html=True
    )

    st.markdown(
        '<div class="label">WHY IT MATTERS</div>',
        unsafe_allow_html=True
    )

    st.markdown(
        f'<div class="body">'
        f'{story["matters"]}'
        f'</div>',
        unsafe_allow_html=True
    )

    if story["effects"]:

        st.markdown(
            '<div class="label">'
            'SECOND-ORDER EFFECTS'
            '</div>',
            unsafe_allow_html=True
        )

        for effect in story["effects"]:

            st.markdown(
                f'<div class="effect">'
                f'→ {effect}'
                f'</div>',
                unsafe_allow_html=True
            )

    if story["markets"]:

        st.markdown(
            '<div class="label">'
            'MARKETS TO WATCH'
            '</div>',
            unsafe_allow_html=True
        )

        market_html = ""

        for market in story["markets"]:

            market_html += (
                f'<span class="market">'
                f'{market}'
                f'</span>'
            )

        st.markdown(
            market_html,
            unsafe_allow_html=True
        )

    st.markdown(
        '</div>',
        unsafe_allow_html=True
    )


# ==================================================
# EMPTY STATE
# ==================================================

if not visible_stories:

    st.markdown(
        '<div class="body">'
        'No stories available for this section yet.'
        '</div>',
        unsafe_allow_html=True
    )


# ==================================================
# FOOTER
# ==================================================

st.markdown(
    '<div class="footer">'
    'THE SIGNAL · AI-ASSISTED FINANCIAL INTELLIGENCE'
    '</div>',
    unsafe_allow_html=True
)