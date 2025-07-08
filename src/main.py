from pdf_extractor.utils import PdfReader

reader = PdfReader(r"C:\\Users\\carlo\\Downloads\\fie_fencing_technical_rules.pdf")
reader.read_pdf()
reader.process_pdf()

with open(r"C:\\Users\\carlo\\fencing-rag\\src\\pdf_extractor\\output.txt", encoding="utf-8") as target_file:
    for i, line in enumerate(target_file, start=1):
        tokens = PdfReader.num_tokens_from_string(line, "cl100k_base")
        print(f"Line {i}, Tokens: {tokens}")
