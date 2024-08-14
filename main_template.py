from flask import Flask, jsonify, request
from flask_restful import Api, Resource
from flasgger import Swagger
from datetime import datetime
import threading

app = Flask(__name__)
api = Api(app)
swagger = Swagger(app)

lock = threading.Lock()  # To ensure thread safety when writing to the file

class UppercaseText(Resource):
    def get(self):
        """
        This method responds to the GET request for this endpoint and returns the data in uppercase.
        ---
        tags:
        - Text Processing
        parameters:
            - name: text
              in: query
              type: string
              required: true
              description: The text to be converted to uppercase
        responses:
            200:
                description: A successful GET request
                content:
                    application/json:
                      schema:
                        type: object
                        properties:
                            text:
                                type: string
                                description: The text in uppercase
        """
        text = request.args.get('text')
        return jsonify({"text": text.upper()})

class RecordTime(Resource):
    def get(self):
        """
        This method responds to the GET request for this endpoint and records the time of the request.
        ---
        tags:
        - Time Recording
        responses:
            200:
                description: A successful GET request
                content:
                    application/json:
                      schema:
                        type: object
                        properties:
                            message:
                                type: string
                                description: Confirmation of time recording
        """
        current_time = datetime.now().isoformat()
        with lock:  # Ensure only one thread writes to the file at a time
            with open("api_calls.txt", "a") as file:
                file.write(f"API call at {current_time}\n")
        return jsonify({"message": f"Time recorded: {current_time}"})

api.add_resource(UppercaseText, "/uppercase")
api.add_resource(RecordTime, "/record-time")

if __name__ == "__main__":
    app.run(debug=True)
