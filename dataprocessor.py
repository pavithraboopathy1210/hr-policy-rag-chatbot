
from pdfreader import read_pdf
from chunker import chunk_pages
from vectorstore import store_in_pinecone

pdf_path = r"C:\Users\Pavithra\Downloads\DS1505-P Fundamentals Deep Learning (Lab Integrated) Updated 09.8.25-1.pdf"


def run():

    # Extract text from PDF
    pages = read_pdf(pdf_path)

    print("Pages extracted:", len(pages))
    print("Total extracted characters:", sum(len(p) for p in pages))

    # Check extracted PDF content
    full_text = "\n".join(pages)

    print("\nContains Monday:", "Monday" in full_text)
    print("Contains 9:00 a.m.:", "9:00 a.m." in full_text)

    print("\n========== EXTRACTED PDF TEXT ==========")
    print(full_text)

    # Split PDF into chunks
    chunks = chunk_pages(
        pages,
        chunk_size=900,
        chunk_overlap=150
    )

    print("\nChunks created:", len(chunks))

    # Inspect generated chunks
    for i, chunk in enumerate(chunks):
        print(f"\n--- Chunk {i} ---")
        print(chunk)

    # Upload only after checking the chunks
    store_in_pinecone(chunks)

    print("\nPDF processing completed!")


if __name__ == "__main__":
    run()
