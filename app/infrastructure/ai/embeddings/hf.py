from langchain_huggingface import HuggingFaceEmbeddings


hf_embeddings = HuggingFaceEmbeddings(
    model_name="BAAI/bge-m3",
    model_kwargs={'device': 'cpu'} 
)