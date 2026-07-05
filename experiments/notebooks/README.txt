Ollama Setup:
url = "http://localhost:11434/api/generate"
"""
Notes : How to work with llama? 

pull ollma docker image : docker pull ollama/ollama 
build container and run : docker run -d -v ollama:/root/.ollama -p 11434:11434 --name ollama ollama/ollama 

run this command in container : docker exec -it ollama ollama pull llama3.2

Wow! 

You can acess with the following url : url = "http://localhost:11434/api/generate"

"""


Steps :

1: Extract/ scraped the data of jobs from differnt company careers pages. 
2.load data into the mongoDB database as staging area
3.Transform the data by cleansing and data normalization,enrichment and triming
    Transformation stages 
        1. mbnz_cleansed.v2.csv : this file contained the updated content of jobs of benz application.
        2. semienz.v2.csv : contains the updated cleaned data

3. Integration of datasources : 
    - Integrate 
    - Normalized the data 
    - final cleaning 

4. Tokenization and removing stopwords / enhanced the quality of texts

5. SKILLs NER 
    - extract Skills 

5. Embeddings generation 

6. Perform the retrieval operations.

7. Evaluation of the recommender 

8. Transform the code into pycharm for streamlit

