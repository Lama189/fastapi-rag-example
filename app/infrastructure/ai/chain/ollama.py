from langchain_core.output_parsers import StrOutputParser

from app.infrastructure.ai.llm.gemini import gemini_llm
from app.infrastructure.ai.prompt.tamplate import prompt_tamplate


chain = prompt_tamplate | gemini_llm | StrOutputParser()