import fitz

    # (page by page)
    # returns:

    #     list[dict]:
    #     [
    #         {
    #             "page_number": 1,
    #             "text": "page text..."
    #         }
    #     ]
    
def extract_pdf_text(pdf_path):

    document = fitz.open(pdf_path)

    pages = []

    for page_index in range(len(document)):
        page = document[page_index]

        pages.append(
            {
                "page_number": page_index + 1,
                "text": page.get_text().strip()
            }
        )

    document.close()

    return pages