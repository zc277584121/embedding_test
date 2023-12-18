from sentence_transformers import SentenceTransformer
from models.base import ModelService
from transformers import AutoTokenizer, AutoModel


class BgeModel(ModelService):
    """
    https://huggingface.co/BAAI/bge-base-en-v1.5
    """

    def __init__(self, model_name='BAAI/bge-base-en-v1.5'):
        self.model_name = model_name
        self.tokenizer = AutoTokenizer.from_pretrained(model_name)
        self.model = SentenceTransformer(model_name)

    def get_embedding(self, text, normalize_embeddings=True):
        return self.model.encode([text], normalize_embeddings=normalize_embeddings)[0]

    def get_token_num(self, text):
        tokens = self.tokenizer(text, padding=True, truncation=False, return_tensors="pt")
        return len(tokens['input_ids'][0])


if __name__ == '__main__':
    model = BgeModel()
    # res = model.get_embedding('I am a student')
    res = model.get_token_num('I am a student')
    print(res)
