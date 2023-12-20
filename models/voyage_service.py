import os
import requests
import json

from models.base import ModelService


class VoyageService(ModelService):
    """
    https://docs.voyageai.com/embeddings/
    """

    def __init__(self, model_name='voyage-01'):
        self.model_name = model_name
        self.voyageai_api_key = os.getenv('VOYAGE_API_KEY')

        import voyageai
        voyageai.api_key = self.voyageai_api_key

    def get_embedding(self, text, input_type='document'):
        """
            input_type (`str`): "query" or "document" for retrieval case.
        """
        from voyageai import get_embeddings
        import voyageai
        voyageai.api_key = self.voyageai_api_key

        documents = [text]
        embeddings = get_embeddings(documents, model=self.model_name, input_type=input_type)
        return embeddings[0]

    def get_token_num(self, text):
        url = "https://api.voyageai.com/v1/embeddings"
        headers = {
            "Content-Type": "application/json",
            "Authorization": f"Bearer {self.voyageai_api_key}"
        }
        data = {
            "input": text,
            "model": self.model_name
        }
        response = requests.post(url, headers=headers, data=json.dumps(data))
        result = response.json()
        return result['usage']['total_tokens']


if __name__ == '__main__':
    voyage_service = VoyageService()
    res = voyage_service.get_token_num('hello')
    print(res)
