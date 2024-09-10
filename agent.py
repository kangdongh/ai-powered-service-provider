import os
import numpy as np
from typing import Dict, Tuple, Callable, Any
from sentence_transformers import SentenceTransformer

from sklearn.metrics.pairwise import cosine_similarity
from langchain_core.prompts import PromptTemplate
from langchain_core.output_parsers import StrOutputParser
from langchain_community.chat_models import ChatPerplexity

def extract_answer(response: str) -> str:
    # Assuming the answer is on a new line or follows a specific pattern
    lines = response.split('\n')
    # Example: Extract the first non-empty line after the prompt
    for line in lines:
        if line.strip():  # Check if the line is not empty
            return line.strip()
    return response  # Fallback to the original response if no extraction is possible



class AIServiceAgent:
    registered_services: Dict[int, Tuple[Callable[[Any], str], Dict]]

    def __init__(self):
        self.registered_services = {}
        self.model = SentenceTransformer('intfloat/multilingual-e5-large')
        self.llm = ChatPerplexity(
            model="llama-3.1-sonar-large-128k-chat",
            temperature=0.7,
            api_key=os.getenv('PERPLEXITY_API_KEY')  # Ensure the API key is set in your environment
        )

    def register(self, service, service_info):
        # Validate service_info
        if 'description' not in service_info or 'kwargs' not in service_info:
            raise ValueError("service_info must contain 'description' and 'kwargs' fields.")
        
        # Generate embedding for the description
        embedding = self.model.encode(service_info['description'])
        
        # Create a unique ID for the service
        service_id = len(self.registered_services) + 1
        
        # Store the service with its information
        self.registered_services[service_id] = (embedding, service, service_info)
        
    def run_service(self, input_query: str):
        # Step 1: Encode the input query
        query_embedding = self.model.encode(input_query)
        
        # Step 2: Find the service with the highest cosine similarity
        max_score = -1
        best_service_id = None
        for service_id, (embedding, service, service_info) in self.registered_services.items():
            score = cosine_similarity([query_embedding], [embedding])[0][0]
            if score > max_score:
                max_score = score
                best_service_id = service_id
        
        # Step 3: Output the best matching service description and score
        _, _, best_service_info = self.registered_services[best_service_id]
        print(f"Best matching service description: {best_service_info['description']}")
        print(f"Score: {max_score}")

        # Step 4-1: Check the score against the threshold
        threshold = 0.7
        if max_score < threshold:
            print("Error: No suitable service found with a high enough similarity score.")
            return
        
        # Step 4-2: Execute the service if the score is above the threshold
        _, best_service, best_service_info = self.registered_services[best_service_id]
        kwargs = {}
        
        for arg_name, arg_info in best_service_info['kwargs'].items():
            # Create a prompt to extract the argument value
            prompt_text = ("Provide only the answer to the following question.\n" +
                f"""Based on the description "{arg_info['description']}", what is a proper value as type of {arg_info['type']} for the query "{input_query}".""")
            
            # Use LangChain to generate the argument value
            prompt = PromptTemplate(template=prompt_text)
            chain = prompt | self.llm | StrOutputParser()
            arg_value_str = chain.invoke({})
            
            # Cast the result to the required type
            try:
                arg_value = arg_info['type'](arg_value_str)
            except ValueError as e:
                print(f"Error casting argument {arg_name}: {e}")
                return
            
            kwargs[arg_name] = arg_value
        
        # Execute the service with the extracted arguments
        result = best_service(**kwargs)
        print(f"Service result: {result}")