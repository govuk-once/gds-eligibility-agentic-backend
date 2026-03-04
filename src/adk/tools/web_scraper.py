import requests
from urllib.parse import urlparse
from html.parser import HTMLParser
from google.adk.tools.tool_context import ToolContext

class SafeTextExtractor(HTMLParser):
    """
    A standard-library HTML parser that safely extracts readable text.
    Very minimal.
    """
    def __init__(self):
        super().__init__()
        self.text_chunks = []
        self.hide_content = False
        self.hidden_tags = {'script', 'style', 'noscript', 'head', 'nav', 'footer'}

    def handle_starttag(self, tag, attrs):
        if tag in self.hidden_tags:
            self.hide_content = True

    def handle_endtag(self, tag):
        if tag in self.hidden_tags:
            self.hide_content = False

    def handle_data(self, data):
        if not self.hide_content:
            clean_text = data.strip()
            if clean_text:
                self.text_chunks.append(clean_text)

    def get_text(self):
        return " ".join(self.text_chunks)


def read_webpage(url: str, max_chars: int = 15_000) -> dict:
    """
    Fetches and extracts the readable text from a webpage.
    Call this tool ONLY when you need to read specific rules or guidance from a URL.
    
    Args:
        url: The full HTTP/HTTPS URL of the webpage to read.
    """
    # Domain Safety Check
    parsed_url = urlparse(url)
    hostname = parsed_url.hostname or ""
    
    if not (hostname == "gov.uk" or hostname.endswith(".gov.uk")):
        return {"error": f"Security restriction: URL domain '{hostname}' is not allowed. Only gov.uk domains are permitted."}
        
    print(f"  [Tool Call] read_webpage triggered for URL: {url}")
    
    try:
        response = requests.get(url, timeout=10, headers={"User-Agent": "Mozilla/5.0"})
        response.raise_for_status()
        
        extractor = SafeTextExtractor()
        extractor.feed(response.text)
        clean_text = extractor.get_text()
        
        # Truncate to protect token window (15k chars is roughly 3-4k tokens)
        truncated_content = clean_text[:max_chars] 
        
        return {"content": truncated_content}
        
    except Exception as e:
        return {"error": f"Failed to fetch webpage: {str(e)}"}