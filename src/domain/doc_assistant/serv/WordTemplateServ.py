from domain.doc_assistant.entity.WordTemplateEntity import WordTemplateEntity
from domain.doc_assistant.daock import WordTemplateDaoCK
from utils import IDUtil

def create(user_file_id ,create_time ):
    newentity = WordTemplateEntity(IDUtil.get_long(),user_file_id ,create_time )
    WordTemplateDaoCK.insert(newentity)
    return newentity

def delete(word_tempalte_id):
    WordTemplateDaoCK.delete_by_id(word_tempalte_id)

def update(word_tempalte_id ,user_file_id ,create_time ):
    newentity = WordTemplateEntity(word_tempalte_id ,user_file_id ,create_time )
    WordTemplateDaoCK.update(newentity)
    return newentity

def get_entity_by_id(word_tempalte_id):
    return WordTemplateDaoCK.select_by_id(word_tempalte_id)

def get_all():
    return WordTemplateDaoCK.select_all()

def get_count():
    return WordTemplateDaoCK.select_count()

def get_vspage(row_cnt, begin, search_params = None):
    entities,total_cnt = WordTemplateDaoCK.select_vspage(row_cnt, begin,search_params)
#    id_list = [e.word_tempalte_id for e in entities]
    return entities,total_cnt

def get_page(row_cnt, begin, search_params = None):
    entities,total_cnt = WordTemplateDaoCK.select_page(row_cnt, begin,search_params)
#    id_list = [e.word_tempalte_id for e in entities]
    return entities,total_cnt

def full_search(row_cnt, begin, search_str):
    entities,total_cnt = WordTemplateDaoCK.full_search(row_cnt=row_cnt, row_begin=begin,search_str=search_str)
#    id_list = [e.word_tempalte_id for e in entities]
    return entities,total_cnt

def update_by_id(word_tempalte_id,update_params):
    entity = WordTemplateDaoCK.update_by_id(word_tempalte_id,update_params)
    return entity
