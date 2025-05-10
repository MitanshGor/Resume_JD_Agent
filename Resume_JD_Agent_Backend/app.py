
import json
from flask import Flask, jsonify, request
from flask_cors import CORS
from langchain_core.messages import HumanMessage
from Workflow.workflow import workflow



graph_instance = workflow()
graph = graph_instance.get_graph()



app = Flask(__name__)
CORS(app, resources={r"/analyze": {"origins": "*"}})  # This allows cross-origin requests

@app.route('/analyze', methods=['POST'])
def analyze():
    data = request.get_json()
    session_id = data.get("session_id")
    user_message = data.get("message")
    if not session_id or not user_message:
        return jsonify({"error": "Missing session_id or message"}), 400

    print(f"Session ID: {session_id}")
    try:
        config = {"configurable": {"session_id": session_id, "thread_id": session_id}}
        result = graph.invoke({"messages": [HumanMessage(content=user_message)]}, config=config)
        messages = result.get("messages", [])
        response_text = messages[-1].content if messages else "No response generated."


        print(f"Response: {response_text}")
        # Check if the response is a valid JSON
        try:
            response_json = json.loads(response_text)
            # If the response is a valid JSON, return it
            return jsonify(response_json)
        except json.JSONDecodeError:
            # If not, return the raw text
            print("Response is not a valid JSON, returning as plain text.")
        return jsonify(response_text)
    
    except Exception as e:
        print(f"Error: {str(e)}")
        return jsonify({"error": str(e)}), 500
   
if __name__ == '__main__':
    app.run(debug=True)
