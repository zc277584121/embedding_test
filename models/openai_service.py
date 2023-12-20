import os

from models.base import ModelService


class OpenAIService(ModelService):
    """
    https://platform.openai.com/docs/guides/embeddings/use-cases
    """

    def __init__(self, model_name='text-embedding-ada-002'):
        from openai import OpenAI

        self.client = OpenAI()
        self.client.api_key = os.getenv('OPENAI_API_KEY')
        self.model_name = model_name

    def get_embedding(self, text):
        text = text.replace("\n", " ")
        return self.client.embeddings.create(input=[text], model=self.model_name).data[0].embedding

    def get_token_num(self, text):
        import tiktoken
        #  For second-generation embedding models like text-embedding-ada-002, use the cl100k_base encoding.
        if self.model_name.endswith('002'):
            encoding_name = 'cl100k_base'
        else:
            raise Exception(f"Unknown encoding name for model {self.model_name}")
        encoding = tiktoken.get_encoding(encoding_name)
        num_tokens = len(encoding.encode(text))
        return num_tokens


if __name__ == '__main__':
    openai_service = OpenAIService()
    # res = openai_service.get_embedding('hello')
    res = openai_service.get_token_num(
        'It helped to have studied art, because the main goal of an online store builder is to make users look ')
    print(res)
