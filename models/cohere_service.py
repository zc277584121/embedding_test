import os
import cohere
from models.base import ModelService


class CohereService(ModelService):
    """
    https://docs.cohere.com/reference/embed
    """

    def __init__(self, model_name='embed-english-v2.0'):
        self.co = cohere.Client(os.getenv('CO_API_KEY'))
        self.model_name = model_name

    def get_embedding(self, text, input_type='search_document'):
        """
            input_type (`str`): "search_query" or "search_document" for retrieval case.
        """
        response = self.co.embed(
            texts=[text],
            model=self.model_name,
            input_type=input_type,
        )
        return response['embeddings'][0]

    def get_token_num(self, text):
        response = self.co.tokenize(
            text=text,
            model=self.model_name
        )
        return len(response.tokens)


if __name__ == '__main__':
    cohere_service = CohereService()
    res = cohere_service.get_token_num(
        'It helped to have studied art, because the main goal of an online store builder is to make users look ')
    print(res)
