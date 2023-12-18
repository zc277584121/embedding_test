import os
import random
from collections import defaultdict

import pandas as pd
from matplotlib import pyplot as plt
from tqdm import tqdm

from models import BgeModel, CohereService, JinaService, OpenAIService, VoyageService


def prepare_input_texts(from_char_num, to_char_num, delta_char_num, datasource):
    input_texts = []
    char_num_list = []
    for char_num in range(from_char_num, to_char_num, delta_char_num):
        with open(datasource, 'r', encoding='utf-8') as file:
            text = file.read()
            assert len(text) >= char_num
            start_index = random.randint(0, len(text) - char_num)
            snippet = text[start_index: start_index + char_num]
            input_texts.append(snippet)
            char_num_list.append(char_num)
    return input_texts, char_num_list


def get_model_class_by_name(model_name):
    if 'bge' in model_name:
        return BgeModel
    if 'jina' in model_name:
        return JinaService
    if 'voyage' in model_name:
        return VoyageService
    if 'text-embedding-ada' in model_name:
        return OpenAIService
    return CohereService


def init_models(model_name_list):
    model_list = []
    for model_name in model_name_list:
        model_class = get_model_class_by_name(model_name)
        model_list.append(model_class(model_name=model_name))
    return model_list


def main(model_name_list, from_char_num, to_char_num, delta_char_num, datasource):
    datasource_name = os.path.basename(datasource).split('.')[0]
    model_list = init_models(model_name_list)
    input_texts, char_num_list, = prepare_input_texts(from_char_num=from_char_num, to_char_num=to_char_num,
                                                      delta_char_num=delta_char_num,
                                                      datasource=datasource)
    xs = char_num_list

    model_name2ys = defaultdict(list)
    for input_text, char_num in tqdm(list(zip(input_texts, char_num_list))):
        for model_name, model in zip(model_name_list, model_list):
            model_token_num = model.get_token_num(input_text)
            # import time
            # time.sleep(20)#todo
            model_name2ys[model_name].append(model_token_num)

    df = pd.DataFrame(model_name2ys)
    df.to_csv(f'./output/{datasource_name}.csv', index=False)

    for model_name, model_ys in model_name2ys.items():
        plt.plot(xs, model_ys, label=model_name)
    plt.legend()

    plt.title(f'{datasource_name} token estimate')
    plt.xlabel('char num')
    plt.ylabel('token num')

    plt.show()


if __name__ == '__main__':
    # model_name_list = ['BAAI/bge-base-en-v1.5',
    #                    'text-embedding-ada-002',
    #                    'embed-english-v2.0',
    #                    'voyage-01',
    #                    'jina-embeddings-v2-base-en',
    #                    ]
    model_name_list = [
                       'BAAI/bge-large-zh-v1.5',
                       'BAAI/bge-base-zh-v1.5',
                       'BAAI/bge-small-zh-v1.5',
        'embed-multilingual-v3.0',
        'embed-multilingual-light-v3.0',
        'embed-multilingual-v2.0'
                       ]

    main(model_name_list, from_char_num=500, to_char_num=3000, delta_char_num=500,
         datasource='./datasource/three_kingdoms.txt')
