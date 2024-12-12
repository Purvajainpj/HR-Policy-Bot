################################## Utilizing DB ################################
# In a new session or script:
import chromadb
from chromadb.utils import embedding_functions
from creds import generate_embeddings_azure_openai
from chromadb import Documents, EmbeddingFunction, Embeddings

class MyEmbeddingFunction(EmbeddingFunction):
    def __call__(self, input: Documents) -> Embeddings:
        # Use the generate_embedding function here
        #print("Input>>>>>>>",input)
        embeddings = generate_embeddings_azure_openai(text= input[0])
        return embeddings

persist_directory = r"ask_hr_chromadb_all_locations"
#persist_directory = r"\ask_hr_chromadb_all_locations"


client = chromadb.PersistentClient(path=persist_directory)

embedding_function = MyEmbeddingFunction()

collection_docs = client.get_collection(
    name="supportive_documens_products",
    embedding_function=embedding_function
)

def get_similiar_content_chromadb(query: str,Location = " ", nresults= 3) -> str :
    results = collection_docs.query(
        query_texts=[query],
        n_results=3,
        where={"Location": Location}
    )
    #similiar_products = ("_"*100).join(results["documents"][0])
    #similiar_docs = ("-"*100).join(results["documents"][0])
    docs = results["documents"][0]
    #len(docs)
    ids = results["ids"][0]
    other_data = results['metadatas'][0]
    for i in range(len(other_data)):
        other_data[i]["actual_content"] = docs[0]
        other_data[i]["id"] = ids[i]
        
    use_url_prompt = True
    sources = []
    similiar_doc = []
    for doc in other_data:
        if "https" in doc["url"]:
            similiar_doc.append("FILE NAME : " +doc["metadatas"] + "\n\nURL : " + doc["url"] + "\n\nCONTEXT: " + doc["actual_content"])
        else : 
            similiar_doc.append("\n\nCONTEXT: " + doc["actual_content"])
            use_url_prompt = False

        sources.append("ID: "+doc["id"] +" : " + doc["metadatas"])

    similiar_docs = "\n\n\n".join(similiar_doc)
    print("Retrived Docs wih new search are :",sources,"\n")
    
    
    
    return similiar_docs,use_url_prompt

################################## Utilizing DB ################################
