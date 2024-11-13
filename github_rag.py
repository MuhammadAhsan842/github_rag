from flask import Flask, jsonify, request
from llama_index.readers.github import GithubRepositoryReader, GithubClient
from llama_index.core import VectorStoreIndex
import os
from dotenv import load_dotenv

load_dotenv() 

app = Flask(__name__)



OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
GITHUB_TOKEN = os.getenv("GITHUB_TOKEN")


if not OPENAI_API_KEY or not GITHUB_TOKEN:
    raise ValueError("Please set the OPENAI_API_KEY and GITHUB_TOKEN as environment variables.")


github_client = GithubClient(github_token=GITHUB_TOKEN, verbose=True)


@app.route('/query', methods=['POST'])
def query_repository():
    
    data = request.get_json()
    prompt = data.get('prompt')
    owner=data.get('owner')
    repo=data.get('repo')
    branch=data.get('branch')
    if not prompt:
        return jsonify({"error": "Prompt is required"}), 400
    if not owner:
        return jsonify({"error": "Prompt is required"}), 400
    if not repo:
        return jsonify({"error": "Prompt is required"}), 400
    if not branch:
        return jsonify({"error": "Prompt is required"}), 400
    
    github_client = GithubClient(github_token=GITHUB_TOKEN, verbose=True)

    loader = GithubRepositoryReader(github_client=github_client, owner=owner, repo=repo, verbose=True)
    
    documents = loader.load_data(branch=branch)
    
    index = VectorStoreIndex.from_documents(documents)
    query_engine = index.as_query_engine()


    response = query_engine.query(prompt)


    return jsonify({"response": str(response),"owner": str(owner),"repo": str(repo),"branch": str(branch)})


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=7680, debug=True)


