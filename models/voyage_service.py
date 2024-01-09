import os

from models.base import ModelService


class VoyageService(ModelService):
    """
    https://docs.voyageai.com/embeddings/
    """

    def __init__(self, model_name='voyage-02'):
        self.model_name = model_name
        self.voyageai_api_key = os.getenv('VOYAGE_API_KEY')

        import voyageai
        voyageai.api_key = self.voyageai_api_key
        self.vo = voyageai.Client()

    def get_embedding(self, text, input_type='document'):
        """
            input_type (`str`): "query" or "document" for retrieval case.
        """
        documents = [text]
        embeddings = self.vo.embed(documents, model=self.model_name, input_type=input_type)
        return embeddings.embeddings[0]

    def get_token_num(self, text):
        total_tokens = self.vo.count_tokens([text])
        return total_tokens


if __name__ == '__main__':
    voyage_service = VoyageService()
    res = voyage_service.get_embedding('hello')
    # res = voyage_service.get_token_num('hello world')
    print(res)
