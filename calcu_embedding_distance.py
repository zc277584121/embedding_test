from models import OpenAIService
from utils.distance import vector_norm, l2_distance, ip_distance

if __name__ == '__main__':
    A = '''sentence1'''

    B = '''sentence2'''

    query = '''this is a question'''

    openai_service = OpenAIService()

    A_emb = openai_service.get_embedding(A)
    B_emb = openai_service.get_embedding(B)
    query_emb = openai_service.get_embedding(query)
    print(vector_norm(A_emb))
    print(vector_norm(B_emb))
    print(vector_norm(query_emb))
    print('')
    print('l2_distance(query_emb, A_emb) =', l2_distance(query_emb, A_emb))
    print('l2_distance(query_emb, B_emb) =', l2_distance(query_emb, B_emb))
    print('')
    print('ip_distance(query_emb, A_emb) =', ip_distance(query_emb, A_emb))
    print('ip_distance(query_emb, B_emb) =', ip_distance(query_emb, B_emb))
