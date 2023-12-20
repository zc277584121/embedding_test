import os
import requests

from models.base import ModelService


class JinaService(ModelService):
    """
    https://jina.ai/embeddings/
    """

    def __init__(self, model_name='jina-embeddings-v2-base-en'):
        self.model_name = model_name

    def get_embedding(self, text):
        response = self._request_text(text)
        return response.json()['data'][0]['embedding']

    def get_token_num(self, text):
        response = self._request_text(text)
        return response.json()['usage']['total_tokens']

    def _request_text(self, text):
        # '''
        # {'model': 'jina-embeddings-v2-base-en', 'object': 'list', 'usage': {'total_tokens': 23, 'prompt_tokens': 23}, 'data': [
        # {'object': 'embedding', 'index': 0,
        # 'embedding': [-0.5820047, -0.5107356, ... 0.0498226]}]}
        # '''
        ## or
        # '''
        # {'detail': "ValidationError(model='TextDoc', errors=[{'loc': ('text',), 'msg': 'Single text cannot exceed 8192 tokens. 169162 tokens given.', 'type': 'value_error'}])"}
        # '''
        jina_api_key = os.getenv('JINA_API_KEY')
        url = 'https://api.jina.ai/v1/embeddings'

        headers = {
            'Content-Type': 'application/json',
            'Authorization': f'Bearer {jina_api_key}'
        }

        data = {
            'input': [text],
            'model': self.model_name
        }
        response = requests.post(url, headers=headers, json=data)
        return response


if __name__ == '__main__':
    jina_service = JinaService()
    res = jina_service.get_embedding(
        'It helped to have studied art, because the main goal of an online store builder is to make users look ')
    print(res)
