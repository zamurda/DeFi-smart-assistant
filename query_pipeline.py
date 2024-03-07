from dotenv import load_dotenv
import os # for env variables
import logging
import sys
logging.basicConfig(stream=sys.stdout, level=logging.INFO)
logging.getLogger().addHandler(logging.StreamHandler(stream=sys.stdout))

# Load environment variables
load_dotenv()
PINECONE_API_KEY = os.getenv('PINECONE_API_KEY')
PINECONE_INDEX_NAME = os.getenv('PINECONE_INDEX_NAME')

from llama_index.core.query_pipeline import QueryPipeline, InputComponent
from llama_index.llms.ollama import Ollama
from llama_index.core import VectorStoreIndex, Settings
from llama_index.core.embeddings import resolve_embed_model

Settings.embed_model = resolve_embed_model('local:BAAI/bge-small-en-v1.5')

# index
from pinecone import Pinecone
from llama_index.vector_stores.pinecone import PineconeVectorStore
pc = Pinecone(api_key=PINECONE_API_KEY)
pc_index = pc.Index(PINECONE_INDEX_NAME)
vector_store = PineconeVectorStore(pinecone_index=pc_index)
index = VectorStoreIndex.from_vector_store(vector_store=vector_store) # load from existing vector store

# retriever
retriever = index.as_retriever(similarity_top_k=5)

#postprocessor
from llama_index.core.postprocessor import SimilarityPostprocessor
postprocessor = SimilarityPostprocessor(similarity_cutoff=0.5)

# llm and synthesiser
from llama_index.core.response_synthesizers import TreeSummarize
llm = Ollama(model='mistral', request_timeout=150.0)
summarizer = TreeSummarize(llm=llm)


# define query pipeline
pipeline = QueryPipeline(verbose=True)
pipeline.add_modules({
    'input': InputComponent(),
    'retriever': retriever,
    'synthesizer': summarizer,
    'postprocessor': postprocessor
})
pipeline.add_link('input', 'retriever') # input -> retriever
pipeline.add_link('retriever', 'postprocessor', dest_key='nodes') # retriever -(nodes)-> postprocessor
pipeline.add_link('input', 'postprocessor', dest_key='query_str') # input -(query_str)-> postprocessor
pipeline.add_link('postprocessor', 'synthesizer', dest_key='nodes') # postprocessor -(nodes)-> summarizer
pipeline.add_link('input', 'synthesizer', dest_key='query_str') # input -(query_str)-> summarizer

# FOR PIPELINE TESTING
if __name__ == '__main__':
    prompt = input('Enter query: ')
    response = pipeline.run(input=prompt)
    print(str(response))
   