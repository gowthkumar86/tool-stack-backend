from bs4 import BeautifulSoup


class HTMLParserProcessor:
    """Parses raw HTML into structured fields."""

    def parse(self, html: str) -> dict:
        soup = BeautifulSoup(html, "html.parser")

        title = soup.title.string.strip() if soup.title and soup.title.string else None
        meta_tag = soup.find("meta", attrs={"name": "description"})
        meta_description = (
            meta_tag.get("content").strip() if meta_tag and meta_tag.get("content") else None
        )

        headings = [
            heading.get_text(strip=True)
            for heading in soup.find_all(["h1", "h2", "h3"])
            if heading.get_text(strip=True)
        ]
        links = [
            anchor.get("href").strip()
            for anchor in soup.find_all("a", href=True)
            if anchor.get("href").strip()
        ]
        plain_text = " ".join(soup.get_text(separator=" ", strip=True).split())

        return {
            "title": title,
            "meta_description": meta_description,
            "headings": headings,
            "links": links,
            "plain_text": plain_text,
        }
