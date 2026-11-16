
from typing import List


def chunk_pages(
    pages: List[str],
    chunk_size: int = 900,
    chunk_overlap: int = 150
) -> List[str]:

    chunks: List[str] = []

    for text in pages:

        if not text or not text.strip():
            continue

        start = 0
        n = len(text)

        while start < n:

            end = min(start + chunk_size, n)

            chunk = text[start:end]

            # Find a sentence boundary
            last_boundary = max(
                chunk.rfind(". "),
                chunk.rfind("? "),
                chunk.rfind("! ")
            )

            if (
                last_boundary != -1
                and end < n
                and last_boundary > chunk_size * 0.5
            ):
                end = start + last_boundary + 2
                chunk = text[start:end]

            chunk = chunk.strip()

            if chunk:
                chunks.append(chunk)

            # Stop after processing the final chunk
            if end >= n:
                break

            # Move forward with overlap
            start = max(end - chunk_overlap, start + 1)

    return chunks
