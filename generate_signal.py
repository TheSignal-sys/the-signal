import feedparser
from openai import OpenAI


def generate_signal():

    sources = {
        "BBC Business": "https://feeds.bbci.co.uk/news/business/rss.xml",
        "Google Finance": "https://news.google.com/rss/search?q=markets%20finance&hl=en-GB&gl=GB&ceid=GB:en"
    }

    articles = []

    for source, url in sources.items():
        feed = feedparser.parse(url)

        for article in feed.entries[:20]:
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

    prompt = f"""
You are the editor of THE SIGNAL, a professional financial intelligence briefing
for an investor following global markets, macroeconomics, commodities and companies.

From the news below, select the FIVE developments with the greatest investment,
macro or market significance.

Prioritise:
- Important developments that may move markets
- Underappreciated or second-order effects
- Changes in rates, inflation, currencies, commodities, credit or equities
- Stories with clear implications for investors

Avoid generic business news and avoid stories simply because they are popular.

For EACH story return exactly:

STORY
Category: [MACRO, CREDIT, EQUITIES, COMMODITIES, FX, EM or similar]
Headline: [maximum 12 words]

What happened:
[25–35 words]

Why it matters:
[25–35 words]

Second-order effects:
- [maximum 15 words]
- [maximum 15 words]
- [maximum 15 words]

Markets to watch:
[3–5 specific assets, indices, yields, currencies or commodities separated by commas]

END STORY

Do not add introductions, conclusions or commentary outside the five stories.

NEWS:

{headlines}
"""

    response = client.responses.create(
        model="gpt-5-mini",
        input=prompt
    )

    signal = response.output_text

    with open("signal.txt", "w", encoding="utf-8") as f:
        f.write(signal)

    return signal


if __name__ == "__main__":
    generate_signal()
    print("Today's Signal generated successfully.")