from langchain_google_genai import GoogleGenerativeAIEmbeddings


google_embeddings = GoogleGenerativeAIEmbeddings(
    model="gemini-embedding-2-preview",
    output_dimensionality=1024  
)