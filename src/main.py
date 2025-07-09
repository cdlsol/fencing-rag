from utils.utils import PdfReader, Chunker, Embedder
import pandas as pd

reader = PdfReader(r"C:\\Users\\carlo\\Downloads\\fie_fencing_technical_rules.pdf")
reader.read_pdf()
reader.process_pdf()

chunker = Chunker("cl100k_base", 100, 0)

with open(r"C:\\Users\\carlo\\fencing-rag\\src\\utils\\output.txt", encoding="utf-8") as target_file:
    texts_pool = []
    for i, line in enumerate(target_file, start=1):
        try:
            tokens = PdfReader.num_tokens_from_string(line, "cl100k_base")
            print(f"Line {i}, Tokens: {tokens}, Line length: {len(line)}")
            try:
                texts = chunker.text_splitter(line)
                texts_pool.extend(texts) 
                print(f"Chunked Line {i}")
            except Exception as e:
                raise 
        except Exception as e:
            raise 

embedder = Embedder("text-embedding-ada-002")

records = []
for i, chunk in enumerate(texts_pool):
    try:
        vector = embedder.embed(chunk)
        records.append({
            "id": f"chunk-{i}",
            "text": chunk,
            "embedding":vector
        })
    except Exception as e:
        print(f"Failed to embed chunk {i}: {e}")
        raise 

df = pd.DataFrame(records)
df.to_csv("chunked_embeddings.csv", index=False)