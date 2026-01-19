from domain.doc_assistant.entity.ExcelTemplateEntity import ExcelTemplateEntity
from domain.doc_assistant.daock import ExcelTemplateDaoCK
from utils import IDUtil

def create(user_file_id ,create_time ):
    newentity = ExcelTemplateEntity(IDUtil.get_long(),user_file_id ,create_time )
    ExcelTemplateDaoCK.insert(newentity)
    return newentity

def delete(excel_template_id):
    ExcelTemplateDaoCK.delete_by_id(excel_template_id)

def update(excel_template_id ,user_file_id ,create_time ):
    newentity = ExcelTemplateEntity(excel_template_id ,user_file_id ,create_time )
    ExcelTemplateDaoCK.update(newentity)
    return newentity

def get_entity_by_id(excel_template_id):
    return ExcelTemplateDaoCK.select_by_id(excel_template_id)

def get_all():
    return ExcelTemplateDaoCK.select_all()

def get_count():
    return ExcelTemplateDaoCK.select_count()

def get_vspage(row_cnt, begin, search_params = None):
    entities,total_cnt = ExcelTemplateDaoCK.select_vspage(row_cnt, begin,search_params)
#    id_list = [e.excel_template_id for e in entities]
    return entities,total_cnt

def get_page(row_cnt, begin, search_params = None):
    entities,total_cnt = ExcelTemplateDaoCK.select_page(row_cnt, begin,search_params)
#    id_list = [e.excel_template_id for e in entities]
    return entities,total_cnt

def full_search(row_cnt, begin, search_str):
    entities,total_cnt = ExcelTemplateDaoCK.full_search(row_cnt=row_cnt, row_begin=begin,search_str=search_str)
#    id_list = [e.excel_template_id for e in entities]
    return entities,total_cnt

def update_by_id(excel_template_id,update_params):
    entity = ExcelTemplateDaoCK.update_by_id(excel_template_id,update_params)
    return entity
