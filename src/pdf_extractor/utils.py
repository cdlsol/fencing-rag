import fitz 
import re
import tiktoken

class PdfReader:
    def __init__(self, path: str) -> None:
        self.path = path
        self.doc = None

    def read_pdf(self) -> None:
        self.doc = fitz.open(self.path)

    def clean_text(self, text: str) -> str:
        text = re.sub(r'-\s+', '', text)         # remove line-break hyphenation
        text = re.sub(r'\s+', ' ', text)         # collapse all whitespace to single space
        text = re.sub(r'\n+', '\n', text)        # remove excess newlines
        # text = re.sub(r'\f+', '\n', text)        # Replace one or more form feeds with a newline

        return text.strip()

    def process_pdf(self, max_pages: int = 61, output_file: str = "output.txt") -> None:
        if not self.doc:
            raise ValueError("PDF not loaded. Call read_pdf() first.")

        with open(output_file, "w", encoding="utf-8") as out:
            for i, page in enumerate(self.doc):
                if i >= max_pages:
                    break
                raw_text = page.get_text()
                cleaned = self.clean_text(raw_text)
                out.write(cleaned + "\n\f")  # \f is form feed
                
    @staticmethod
    def num_tokens_from_string(string: str, encoding_name: str) -> int:
        """Returns the number of tokens in a text string."""
        encoding = tiktoken.get_encoding(encoding_name)
        num_tokens = len(encoding.encode(string))
        return num_tokens