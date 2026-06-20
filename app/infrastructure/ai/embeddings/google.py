from langchain_google_genai import GoogleGenerativeAIEmbeddings


google_embeddings = GoogleGenerativeAIEmbeddings(
    model="models/text-embedding-004"
)