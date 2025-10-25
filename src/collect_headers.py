from bs4 import BeautifulSoup
import pandas as pd

def main():
    # Load local HTML file
    soup = BeautifulSoup(open('/home/dmy/A7/data/index.html'), 'html.parser')

    # Find the trending section
    trending_section = soup.select_one(".list__widgets--category-feed")
    # Find all articles within it
    articles = trending_section.select("article.article-card")

    # Create lists to store data
    headlines = []
    links = []

    for i, article in enumerate(articles, start=1):
        link_tag = article.select_one("a.article-card__link")
        headline_tag = article.select_one("h3.article-card__headline")

        if link_tag and headline_tag:
            headline = headline_tag.get_text(strip=True)
            href = link_tag.get("href")
            
            # Add to lists
            headlines.append(headline)
            links.append(f"https://montrealgazette.com{href}")

            print(f"{i}. {headline}")
            print(f"   https://montrealgazette.com{href}")
            print('-' * 60)
    
    # Create DataFrame from lists
    df = pd.DataFrame({
        "Headline": headlines,
        "Link": links
    })
    
    print(df)
    return df

if __name__ == '__main__':
    main()
