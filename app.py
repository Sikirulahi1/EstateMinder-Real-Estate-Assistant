from flask import Flask, render_template, request, jsonify
from pinecone import Pinecone
import cohere

app = Flask(__name__)

# Initialize Cohere and Pinecone clients
cohere_api_key = "PINECONE_API_KEY"
co = cohere.Client(cohere_api_key)

pinecone_api_key = 'COHERE_API_KEY'
pc = Pinecone(api_key=pinecone_api_key)

# Function to generate a query embedding
def embed_query(text):
    response = co.embed(texts=[text], model="embed-english-v2.0", input_type='search_query')
    return response.embeddings[0]

# Function to query Pinecone and retrieve top matches with price filtering
def query_pinecone(query_text, namespace, min_price, max_price, top_k=5):
    index_name = "real-estate-embeddings"
    host = "https://real-estate-embeddings-aima004.svc.aped-4627-b74a.pinecone.io"
    index = pc.Index(index_name, host=host)

    query_embedding = embed_query(query_text)
    result = index.query(
        vector=query_embedding,
        top_k=top_k,
        namespace=namespace,
        include_metadata=True,
        filter={
            'numPrice': {
                "$gte": min_price,
                "$lte": max_price
            }
        }
    )
    return result['matches']

# Route for chatbot interface
@app.route('/')
def home():
    return render_template('chatbot.html')

# Route for querying the chatbot
@app.route('/query', methods=['POST'])
def query():
    data = request.get_json()
    query_text = data.get('query_text')
    namespace = data.get('house_type')
    min_price = data.get('min_price')
    max_price = data.get('max_price')
    
    min_price = int(min_price)
    max_price = int(max_price)

    print(f"Received Query: {query_text}, House Type: {namespace}, Min Price: {min_price}, Max Price: {max_price}")


    # Query Pinecone with user inputs
    results = query_pinecone(query_text, namespace, min_price, max_price)
    print(f'Results : {results}')
    # Format the response
    formatted_results = []
    for result in results:
        formatted_results.append({
            'property_id': result['id'],
            'score': result['score'],
            'metadata': result['metadata']
        })

        print(f"Property ID: {result['id']}")
        print(f"Score: {result['score']}")
        print(f"Metadata: {result['metadata']}")
        print("\n")
    return jsonify({'results': formatted_results})



if __name__ == '__main__':
    app.run(debug=True)