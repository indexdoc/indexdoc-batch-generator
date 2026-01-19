from domain.doc_assistant.entity.GenerateFilesEntity import GenerateFilesEntity
from domain.doc_assistant.daock import GenerateFilesDaoCK
from utils import IDUtil

def create(user_file_id ,excel_template_id ,create_time ):
    newentity = GenerateFilesEntity(IDUtil.get_long(),user_file_id ,excel_template_id ,create_time )
    GenerateFilesDaoCK.insert(newentity)
    return newentity

def delete(generate_file_id):
    GenerateFilesDaoCK.delete_by_id(generate_file_id)

def update(generate_file_id ,user_file_id ,excel_template_id ,create_time ):
    newentity = GenerateFilesEntity(generate_file_id ,user_file_id ,excel_template_id ,create_time )
    GenerateFilesDaoCK.update(newentity)
    return newentity

def get_entity_by_id(generate_file_id):
    return GenerateFilesDaoCK.select_by_id(generate_file_id)

def get_all():
    return GenerateFilesDaoCK.select_all()

def get_count():
    return GenerateFilesDaoCK.select_count()

def get_vspage(row_cnt, begin, search_params = None):
    entities,total_cnt = GenerateFilesDaoCK.select_vspage(row_cnt, begin,search_params)
#    id_list = [e.generate_file_id for e in entities]
    return entities,total_cnt

def get_page(row_cnt, begin, search_params = None):
    entities,total_cnt = GenerateFilesDaoCK.select_page(row_cnt, begin,search_params)
#    id_list = [e.generate_file_id for e in entities]
    return entities,total_cnt

def full_search(row_cnt, begin, search_str):
    entities,total_cnt = GenerateFilesDaoCK.full_search(row_cnt=row_cnt, row_begin=begin,search_str=search_str)
#    id_list = [e.generate_file_id for e in entities]
    return entities,total_cnt

def update_by_id(generate_file_id,update_params):
    entity = GenerateFilesDaoCK.update_by_id(generate_file_id,update_params)
    return entity
