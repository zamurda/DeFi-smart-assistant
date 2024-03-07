from llama_index.core import PromptTemplate

# query_str and context_str optional which is hacky
summary_tmpl_with_mem_str = (
    'Context information directly related to the query is below.\n'
    '--------------------------------\n'
    '{{context_str}}\n'
    '--------------------------------\n'
    'Information from your last conversation is below. Use it to enhance your answer if needed.\n'
    '--------------------------------\n'
    '{memory_str}\n'
    '--------------------------------\n'
    'Given the context information and the information from your last conversation, and not prior knowledge,'
    'Answer the query below.\n'
    '--------------------------------\n'
    'Query: {{query_str}}\n'
    'Answer:'
)
summary_tmpl_with_mem = PromptTemplate(summary_tmpl_with_mem_str)