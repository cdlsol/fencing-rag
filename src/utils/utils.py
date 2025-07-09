from typing import List
import fitz 
import re
import tiktoken
from openai import OpenAI
from langchain_text_splitters import CharacterTextSplitter
from dotenv import load_dotenv
import os

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
        # text = re.sub(r'\f+', '\n', text)      # replace one or more form feeds with a newline

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

class Chunker:
    def __init__(self, enconding_name: str, chunk_size: int, chunk_overlap: int):
        self.encoding_name = enconding_name
        self.chunk_size = chunk_size
        self.chunk_overlap = chunk_overlap   
    
    def text_splitter(self, document: str) -> List[str]:
        text_splitter = CharacterTextSplitter.from_tiktoken_encoder(
            encoding_name = self.encoding_name, chunk_size = self.chunk_size,
            chunk_overlap = self.chunk_overlap
        )
        texts = text_splitter.split_text(document)
        return texts

class Embedder:
    def __init__(self, model: str):

        load_dotenv()

        if not os.getenv("OPENAI_API_KEY"):
            raise ValueError("OPENAI_API_KEY not found.")

        self.client = OpenAI()
        self.model = model

    def embed(self, text: str) -> List[float]:
        response = self.client.embeddings.create(
            input=text,
            model=self.model
        )
        return response.data[0].embedding