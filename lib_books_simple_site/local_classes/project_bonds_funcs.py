
### TODO: УДАЛИТЬ ЭТОТ МОДУЛЬ. Перенести все необходимое в локальные функции

from noocube.sqlite_processor_speedup import SqliteProcessorSpeedup
from noocube.sqlite_pandas_processor_speedup import SqlitePandasProcessorSpeedup
# from noocube.django_view_manager import DjangoViewManager
from noocube.bonds_main_manager_speedup import BondsMainManagerSpeedup
from noocube.request_manager_jango import RequestManagerJango
from noocube.pandas_manager import PandasManager
from noocube.sql_syntaxer import SQLSyntaxer
from noocube.json_manager import JsonManager
import pandas as pd
# import noocube.funcs_general  as FG

# import uno
# from com.sun.star.beans import PropertyValue

# Динамическое подключение settings_bdp_main в корне проекта
import sys
sys.path.append('/home/ak/projects/P21_Telegram_Channel_Parsing_Django/telegram_channel_parsing_django')
import settings_bdp_main as ms # общие установки для всех модулей


class ProjectBondsFunctions ():
    """ 
    Методы проекта, связанные с облигациями и, в частности, с БД 'bonds'
    dicTrhough - сквозной словарь данных (аналог **kwargs)
    """


    def __init__(self, dicTrough={}):
        self.db_uri = f"sqlite:///{ms.DB_CONNECTION.dataBase}" # Pandas по умолчанию работает через SQLAlchemy и может создавать сама присоединение к БД по формату адреса URI (см. в документации SQLAlchemy)
        self.db_connection = ms.DB_CONNECTION
        self.sps = SqliteProcessorSpeedup(self.db_connection) # Обьект класса SqliteProcessorSpeedup
        self.spps = SqlitePandasProcessorSpeedup(self.db_connection) # Обьект класса SqlitePandasProcessorSpeedup
        self.bmms = BondsMainManagerSpeedup(self.db_connection)
        # self.request = request
        self.dicTrough = dicTrough
        

        # self.fullviewName = request.resolver_match.view_name # Полное название текущего View
        




    @staticmethod
    def add_to_context_left_nav_dict(context):
        """ 
        ProjectBondsFunctions
        Добавить к контекстной переменной значения словаря для левого навигатора , для его разделов-подразделов
        """
        
        dfPackages = ProjectBondsFunctions.get_index_packages_static_pbf(getFields = ['nick'])
        
        listInxPckgs = PandasManager.get_columns_vals_as_list_static(dfPackages, 'nick')
        
        context['left_nav'] = {}
        context['left_nav']['inx_pckgs'] = listInxPckgs
        
        return context




    def view_context_inicialization_pbf (self):
        """ 
        Инициализация дефолтных парметров контекста View
        """
        
        # Раскрытие раздела левой панели навигации в зависимости от названия текущего View
        if self.dicTrough['appView'] in ms.LEFT_NAVIGATOR_ACTIVE_:
            leftNavActive = ms.LEFT_NAVIGATOR_ACTIVE_[self.dicTrough['appView']] # dicDecor['appView'] - Название текущего View задает маркер раскрытия левого навигатора
        else:
            leftNavActive = ''
        
        
        # Формирование кода таблицы в контексте, если таблица предусмотрена
        if 'tableCode' in self.dicTrough:
            tbCode = self.dicTrough['tableCode']
        else:
            tbCode = ''
            
        # Формирование кол-ва рядов исходного для подсчета рядов фрейма, если фрейм и таблица предусмотрены View
        if 'dfQn' in self.dicTrough:
            dfQn = self.dicTrough['dfQn']
        else:
            dfQn = ''
            
        # Стандартные параметры для контекста вывода таблиц по фрейму на сайт
        baseContext = {
            'tbCode' : tbCode,
            'left_nav_view' : leftNavActive, # Открывающийся раздел в левом навигаторе
            'df_qn' : dfQn,
            # 'dfPackages' : self.bmms.get_index_packages_df_BMMS(), # фрейм с индексными пакетами 
            # 'srch_str' : srch_str,
        }
        
        
        # Для выделения подразделов левого навигатора и прочих применений
        baseContext['view'] = self.dicTrough['appView']
        # print(f"LLLLLLLLLLL   PR_119 baseContext['view'] = {baseContext['view']}")
        
        # Вставка элемента в зависимости от его присутствия в self.requestDic
        
        # Добавить месяц в baseContext
        if 'payment_month' in self.dicTrough['requestDic']:
            baseContext['payment_month'] = self.dicTrough['requestDic']['payment_month']
            
        # Добавить поисковый текстовый фрагмент
        if 'srch_str' in self.dicTrough['requestDic']:
            baseContext['srch_str'] = self.dicTrough['requestDic']['srch_str']
            
            
        # Добавить наименование текущей страницы сайта
        if 'pg_title' in self.dicTrough:
            baseContext['pg_title'] = self.dicTrough['pg_title']
            
        # context['left_nav']['inx_pckgs']
        # # Добавить словари с  разделами-подразделами левого навигатора , сожержащихся в context['left_nav'] словаре. Прим: context['left_nav']['inx_pckgs'] - подразделы раздела Индексных пакетов
        # baseContext = ProjectBondsFunctions.add_to_context_left_nav_dict(baseContext) 

            
        # # добавить динамические разделы -подразделы левого меню
        # inxPckgs = 

        return baseContext





    @staticmethod
    def view_inicilization_pbf (request, viewFrameProcSettings):
        """ 
        ProjectBondsFunctions
        Инициализировать необходимые обще-дефолтные данные для View, а именно:
        bmms - модуль необходимых методов работы с облигациями
        requestDic - словарь аргументов url-строки из request
        dicDecorRes - сквозной словарь для декораторов, в котором инициализируются названия приложения dicDecorRes['appName']  и название метода view dicDecorRes['appView']
        dicDecorRes['decor_kwargs']  - общие настройки для всех Views, которые связаны с построением табличного кода для вывода на сайт
        Category: Request JANGO
        """
        
        bmms = BondsMainManagerSpeedup(ms.DB_CONNECTION) # Подключение к конекшену

        # Словарь URL-параметров
        requestDic = RequestManagerJango.read_urls_args_dic_from_request_django(request)
        
        # TODO: Изменить имя. Сквозной словарь не связан только с результатом по декораторам. Он более общий. имя типа: dicProjEndToEnd
        dicDecorRes = {} # Сквозной входной-выходной словарь декораторов, куда можно записывать любые данные и который проходит сквозь все декораторы как репозиторий параметров
        
        # Присвоить в сквозной словарь словарь текущих атрибутов URL строки
        dicDecorRes['requestDic'] = requestDic
        
        # Считывание и внесение в dicDecorRes названий приложения и текущего View . Обязательно использовать при использовании декораторов вначале каждого view с декораторами!!!
        dicDecorRes = RequestManagerJango.read_curr_application_and_view_names_to_dic_decor (request, dicDecorRes)
        
        # Дефолтные установки по именным параметрам декораторов, если они не заданы в settings.py
        
        if 'formatters' in viewFrameProcSettings : # Форматеры
            fromaters = viewFrameProcSettings['formatters']
        else:
            fromaters = {}
            
        
        if 'table_codes' in viewFrameProcSettings : # Форматеры
            tableCodes = viewFrameProcSettings['table_codes']
        else:
            tableCodes = {}
        
        if 'assoc_titles' in viewFrameProcSettings : # Форматеры
            assocTitles = viewFrameProcSettings['assoc_titles']
        else:
            assocTitles = {}
            
            
        # Настройки именных параметров для основного декоратора процедурного фрейма с учетом дефолтных настроек
        # TODO: Изменить ключ на что-то типа : 'gen_decor_settings' или 'view_gen_settings'
        dicDecorRes['decor_kwargs'] = {
            
            'table_codes' :tableCodes,
            'pagination' : ms.PAGINATOR_SET_FUNCS_,
            'filtering' : ms.FILTERS_EXPR_TEMPLATES_FOR_FUNCS_BY_TYPE_V2_, # Общая для всех Views ( все фильтры хранятся в одной и той же константе)
            'sorting' : ms.SORT_SETTINGS,
            'formatters': fromaters,
            'assoc_titles': assocTitles,
            
        }
        
        return bmms, requestDic, dicDecorRes




    ########### ОПЕРАЦИИ С ОБЛИГАЦИЯМИ
    
    def get_inx_package_id_by_nickname_pbf(self, nick):
        """Получить id индексного пакета по его ник-нейму"""
        
        sql = f'SELECT id FROM index_packages WHERE nick = "{nick}"'
        res = self.sps.get_result_from_sql_exec_proc_sps(sql)

        return res[0]


    def get_inx_package_nick_by_id_pbf(self, id):
        """Получить nick индексного пакета по его id"""
        
        sql = f'SELECT nick FROM index_packages WHERE id = "{id}"'
        res = self.sps.get_result_from_sql_exec_proc_sps(sql)

        return res[0]


    def get_index_packages_pbf(self, getFields = ['*']):
        """Получить фрейм с индексными пакетами из табл 'index_packages' из БД 'bonds' """

        if getFields[0] == '*':
            sql = 'SELECT * FROM index_packages'
        else:
            fields = ','.join(getFields)
            sql = f'SELECT {fields} FROM index_packages'
            # print(f"sql = {sql}")

        dfPackages = self.spps.read_sql_to_df_pandas_SPPS(sql)

        return dfPackages




    
    @staticmethod
    def get_index_packages_static_pbf(getFields = ['*']):
        """
        ProjectBondsFunctions
        Получить фрейм с индексными пакетами из табл 'index_packages' из БД 'bonds' 
        """

        spps = SqlitePandasProcessorSpeedup(ms.DB_CONNECTION)

        if getFields[0] == '*':
            sql = 'SELECT * FROM index_packages'
        else:
            fields = ','.join(getFields)
            sql = f'SELECT {fields} FROM index_packages'
            # print(f"sql = {sql}")

        dfPackages = spps.read_sql_to_df_pandas_SPPS(sql)

        return dfPackages



    @staticmethod
    def get_dic_index_packages_static_pbf(getFields = ['*']):
        """
        ProjectBondsFunctions
        Получить словарь с индексными пакетами из табл 'index_packages' из БД 'bonds' 
        """

        dfPackages = ProjectBondsFunctions.get_index_packages_static_pbf(getFields)
        dicInxPackages = {}
        for inx, row in dfPackages.iterrows():
            pass
            key = row['id']
            val = row['nick']
            
            dicInxPackages[key] = val
        
        

        return dicInxPackages





    def get_full_atributes_frame_with_all_inx_pckg_bonds_pbf (self, inxPckgNick):
        """ 
        OBSOLETED: Use get_full_atributes_frame_with_all_inx_pckg_bonds_pbf_v2 ()
        Получить фрейм со всеми облигациями из задаваемого индексного пакета и со всеми атрибутами облигаций , основанных на множестве всех архивных облигаций из таблиц '..._archive'
        inxPckgNick - ник индексного пакета
        """
        
        # Получить ID индексного пакета по его ник-нейму
        inxPckgId = self.get_inx_package_id_by_nickname_pbf(inxPckgNick)
        # Получить название таблицы для задаваемого индексного пакета
        # inxPckgTb = f"inx_package_{inxPckgId}"
        
        # B. Получить ИСИН облигаций заданного индексного пакета
        listIsins = self.bmms.get_isins_list_from_inx_pkg_with_given_id_bmms(inxPckgId)
        
        # print(f"PR_472 --> listIsins = {listIsins}")
        
        # print(f"PR_474 --> listIsins_N = {len(listIsins)}")
        # Получить комплекс всех облигаций из таблиц с расширением '..._archive'
        dfComplexArchive = self.bmms.get_complex_bonds_archive_df_with_added_diff_columns_bmms()
        
        # C. Отфильтровать из общего комплексного массива те облигации, которые есть в списке listIsins
        dfInxPckgWithArchiveTbs  = PandasManager.filter_df_by_field_vals_list(dfComplexArchive, 'isin', listIsins)
        # PandasManager.print_df_gen_info_pandas_IF_DEBUG_static(dvm.dicDecorRes['df'] , True, marker="PR_473 -->")
        
        return dfInxPckgWithArchiveTbs
        



    def get_full_atributes_df_of_inx_pckg_bonds_archive_dim_pbf_v2 (self, inxPckgNick):
        """ 
        Версия 2: Используем теперь единую таблицу для всех облигаций из индексных пакетов 'inx_packgs_bonds'

        Получить фрейм со всеми облигациями из задаваемого индексного пакета и со всеми атрибутами облигаций , основанных на множестве всех архивных облигаций из таблиц '..._archive'
        inxPckgNick - ник индексного пакета
        """
        
        print(f"PR_579 --> inxPckgNick = {inxPckgNick}")
        
        # Получить ID индексного пакета по его ник-нейму
        inxPckgId = self.get_inx_package_id_by_nickname_pbf(inxPckgNick)
        print(f"PR_580 --> inxPckgId = {inxPckgId}")
        # Получить название таблицы для задаваемого индексного пакета
        # inxPckgTb = f"inx_package_{inxPckgId}"
        
        # B. Получить ИСИН облигаций заданного индексного пакета
        listIsins = self.bmms.get_isins_list_from_inx_pkg_bonds_tb_with_given_pckg_id_bmms(inxPckgId)
        
        print(f"PR_472 --> listIsins = {listIsins}")
        
        # print(f"PR_474 --> listIsins_N = {len(listIsins)}")
        # Получить комплекс всех облигаций из таблиц с расширением '..._archive'
        dfComplexArchive = self.bmms.get_complex_bonds_archive_df_with_added_diff_columns_bmms()
        
        # C. Отфильтровать из общего комплексного массива те облигации, которые есть в списке listIsins
        dfInxPckgWithArchiveTbs  = PandasManager.filter_df_by_field_vals_list(dfComplexArchive, 'isin', listIsins)
        # PandasManager.print_df_gen_info_pandas_IF_DEBUG_static(dvm.dicDecorRes['df'] , True, marker="PR_473 -->")
        
        print(f"PR_584 --> END: get_full_atributes_frame_with_all_inx_pckg_bonds_pbf_v2()")
        
        return dfInxPckgWithArchiveTbs
    
    
    

    def get_df_of_inx_pckg_bonds_inner_joined_with_bonds_arch_and_bonds_bought_pbf (self, inxPckgNick):
        """ 
        Получить  записи из индексного пакета, расширенные всем и атрибутами этих облигаций из таблицы bonds_archive      
        inxPckgNick - ник индексного пакета
        """
        
        print(f"PR_902 -->START: get_united_atributes_df_of_inx_pckg_bonds_and_its_archive_extension_pbf()")
        
        # Получить ID индексного пакета по его ник-нейму
        inxPckgId = self.get_inx_package_id_by_nickname_pbf(inxPckgNick)
        print(f"PR_903 --> inxPckgId = {inxPckgId}")
        # Получить название таблицы для задаваемого индексного пакета
        # inxPckgTb = f"inx_package_{inxPckgId}"
        
        # A. Сложный SQL- запрос, включая комплексный запрос со всех архивных типов облигаций
        # TODO: Выбирать нужно из комлексного массива облигаций, а не только от корпоративов, Так как в индексных пакетах могут быть
        # все типы облигаций
        
        sql = f"""SELECT *, SUM (bb.qn) as sum_qn
                    FROM inx_packgs_bonds AS ipb 
                    INNER JOIN
                    (SELECT * FROM bonds_archive UNION SELECT * FROM ofz_archive UNION SELECT * FROM municip_archive) AS bcmplx
                    ON ipb.bond_isin  = bcmplx.isin 
                    LEFT JOIN
                    bonds_bought AS bb
                    ON ipb.bond_isin  = bb.isin 
                    LEFT JOIN
                    (SELECT * FROM comp_bond_analisys AS cba 
                    LEFT JOIN comp_analisys as ca
                    ON cba.inn=ca.inn) as cbaca	
                    ON ipb.bond_isin  = cbaca.isin
                    WHERE ipb.inx_pckg_id={inxPckgId}
                    GROUP BY ipb.bond_isin
        """
        
        print(f"PR_906 --> sql = {sql}")
        
        # B. Получить фрейм на оснвое sql
        df = self.spps.read_sql_to_df_pandas_SPPS(sql)
        # PandasManager.print_df_gen_info_pandas_IF_DEBUG_static(df,  False, colsIndxed = True, marker=f"PR_967 --> df")
        
        
        # C. Конвертировать колонки с процентами в флоат
        colListToConvert = ['annual_yield', 'last_annual_yield', 'curr_price']
        df = PandasManager.convert_list_of_df_columns_clear_from_str_empty_with_persent_and_empty_str_to_float_pm (df, colListToConvert)
        
        
        # # B. Получить ИСИН облигаций заданного индексного пакета
        # listIsins = self.bmms.get_isins_list_from_inx_pkg_bonds_tb_with_given_pckg_id_bmms(inxPckgId)
        
        # print(f"PR_904 --> listIsins = {listIsins}")
        
        # # print(f"PR_474 --> listIsins_N = {len(listIsins)}")
        # # Получить комплекс всех облигаций из таблиц с расширением '..._archive'
        # dfComplexArchive = self.bmms.get_complex_bonds_archive_df_with_added_diff_columns_bmms()
        
        # # C. Отфильтровать из общего комплексного массива те облигации, которые есть в списке listIsins
        # dfInxPckgWithArchiveTbs  = PandasManager.filter_df_by_field_vals_list(dfComplexArchive, 'isin', listIsins)
        # # PandasManager.print_df_gen_info_pandas_IF_DEBUG_static(dvm.dicDecorRes['df'] , True, marker="PR_473 -->")
        
        print(f"PR_905 --> END: get_united_atributes_df_of_inx_pckg_bonds_and_its_archive_extension_pbf()")
        
        return df



    def get_full_atributes_df_with_inx_pckg_current_tbs_bonds_intersection_pbf (self, inxPckgNick):
        """ 
        OBSOLETED: Use get_full_atributes_df_with_inx_pckg_current_tbs_bonds_intersection_pbf_v2(). Ранее использовались индивидуальные таблицы для индексных пакетов
        Получить фрейм с полно-атрибутными облигациями из индексного пакета, которые пересекаются с множеством текущих оперативных облигаций из
        таблиц с расширением '..._current'
        inxPckgNick - ник индексного пакета
        """
        
        # Получить ID индексного пакета по его ник-нейму
        inxPckgId = self.get_inx_package_id_by_nickname_pbf(inxPckgNick)
        # Получить название таблицы для задаваемого индексного пакета
        # inxPckgTb = f"inx_package_{inxPckgId}"
        
        # B. Получить ИСИН облигаций заданного индексного пакета
        listIsins = self.bmms.get_isins_list_from_inx_pkg_with_given_id_bmms(inxPckgId)
        
        # print(f"PR_472 --> listIsins = {listIsins}")
        
        # print(f"PR_474 --> listIsins_N = {len(listIsins)}")
        
        # Получить комплекс всех облигаций из таблиц с расширением '..._current'
        dfComplexCurrent = self.bmms.get_complex_bonds_df_with_added_diff_columns_BMMS_v2()
        
        # C. Отфильтровать из общего комплексного массива те облигации, которые есть в списке listIsins
        dfInxPckgWithCurrentTbs  = PandasManager.filter_df_by_field_vals_list(dfComplexCurrent, 'isin', listIsins)
        # PandasManager.print_df_gen_info_pandas_IF_DEBUG_static(dvm.dicDecorRes['df'] , True, marker="PR_473 -->")
        
        return dfInxPckgWithCurrentTbs



    def get_full_atributes_df_of_inx_pckg_bonds_current_dim_pbf_v2 (self, inxPckgNick):
        """ 
        Версия 2: Используем теперь единую таблицу для всех облигаций из индексных пакетов 'inx_packgs_bonds'
        Получить фрейм с полно-атрибутными облигациями из индексного пакета, которые пересекаются с множеством текущих оперативных облигаций из
        таблиц с расширением '..._current'
        inxPckgNick - ник индексного пакета
        """
        
        # Получить ID индексного пакета по его ник-нейму
        inxPckgId = self.get_inx_package_id_by_nickname_pbf(inxPckgNick)
        # Получить название таблицы для задаваемого индексного пакета
        # inxPckgTb = f"inx_package_{inxPckgId}"
        
        # B. Получить ИСИН облигаций заданного индексного пакета из таблицы 'inx_packgs_bonds' по ключу inxPckgId
        listIsins = self.bmms.get_isins_list_from_inx_pkg_bonds_tb_with_given_pckg_id_bmms(inxPckgId)
        
        # print(f"PR_472 --> listIsins = {listIsins}")
        
        # print(f"PR_474 --> listIsins_N = {len(listIsins)}")
        
        # Получить df комплекс всех облигаций из таблиц с расширением '..._current'
        dfComplexCurrent = self.bmms.get_complex_bonds_df_with_added_diff_columns_BMMS_v2()
        
        # C. Отфильтровать из общего комплексного массива те облигации, которые есть в списке listIsins
        dfInxPckgWithCurrentTbs  = PandasManager.filter_df_by_field_vals_list(dfComplexCurrent, 'isin', listIsins)
        # PandasManager.print_df_gen_info_pandas_IF_DEBUG_static(dvm.dicDecorRes['df'] , True, marker="PR_473 -->")
        
        return dfInxPckgWithCurrentTbs



    def get_full_atributes_frame_of_given_list_isins_pbf (self, listIsins):
        """ 
        Получить фрейм облигаций со всеми атрибутами соответствующих задаваемому списку ИСИНов 
        inxPckgNick - ник индексного пакета
        """

        # print(f"PR_474 --> listIsins_N = {len(listIsins)}")
        # Получить комплекс всех облигаций из таблиц с расширением '..._archive'
        dfComplexArchive = self.bmms.get_complex_bonds_archive_df_with_added_diff_columns_bmms()
        
        # C. Отфильтровать из общего комплексного массива те облигации, которые есть в списке listIsins
        dfGivenIsinsList  = PandasManager.filter_df_by_field_vals_list(dfComplexArchive, 'isin', listIsins)
        # PandasManager.print_df_gen_info_pandas_IF_DEBUG_static(dvm.dicDecorRes['df'] , True, marker="PR_473 -->")
        
        return dfGivenIsinsList
    




    def get_full_atributes_bonds_form_inx_pckg_that_not_in_current_tbs_bonds_pbf (self, inxPckgNick):
        """ 
        Получить фрейм с полно-атрибутными облигациями из индексного пакета, которые пересекаются с множеством текущих оперативных облигаций из
        таблиц с расширением '..._current'
        То есть облигации, которые есть в индексном пакете, но которых нет в массиве текущих оперативных облигаций из таблиц '..._current'
        inxPckgNick - ник индексного пакета
        """
        
        print(f"PR_583 --> START: get_full_atributes_bonds_form_inx_pckg_that_not_in_current_tbs_bonds_pbf()")
        
        # 1. Получить ID индексного пакета по его ник-нейму
        inxPckgId = self.get_inx_package_id_by_nickname_pbf(inxPckgNick)
        
        print(f"PR_586 --> (1) - DONE")
        
        # 2. Получить комплексный список исинов из таблиц '..._current'
        dfComplexCurrentTbs = self.bmms.get_complex_bonds_df_with_added_diff_columns_BMMS_v2()
        print(f"PR_587 --> (2) - DONE")
    
        # 3. Получить фрейм исин всех обл из текущего индексного пакета
        dfPkgIsins =  self.bmms.get_isins_from_inx_pkg_bonds_by_pckg_id_BMMS (inxPckgId)
        print(f"PR_588 --> (3) - DONE")
        
        # 4. Получить список исин всех обл из текущего индексного пакета
        listPkgIsins = PandasManager.get_unique_col_vals_as_list_static(dfPkgIsins,'bond_isin') # Список исинов облигаций в индексном пакете
        print(f"PR_589 --> (4) - DONE")
        # print(f"PR_480 --> listPkgIsins = {listPkgIsins}")
        # print(f"PR_481 --> listPkgIsins_N = {len(listPkgIsins)}")

        
        
        # K. Получить список ИСИНов из комплексного массива облигаций из таблиц '..._currrent'
        listComplexCurrentTbs = PandasManager.get_unique_col_vals_as_list_static(dfComplexCurrentTbs,'isin')
        # print(f"PR_482 --> listComplexCurrentTbs_N = {len(listComplexCurrentTbs)}")
        
        
        # L. Поулчить список облигаций из текущего индексного пакета, которых нет в комплексном массиве текущих облигаций  из таблиц '..._currrent'
        listIsinsOuts = [x for x in listPkgIsins if x not in listComplexCurrentTbs]
        # print(f"PR_483 --> listIsinsOuts_N = {len(listIsinsOuts)}")
        
        
        
        
        # H. Получить фрейм с полно-атрибутными данными облигаций из задаваемог лосписка ИСИНов
        dfInxPckgOuts = self.get_full_atributes_frame_of_given_list_isins_pbf(listIsinsOuts)

        
        print(f"PR_585 --> END: get_full_atributes_bonds_form_inx_pckg_that_not_in_current_tbs_bonds_pbf()")
        
        return dfInxPckgOuts



    def get_inx_pckg_tb_name_by_pckg_nick (self, inxPckgNick):
        """ 
        Получить название таблицы индексного пакета оп его нику
        """
        
        inxPckgId = self.get_inx_package_id_by_nickname_pbf(inxPckgNick)
        inxPckgTbName = f"inx_package_{inxPckgId}"
        
        return inxPckgTbName
    
    
    

    def get_inx_pckg_tb_name_by_pckg_id (self, inxPckgId):
        """ 
        OBSOLETED: Больше нет отдельных таблиц для индексных пакетов. Есть единая множественная таблица
        Получить название таблицы индексного пакета оп его id
        """
        
        inxPckgTbName = f"inx_package_{inxPckgId}"
        
        return inxPckgTbName
    
    
    
    def get_inx_pckg_id_of_bond_by_isin_from_inx_packgs_bonds_pbf (self, isin):
        """ 
        Получить ID индексного пакета для облигации из таблицы 'inx_packgs_bonds' по еее ИСИН
        """
        
        sql = f"SELECT inx_pckg_id FROM inx_packgs_bonds WHERE bond_isin = '{isin}'"
        
        res = self.sps.get_result_from_sql_exec_proc_sps(sql)
        
        if not isinstance (res, int):
            ret = res[0]
        else:
            ret = -1
            
        return ret
        
        
        
    
    
    
    def get_lists_of_isins_of_inx_packages_pbf(self):
        """ 
        Получить списки ИСИНов и всех индексных пакетов 
        """
        
        # Получить ID индексных пакетов
        inxPcgsIds = self.bmms.get_inx_packages_id_bmms()
        
        # Словарь с ИСИНами облишаций в индексных пакетах
        dicInxPckgsIsins = {}
        
        # Цикл по индексным пакетам
        for inxPckgId in inxPcgsIds:
        
            # Получить ID индексного пакета по его ник-нейму
            inxPckgNick = self.bmms.get_nickname_by_inx_package_id_BMMS(inxPckgId)
            # Получить название таблицы для задаваемого индексного пакета
            # inxPckgTb = f"inx_package_{inxPckgId}"
        
            # Ошибка может быть потому, что нет таблицы с пакетом облигаций по  id-пакета, так как систему переводим на другой поодход,
            # в которм все облигации индексных пакетов хранятся в однйо многие-ко-многим таблице 'inx_packgs_bonds'
            try:
                # B. Получить ИСИН облигаций заданного индексного пакета
                listIsins = self.bmms.get_isins_list_from_inx_pkg_with_given_id_bmms(inxPckgId)
                
            except:
                listIsins = []
                
            # Присвоить в словарь
            dicInxPckgsIsins[inxPckgNick] = listIsins
            
        return dicInxPckgsIsins
    
    
    
    def get_unique_emitents_inns_list_from_given_inx_pckg_by_id_pbf (self, inxPckgId):
        """ 
        Получить уникальные ИНН эмитентов, облигации которых входят в заданный по ID индексный пакет
        """
        
        dfInxPckgInns = self.get_df_emitents_inns_isins_from_given_inx_pckg_by_id_pbf(inxPckgId)
        
        # список уникальных ИНН эмитентов из заданного индексного пакета
        listInxPckgInns = PandasManager.get_unique_col_vals_as_list_static(dfInxPckgInns, 'inn_ref')
        
        return listInxPckgInns



    def get_df_emitents_inns_isins_from_given_inx_pckg_by_id_pbf (self, inxPckgId):
        """ 
        Получить фрейм с исин и соотвтетсующими им инн эмитентов из заданного индексного пакета
        """
    
        listPckgIsins = self.bmms.get_isins_list_from_inx_pkg_bonds_tb_with_given_pckg_id_bmms(inxPckgId)
        listPckgIsins = ["'" + x + "'" for x in listPckgIsins] # Обрамляем апострофами
        
        sql = f"SELECT isin, inn_ref FROM {ms.TB_BONDS_ARCHIVE} WHERE isin IN ({str(','.join(listPckgIsins))})"

        dfInxPckgInnsIsins = self.spps.read_sql_to_df_pandas_SPPS(sql)
        
        return dfInxPckgInnsIsins
    
    
    
    
    def get_bonds_list_isins_of_emeitent_from_given_inx_pckg(self, inxPckgId, emitentInn):
        """ 
        Получить список ИСИнов облигаций заданного эмитента из заданного индексного пакета
        """
    
        dfInxPckgInnsIsins = self.get_df_emitents_inns_isins_from_given_inx_pckg_by_id_pbf (inxPckgId)
        # PandasManager.print_df_gen_info_pandas_IF_DEBUG_static(dfInxPckgInnsIsins, True, colsIndxed=True, marker=f"PR_882 --> dfInxPckgInnsIsins")

        # фильтруем исины по заданному ИНН
        query = f"inn_ref=='{emitentInn}'"
        print(f"PR_883 --> query = {query}")
        dfIsinsFilteredByInn = dfInxPckgInnsIsins.query(query)
        
        # PandasManager.print_df_gen_info_pandas_IF_DEBUG_static(dfIsinsFilteredByInn, True, colsIndxed=True, marker=f"PR_881 --> dfIsinsFilteredByInn")
        
        listIsinsOfEmitentFromInxPckg = dfIsinsFilteredByInn['isin'].tolist()
        
        return listIsinsOfEmitentFromInxPckg
        
        
    
    
    
    
    def get_dic_of_emitents_inns_of_each_inx_pckg (self):
        """  
        ПРИМ: требуется точная проверка всех нюансов
        Получить словарь с id индексных пакетов и соотвтетсвующими им списками уникальных ИНН эмитентов, облигации которых входят в соотвтетсвующие
        индексные пакеты
        """
        
        dfInxPckgs = self.get_index_packages_static_pbf(['id'])
        listInxpckgsIds = dfInxPckgs['id'].tolist()
        dicInxPckgInns = {} # словарь {id индексного пакета : уникальные инН эмитентов}
        
        for inxPackgId in listInxpckgsIds:
            
            listInxPckgInns = self.get_unique_emitents_inns_list_from_given_inx_pckg_by_id_pbf(inxPackgId)
            dicInxPckgInns[inxPackgId] = listInxPckgInns
        
        return dicInxPckgInns
        
    
    
    
            
            

    def get_comp_descriptions_dic_by_inn_pbf (self, compInn):
        """ 
        Получить словарь с описаниями компании по ее ИНН и соотвтетсвующими ключами словаря с названиями www-ресурсов, с которых скачено данное описание
        Описание компании само представлено словарем с ключами по типу информации о компании
        {wwwResourceNick : dicCompDescr}
        
        """
        
        # Получить фрейм с описаниями компаний и их ИНН
        # pars
        getFields = ['inn','descr1', 'descr2','descr3','descr4','descr5']
        dfCompsDescr = self.spps.read_table_by_sql_to_df_pandas_SPPS(ms.TB_COMP_DESCR, getFields)
        print(f"PR_608 --> DEBUG")
        PandasManager.print_df_gen_info_pandas_IF_DEBUG_static(dfCompsDescr, True, colsIndxed=True,marker=f"PR_705 --> dfCompsDescr=")
        # Словарь результатов
        dicRes = {}
        # разделители для парсинга стрингового словаря JSAN
        elemDelim = '$$$' # для деления на элементы словаря
        keyValDelim = '&&&' # для деления на ключ - значение элемента словаря 
            
        # Цикл по полям с описанием компаний в таблице comps_descr
        for dfield in ms.COMPS_DESCR_FIELDS_FOR_TEXT:
            print(f"PR_609 --> DEBUG")
            # Описание компании по текущему источнику в форме словаря json
            # Обработка ошибки в случае, если в фрейме с описаниями компани dfCompsDescr нет записи с ИНН текущим
            resVal = PandasManager.get_col_name_val_by_key_col_name_val_pandas(dfCompsDescr, 'inn', compInn, dfield )
            
            # Если в результате есть метка распечатки ошибки из функции, то переиначиваем результат в понятный вид для этой функции
            if resVal and 'PR_713' in resVal:
                resVal = f'В таблице comps_descr нет записи о компании с ИНН = {compInn} и ее описаний (PR_714)'
                print (f"!!! ERROR !!! PR_715 --> В таблице comps_descr нет записи о компании с ИНН = {compInn} и ее описаний")
            
            print(f"PR_610 --> DEBUG")
            print(f"PR_569 --> get_col_name_val_by_key_col_name_val_pandas() = {resVal}")
            if resVal:
                
                resDic = JsonManager.deserrialization_from_dic_string_type1(resVal, elemDelim, keyValDelim)
            else:
                resDic = 'Нет записи в comps_descr по этому полю'
            
            # Ресурс, соотвтетсвующий текущему полю с описанием из табл comps_descr
            wwwResource = ms.DIC_COMP_DESCR_COLUMNS_TO_WWW_RESOURCES[dfield]
        
            dicRes[wwwResource] = resDic
        

        # print(f"PR_545 --> dicRes = {dicRes['RBC']}")
        
        return dicRes
    
    
    
    def get_comp_descriptions_dic_from_www_src_tables_by_inn_pbf (self, compInn):
        """ 
        Получить словарь с описаниями компании по ее ИНН и соотвтетсвующими ключами словаря с названиями www-ресурсов, с которых скачено данное описание
        Описание компании само представлено словарем с ключами по типу информации о компании
        {wwwResourceNick : dicCompDescr}
        Данные считываются из разнесенных индивидуальных таблиц  www-источников, типа comps-descr_spark  и др
        ~ https://pandas.pydata.org/docs/reference/api/pandas.DataFrame.to_dict.html
        """
        dicCompDescr = {}
        # Цикл по словарю с источниками данных по компаниям, разнесенных по разным таблицам от www-ресурсов
        for key, val in ms.DIC_ASSOC_COMP_DESCR_TABLES_AND_WWW_RESOURCES_NICKS.items():
        
            # Считать данные с текущей таблицы 
            sql = f"SELECT * FROM {key} WHERE inn = '{compInn}'"
            
            dfCompDescrCurr = self.spps.read_sql_to_df_pandas_SPPS(sql)
            
            # print(f"PR_734 -->  dfCompDescrCurr.to_dict() = { dfCompDescrCurr.to_dict()} ")
            
            dicCompDescr[val] = dfCompDescrCurr.to_dict()

        return dicCompDescr
            
            
        
        
        
        
        
        
        
        #return dicRes
    

    
    
    
    def get_comp_descr_links_dic_by_inn_pbf (self, compInn):
        """ 
        Получить словарь с ссылками на www-ресурсы компании, по которым ситывались описания компании, по ее ИНН и соотвтетсвующими ключами словаря с названиями www-ресурсов, с которых скачено данное описание
        Описание компании само представлено словарем с ключами по типу информации о компании
        {wwwResourceNick : dicCompDescr}
        
        """
        
        # Получить фрейм с описаниями компаний и их ИНН
        # pars
        getFields = ['inn','link1', 'link2','link3','link4','link5']
        dfCompsDescr = self.spps.read_table_by_sql_to_df_pandas_SPPS(ms.TB_COMP_DESCR, getFields)

        # Словарь результатов
        dicRes = {}
            
        # Цикл по полям с описанием компаний в таблице comps_descr
        for dfield in ms.COMPS_DESCR_FIELDS_FOR_LINKS:

            resVal = PandasManager.get_col_name_val_by_key_col_name_val_pandas(dfCompsDescr, 'inn', compInn, dfield )
            
            # Если в результате есть метка распечатки ошибки из функции, то переиначиваем результат в понятный вид для этой функции
            if resVal and 'PR_713' in resVal:
                resVal = f'comps_descr и globalA нет запией о компании с ИНН = {compInn}, ссылок и описаний (PR_715)'
                print (f"!!! ERROR !!! PR_716 --> В таблице comps_descr нет записи о компании с ИНН = {compInn} и ее описаний")
            
            
            # Ресурс, соотвтетсвующий текущему полю с описанием из табл comps_descr
            wwwResource = ms.DIC_COMP_DESCR_COLUMNS_FOR_LINKS_TO_WWW_RESOURCES[dfield]
        
            dicRes[wwwResource] = resVal
        

        # print(f"PR_545 --> dicRes = {dicRes['RBC']}")
        
        return dicRes
    
    
    
    def get_df_comp_descr_by_inn_pbf (self, inn):
        """ 
        Получить фрейм с одной строкой из табл comp_descr для компании по заданному inn
        """
        
        # Получить SQL-запрос для вывода данных компании по ИНН из табл comps_descr
        # Pars: 
        conds = {'ONE': ['inn', '=', inn]}
        sql = SQLSyntaxer.select_from_table_with_where_condition_sql (ms.TB_COMPS_DESCR, ['*'], conds)
        # Получить фрейм на базе запроса sql с данными по описанию компании
        dfOneCompData = self.spps.read_sql_to_df_pandas_SPPS(sql)
        
        return dfOneCompData





    def get_comp_name_by_inn_pbf(self, inn):
        """
        ProjectBondsFunctions
        Получить название компании по ее ИНН
        Category: Облигации
        """
        # Pars:
        
        conds = {'ONE':['inn','=',inn]}
        compName = self.sps.select_from_table_with_where_condition_sps(ms.TB_COMPS, ['comp_name'], conds)
        return compName[0]




    def get_complex_bonds_df_with_added_diff_columns_pbf_v3(self, bgColors = ['corp_row_css', 'ofz_row_css', 'munic_row_css']):
            """
            ProjectBondsFunctions
            Сформировать обьединенный комплексный фрейм со смешанными бумагами всех типов с дифференциалльными метками по типу бумаг и цвету в отдельных добавленных колонках фрейма
            Версия 2: Таблицы задаются внутри метода и не нужно их передавать в параметрах
            Версия 3: Переведена в класс ProjectBondsFunctions. И !!! теперь в поле bg_col, которое является отображением скрытного поля HIDDEN__bg_color
            , теперь передается не цвет бэкграунда для выделения цветом строки таблицы, а ее класс в стилях css, который должен быть задан !
            BondsMainManagerSpeedup
            bgColors - задает цвета фона рядов для трех видов облигаций для цветовой дифференциации
            Колонки annual_yield, last_annual_yield и curr_price прочищены от % и трансформированы в тип float
            Category: Облигации
            """

            # db_proc = SqlitePandasProcessor(DB_BONDS_)
            # Корпоративные облигации из табл bonds_current
            dfCorpBonds = self.bmms.read_table_by_sql_to_df_pandas_BMMS('bonds_current')
            dfCorpBonds['type'] = 'КОРП'
            dfCorpBonds['bg_color'] = bgColors[0]
            # Государственные облигации ОФЗ из табл ofz_current
            dfOfzBonds = self.bmms.read_table_by_sql_to_df_pandas_BMMS('ofz_current')
            dfOfzBonds['type'] = 'ОФЗ'
            dfOfzBonds['bg_color'] = bgColors[1]
            # Субфедеральные или муниципальные облигации из табл municip_current
            dfMunicipBonds = self.bmms.read_table_by_sql_to_df_pandas_BMMS('municip_current')
            dfMunicipBonds['type'] = 'МУНИЦ'
            dfMunicipBonds['bg_color'] = bgColors[2]


            # Обьединение 3х фреймлв в один, чтобы поля одинаковых смысловых колонок соотвтетсвовали друг другу
            frames = [dfCorpBonds, dfOfzBonds, dfMunicipBonds]
            dfComplexBonds = pd.concat(frames, ignore_index=True) # autoreset index after a concatenation

            # Очистка колонок с действительными числами в стринговом выражении от знака '%'
            # dfComplexBonds= PandasManager.clear_str_float_from_persent_simb(dfComplexBonds, 'annual_yield')
            dfComplexBonds = PandasManager.convert_str_empty_with_persent_and_empty_str_to_float(dfComplexBonds, 'annual_yield')
            dfComplexBonds = PandasManager.convert_str_empty_with_persent_and_empty_str_to_float(dfComplexBonds, 'last_annual_yield')  # !!
            dfComplexBonds  = PandasManager.convert_str_empty_with_persent_and_empty_str_to_float(dfComplexBonds, 'curr_price')


            return dfComplexBonds




    def get_complex_archive_bonds_df_with_added_diff_columns_pbf(self, bgColors = ['corp_row_css', 'ofz_row_css', 'munic_row_css']):
            """
            ProjectBondsFunctions
            Сформировать обьединенный комплексный фрейм со смешанными АРХИВНЫМИ бумагами всех типов с дифференциалльными метками по типу бумаг и цвету в отдельных добавленных колонках фрейма
            Версия 2: Таблицы задаются внутри метода и не нужно их передавать в параметрах
            Версия 3: Переведена в класс ProjectBondsFunctions. И !!! теперь в поле bg_col, которое является отображением скрытного поля HIDDEN__bg_color
            , теперь передается не цвет бэкграунда для выделения цветом строки таблицы, а ее класс в стилях css, который должен быть задан !
            BondsMainManagerSpeedup
            bgColors - задает цвета фона рядов для трех видов облигаций для цветовой дифференциации
            Колонки annual_yield, last_annual_yield и curr_price прочищены от % и трансформированы в тип float
            Category: Облигации
            """

            # db_proc = SqlitePandasProcessor(DB_BONDS_)
            # Корпоративные облигации из табл bonds_current
            dfCorpBonds = self.bmms.read_table_by_sql_to_df_pandas_BMMS(ms.TB_BONDS_ARCHIVE)
            dfCorpBonds['type'] = 'КОРП'
            dfCorpBonds['bg_color'] = bgColors[0]
            # Государственные облигации ОФЗ из табл ofz_current
            dfOfzBonds = self.bmms.read_table_by_sql_to_df_pandas_BMMS(ms.TB_OFZ_ARCHIVE)
            dfOfzBonds['type'] = 'ОФЗ'
            dfOfzBonds['bg_color'] = bgColors[1]
            # Субфедеральные или муниципальные облигации из табл municip_current
            dfMunicipBonds = self.bmms.read_table_by_sql_to_df_pandas_BMMS(ms.TB_MUNICIP_ARCHIVE)
            dfMunicipBonds['type'] = 'МУНИЦ'
            dfMunicipBonds['bg_color'] = bgColors[2]


            # Обьединение 3х фреймлв в один, чтобы поля одинаковых смысловых колонок соотвтетсвовали друг другу
            frames = [dfCorpBonds, dfOfzBonds, dfMunicipBonds]
            dfComplexBonds = pd.concat(frames, ignore_index=True) # autoreset index after a concatenation

            # Очистка колонок с действительными числами в стринговом выражении от знака '%'
            # dfComplexBonds= PandasManager.clear_str_float_from_persent_simb(dfComplexBonds, 'annual_yield')
            dfComplexBonds = PandasManager.convert_str_empty_with_persent_and_empty_str_to_float(dfComplexBonds, 'annual_yield')
            dfComplexBonds = PandasManager.convert_str_empty_with_persent_and_empty_str_to_float(dfComplexBonds, 'last_annual_yield')  # !!
            dfComplexBonds  = PandasManager.convert_str_empty_with_persent_and_empty_str_to_float(dfComplexBonds, 'curr_price')


            return dfComplexBonds



    def if_bond_exist_in_tb_archive_by_isin (self, tbArch, isin):
        """ 
        Проверить, есть ли в заданнйо архивной таблице tbArch облигация с заданным ИСИН isin
        """
        
        sql = f"SELECT COUNT(*) FROM {tbArch} WHERE isin='{isin}'"
        
        print(f"PR_753 --> sql = {sql}")
        
        res = self.sps.get_result_from_sql_exec_proc_sps(sql)
        
        # print(f"PR_751 --> res = {res[0]}")
        
        if res[0] > 0:
            ret = True
        else:
            ret = False
            
        return ret
        
        
        
        
    def if_bond_exist_in_all_index_packages_by_isin (self, isin):
        """ 
        Проверить, есть ли в таблице с индексными пакетами inx_packgs_bonds облигация с заданным  isin
        """
        
        sql = f"SELECT COUNT(*) FROM inx_packgs_bonds WHERE bond_isin='{isin}'"
        
        print(f"PR_753 --> sql = {sql}")
        
        res = self.sps.get_result_from_sql_exec_proc_sps(sql)
        
        # print(f"PR_751 --> res = {res[0]}")
        
        if res[0] > 0:
            ret = True
        else:
            ret = False
            
        return ret
        
        
        
        
    def get_okpo_from_archive_by_isin(self, isin):
        """ 
        Получить OKPO облигации из архивной таблицы корпоративов
        """

        sql = f"SELECT okpo FROM bonds_archive WHERE isin = '{isin}'"
        
        res = self.sps.get_result_from_sql_exec_proc_sps(sql)
        
        if not isinstance (res, int):
            ret = res[0]
        else:
            ret = -1
        
        
        return ret
    
    
    
    def get_inn_from_archive_by_isin(self, isin):
        """ 
        Получить OKPO облигации из архивной таблицы корпоративов
        """

        sql = f"SELECT inn_ref FROM bonds_archive WHERE isin = '{isin}'"
        
        inn = self.sps.get_result_from_sql_exec_proc_sps(sql)[0]
        
        return inn
    
    
    
    
    def get_df_record_data_of_comp_in_tb_comps_by_inn_pbf (self, inn):
        """ 
        Получить данные по записи в табл comps по ИНН компании. Или подтвердить их отсутствие
        """
        
        sql = f"SELECT inn, comp_name, okpo, sector FROM comps WHERE inn='{inn}'"
        dfCompByInn = self.spps.read_sql_to_df_pandas_SPPS(sql)
        
        return dfCompByInn
    
    
    
    
    def if_record_in_www_comp_data_table_exists_by_inn_pbf (self, wwwTb, compInn):
        """ 
        Проверить наличие записи в таблице, предназначенной для хранения данных о компании из www-ресурсов, по ИНН заданной компании 
        """
        
        sql = f"SELECT COUNT(*) FROM {wwwTb} WHERE inn='{compInn}'"
        
        print(f"PR_780 --> sql = {sql}")
        
        res = self.sps.get_result_from_sql_exec_proc_sps(sql)
        
        # print(f"PR_751 --> res = {res[0]}")
        
        if res[0] > 0:
            ret = True
        else:
            ret = False
            
        return ret
    



    def if_link_in_www_comp_data_table_exists_by_inn_pbf (self, wwwTb, compInn):
        """ 
        Проверить наличие ссылки в поле 'link' с анализом формата в соотвественной www-таблицы, по ИНН заданной компании 
        """
        
        sql = f"SELECT link FROM {wwwTb} WHERE inn='{compInn}'"
        
        print(f"PR_805 --> sql = {sql}")
        
        res = self.sps.get_result_from_sql_exec_proc_sps(sql)
        
        # TODO: Сделать проверку формата ссылки через regular expressins
        link = res[0]
        
        
        if link and len(link) > 0: # Если ссылка существует и ее размер больше 0, то:
            ret = True
        else: # Если ссылка НЕ существует
            ret = False
            
        return ret




    def get_bonds_nick_name_by_isin_arch_tb_pbf (self, isin):
        """ 
        Получить ник-нейм облигации по ее ИСИН из архивной таблицы
        """
        
        sql = f"SELECT bond_name FROM {ms.TB_BONDS_ARCHIVE} WHERE isin = '{isin}'"
        res = self.sps.get_result_from_sql_exec_proc_sps(sql)
        
        return res[0]





    def get_comp_name_by_bond_isin_pbf (self, isin):
        """ 
        Получить название компании-эмитента облигации по ее ИСИН из таблицы comps
        """
        
        # ИНН компании по ИСИН облигации
        compInn = self.get_inn_from_archive_by_isin(isin)
        
        if compInn and len(compInn) > 0: #  Значит ИНН компании найден через архивную облигацию
            # Найти ник-нейм компании по ее ИНН из табл comps
            sql = f"SELECT comp_name FROM comps WHERE inn = {compInn}" 
            res = self.sps.get_result_from_sql_exec_proc_sps(sql)
            
            if isinstance(res, int) :
                print(f"PR_848 --> Имя компании не найдено")
                compName = ''
            else:
                compName = res[0]
            
            
            
        
        else: # ИНН компании не найден в архивной облигации
            print(f"PR_841 --> ИНН компании не найден через ИСИН облигации. Значит в архивной олигации с ИСИН={isin} не проставлен ИНН компании-эмитента в поле inn_ref")
            print(f"PR_842 --> Необходимо запустить Интерактивный www-поиск компании-эмитента по ее ИСИН, что бы проставить ИНН в архивнйо облигации")
            compName = f"Не найден"

        return compName
    
    
    
    def get_bond_com_sector_by_idin_pbf (self, isin):
        """ 
        Получить сектор или отрась компании как производную от облигации этой компании с заданным ИСИН
        """
        
        # ИНН компании по ИСИН облигации
        compInn = self.get_inn_from_archive_by_isin(isin)
        
        if compInn and len(compInn) > 0: #  Значит ИНН компании найден через архивную облигацию
            # Найти ник-нейм компании по ее ИНН из табл comps
            sql = f"SELECT sector FROM comps WHERE inn = {compInn}" 
            res = self.sps.get_result_from_sql_exec_proc_sps(sql)
            
            if isinstance(res, int) :
                print(f"PR_848 --> Имя компании не найдено")
                compSector = ''
            else:
                compSector = res[0]
            
        
        else: # ИНН компании не найден в архивной облигации
            print(f"PR_844 --> ИНН компании не найден через ИСИН облигации. Значит в архивной олигации с ИСИН={isin} не проставлен ИНН компании-эмитента в поле inn_ref")
            print(f"PR_845 --> Необходимо запустить Интерактивный www-поиск компании-эмитента по ее ИСИН, что бы проставить ИНН в архивнйо облигации")
            compSector = f"Не найден"
        
        return compSector
    
    


    def get_bond_archive_cupon_frequency_payments_pbf (self, isin):
        """ 
        Поулчить частоту выплат купонов в году облигации с заданынм ИСИН у архивной облигации
        """
        
        sql = f"SELECT frequency FROM {ms.TB_BONDS_ARCHIVE} WHERE isin = '{isin}'"
        frequency = self.sps.get_result_from_sql_exec_proc_sps(sql)[0]

        return frequency
    
    
    
    
    def get_bond_years_to_end_by_isin_pbf (self, isin):
        """ 
        Поулчить срок погашения оббигации в годах
        """
        
        sql = f"SELECT years_to_end FROM {ms.TB_BONDS_ARCHIVE} WHERE isin = '{isin}'"
        res = self.sps.get_result_from_sql_exec_proc_sps(sql)
        
        print(f"PR_899 --> res = {res}")

        # yearsToEnd = res[0]
        
        
        if not isinstance(res,int): # 
            ret = res[0]
        else: # 
            ret = ''
            
        return ret
    
    
    
    def get_comp_finp_plan_link_by_inn(self, inn):
        """ 
        Получить ссылку для компании на ресурсе FINPLAN по ее ИНН
        """
    
    
        sql = f"SELECT link FROM {ms.TB_WWW_DATA_FINPLAN} WHERE inn = '{inn}'"
        print(f"PR_846 --> sql = {sql}")
        res = self.sps.get_result_from_sql_exec_proc_sps(sql)
        
        if isinstance(res, int) :
            print(f"PR_847 --> Ссылка не найдена")
            compFinplanLink = ''
        else:
            compFinplanLink = res[0]
        
        
        return compFinplanLink
    
    
    
    
    
    
    # def get_inx_pckg_nick_by_id(self, pckgId):
    #     """ 
    #     OBSOLETED: Более универсальное получение значений атрибутов записей по индексномупакету в табл index_packages по названию поля в get_inx_pckg_filed_val_by_id()
    #     Получить ник-нейм индексного пакета по его id
    #     """
        
    #     sql = f"SELECT nick FROM {ms.TB_INDEX_PACKAGES} WHERE id={pckgId}"
    #     pckgNick = self.sps.get_result_from_sql_exec_proc_sps(sql)[0]
        
    #     return pckgNick
    
    
    
    
    
    def get_inx_pckg_filed_val_by_id(self, pckgId, fieldName):
        """ 
        Получить значение заданного поля из табл index_packages по  id интересуемого индексного пакета (или рядя в таблице по id)
        """
        
        sql = f"SELECT {fieldName} FROM {ms.TB_INDEX_PACKAGES} WHERE id={pckgId}"
        fieldVal = self.sps.get_result_from_sql_exec_proc_sps(sql)[0]
        
        return fieldVal
    
    
    # def get_pckg_name_val_by_id(self, pckgId, fieldName):
    #     """ 
    #     Получить значение заданного поля из табл index_packages по  id интересуемого индексного пакета (или рядя в таблице по id)
    #     """
        
    #     sql = f"SELECT {fieldName} FROM {ms.TB_INDEX_PACKAGES} WHERE id={pckgId}"
    #     fieldVal = self.sps.get_result_from_sql_exec_proc_sps(sql)[0]
        
    #     return fieldVal
    
    
    
    
    def get_bond_curr_price_from_curr_complex_bonds(self):
        """ 
        В ПРОРАБОТКЕ не закончен! 
        Поулчить текущую цену облигации из комплексного массива всех облигаций из текущих операционных таблиц
        """
        
        bondsComplexCurr = self.get_complex_bonds_df_with_added_diff_columns_pbf_v3()
    
        
    
    
    
    def get_comp_analisys_by_inn_pbf(self, inn):
        """ 
        Поулчить анализ компании из табл 'comp_analisys' по inn компании
        """
        
        sql = f"SELECT comp_analisys FROM {ms.TB_COMP_ANALISYS} WHERE inn='{inn}'"
        
        res = self.sps.get_result_from_sql_exec_proc_sps(sql)
        
        if not isinstance(res, int): # если есть данные в  ответе от SQL-запроса
            compAnalisys = res[0]
        else:
            compAnalisys = ''
        
        return compAnalisys
        
    
    
    
    def get_comp_bond_analisys_by_inn_and_isin_pbf(self, inn, isin):
        """ 
        Получить анализ облигации по заданной ИСИН от компании с заданным ИНН
        """
    
        sql = f"SELECT comp_bonds_analisys FROM {ms.TB_COMP_BONDS_ANALISYS} WHERE inn='{inn}' AND isin='{isin}'"
        
        # print(f"PR_875 --> sql = {sql}")
        
        res = self.sps.get_result_from_sql_exec_proc_sps(sql)
        
        if not isinstance(res, int): # если есть данные в  ответе от SQL-запроса
            compBondAnalisys = res[0]
        else:
            compBondAnalisys = ''
            
        return compBondAnalisys
    
    
    
    def get_comp_bond_analisys_coeff_by_inn_and_isin_pbf(self, inn, isin):
        """ 
        Получить коэффициент риска по облигации  по заданной ИСИН от компании с заданным ИНН
        """
    
        sql = f"SELECT bond_analis_coeff FROM {ms.TB_COMP_BONDS_ANALISYS} WHERE inn='{inn}' AND isin='{isin}'"
        
        # print(f"PR_875 --> sql = {sql}")
        
        res = self.sps.get_result_from_sql_exec_proc_sps(sql)
        
        if not isinstance(res, int): # если есть данные в  ответе от SQL-запроса
            compBondAnalisysCoeff = res[0]
        else:
            compBondAnalisysCoeff = ''
            
        return compBondAnalisysCoeff

    
    
    
    def get_bond_analisys_notes_by_inn_and_isin_pbf(self, inn, isin):
        """ 
        Получить заметки  по облигации  по заданной ИСИН от компании с заданным ИНН
        """
    
        sql = f"SELECT cba_notes FROM {ms.TB_COMP_BONDS_ANALISYS} WHERE inn='{inn}' AND isin='{isin}'"
        
        # print(f"PR_875 --> sql = {sql}")
        
        res = self.sps.get_result_from_sql_exec_proc_sps(sql)
        
        if not isinstance(res, int): # если есть данные в  ответе от SQL-запроса
            compBondAnalisysNotes = res[0]
        else:
            compBondAnalisysNotes = ''
            
        return compBondAnalisysNotes
    
    
    
    def get_comp_analisys_notes_by_inn_pbf(self, inn):
        """ 
        Получить заметки  по эмитенту  от компании с заданным ИНН в таблице анализов эмитентов comps_analisys
        """
    
        sql = f"SELECT notes FROM {ms.TB_COMP_ANALISYS} WHERE inn='{inn}'"
        
        # print(f"PR_875 --> sql = {sql}")
        
        res = self.sps.get_result_from_sql_exec_proc_sps(sql)
        
        if not isinstance(res, int): # если есть данные в  ответе от SQL-запроса
            compAnalisysNotes = res[0]
        else:
            compAnalisysNotes = ''
            
        return compAnalisysNotes
    
    
    
    
    
    
    
    
    
    @staticmethod
    def get_bond_period_payback_pbf_static(bondCurrPrice, bondCurrNominal, bondCurrCoupon):
        """ 
        ProjectBondsFunctions
        Получить относительный период окупаемости облигации, если ее текущая цена выше 100%
        Период равен периоду выплат купонов по облигации. Если это один месяц - то относительный период = 1 мес. Если 3 месяца, то период окупаемости - 3 мес
        bondCurrPrice - текущая цена облигации
        bondCurrNominal - текущий номинал облигации
        bondCurrCoupon - текущий купон облигации
        ПРИМ: Пока эта формула относиться к облигациям с фиксированным купонам по облигациям без амортизации. Но в дальнейшем можно расширить формулу
        Category: Формулы по облигациям
        """
        
        # Перевод стринговые паарметры в числовые
        if len(bondCurrPrice) > 0 and  len(bondCurrNominal) > 0 and len(bondCurrCoupon) > 0:
            bondCurrPrice = float(bondCurrPrice)
            bondCurrNominal = float(bondCurrNominal)
            bondCurrCoupon = float(bondCurrCoupon)
            
            if bondCurrPrice > 100: # Если текущая цена больше 100%
                paybackCouponPeriod = (bondCurrPrice * bondCurrNominal/100 - bondCurrNominal) / bondCurrCoupon
                paybackCouponPeriod = str(round(paybackCouponPeriod,3)) # Обратно в string
            else:
                paybackCouponPeriod = ''
            
        else:
            paybackCouponPeriod = ''
        
            
        return paybackCouponPeriod
        
        
        
    
    
    
    def insert_or_update_interactive_data_by_isin(self, isin, dfInteractiveData):
        """ 
        Вставить или обновить данные таблицы interactive_data на основе фрейма с полученными данными dfInteractiveData
        Необходим для нового подхода: один раз заходим на ресурс и считываем все, что может пригодится в будущем !!!
        И сохраняем в БД
        """
        
        sql = f"SELECT * FROM {ms.TB_INTERACTIVE_DATA_} WHERE isin='{isin}'"
        if self.sps.if_select_result_exists_sps(sql): # Если ответ есть, значит запись с ИСИН уже есть и значит делаем UPDATE записи
            print(f"PR_877 --> SYS: Запись с ИСИН = {isin} уже есть в таблице interactice_data. Делаем UPDATE")
            self.spps.update_from_df_by_key_col_pandas_spps(ms.TB_INTERACTIVE_DATA_, dfInteractiveData, 'isin')
            
        else: # если записи нет. то делаем INSERT
            print(f"PR_878 --> SYS: Записи с ИСИН = {isin} нет в таблице interactice_data. Делаем INSERT")
            self.spps.insert_df_to_tb_no_key_check_pandas_spps(dfInteractiveData, ms.TB_INTERACTIVE_DATA_)
        
        
    
    
    
    def get_bond_coupon_frequency (self, isin):
        """ 
        Получить частоту купона облигации
        """
        
        sql = f"SELECT frequency FROM {ms.TB_BONDS_ARCHIVE} WHERE isin='{isin}'"
    
        res = self.sps.get_result_from_sql_exec_proc_sps(sql)
        
        if not isinstance(res, int): # если есть данные в  ответе от SQL-запроса
            coupFrq = res[0]
        else:
            coupFrq = ''
            
        return coupFrq
    
    
    
    
    def get_bond_oferta_date_arch_pbf (self, isin):
        """ 
        Получить дату оферты по заданной облигации из табл bonds_archive
        """
        
        sql = f"SELECT oferta FROM {ms.TB_BONDS_ARCHIVE} WHERE isin='{isin}'"
    
        res = self.sps.get_result_from_sql_exec_proc_sps(sql)
        
        if not isinstance(res, int): # если есть данные в  ответе от SQL-запроса
            bondOfertaDate = res[0]
        else:
            bondOfertaDate = ''
            
        return bondOfertaDate
    
    
    
    def get_bond_oferta_type_arch_pbf (self, isin):
        """ 
        Получить тип оферты по заданной облигации из табл bonds_archive из поля 'f3', которое теперь предназначено для типа оферты облигации
        Типы оферты: CALL, PUT
        """
        
        sql = f"SELECT f3 FROM {ms.TB_BONDS_ARCHIVE} WHERE isin='{isin}'"
    
        res = self.sps.get_result_from_sql_exec_proc_sps(sql)
        
        if not isinstance(res, int): # если есть данные в  ответе от SQL-запроса
            bondOfertaType = res[0]
        else:
            bondOfertaType = ''
            
        return bondOfertaType
    
    
    
    
    def get_bond_bought_data_pbf (self, isin):
        """ 
        Получить значение заданных параметров облигации в портфолио в табл bonds_bought по ее исин
        """
        resData = {}
        sql = f"SELECT curr_coupon, qn FROM {ms.TB_BONDS_BOUGHT} WHERE isin='{isin}'"
    
        res = self.sps.get_result_from_sql_exec_proc_sps(sql)
        
        print(f"PR_888 --> res = {res}")
        
        if not isinstance(res, int): # если есть данные в  ответе от SQL-запроса
            resData['curr_coupon'] = res[0][0]
            resData['bond_bought_qn'] = res[0][1]
        else:
            resData['curr_coupon'] = '0'
            resData['bond_bought_qn'] = '0'
            
        return resData
    
    
    
    
    def update_pay_matrix_bond_month_sum_coupons_payments_by_isin_pbf (self, isin):
        """ 
        Обновить значения суммарных помесячных выплат купонов облигации с учетом их количеств в лоте портфолио (табл bonds_bought)
        на основе известного куполна облигации и ее кол-ва в лоте, а так же в соотвтетсвии с вектором месяцев, в которых производится выплаты
        купонов. По входному  isin  облигации
        """

        # Текущий купон, проставленный вручную в формк регистрации лота покупки облигации данного ISIN
        currCoupon = float(self.get_bond_bought_data_pbf(isin)['curr_coupon']) 
        
        # кол-во облигаций, купленных в этом лотк данной облигации с данным ISIN
        qn = int(self.get_bond_bought_data_pbf(isin)['bond_bought_qn']) 

        # Суммарная выплата помесячно по вектору месячных выплат для данной облигации
        totalMonthPay = round(currCoupon * qn, 2) 
        
        # Получить вектор нормального распределения помесячных выплат для данной олигации с известным ISIN
        monthIsinPayVectors = self.bmms.get_bond_month_payment_objects_by_isin_BMMS(isin)

        # Поля для вставки помесячных выплат на основе полученных веторов распределения помесЯчных выплат
        monthCols = monthIsinPayVectors[1]

        # Формируем словарь с необходимыми полями по месяцам и значениями равными сумарному значению купонов totalMonthPay
        dicUpdateMonthesPayments = {}
        dicUpdateMonthesPayments['isin'] = isin
        
        for month in monthCols:
            pass
            dicUpdateMonthesPayments[month] = totalMonthPay
            
        # Формируем фрейм на основе словаря dicUpdateMonthesPayments
        dfUpdateMonthesPayments = PandasManager.read_df_from_dictionary_static(dicUpdateMonthesPayments)
        
        # print (f"PR_889 --> dfUpdateMonthesPayments = \n{dfUpdateMonthesPayments}")

        # Провести UPDATE месячных выплат для облигации с заданным ИСИН по вычесленному вектору месяцев выплат
        self.spps.update_from_df_by_key_col_pandas_spps(ms.TB_BONDS_BOUGHT, dfUpdateMonthesPayments, 'isin')




    def update_pay_matrix_bond_month_sum_coupons_payments_by_list_isins_pbf (self, listIsins):
        """ 
        Обновить значения суммарных помесячных выплат купонов облигации с учетом их количеств в лоте портфолио (табл bonds_bought)
        на основе известного куполна облигации и ее кол-ва в лоте, а так же в соотвтетсвии с вектором месяцев, в которых производится выплаты
        купонов. По входному списку isins  облигаций
        """

        for isin in listIsins:
            pass
            self.update_pay_matrix_bond_month_sum_coupons_payments_by_isin_pbf(isin)




    def get_dic_corporative_portfolio_bonds_consolidated_qn_by_inn_pbf (self):
        """ 
        Получить суммарное колличество всех облигаций (с разными ИСИН) в портфолио по одному заданному эмитенту 
        для корпоративных облигаций портфолио в виде словаря {inn : SUM(qn) by INN}
        """
        
        sql = f"""SELECT *, SUM(qn) FROM {ms.TB_BONDS_BOUGHT} AS bb
                    LEFT JOIN {ms.TB_BONDS_ARCHIVE} AS ba
                    ON  bb.isin = ba.isin
                    WHERE inn_ref NOT NULL
                    GROUP  BY inn_ref
        """

        # Фрейм с консолидированными по ИНН кол-вом облигаций в портфолио
        dfConsolByInnQnBonds = self.spps.read_sql_to_df_pandas_SPPS(sql)
        # PandasManager.print_df_gen_info_pandas_IF_DEBUG_static(dfConsolByInnQnBonds, True, colsIndxed = True, marker = f"PR_962 --> dfConsolByInnQnBonds")

        # Формирвоание словаря с ключами ввиде ИНН эмитента и значениями в виде суммарного кол-ва облигаций из портфолио данного эмитента
        dicPortfolioBondsConsolidatedQnByInn = PandasManager.convert_key_col_and_val_col_of_df_to_dic_pm_static(dfConsolByInnQnBonds, 'inn_ref', 'SUM(qn)')
        
        return dicPortfolioBondsConsolidatedQnByInn
    
    
    
    
    def get_corporative_inx_packages_bonds_frame_with_analisys_ext_pbf (self):
        """ 
        Получить фрейм  с портфолио-облигациями с расширением по анализу по облигациям и компании
        """
        
        sql = f"""SELECT * FROM inx_packgs_bonds AS ipb
                    LEFT JOIN {ms.TB_BONDS_ARCHIVE} AS ba
                    ON  ipb.bond_isin = ba.isin
                    LEFT JOIN comp_bond_analisys AS cba 
                    ON ipb.bond_isin = cba.isin
        """
        
        print(f"PR_A011 --> sql = {sql}")
        
        dfCorpinxPckgsArchBondsWithAnalisys = self.spps.read_sql_to_df_pandas_SPPS(sql)
        
        return dfCorpinxPckgsArchBondsWithAnalisys
    
    
    
    
    def get_inx_packages_bonds_coefficients_of_given_emitent_pbf (self, inn):
        """ 
        Получить словарь с набором облигаций (их ИСИНов как  ключи словаря) по индексным пакетам, принадлежащим заданному по ИНН эмитенту , с их 
        собственными коэффициентами риска из табл comp_bonds_analisys
        """
        
        dfCorpinxPckgsArchBondsWithAnalisys = self.get_corporative_inx_packages_bonds_frame_with_analisys_ext_pbf()
        
        # Формирвоание словаря с ключами ввиде ИСИН облигаций и значениями коэффф риска облигаций
        dicInxPckgsBondsCoeffByInn = PandasManager.convert_key_col_and_val_col_of_df_to_dic_pm_static(dfCorpinxPckgsArchBondsWithAnalisys, 'bond_isin', 'bond_analis_coeff')
        
        return dicInxPckgsBondsCoeffByInn
    
    
    
    def  get_sum_qn_of_all_bonds_in_portfolio_for_given_emitent_pbf (self, inn):
        """ 
        ПОулчить суммарное кол-во всех единиц облигаций в портфолио по заданному эмитенту по его ИНН
        """      
        
        sql = f"""SELECT SUM(qn) FROM {ms.TB_BONDS_BOUGHT} AS bb
                    LEFT JOIN {ms.TB_BONDS_ARCHIVE} AS ba
                    ON  bb.isin = ba.isin
                    WHERE inn_ref = '{inn}'
        """
        
        print(f"PR_A008 --> sql = {sql}")
        
        res = self.sps.get_result_from_sql_exec_proc_sps(sql)
        
        if not isinstance (res, int):
            ret = res[0]
        else:
            ret = -1
        
        BondsEmitentQn = ret
        
        return BondsEmitentQn
    
    

        
        
    def get_dic_ofz_municip_portfolio_bonds_consolidated_qn_by_isin_pbf (self):
        """ 
        Получить суммарное колличество всех облигаций (с разными ИСИН) в портфолио 
        для ОФЗ и муниципалоьных облигаций портфолио в виде словаря {isin : SUM(qn) by ISIN}
        """
    
    
    
        sql = f"""SELECT *, SUM(qn) 
                    FROM {ms.TB_BONDS_BOUGHT} AS bb 
                    LEFT JOIN
                    (SELECT * FROM ofz_archive UNION SELECT * FROM municip_archive) AS omclx
                    ON bb.isin  = omclx.isin 
                    GROUP  BY bb.isin
        """
        
        # Фрейм с консолидированными по ИСИН кол-вом облигаций в портфолио типа ОФЗ и муниципалов
        dfConsolByIsinQnOfzMunicBonds = self.spps.read_sql_to_df_pandas_SPPS(sql)
        

        # Индексировать названия колонок в фрейме с одинаковыми названиями (в данном случае nkd имеет две колонки с одним и тем же названием)
        dfConsolByIsinQnOfzMunicBonds = PandasManager.index_duplicated_name_columns_in_df(dfConsolByIsinQnOfzMunicBonds)
        
        # PandasManager.print_df_gen_info_pandas_IF_DEBUG_static(dfConsolByIsinQnOfzMunicBonds, True, colsIndxed = True, marker = f"PR_969 --> dfConsolByInnQnBonds")

        
        # Формирвоание словаря с ключами ввиде ИНН эмитента и значениями в виде суммарного кол-ва облигаций из портфолио данного эмитента
        dicPConsolByIsinQnOfzMunicBonds = PandasManager.convert_key_col_and_val_col_of_df_to_dic_pm_static(dfConsolByIsinQnOfzMunicBonds, 'isin', 'SUM(qn)')



        return dicPConsolByIsinQnOfzMunicBonds
    
    
    
    def get_list_ofz_municip_archive_bonds_isins_pbf (self):
        """ 
        Получить список ISIN облигаций типа ОФЗ и Муницип из архивных таблиц
        """
    
        sql = f"""SELECT isin FROM ofz_archive UNION SELECT isin FROM municip_archive
                    GROUP BY isin
        """
        
        print(f"PR_989 --> sql = {sql}")
        
        # Фрейм с консолидированными по ИСИН кол-вом облигаций в портфолио типа ОФЗ и муниципалов
        dfIsinsOfOfzAnaMunicipBonds = self.spps.read_sql_to_df_pandas_SPPS(sql)

        # PandasManager.print_df_gen_info_pandas_IF_DEBUG_static(dfConsolByIsinQnOfzMunicBonds, True, colsIndxed = True, marker = f"PR_969 --> dfConsolByInnQnBonds")

        listIsinsOfOfzAnaMunicipBonds = list(dfIsinsOfOfzAnaMunicipBonds['isin'])


        return listIsinsOfOfzAnaMunicipBonds
    
    
    
    
    def get_total_ofz_munic_bonds_portfolio_qn_in_all_inx_packages_pbf (self):
        """ 
        Получить общее количество облигаций по всем индексным пакетам и в пересечении с портфолио 
        """
        
        sql = f"""SELECT *, SUM(qn) as qnt
                    FROM inx_packgs_bonds AS ipb 
                    INNER JOIN
                    bonds_bought AS bb 
                    ON ipb.bond_isin  = bb.isin
                    INNER JOIN
                    (SELECT * FROM ofz_archive UNION SELECT * FROM municip_archive) AS omclx
                    ON ipb.bond_isin  = omclx.isin
        """
        
        print(f"PR_980 --> sql = {sql}")
    
        # Фрейм с консолидированными по ИСИН кол-вом облигаций в портфолио типа ОФЗ и муниципалов
        dfQnOfzMunicIpBondsBought = self.spps.read_sql_to_df_pandas_SPPS(sql)
        

        # Индексировать названия колонок в фрейме с одинаковыми названиями (в данном случае nkd имеет две колонки с одним и тем же названием)
        dfQnOfzMunicIpBondsBought = PandasManager.index_duplicated_name_columns_in_df(dfQnOfzMunicIpBondsBought)
        
        # PandasManager.print_df_gen_info_pandas_IF_DEBUG_static(dfConsolByIsinQnOfzMunicBonds, True, colsIndxed = True, marker = f"PR_969 --> dfConsolByInnQnBonds")

        totalofzMunicBondsQn = dfQnOfzMunicIpBondsBought.iloc[0]['qnt']
        
        print(f"PR_979 --> totalofzMunicBondsQn = {totalofzMunicBondsQn}")
        
        return totalofzMunicBondsQn
    
    
    def get_sum_positive_delta_of_norm_qn_and_portf_qn_corporative_for_given_inx_pckg_bonds_pbf (self, inxPckgId, ipLotBondsQn):
        """ 
        Получить сумму положительных дельта-разниц между нормой по кол-ву корпоративных облигаций эмитента и реальным кол-во облигаций от эмитента в портфолио.
        Норма отображает кол-во потенциально необходимых облигаций
        по каждому эмитенту и его рискам. Дельта - разница между нормой , зависящей от риска компании и установочному
        кол-ву облигаций в одном лоте. 
        """
        
        # pbf = ProjectBondsFunctions()
        
        # inxPckgId = 5
        # ipLotBondsQn = 6
        
        # A. Получить массив облигаций из индексного пакета расширенного атрибутами архивных таблиц корпоративов и bonds_bought
        sql = f"""SELECT *, 
                        SUM(qn) as qnt, 
                        ip_koeff * {ipLotBondsQn} as QN , 
                        ip_koeff * {ipLotBondsQn} - SUM(qn) as delta
                    FROM inx_packgs_bonds AS ipb 
                    INNER JOIN
                    (SELECT * FROM bonds_archive) AS ba
                    ON ipb.bond_isin  = ba.isin 
                    LEFT JOIN
                    bonds_bought AS bb
                    ON ipb.bond_isin  = bb.isin 
                    LEFT JOIN
                    comp_analisys as ca
                    ON ba.inn_ref  = ca.inn
                    WHERE ipb.inx_pckg_id={inxPckgId} 
                    GROUP BY ba.inn_ref
        """
        
        
        
        # C. Фрейм
        dfIpCorporativePortfolioConsolByInn =  self.spps.read_sql_to_df_pandas_SPPS(sql)
        
        # PandasManager.print_df_gen_info_pandas_IF_DEBUG_static(dfIpCorporativePortfolioConsolByInn, True, colsIndxed=True, 
        #                                                     marker=f"PR_976 --> dfIpCorporativePortfolioConsolByInn")
        
        # D. Получить сумму положительных дельта-разниц между нормой по кол-ву облигаций, норма отображает кол-во потенциально необходимых облигаций
        # по каждому эмитенту и его рискам. Дельта - разница между нормой , зависящей от риска компании и установочному
        # кол-ву облигаций в одном лоте. 
        
        resQnSum = int(dfIpCorporativePortfolioConsolByInn.query('delta > 0')['delta'].sum())
        
        return resQnSum
    
    
    
    def get_sum_positive_delta_for_all_bought_bonds_and_for_all_inx_pckgs_group_by_inn_pbf (self, ipLotBondsQn):
        """ 
        Получить сумму положительных дельта-разниц между нормой по кол-ву корпоративных облигаций эмитента и реальным кол-во облигаций от эмитента в портфолио.
        Норма отображает кол-во потенциально необходимых облигаций
        по каждому эмитенту и его рискам. Дельта - разница между нормой , зависящей от риска компании и установочному
        кол-ву облигаций в одном лоте. 
        """
        
        # A. Получить массив облигаций из индексного пакета расширенного атрибутами архивных таблиц корпоративов и bonds_bought
        sql = f"""SELECT *, 
                        SUM(qn) as qnt, 
                        ip_koeff * {ipLotBondsQn} as QN , 
                        ip_koeff * {ipLotBondsQn} - SUM(qn) as delta
                    FROM inx_packgs_bonds AS ipb 
                    INNER JOIN
                    (SELECT * FROM bonds_archive) AS ba
                    ON ipb.bond_isin  = ba.isin 
                    LEFT JOIN
                    bonds_bought AS bb
                    ON ipb.bond_isin  = bb.isin 
                    LEFT JOIN
                    comp_analisys as ca
                    ON ba.inn_ref  = ca.inn
                    GROUP BY ba.inn_ref
        """
        
        # C. Фрейм
        dfIpCorporativePortfolioConsolByInn =  self.spps.read_sql_to_df_pandas_SPPS(sql)
        
        # PandasManager.print_df_gen_info_pandas_IF_DEBUG_static(dfIpCorporativePortfolioConsolByInn, True, colsIndxed=True, 
        #                                                     marker=f"PR_976 --> dfIpCorporativePortfolioConsolByInn")
        
        # D. Получить сумму положительных дельта-разниц между нормой по кол-ву облигаций, норма отображает кол-во потенциально необходимых облигаций
        # по каждому эмитенту и его рискам. Дельта - разница между нормой , зависящей от риска компании и установочному
        # кол-ву облигаций в одном лоте. 
        
        # E. Позитивные Дельта для облигаций, которые есть в портфолио 
        allPositiveDeltaSumForAllIpPortfolioBonds = int(dfIpCorporativePortfolioConsolByInn.query('delta > 0')['delta'].sum())
        # F. Позитивные Дельта, которых нет в портфолио, но которые внесены в индексные пакеты для покупки
        # TODO: ??? Возможно-Проверить: Слегка неправильная формула, так как не учитывает ие облигации, которые уже есть от эмитента. Вернее, наоборот, учитывает новую норму
        #  для облигаций, добавленных в индексный пакет, но не вычитает кол-во купленных дугих облигаций , если эмитент уже имеет в предыдущем
        # прочие облигации !!! Формула должна быть более сложной. Сделать по подобию расчета колонки Delta в таблице, где этот нюанс учитывается
        allPositiveDeltaSumNotInPortfolioButInInxPckgToBeBought = int(dfIpCorporativePortfolioConsolByInn.query('QN > 0' and 'qnt != qnt')['QN'].sum())
        
        totalPositiveDelta = allPositiveDeltaSumForAllIpPortfolioBonds + allPositiveDeltaSumNotInPortfolioButInInxPckgToBeBought
        
        return totalPositiveDelta
    
    
    
    
    def get_sum_positive_delta_of_norm_qn_and_portf_qn_all_ofz_munic_for_given_inx_pckg_bonds_pbf (self, inxPckgId, ipLotBondsQn, ipOfzMunicCoeff):
        """ 
        Получить сумму положительных дельта-разниц между нормой по кол-ву ОФЗ и Муницип облигаций  и реальным кол-во  ОФЗ и Муницип облигаций в портфолио.
        Норма отображает кол-во потенциально необходимых облигаций
        по каждому эмитенту и его рискам. Дельта - разница между нормой , зависящей от риска эмитента и установочному
        кол-ву облигаций в одном лоте. 
        ПРИМ: Считаем, что все ОФЗ и Муницип облигации от одного эмитента: Государства. Поэтому риск эмитента для 
        всех этого типа облигаций один (Его где-то надо устанавливать в одном  месте). От него расчитывается норма и дельта
        как буд-то для одного эмитента - государвтсва
        """
    
        # B. Получить сумму количеств всех облигаций из пересечения подмножеств облигаций заданного инвест-пакета и облигаций портфолио
        sql = f"""SELECT *, 
                        SUM(qn) as qnt, 
                        {ipOfzMunicCoeff} * {ipLotBondsQn} as QN , 
                        {ipOfzMunicCoeff} * {ipLotBondsQn} - SUM(qn) as delta
                    FROM inx_packgs_bonds AS ipb 
                    INNER JOIN
                    (SELECT * FROM ofz_archive UNION SELECT * FROM municip_archive) AS omclx
                    ON ipb.bond_isin  = omclx.isin 
                    LEFT JOIN
                    bonds_bought AS bb
                    ON ipb.bond_isin  = bb.isin 
                    WHERE ipb.inx_pckg_id={inxPckgId}
        """
        # print(f"PR_977 --> sql = {sql}")
        
        # C. Фрейм
        dfIpOfzMunicSumQn =  self.spps.read_sql_to_df_pandas_SPPS(sql)
        
        # PandasManager.print_df_gen_info_pandas_IF_DEBUG_static(dfIpOfzMunicSumQn, True, colsIndxed=True, 
        #                                                     marker=f"PR_978 --> dfIpOfzMunicSumQn")
        
        # Если в колонке 'delta' - нет значений (то есть не найдено никаких облигаций в индексном пакете)
        if dfIpOfzMunicSumQn.iloc[0]['delta'] is not None: 
            resQnSum = int(dfIpOfzMunicSumQn.query('delta.notnull() & delta > 0')['delta'].sum())
        else:
            resQnSum = 'No rows'
        
        return resQnSum
    
    
    
    
    
    
    def get_bond_gkd_by_isin_pbf (self, isin):
        """ 
        Получить ГКД облигации
        """
    
        sql = f"SELECT annual_yield FROM bonds_archive WHERE isin = '{isin}'"
    
        res = self.sps.get_result_from_sql_exec_proc_sps(sql)
        
        if not isinstance (res, int):
            ret = res[0]
        else:
            ret = -1
        
        gkd = ret
        
        return gkd    
    
    
    
    
    def get_dictionary_of_oferta_type_for_inx_packages_bonds_pbf (self):
        """ 
        Получить словарь с ключами в виде ISIN  облигаций из облигаций во всех индексных пакетах и со значениями типа оферты 
        в поле 'f3' расширяющей таблицы bonds_archive 
        """
        
        sql = f"""SELECT isin, f3 FROM inx_packgs_bonds AS ipb
                    LEFT JOIN {ms.TB_BONDS_ARCHIVE} AS ba
                    ON  ipb.bond_isin = ba.isin
        """
        
        # print(f"PR_A023 --> sql = {sql}")
        
        df = self.spps.read_sql_to_df_pandas_SPPS(sql)
        
        
        # Получить словарь с ключами в по заданной колонке ключей в фрейме и значениями равными значениям в так же задаваемой колонке фрейма
        dict = PandasManager.get_dict_from_df_with_key_col_name_and_val_col_name_pbf(df, 'isin', 'f3')
        

        return dict
    
    
    
    ########### END ОПЕРАЦИИ С ОБЛИГАЦИЯМИ



    ########### ОПРЕЦИИ С СИСТЕМНЫМИ НАСТРОЙКАМИ ################
    
    def get_inx_package_lot_bonds_qn_set_sys_db_var_pbf (self):
        """ 
        Получить настройку по кол-ву облигаций в лоте для работы с индексными пакетами
        """
        
        sql = f"SELECT set_data_int FROM {ms.TB_SYS_BONDS_SETTINGS} WHERE set_id = 'IP_LOT_BONDS_QN'"
    
        res = self.sps.get_result_from_sql_exec_proc_sps(sql)
        
        
        
        ipLotBondsQn = res[0]
        
        print(f"PR_959 --> ipLotBondsQn = {ipLotBondsQn}")
        
        return ipLotBondsQn
    
    
    
    def get_ofz_munic_inx_pckg_risk_coeff (self):
        """ 
        Получить риск-коэффициент для бумаг инвест-пакетов типа ОФЗ и Муницип, где эмитентом выступает Государство
        """
        
        sql = f"SELECT set_data_int FROM {ms.TB_SYS_BONDS_SETTINGS} WHERE set_id = 'IP_OFZ_MUNIC_RISK_COEFF'"
    
        res = self.sps.get_result_from_sql_exec_proc_sps(sql)
        
        ipOfzMunicRiskCoeff = res[0]
        
        return ipOfzMunicRiskCoeff
        
    
    
    
    ########### END ОПРЕЦИИ С СИСТЕМНЫМИ НАСТРОЙКАМИ ################





if __name__ == '__main__':
    pass




    # ПРОРАБОТКА: Получить суммарное кол-во необходимых дельта-плюсов (только позитивных, исключая негативны и исключая ОФЗ и Муницип) 
    # корпоративных облигаций по всем индексным пакетам
    
    pbf = ProjectBondsFunctions()
    
    # inxPckgId = 6
    ipLotBondsQn = 3
    # ipOfzMunicCoeff = 20
    

    allPositiveDeltaSumForAllIpPortfolioBonds = pbf.get_sum_positive_delta_for_all_bought_bonds_and_for_all_inx_pckgs_group_by_inn_pbf (ipLotBondsQn)

    print(f"PR_965 --> allPositiveDeltaSumForAllIpPortfolioBonds = {allPositiveDeltaSumForAllIpPortfolioBonds}")


    
    
    
    
    # # ПРОРАБОТКА: Функция получения колличеств всех облигаций (с разными ИСИН) в портфолио по одному заданному эмитенту 
    # # (только для корпоративов, у которых могут быть разные ИСИН для одного эмитента). Для ОФЗ и Муниципалов - нет ИНН и каждый ИСИН - это отдельная облигация
    
    # pbf = ProjectBondsFunctions()
    
    # # Формирвоание словаря с ключами ввиде ИНН эмитента и значениями в виде суммарного кол-ва облигаций из портфолио данного эмитента
    # dicPortfolioBondsConsolidatedQnByInn = pbf.get_dic_corporative_portfolio_bonds_consolidated_qn_by_inn_pbf()
    # print(f"PR_965 --> dicInnAndConsolidatedQn = {dicPortfolioBondsConsolidatedQnByInn}")
    


    # # ПРОРАБОТКА: get_united_atributes_df_of_inx_pckg_bonds_and_its_archive_extension_pbf (self, inxPckgNick)
    
    
    # inxPckgNick = 'Пакет AB'
    
    # pbf = ProjectBondsFunctions()
    
    # df = pbf.get_united_atributes_df_of_inx_pckg_bonds_and_its_archive_extension_pbf(inxPckgNick)
    
    # PandasManager.print_df_gen_info_pandas_IF_DEBUG_static(df, True, colsIndxed = True, marker=f"PR_907 --> df")



    # # ПРОРАБОТКА: update_pay_matrix_bond_month_sum_coupons_payments_by_isin()
    
    # listIsins = [
        
    #     'RU000A106SL0',
    #     'RU000A106T85',
    #     'RU000A106TJ2',
    #     'RU000A106U90',
    #     'RU000A106UA9',
    #     'RU000A106UW3',
    #     'RU000A106X89',
    #     'RU000A106XJ4',
    #     'RU000A106Y70',
    #     'RU000A106YL8',
    #     'RU000A106YN4',
    #     'RU000A106Z38',
    #     'RU000A1070A3',
    #     'RU000A1071R5',
    #     'RU000A106YE3',
    #     'RU000A107043',
    #     'RU000A1070X5',
    #     'RU000A105QL6',
    #     'RU000A104WZ7',
    #     'RU000A107225',
    #     'RU000A106CM2',
    # ]
    
    # pbf = ProjectBondsFunctions()
    
    # pbf.update_pay_matrix_bond_month_sum_coupons_payments_by_list_isins_pbf(listIsins)



    # # ПРОРАБОТКА: Получение описсаний компании по ИНН
    
    # pbf = ProjectBondsFunctions()
    
    # inn = '7729686084'
    # dicCompDescrs = pbf.get_comp_descriptions_by_inn(inn)
    
    # print(f"PR_545 --> dicRes = {dicCompDescrs['SPARK']}")
    




