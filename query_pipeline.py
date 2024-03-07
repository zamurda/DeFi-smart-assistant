from dotenv import load_dotenv
import os # for env variables
import re # for regex (needed for doc parsing etc)
import logging
import sys
logging.basicConfig(stream=sys.stdout, level=logging.INFO)
logging.getLogger().addHandler(logging.StreamHandler(stream=sys.stdout))

# Load environment variables
load_dotenv()
PINECONE_API_KEY = os.getenv('PINECONE_API_KEY')
PINECONE_INDEX_NAME = os.getenv('PINECONE_INDEX_NAME')

from llama_index.core.query_pipeline import QueryPipeline
from llama_index.llms.ollama import Ollama
from llama_index.core import VectorStoreIndex, PromptTemplate, Settings
from llama_index.core.embeddings import resolve_embed_model

Settings.embed_model = resolve_embed_model('local:BAAI/bge-small-en-v1.5')

# index
from pinecone import Pinecone
from llama_index.vector_stores.pinecone import PineconeVectorStore
pc = Pinecone(api_key=PINECONE_API_KEY)
pc_index = pc.Index(PINECONE_INDEX_NAME)
vector_store = PineconeVectorStore(pinecone_index=pc_index)
index = VectorStoreIndex.from_vector_store(vector_store=vector_store) # load from existing vector store

# prompt
qa_prompt = PromptTemplate('Generate a question about Paul Graham\'s life about the following topic: {topic}')

# retriever
retriever = index.as_retriever(similarity_top_k=5)

#postprocessor
from llama_index.core.postprocessor import SimilarityPostprocessor
postprocessor = SimilarityPostprocessor(similarity_cutoff=0.1)

# llm and synthesiser
from llama_index.core.response_synthesizers import TreeSummarize
llm = Ollama(model='mistral', request_timeout=150.0)
summarizer = TreeSummarize(llm=llm)


# define query pipeline
pipeline = QueryPipeline(verbose=True)
pipeline.add_modules({
    'llm': llm,
    'prompt_tmpl': qa_prompt,
    'retriever': retriever,
    'summarizer': summarizer,
    'postprocessor': postprocessor
})
pipeline.add_link("prompt_tmpl", "llm") # link prompt template to llm for rewriting
pipeline.add_link("llm", "retriever") # link rewritten query to retriever for retrieval
pipeline.add_link("retriever", "postprocessor", dest_key="nodes") # link retrieved nodes to postprocessor for reranking
pipeline.add_link("llm", "postprocessor", dest_key="query_str") # link rewritten query to postprocessor's input query key for reranking
pipeline.add_link("postprocessor", "summarizer", dest_key="nodes") # link postprocessed nodes to summarizer
pipeline.add_link("llm", "summarizer", dest_key="query_str") # link rewritten query to summarizer's input query key

if __name__ == "__main__":
    topic = input("Enter topic: ")
    resp = pipeline.run(topic=topic)
    print(str(resp))
   