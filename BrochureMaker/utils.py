import bs4
import requests
import urllib.parse

headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/117.0.0.0 Safari/537.36"
}

def get_website_links(url):
    response=requests.get(url,headers=headers)
    soup=bs4.BeautifulSoup(response.content,"html.parser")
    content_links = []
    for link in soup.find_all("a"):
        href = link.get("href")
        if href:
            full_href = urllib.parse.urljoin(url, href)
            content_links.append(full_href)
            
    img_links = []
    for img in soup.find_all("img"):
        img_src = img.get("data-src") or img.get("data-lazy") or img.get("src")
        
        if img_src:
            full_img_url = urllib.parse.urljoin(url, img_src)
            img_links.append(full_img_url)
    return (content_links, img_links)

def get_website_content(url):
    response = requests.get(url, headers=headers)
    soup = bs4.BeautifulSoup(response.content, "html.parser")
    title = soup.title.string if soup.title else "No title found"
    if soup.body:
        for irrelevant in soup.body(["script", "style", "img", "input"]):
            irrelevant.decompose()
        text = soup.body.get_text(separator="\n", strip=True)
    else:
        text = ""
    return (title + "\n\n" + text)[:2_000]