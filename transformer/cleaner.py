import re
from bs4 import BeautifulSoup
from typing import Optional

def html_to_text(html: Optional[str]) -> str:
    if not html:
        return ""
    soup = BeautifulSoup(html, "html.parser")
    for code in soup.find_all("code"):
        code.replace_with(f"```{code.get_text()}```")
    text = soup.get_text(separator="\n")
    text = re.sub(r"\n{3,}", "\n\n", text)
    return text.strip()
