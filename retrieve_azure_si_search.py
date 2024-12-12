import time
from azure.search.documents import SearchClient
from azure.search.documents.models import RawVectorQuery
from creds import azure_credential,EMBEDDING_MODEL_Large
from creds import AZURE_COGNITIVE_SEARCH_ENDPOINT, AZURE_COGNITIVE_SEARCH_INDEX_NAME, azure_credential
from creds import generate_embeddings_azure_openai

## This file can be used to get the similiarr context(text) from Retriver given a user query.

class Retriver: 
    """ Class that connects with Knowledge base and returns a retriver object for get_similiar_object function. """

    def __init__(self,query = " ", retrive_fields = ["id","actual_content", "metadata","url","Location","category"]):

        """  Creates the object of class with query and retrive _fields values.

    Input Parameters :
    -------------------------
    query = str
                 User's query or text that needs to be searched in Knowledge base

    retrive_fields = List[str1,str2..]
                     Field needs to be retrived from Knoweldge base.
    
    """



        if query:
            self.query = query

        self.search_client = SearchClient(AZURE_COGNITIVE_SEARCH_ENDPOINT , AZURE_COGNITIVE_SEARCH_INDEX_NAME, azure_credential)
                                                         
        self.retrive_fields = retrive_fields
    
    def hybrid_search(self,top = 2, k = 2,vector_field = "vector",query_embedding = [],Location = " "):

        """ Function which perform hybrid search in Knowledge base
    
    Input Parameters :
    -------------------------
    k = int
        top results to retrive from vector search

    top = str
          top results to retrive from text search

    vector_field = str
                   with which feild to perform similiarity search in Knowledge base

    query_embedding = List[1536 float values]
                      a list which contains the generated embedding for the given user query
          
    Returns :
    -------------------------
    result : Retriver Object
             A retriver object that can be used by get_similiar_content function to extrcat data."""
        
        vector_query = RawVectorQuery(vector=query_embedding, k=k, fields=vector_field)
        
        Location_to_use = """Location eq """ +"'"+ Location + "'"
        print("Using Location :",Location_to_use)
        
        results = self.search_client.search(search_text=self.query,  vector_queries= [vector_query],
                                                select=self.retrive_fields,top=top, filter = Location_to_use )  

        return results


# def get_similiar_content(user_query = " ",
#                       search_type = "hybrid",top = 3, k = 3,Location = " "):


#     retrive_docs = Retriver(query = user_query)
#     if search_type == "hybrid":
#         start = time.time()
#         vector_of_search_query = generate_embeddings_azure_openai(user_query,model=EMBEDDING_MODEL_Large)
#         #print("Generated embedding for search query in :", time.time()-start,'seconds.')

#         start = time.time()
#         r = retrive_docs.hybrid_search(top = top, k=k, query_embedding = vector_of_search_query,Location = Location)

#         sources = []
#         similiar_doc = []
#         for doc in r:
#             similiar_doc.append("Metadata : " +doc["metadata"] + "\n" "URL : " + doc["url"] + "\ncontent : " + doc["actual_content"])
#             sources.append("ID: "+doc["id"] +" : " + doc["metadata"])
#         similiar_docs = "\n\n\n".join(similiar_doc)
#         #print("*"*100)
#         #print("Retrived similiar documents with Hybrid search in :", time.time()-start,'seconds.')
#         #print("similiar_doc :", similiar_doc)
#         print("Retrived Docs wih Hybrid search are :",sources,"\n")
#         #source = " ".join(sources)
#     return similiar_docs



def get_similiar_content_azure(user_query = " ",
                      search_type = "hybrid",top = 3, k = 3,Location = " "):


    retrive_docs = Retriver(query = user_query)
    if search_type == "hybrid":
        start = time.time()
        vector_of_search_query = generate_embeddings_azure_openai(user_query,model=EMBEDDING_MODEL_Large)
        #print("Generated embedding for search query in :", time.time()-start,'seconds.')

        start = time.time()
        r = retrive_docs.hybrid_search(top = top, k=k, query_embedding = vector_of_search_query,Location = Location)
        
        use_url_prompt = True
        sources = []
        similiar_doc = []
        for doc in r:
            if "https" in doc["url"]:
                similiar_doc.append("FILE NAME : " +doc["metadata"] + "\n\nURL : " + doc["url"] + "\n\nCONTEXT: " + doc["actual_content"])
            else : 
                similiar_doc.append("\n\nCONTEXT: " + doc["actual_content"])
                use_url_prompt = False
                
            sources.append("ID: "+doc["id"] +" : " + doc["metadata"])
                
        similiar_docs = "\n\n\n".join(similiar_doc)
        
        #print("*"*100)
        #print("Retrived similiar documents with Hybrid search in :", time.time()-start,'seconds.')
        #print("similiar_doc :", similiar_doc)
        
        print("Retrived Docs wih neww Hybrid search are :",sources,"\n")
        
        #source = " ".join(sources)
    return similiar_docs,use_url_prompt
