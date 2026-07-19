# -*- coding: utf-8 -*-
import json
import os
import re
import urllib.request

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
OUT = os.path.join(ROOT, "images")
os.makedirs(OUT, exist_ok=True)

FEED = "https://pegasus-tech.blogspot.com/feeds/posts/default?alt=json&max-results=50"
HOME_LOGO = (
    "https://blogger.googleusercontent.com/img/b/R29vZ2xl/"
    "AVvXsEigA2JwuVTCFSNnAxEG7jhtHI_gez3rtLt9pxXL8_sG_Opw6rglMqLsiE9f5f4ydER4pcddfmAa"
    "YJUFdKBNuA0y41iGRPI2GArV-oH4pzpZTF8IpnCabUKvfSXqLvuS3hsaysh5tPY12Dpq/s1600/index1.jpg"
)
IMG_RE = re.compile(
    r'https://[^"\'\\s<>]+(?:blogger\\.googleusercontent\\.com|bp\\.blogspot\\.com)[^"\'\\s<>]*'
    .replace("\\\\", "\\")
)


def enlarge(url: str) -> str:
    url = url.replace("\\/", "/")
    url = re.sub(r"/s\d+(-c)?/", "/s1600/", url)
    url = re.sub(r"=s\d+", "=s1600", url)
    return url


def guess_ext(url: str) -> str:
    lower = url.lower()
    for ext in (".png", ".webp", ".gif", ".jpeg", ".jpg"):
        if ext in lower:
            return ".jpg" if ext == ".jpeg" else ext
    return ".jpg"


def main() -> None:
    # Fix regex properly
    pattern = re.compile(
        r'https://[^"\'\s<>]+(?:blogger\.googleusercontent\.com|bp\.blogspot\.com)[^"\'\s<>]*'
    )
    with urllib.request.urlopen(FEED, timeout=30) as resp:
        data = json.loads(resp.read().decode("utf-8"))

    entries = data.get("feed", {}).get("entry", [])
    print("entries", len(entries))
    imgs = []

    for entry in entries:
        title = entry.get("title", {}).get("$t", "")
        print("POST", title)
        content = (entry.get("content") or entry.get("summary") or {}).get("$t", "") or ""
        for match in pattern.findall(content):
            imgs.append(match)
            print(" ", match)
        media = entry.get("media$thumbnail")
        if media and media.get("url"):
            imgs.append(media["url"])
            print(" THUMB", media["url"])
        # also links
        for link in entry.get("link", []) or []:
            href = link.get("href", "")
            if "blogger.googleusercontent.com" in href or "bp.blogspot.com" in href:
                imgs.append(href)

    imgs.append(HOME_LOGO)
    unique = []
    for url in imgs:
        if url not in unique:
            unique.append(url)

    print("unique", len(unique))
    for i, url in enumerate(unique, 1):
        url2 = enlarge(url)
        path = os.path.join(OUT, f"blog-{i:02d}{guess_ext(url2)}")
        try:
            urllib.request.urlretrieve(url2, path)
            print("saved", path, os.path.getsize(path))
        except Exception as exc:
            print("fail", url2, exc)

    # Save mapping for reference
    with open(os.path.join(OUT, "sources.txt"), "w", encoding="utf-8") as f:
        for i, url in enumerate(unique, 1):
            f.write(f"blog-{i:02d}: {enlarge(url)}\n")


if __name__ == "__main__":
    main()
