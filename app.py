import streamlit as st
from datetime import date

st.set_page_config(
    page_title="The Signal",
    page_icon="◈",
    layout="wide"
)

st.markdown("""
<style>
.stApp {
    background: #0b0f14;
    color: #e8edf2;
}

.block-container {
    max-width: 950px;
    padding: 55px 45px 80px;
}

.kicker {
    color: #7f8b98;
    font-size: 10px;
    font-weight: 700;
    letter-spacing: 3px;
}

.title {
    color: #f4f6f8;
    font-family: Georgia, serif;
    font-size: 60px;
    font-weight: 700;
    line-height: 1;
    margin-top: 8px;
}

.subtitle {
    color: #8f9aa6;
    font-size: 15px;
    margin-top: 10px;
}

.rule {
    border-top: 1px solid #252c34;
    margin: 25px 0 17px;
}

.date {
    color: #687582;
    font-size: 10px;
    font-weight: 700;
    letter-spacing: 2px;
}

.section {
    color: #7f8b98;
    font-size: 10px;
    font-weight: 700;
    letter-spacing: 3px;
    margin: 48px 0 18px;
}

.story {
    border-top: 1px solid #252c34;
    padding: 28px 0 35px;
}

.meta {
    color: #687582;
    font-size: 10px;
    font-weight: 700;
    letter-spacing: 2px;
}

.category {
    color: #9aa6b2;
    margin-left: 12px;
}

.headline {
    color: #f4f6f8;
    font-family: Georgia, serif;
    font-size: 28px;
    font-weight: 700;
    line-height: 1.25;
    margin: 9px 0 24px;
}

.label {
    color: #7f8b98;
    font-size: 9px;
    font-weight: 700;
    letter-spacing: 2px;
    margin: 18px 0 7px;
}

.body {
    color: #c4cbd2;
    font-size: 14px;
    line-height: 1.65;
}

.effect {
    color: #c4cbd2;
    font-size: 13px;
    line-height: 1.55;
    margin: 5px 0;
}

.market {
    display: inline-block;
    background: #151b22;
    border: 1px solid #252c34;
    border-radius: 3px;
    color: #dce2e7;
    padding: 6px 9px;
    margin: 2px 5px 2px 0;
    font-size: 10px;
    font-weight: 600;
}

.footer {
    border-top: 1px solid #252c34;
    margin-top: 50px;
    padding-top: 18px;
    color: #687582;
    font-size: 9px;
    letter-spacing: 1px;
}
</style>
""", unsafe_allow_html=True)


# HEADER

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
    f'<div class="date">{date.today().strftime("%A · %d %B %Y").upper()}</div>',
    unsafe_allow_html=True
)


# AUTOMATICALLY GENERATE THE SIGNAL

with open("signal.txt", "r", encoding="utf-8") as f:
    result = f.read()


# SIGNAL

st.markdown(
    '<div class="section">TODAY\'S SIGNAL</div>',
    unsafe_allow_html=True
)

stories = result.split("STORY")

story_number = 0

for raw_story in stories:

    story = raw_story.strip()

    if not story:
        continue

    story = story.split("END STORY")[0]

    story_number += 1

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
            category = line.replace("Category:", "", 1).strip()

        elif line.startswith("Headline:"):
            headline = line.replace("Headline:", "", 1).strip()

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


    # STORY

    st.markdown(
        '<div class="story">',
        unsafe_allow_html=True
    )

    st.markdown(
        f'<span class="meta">{story_number:02d}</span>'
        f'<span class="meta category">{category}</span>',
        unsafe_allow_html=True
    )

    st.markdown(
        f'<div class="headline">{headline}</div>',
        unsafe_allow_html=True
    )

    st.markdown(
        '<div class="label">WHAT HAPPENED</div>',
        unsafe_allow_html=True
    )

    st.markdown(
        f'<div class="body">{happened}</div>',
        unsafe_allow_html=True
    )

    st.markdown(
        '<div class="label">WHY IT MATTERS</div>',
        unsafe_allow_html=True
    )

    st.markdown(
        f'<div class="body">{matters}</div>',
        unsafe_allow_html=True
    )

    if effects:

        st.markdown(
            '<div class="label">SECOND-ORDER EFFECTS</div>',
            unsafe_allow_html=True
        )

        for effect in effects:

            st.markdown(
                f'<div class="effect">→ {effect}</div>',
                unsafe_allow_html=True
            )

    if markets:

        st.markdown(
            '<div class="label">MARKETS TO WATCH</div>',
            unsafe_allow_html=True
        )

        market_html = ""

        for market in markets:

            market_html += (
                f'<span class="market">{market}</span>'
            )

        st.markdown(
            market_html,
            unsafe_allow_html=True
        )

    st.markdown(
        '</div>',
        unsafe_allow_html=True
    )


# FOOTER

st.markdown(
    '<div class="footer">'
    'THE SIGNAL · AI-ASSISTED FINANCIAL INTELLIGENCE'
    '</div>',
    unsafe_allow_html=True
)