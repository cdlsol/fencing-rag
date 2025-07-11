from openai import OpenAI
import duckdb
from dotenv import load_dotenv
load_dotenv()

client = OpenAI()
con = duckdb.connect(r"src\duckdb\fencing_rag_vectordb.duckdb")
con.execute("INSTALL vss;")
con.execute("LOAD vss;")

MODEL_EMBEDDING = "text-embedding-ada-002"
VECTOR_DIM = 1536

def handle_rag_query(user_question: str) -> dict:
    
    embedding = client.embeddings.create(
        input=user_question,
        model=MODEL_EMBEDDING
    ).data[0].embedding

    
    results = con.execute("""
        SELECT id, text, list_distance(embedding, ?) AS score
        FROM fencing_rag
        ORDER BY score
        LIMIT 3;
    """, [embedding]).fetchall()

    context = "\n---\n".join(row[1] for row in results)
    
    prompt = f"""
    Use the following context to answer the question as accurately as possible.
    \n\nContext:\n{context}\n\nQuestion:\n{user_question}
    """

    response = client.chat.completions.create(
        model="gpt-4o-mini", 
        messages=[
            {"role": "system", "content": "You are a helpful fencing expert who is aiding non fencers to understand fencing concepts and rules."},
            {"role": "user", "content": prompt}
        ],
        max_tokens=500,
    )
    answer = response.choices[0].message.content

    return {
        "question": user_question,
        "context": context,
        "answer": answer
    }
