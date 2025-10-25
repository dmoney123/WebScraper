from bs4 import BeautifulSoup
import pandas as pd
import requests
import time
import sys
sys.path.append('/home/dmy/A7/src')
from collect_headers import main as collect_headers

def main():
    # Get the DataFrame with headlines and URLs
    df = collect_headers()


    # Create a session for better performance
    session = requests.Session()
    headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'}
    

    # Create a list to store the article text
    article_text = []
    article_title = []
    author = []
    blurb = []
    published_date = []
    # Loop through each row in the DataFrame
    for index, row in df.iterrows():
        headline = row['Headline']
        url = row['Link']
        
        try:
            # Fetch the HTML content
            response = session.get(url, headers=headers, timeout=10)
            response.raise_for_status()

            # Parse the HTML content
            soup = BeautifulSoup(response.text, 'html.parser')
            article = soup.select_one("article")
            
            if article:
                # Extract article elements safely
                title_elem = article.select_one("h1")
                title = title_elem.get_text(strip=True) if title_elem else "No title found"
                
                date_elem = article.select_one(".published-date__since")
                date = date_elem.get_text(strip=True) if date_elem else "No date found"
                
                author_elem = article.select_one(".published-by__author")
                author_name = author_elem.get_text(strip=True) if author_elem else "No author found"
                
                subtitle_elem = article.select_one("p.article-subtitle")
                subtitle = subtitle_elem.get_text(strip=True) if subtitle_elem else "No subtitle found"
                
                # Extract only the main article content, not navigation/breadcrumbs
                # Look for the main content area
                content_area = article.select_one(".article-content") or article.select_one(".story-content") or article.select_one("div[data-module='ArticleBody']")
                
                if content_area:
                    # Get text from the main content area only
                    article_text_content = content_area.get_text(strip=True)[:500] + "..."
                else:
                    # Fallback: try to get text from paragraphs only
                    paragraphs = article.select("p")
                    if paragraphs:
                        article_text_content = " ".join([p.get_text(strip=True) for p in paragraphs[:3]])[:500] + "..."
                    else:
                        # Last resort: get all text but limit it
                        article_text_content = article.get_text(strip=True)[:500] + "..."
            else:
                # Fallback if article element not found
                title = headline
                date = "No date found"
                author_name = "No author found"
                subtitle = "No subtitle found"
                # Try to get content from paragraphs only
                paragraphs = soup.select("p")
                if paragraphs:
                    article_text_content = " ".join([p.get_text(strip=True) for p in paragraphs[:3]])[:500] + "..."
                else:
                    article_text_content = soup.get_text(strip=True)[:500] + "..."
            
            # Append to lists
            article_title.append(title)
            published_date.append(date)
            author.append(author_name)
            blurb.append(subtitle)
            article_text.append(article_text_content)
            
        except Exception as e:
            print(f"Error processing {url}: {e}")
            # Add empty values for failed requests
            article_title.append("Error loading article")
            published_date.append("N/A")
            author.append("N/A")
            blurb.append("N/A")
            article_text.append("N/A")
        
        time.sleep(1)  # Reduced from 10 seconds to 1 second
    
    session.close()

    df2 = pd.DataFrame({
        'Headline': article_title,
        'Published Date': published_date,
        'Author': author,
        'Blurb': blurb,
        'Article Text': article_text
    })
    
    # Export to CSV
    #csv_path = '/home/dmy/A7/data/testdata.csv'
    #df2.to_csv(csv_path, index=False)
    #print(f"Data exported to: {csv_path}")
    #print(f"Exported {len(df2)} articles")
    #print(df2)
    return df2

if __name__ == '__main__':
    main()
