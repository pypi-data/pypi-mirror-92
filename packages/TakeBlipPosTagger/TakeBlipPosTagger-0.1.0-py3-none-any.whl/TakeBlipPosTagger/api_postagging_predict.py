import torch
import logging

import os
import json
from glob import glob
from shutil import copyfile

from predict import PosTaggerPredict

class AzuremlPosTaggingPredict():
    def __init__(self):
        self.pad_string = '<pad>'
        self.unk_string = '<unk>'
        self.set_postagging_predict()

    def set_postagging_predict(self):
        embedding_path = self.get_embedding_path(
            embedding_container = 'spellcheckedembedding', 
            embedding_model_registry_name = 'EmbeddingModel',
            embedding_name = 'titan_v2_after_correction_fasttext_window4_mincount20_cbow.kv'
        )
        postagging_model = self.get_postagging_model(
            postagging_container = 'postagging_files_from_training',
            postagging_model_registry_name = 'PostaggingModel'
        )
        postagging_label_path = self.get_postagging_label_path(
            postagging_container = 'postagging_files_from_training',
            postagging_label_registry_name = 'PostaggingLabel'
        )
        self.postagger_predicter = PosTaggerPredict(
            model=postagging_model,
            label_path=postagging_label_path,
            embedding_path=embedding_path
        )
    
    def predict(self, input_sentence):
        return self.postagger_predicter.predict_line(input_sentence)
    
    def predict_batch(self, batch_size, shuffle, use_pre_processing, output_lstm, input_sentences):
        return self.postagger_predicter.predict_batch('', '', self.pad_string, self.unk_string,
         batch_size, shuffle, use_pre_processing, output_lstm, input_sentences)

    def get_embedding_path(self, embedding_container, embedding_model_registry_name, embedding_name):
        logging.info('Getting embedding path...')
        embedding_path = self.__get_model_path(embedding_container, embedding_model_registry_name, embedding_name)
        return embedding_path

    def get_postagging_model(self, postagging_container, postagging_model_registry_name):
        logging.info('Started reading model ...')
        self.__copy_python_file(postagging_container, postagging_model_registry_name, 'model.py')
        postag_model_path = self.__get_model_path(postagging_container, postagging_model_registry_name, 'model.pkl')
        postagging_model = torch.load(postag_model_path)
        logging.info('Loaded postagging model ...')
        return postagging_model

    def get_postagging_label_path(self, postagging_container, postagging_label_registry_name):
        logging.info('Getting labels path...')
        self.__copy_python_file(postagging_container, postagging_label_registry_name, 'vocab.py')
        postagging_label_path = self.__get_model_path(postagging_container, postagging_label_registry_name, 'vocab-label.pkl')
        return postagging_label_path

    def __copy_python_file(self, postagging_container, postagging_registry_name, file_name):
        postagging_code_path = self.__get_model_path(postagging_container, postagging_registry_name, file_name)
        copyfile(postagging_code_path, os.path.join(os.getcwd() , file_name))

    def __get_model_path(self, container, model_registry_name, model_file_name):
        azure_ml_dir = os.getenv('AZUREML_MODEL_DIR')
        logging.info('Azuredir list')
        logging.info(azure_ml_dir)
        logging.info('OS list azuredir')
        logging.info(os.listdir(azure_ml_dir))
        version_container_dir = os.path.join('*', container) 
        azure_models_path = os.path.join(azure_ml_dir, '{}', version_container_dir, '{}')
        logging.info('Azure Path Test')
        logging.info(azure_models_path.format(model_registry_name, model_file_name))
        model_path = glob(azure_models_path.format(model_registry_name, model_file_name))[0]
        logging.info(model_path)
        return model_path