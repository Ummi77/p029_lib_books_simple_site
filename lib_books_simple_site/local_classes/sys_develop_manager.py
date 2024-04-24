


import sys
sys.path.append('/home/ak/projects/P21_Telegram_Channel_Parsing_Django/telegram_channel_parsing_django')
import settings_bdp_main as ms # общие установки для всех модулей

from noocube.sqlite_processor_speedup import SqliteProcessorSpeedup
from noocube.sqlite_pandas_processor_speedup import SqlitePandasProcessorSpeedup

from noocube.switch import Switch

import pyperclip

# from telegram_monitor.local_classes.sys_develop_manager import SysDevelopManager

class SysDevelopManager ():
    """ 
    Системный менеджер, помогающий в развработке проекта. автоматическое создание кодов и пр
    """
    
    
    def __init__(self): 

        self.sps = SqliteProcessorSpeedup(ms.DB_CONNECTION) # Обьект класса SqliteProcessorSpeedup
        self.spps = SqlitePandasProcessorSpeedup(ms.DB_CONNECTION) # Обьект класса SqlitePandasProcessorSpeedup
    


        
    def prepare_html_code_for_edit_table_redactor_mysql_sdm (self, db, tb, **formSettings):
        """ 
        SysDevelopManager
        Создать html-код для редактирования задаваемых данных в таблицах
        
        """
        
        print(f"PR_A487 --> START: prepare_html_code_for_edit_table_redactor_mysql_sdm()")
        
        # A. Получить список полей таблицы с их атрибутами при создании
        resfields = self.sps.meta_get_tb_fields_mysql_sps(db, tb)
        
        # print(f"PR_A486 --> listtbFields = {listtbFields}")
        
        # B. В зависимости от типа и свойств полей составить список полей формы на основе полученного массива полей и на основе предписываемых 
        # типов полей для формы
        """ 
        [['id', 'int(11)', 'NO', 'PRI', None, 'auto_increment'], ['author_first_name', 'varchar(40)', 'YES', '', None, ''], 
        ['author_second_name', 'varchar(40)', 'NO', '', None, ''], ['author_full_name', 'varchar(100)', 'YES', 'UNI', None, '']]
        """
        
        # INI: инициализация по сквозным именным параметров
        
        # НЕ УДАЛЯТЬ: Настройки формы
        # formSettings['form_action'] = f"http://127.0.0.1:6070/telegram_monitor/save_edited_lib_book"
        # formSettings['flag_form'] = True
        # formSettings['form_id'] = 'edit_authors_form'
        # formSettings['li_label_class'] = 'text-small-uppercase'
        # formSettings['li_field_class'] = 'gen_filter_inp'
        # formSettings['flag_btn_submit'] = True
        # formSettings['btn_submit_name'] = 'Сохранить'
        
        
        form_action = formSettings['form_action']
        flag_form = formSettings['flag_form']
        form_id = formSettings['form_id'] # ID формы
        li_label_class = formSettings['li_label_class']
        li_field_class = formSettings['li_field_class']
        flag_btn_submit = formSettings['flag_btn_submit']
        btn_submit_name = formSettings['btn_submit_name']
        # Словарь, определяющий. какие поля из множества полей обрабатываемой таблицы БД будут превращены в поля формы для блока оформленного  html-кода
        formFieldAssoc =  formSettings['formFieldAssoc'] 
        
        ulClass = f'ul_{form_id}'
        
        
        # for field in resfields:
        
        #     # INI
        #     """ 
        #     [['id', 'int(11)', 'NO', 'PRI', None, 'auto_increment'], ['author_first_name', 'varchar(40)', 'YES', '', None, ''], 
        #     ['author_second_name', 'varchar(40)', 'NO', '', None, ''], ['author_full_name', 'varchar(100)', 'YES', 'UNI', None, '']]
        #     """
        #     metaFieldName = field[0]
            
        #     metaFieldType = field[1]
            
        # # Словарь, определяющий. какие поля из множества полей обрабатываемой таблицы БД будут превращены в поля формы для блока оформленного  html-кода
        # formFieldAssoc = {
            
        #     'id' : 
        #             {
        #                 'prefix' : 'author', # Если есть prefix. то он добавляется слева к id и name поля (он нужен для таких названий полей. которые могуь повторится в других полях на странице)
        #                 'type' : 'hidden',
        #                 'label' : 'Имя',
        #             },
                    
        #     'author_first_name' : 
        #             {
        #                 'label' : 'Имя',
        #             },
                    
        #     '' : 
        #             {
        #                 'label' : 'Фамилия',
        #             },                    
        # }
            
            
            
        htmlCodeBlock = ""

        # Если задан флаг обертывания списка полей в тэги формы
        if flag_form:
        
            htmlCodeBlock += f'<form id="{form_id}" action="{form_action}">\n<ul>\n'
            
        else:
            htmlCodeBlock += f'<ul class="{ulClass}">\n'
        
        
        # Цикл по списку полей таблицы, полученных из мета-запроса к заданной таблице в БД
        for field in resfields:
        
            # INI 
            # название поля из множественного списка атрибутов поля, полученными из мета-запроса к заданной таблице
            # fieldName = field[0] 
            
            # поле с названием из текущего списка по спискам полей в результате мета-запроса к БД по заданной таблице
            metaTbFieldName = field[0]
            # поле с типом текущего поля из текущего списка по спискам полей в результате мета-запроса к БД по заданной таблице
            metaTbFieldType = field[1]
            
        
            # Если название из мета-поля из таблицы находится в подмножестве ключей словаря  formFieldAssoc, то включаем создание кода для этого поля для выходного блока с кодом
            if metaTbFieldName in formFieldAssoc: # fieldName ищется в ключах словаря в такой конструкции
            
                # INI
                # # Тип поля из заданного словаря ассоциаций formFieldAssoc
                # fieldType = formFieldAssoc[metaTbFieldName]['type']
                
                # название в лейбле из заданного словаря ассоц
                if 'label' in formFieldAssoc[metaTbFieldName]:
                    label = formFieldAssoc[metaTbFieldName]['label']
                else:
                    label = None
                
                # A. Вычислить корень поля из типа поля в Mysql metaTbFieldType поле из мета-запроса, в котормо хранятся множество свойств этого поля,
                # включая его тип по стандартам MySql
                """ 
                [['id', 'int(11)', 'NO', 'PRI', None, 'auto_increment'], ['author_first_name', 'varchar(40)', 'YES', '', None, ''], 
                ['author_second_name', 'varchar(40)', 'NO', '', None, ''], ['author_full_name', 'varchar(100)', 'YES', 'UNI', None, '']]
                """
                partsOfTypeField = metaTbFieldType.split('(')
                
                # Тип поля в форматах MySql
                fieldTypeMySqlFormat = partsOfTypeField[0]
                # Переприсваиваем в более стандратное название тип поля
                finalFieldType = fieldTypeMySqlFormat
                
                # B. Сверяем тип поля с типом, заданным по этому названию поля в словаре ассоциаций. И, если в словаре ассоц указано, что это поле должно иметь 
                # тип 'hidden', то присваиваем этот тип в fieldTypeMySqlFormat
                
                # Если в словаре formFieldAssoc по текущему полю с названием metaTbFieldName задан тип поля, то присваиваем этот тип к конечному типу поля
                # В конечном итоге, моэет быть два варианта: либо тип поля определяется типом в формате Mysql, либо это поле определяется насильственно в словаре 
                # ассоциаций как 'hidden' (на данный момент. В будущем моэет еще что-то появиться)
                if 'type' in formFieldAssoc[metaTbFieldName]: 
                    finalFieldType = formFieldAssoc[metaTbFieldName]['type']
                
                # Вычисляем размер поля для потенциального использования в будущем
                fieldSize = partsOfTypeField[1].strip(')')
                
                # Фиксация размера - если пустота, то fieldSize = None. Иначе fieldSize = размеру, числу в стринге
                if len(fieldSize) > 0:
                    fieldSizeInt = int(fieldSize)
                else:
                    fieldSizeInt = None
                
                print(f"PR_A491 --> fieldTypeMySqlFormat = {fieldTypeMySqlFormat}")

                # дифференциатор по конечному типу вычесленному поля и созданию соотвесттвующих html-кодов для текущих полей в зависимости от конечного типа поля finalFieldType
                # то есть автоматизируем определение типа поля и соотвтетсующее создание кода для поля . теперь это зависит только от типа поля в Mysql 
                # или насильственный 'hidden' тип из словаря ассоц
                for case in Switch(finalFieldType):
                    
                    if case('int'): 
                        print(f"PR_A493 --> SYS LOG: Тип поля с названием {metaTbFieldName} определен в дифференциаторе Switch. Конечный тип поля для обработки: 'int'")
                        fieldType = 'text'
                        
                        # конструируем название поля. если был задан его префикс в словаре ассоц formFieldAssoc
                        if 'prefix' in formFieldAssoc[metaTbFieldName]: # Если задан префикс у поля
                            prefix = formFieldAssoc[metaTbFieldName]['prefix']
                            metaTbFieldName = f"{prefix}_{metaTbFieldName}"
                        
                        if label: # Если задан  label к полю
                            htmlCodeBlock += f'\n<li><label for="author_filter" class="{li_label_class}">{label}</label></li>\n'
                            
                        htmlCodeBlock += f'\n<li><input  type="{fieldType}" id="{metaTbFieldName}" name="{metaTbFieldName}" class="{li_field_class}"  value=""></li>\n'
                        break

                    if case('varchar'): 
                        print(f"PR_A494 --> SYS LOG: Тип поля с названием {metaTbFieldName}  определен в дифференциаторе Switch. Конечный тип поля для обработки: 'varchar'")
                        fieldType = 'text'
                        
                        # конструируем название поля. если был задан его префикс в словаре ассоц formFieldAssoc
                        if 'prefix' in formFieldAssoc[metaTbFieldName]: # Если задан префикс у поля
                            prefix = formFieldAssoc[metaTbFieldName]['prefix']
                            metaTbFieldName = f"{prefix}_{metaTbFieldName}"
                        
                        htmlCodeBlock += f'\n<li><label for="author_filter" class="{li_label_class}">{label}</label></li>\n'
                        htmlCodeBlock += f'\n<li><input  type="{fieldType}" id="{metaTbFieldName}"  name="{metaTbFieldName}"  class="{li_field_class}"  value=""></li>\n'
                        break

                    if case('hidden'): 
                        print(f"PR_A495 --> SYS LOG: Тип поля с названием {metaTbFieldName}  определен в дифференциаторе Switch. Конечный насильственный тип поля для обработки: 'hidden'")
                        fieldType = 'hidden'
                        
                        # конструируем название поля. если был задан его префикс в словаре ассоц formFieldAssoc
                        if 'prefix' in formFieldAssoc[metaTbFieldName]: # Если задан префикс у поля
                            prefix = formFieldAssoc[metaTbFieldName]['prefix']
                            metaTbFieldName = f"{prefix}_{metaTbFieldName}"
                            
                        # ПРИМ: %%{metaTbFieldName}_KEY_VAL%% - это маркер для замещения текущим id автора, который сейчас редактируется в этом общем коде. 
                        # Это - изменяемая переменная на одном уровне выше
                        htmlCodeBlock += f'\n<li><input  type="{fieldType}" id="{metaTbFieldName}" name="{metaTbFieldName}"   class="{li_field_class}"  value="%%{metaTbFieldName}_KEY_VAL%%"></li>\n'
                        break

                    if case(): # default
                        print(f'PR_A492 --> SYS LOG: Тип поля не найден в диффренциаторе по типу в Switch - диффренциаторе')
                        break
                    
                
                
    
        # Если флаг вывода кнопки Submit is True
        if flag_btn_submit:
            htmlCodeBlock += f'\n<li><button type="submit" id = "sbtn_{form_id}" form="{form_id}" value="Submit">{btn_submit_name}</button></li>\n'
            
        
        if flag_form:
        
            htmlCodeBlock += f'\n</ul>\n</form>'
            
        else:
            htmlCodeBlock += f'\n</ul>'
            
        print(f"PR_A496 --> SYS LOG: htmlCodeBlock = \n{htmlCodeBlock}")
        
        # скопировать в буфер
        pyperclip.copy(htmlCodeBlock)
        
        
        print(f"PR_A488 --> END: prepare_html_code_for_edit_table_redactor_mysql_sdm()")
        
        return htmlCodeBlock
        
        



    def prepare_form_ajax_submit_jquery_code_sdm (self, **formSettings):
        """ 
        SysDevelopManager
        Составить jquery-код для отправки submit формы через AJAX
        """
        
        # INI
        
        urlViewModule = formSettings['url_view_module']
        formId = formSettings['form_id']
        
        formFieldAssoc = formSettings['formFieldAssoc']

        # A. сформировать словарь с данынми на основе полей формы (включая спрятанные)
        
        def prepare_form_data_using_form_fields_():
            """
            Подготовить код в текстовом варианте для словаря по полям формы
            """

            formData = 'var formData = \n\t\t\t{ \n'
            
            # Цикл по полям формы
            for key, val in formFieldAssoc.items():
                
                # INI
                # Если для текущего названия поля в словаре formFieldAssoc ест префикс, то надо присвоить префикс к названию поля слева
                if 'prefix' in formFieldAssoc[key]:
                    # префикс, если он задан для названия текущего поля для id поля
                    prefix = formFieldAssoc[key]['prefix']
                    fieldId = f'{prefix}_{key}'
                else:
                    fieldId = key

                fieldLine = f'\t\t\t{fieldId}: $("#{fieldId}").val(),\n'

                formData += fieldLine
                
                
            ajaxLine = '\t\t\tajax: "True",' # параметр для ajax
            formData += ajaxLine
            
            formData += '\n\t\t\t};'
            
            return formData
        
            
        # Подготовить код в текстовом варианте для словаря по полям формы
        formData = prepare_form_data_using_form_fields_()
        
        ajaxTemplate = """ 
        
            $(document).ready(function () {
            $("#%%FORM_ID%%").submit(function (event) {

            %%FORM_DATA%%

            $.ajax({
                type: "POST",
                url: "%%VIEW_MODULE%%",
                data: formData,
                dataType: "text", 
                encode: true, 
                //context: this, 
                success: (data) => { // тут можно выполнять работу с полученными данными. Позволяет разделить успешное и неуспешное завершение ajax 
                
                },
                error: (error) => {
                    alert("AJAX JQERY ERROR in View: %%VIEW_MODULE%%()");
                }

            }).done(function (data) { 

            }),
            
            event.preventDefault(); // to prevent the form from behaving by default by reloading the page on submission
            });
        });

        """
        
        # A. Заместить %%FORM_DATA%% спсиком данных по полям в словаре
        ajaxTemplate = ajaxTemplate.replace('%%FORM_DATA%%', formData)
        
        # B.  Заместить %%VIEW_MODULE%% названием модуля, к которому аппелирует AJAX
        ajaxTemplate = ajaxTemplate.replace('%%VIEW_MODULE%%', urlViewModule)
        
        # C. Заместить %%FORM_ID%% id формы
        ajaxTemplate = ajaxTemplate.replace('%%FORM_ID%%', formId)
        
        # скопировать в буфер
        pyperclip.copy(ajaxTemplate)

            
        
        # print(f"PR_A503 --> ajaxTemplate = \n{ajaxTemplate}")
        
        return ajaxTemplate



        
        













if __name__ == '__main__':
    pass




    # # # ПРОРАБОТКА: prepare_html_code_for_edit_table_redactor_mysql_sdm () -->  для таблицы lib_book_statuses и метода VIEW: save_book_status_edited_data
    
    # # INI
    # sdm = SysDevelopManager()
    
    # # SETS

    # # Словарь, определяющий. какие поля из множества полей обрабатываемой таблицы БД будут превращены в поля формы для блока оформленного  html-кода
    # formFieldAssoc = {
        
    #     'id' : 
    #             {
    #                 'prefix' : 'book_status', # Если есть prefix. то он добавляется слева к id и name поля (он нужен для таких названий полей. которые могуь повторится в других полях на странице)
    #                 'type' : 'hidden',
    #             },
                
    #     'book_status' : 
    #             {
    #                 'label' : 'Статус',
    #             },
    
    # }
    
    
    
    # formSettings = {}
    # formSettings['form_action'] = ""
    # formSettings['flag_form'] = True
    # formSettings['form_id'] = 'edit_book_status_form'
    # formSettings['li_label_class'] = 'text-small-uppercase'
    # formSettings['li_field_class'] = 'gen_filter_inp'
    # formSettings['flag_btn_submit'] = True
    # formSettings['btn_submit_name'] = 'Сохранить'
    # formSettings['formFieldAssoc'] = formFieldAssoc


    # # PARS:
    # db = 'labba'
    # tb = 'lib_book_statuses'
    
    # htmlCodeBlock = sdm.prepare_html_code_for_edit_table_redactor_mysql_sdm(db, tb, **formSettings)
    
    # print(f"PR_A502 --> htmlCodeBlock = {htmlCodeBlock}")





    
    

    # # ПРОРАБОТКА: prepare_html_code_for_edit_table_redactor_mysql_sdm () -->  для таблицы lib_authors и метода VIEW: save_edited_lib_book
    
    # # INI
    # sdm = SysDevelopManager()
    
    # # SETS

    # # Словарь, определяющий. какие поля из множества полей обрабатываемой таблицы БД будут превращены в поля формы для блока оформленного  html-кода
    # formFieldAssoc = {
        
    #     'id' : 
    #             {
    #                 'prefix' : 'author', # Если есть prefix. то он добавляется слева к id и name поля (он нужен для таких названий полей. которые могуь повторится в других полях на странице)
    #                 'type' : 'hidden',
    #                 'label' : 'Имя',
    #             },
                
    #     'author_first_name' : 
    #             {
    #                 'label' : 'Имя',
    #             },
                
    #     'author_second_name' : 
    #             {
    #                 'label' : 'Фамилия',
    #             },                    
    # }
    
    
    
    # formSettings = {}
    # formSettings['form_action'] = f"http://127.0.0.1:6070/telegram_monitor/save_edited_lib_book"
    # formSettings['flag_form'] = True
    # formSettings['form_id'] = 'edit_authors_form'
    # formSettings['li_label_class'] = 'text-small-uppercase'
    # formSettings['li_field_class'] = 'gen_filter_inp'
    # formSettings['flag_btn_submit'] = True
    # formSettings['btn_submit_name'] = 'Сохранить'
    # formSettings['formFieldAssoc'] = formFieldAssoc


    # # PARS:
    # db = 'labba'
    # tb = 'lib_authors'
    
    # htmlCodeBlock = sdm.prepare_html_code_for_edit_table_redactor_mysql_sdm(db, tb, **formSettings)
    
    # print(f"PR_A502 --> htmlCodeBlock = {htmlCodeBlock}")





    # # ПРОРАБОТКА: prepare_form_ajax_submit_jquery_code_sdm ()

    
    # # INI
    # sdm = SysDevelopManager()
    
    # # SETS

    # # Словарь, определяющий. какие поля из множества полей обрабатываемой таблицы БД будут превращены в поля формы для блока оформленного  html-кода
    # formFieldAssoc = {
        
    #     'id' : 
    #             {
    #                 'prefix' : 'author', # Если есть prefix. то он добавляется слева к id и name поля (он нужен для таких названий полей. которые могуь повторится в других полях на странице)
    #                 'type' : 'hidden',
    #             },
                
    #     'author_first_name' : 
    #             {
    #                 'label' : 'Имя',
    #             },
                
    #     'author_second_name' : 
    #             {
    #                 'label' : 'Фамилия',
    #             },                    
    # }
    
    
    
    # formSettings = {}
    # formSettings['form_action'] = f"http://127.0.0.1:6070/telegram_monitor/save_edited_lib_book"
    # formSettings['url_view_module'] = f"save_book_author_edited_data"
    # formSettings['flag_form'] = True
    # formSettings['form_id'] = 'edit_authors_form'
    # formSettings['li_label_class'] = 'text-small-uppercase'
    # formSettings['li_field_class'] = 'gen_filter_inp'
    # formSettings['flag_btn_submit'] = True
    # formSettings['btn_submit_name'] = 'Сохранить'
    # formSettings['formFieldAssoc'] = formFieldAssoc
    



    # sdm.prepare_form_ajax_submit_jquery_code_sdm(**formSettings)






