import feedparser
from openai import OpenAI


def generate_signal():

    # --------------------------------------------------
    # NEWS SOURCES
    # --------------------------------------------------

    sources = {
        "BBC Business": "https://feeds.bbci.co.uk/news/business/rss.xml",
        "Google Finance": "https://news.google.com/rss/search?q=markets%20finance&hl=en-GB&gl=GB&ceid=GB:en"
    }

    articles = []

    for source, url in sources.items():

        feed = feedparser.parse(url)

        for article in feed.entries[:30]:

            articles.append({
                "source": source,
                "title": article.title,
                "link": article.link
            })


    headlines = "\n".join(
        f"{i+1}. {article['title']} ({article['source']})"
        for i, article in enumerate(articles)
    )


    client = OpenAI()


    # --------------------------------------------------
    # GENERATE 30 STORIES
    # --------------------------------------------------

    prompt = f"""
You are the senior editor of THE SIGNAL, a professional financial
intelligence briefing for investors following global markets.

Turn the news below into a structured daily research briefing.

Produce EXACTLY FIVE stories for EACH of these six categories:

EQUITIES
FX
FIXED INCOME
COMMODITIES
MACRO
CREDIT

That means EXACTLY 30 stories in total.

The category distribution MUST be:

5 EQUITIES
5 FX
5 FIXED INCOME
5 COMMODITIES
5 MACRO
5 CREDIT

Do not produce fewer than five stories for any category.

If there is limited obvious news for a category, use the most
relevant available development and explain its market implications.
Do not invent facts.

EQUITIES:
Company results, corporate developments, equity markets, sectors,
valuations, M&A and equity-specific developments.

FX:
Currencies, foreign exchange markets, central-bank divergence,
capital flows and currency-specific developments.

FIXED INCOME:
Government bonds, yields, interest rates, curves, duration and
monetary-policy expectations.

COMMODITIES:
Oil, gas, metals, agriculture and commodity-specific supply,
demand and pricing developments.

MACRO:
Inflation, growth, employment, central banks, fiscal policy,
economic data and major geopolitical developments affecting markets.

CREDIT:
Corporate credit, sovereign credit, spreads, refinancing,
defaults and financial conditions.

Prioritise developments that could materially affect markets.

Avoid generic business stories.

Prefer:
- Clear market implications
- Meaningful changes in expectations
- Second-order effects
- Identifiable assets to monitor
- Developments that an investor would genuinely want to know

For EACH story return exactly:

STORY
Category: [EQUITIES, FX, FIXED INCOME, COMMODITIES, MACRO or CREDIT]
Headline: [maximum 12 words]

What happened:
[25–40 words]

Why it matters:
[25–40 words]

Second-order effects:
- [maximum 15 words]
- [maximum 15 words]
- [maximum 15 words]

Markets to watch:
[3–5 specific assets, indices, yields, currencies or commodities separated by commas]

END STORY

Repeat this format exactly 30 times.

Do not add introductions, conclusions or commentary.

NEWS:

{headlines}
"""


    response = client.responses.create(
        model="gpt-5-mini",
        input=prompt
    )

    stories = response.output_text


    # --------------------------------------------------
    # RANK THE 30 STORIES
    # --------------------------------------------------

    ranking_prompt = f"""
You are the chief editor of THE SIGNAL.

Below are 30 financial market stories.

Select the FIVE stories that are most important for an investor
to understand today.

Rank them from 1 to 5.

Prioritise:

- Expected market impact
- Importance to global asset prices
- Changes in monetary policy expectations
- Changes in growth or inflation expectations
- Significant corporate developments
- Significant commodity developments
- Cross-asset implications
- Second-order effects

Do NOT select stories simply because they are interesting.

The story number refers to the order in which the stories appear,
starting with 1.

Return ONLY this format:

DAILY SIGNAL
1: [story number]
2: [story number]
3: [story number]
4: [story number]
5: [story number]
END DAILY SIGNAL

Here are the 30 stories:

{stories}
"""


    ranking_response = client.responses.create(
        model="gpt-5-mini",
        input=ranking_prompt
    )

    ranking = ranking_response.output_text


    # --------------------------------------------------
    # SAVE DAILY SIGNAL + ALL STORIES
    # --------------------------------------------------

    with open("signal.txt", "w", encoding="utf-8") as f:

        f.write(ranking.strip())
        f.write("\n\n")
        f.write(stories.strip())


    return stories


if __name__ == "__main__":

    generate_signal()

    print("Today's Signal generated successfully.")