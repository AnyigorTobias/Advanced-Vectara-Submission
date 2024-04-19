import json

import os

from dotenv import load_dotenv
import logging


import requests
from authlib.integrations.requests_client import OAuth2Session




prompt = [
    {
        "role": "system",
        "content": "You are a trained a Senior Advocate of Nigeria or barrister acting on behalf of your client. You are provided with search results from previous legal judgements, casel laws and the constitution. The format of each result the name of past judgement and constitution with name of document. You must summarize these results into a coherent answer. Only use information provided in this chat."
    },
    #foreach ($qResult in $vectaraQueryResults)
    #if ($foreach.first)
        {"role": "user", "content": "Search for '$esc.java(${vectaraQuery})', and give me the first search result."},
        {"role": "assistant", "content": "$esc.java(${qResult.getText()})" },
    #else
        {"role": "user", "content": "Give me the $vectaraIdxWord[$foreach.index] search result."},
        {"role": "assistant", "content": "${qResult.getText()}" },
    #end
    #end
    {
        "role": "user",
        "content": "Generate a comprehensive and informative answer for the question '$esc.java(${vectaraQuery})' solely based  on the search results in this chat. You must only use information from the provided results. Combine search results together into a coherent answer. Do not repeat text. Only use the most relevant results that answer the question  accurately. If there are 2 answers that seem in conflict, use the most recent answer according to the date. If a result does not answer the question, do not use it. If the search results are not valid, respond with 'The returned results did not contain sufficient information to the question.'"
    }
]



class Searching:
    def __init__(self):
        self.customer_id = os.getenv('VECTARA_CUSTOMER_ID')
        self.api_key = os.getenv('VECTARA_API_KEY')
        
        
        
    def send_query(self, corpus_id, query_text, num_results, summarizer_prompt_name, response_lang, max_summarized_results):
        api_key_header = {
            "customer-id": self.customer_id,
            "x-api-key": self.api_key,
            "Content-Type": "application/json"
        }

        data_dict = {
            "query": [
                {
                    "query": query_text,
                    "num_results": num_results,
                    "corpus_key": [{"customer_id": self.customer_id, "corpus_id": corpus_id}],
                    'summary': [
                        {
                            'summarizerPromptName': summarizer_prompt_name,
                            'promptText': prompt,
                            'responseLang': response_lang,
                            'maxSummarizedResults': max_summarized_results
                        }
                    ]
                }
            ]
        }

        payload = json.dumps(data_dict)

        response = requests.post(
            "https://api.vectara.io/v1/query",
            data=payload,
            verify=True,
            headers=api_key_header
        )

        if response.status_code == 200:
            print("Request was successful!")
            data = response.json()
            texts = [item['text'] for item in data['responseSet'][0]['response'] if 'text' in item]
            return texts
        else:
            print("Request failed with status code:", response.status_code)
            print("Response:", response.text)
            return None