

from noocube.bonds_main_manager import BondsMainManager
from noocube.html_manager_django import HTMLSiteManagerJango
import pandas as pd
from  noocube.table_html_manager import TableHtmlManager
from noocube.bonds_main_manager_speedup import BondsMainManagerSpeedup


import sys
sys.path.append('/home/ak/projects/P21_Telegram_Channel_Parsing_Django/telegram_channel_parsing_django')
import settings_bdp_main as ms # общие установки для всех модулей


from noocube.sqlite_processor_speedup import SqliteProcessorSpeedup
from noocube.funcs_general_class import FunctionsGeneralClass


class LocalFunctions ():
    """ 
    Локальные вспомогательные функциии для модуля bonds_dj_app (bda)
    """
    
    
    def __init__(self): 
        pass
        
    
    
    
    
    ##### XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX  PRJ_021  XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX

    
    
    
    @staticmethod
    def get_delta_detween_max_and_min_ids_in_registration_messages_tabeles_simple():
        """ 
        LocalFunctionsBda
        Получение ориентировочного значения кол-ва загруженных и зарегестрированных в БД сообщений в каналена данный момент 
        (естественно они не включают новые появившиеся сообщения в канале)
        
        Получить разницу между максимальными и минимальными значениями собственных ID сообщений, зарегестрированных в таблицах 'tg_messages_proceeded' 
        и 'tg_auxilary_messages_proceeded' , чтобы получить ориентировочное значение успешно обработанных значений сообщений в канале с конца, определяемых
        во View analyze_and_download_messages_from_ch_id_01() лимитом сообщений для обработки , начиная с конца и вверх по каналу
        Это значение не абсолютно, так как оно отображает зафиксированное значение сообщений из канала на тото момент, когда была запущена
        функция скачивания и обработки сообщений. С той поры в канале согут прибавится новые сообщений. Но примерное значение обработанных сообщений 
        в предыдущих сессиях может быть понятно ля того, что бы ориентировочно задавать следующий лимит в view analyze_and_download_messages_from_ch_id_01()
        
        ПРМИ: simple - означает то, что разницу в макисмльных и минимальных значениях ID сообщений вычисляется макимально просто, без анализа статуса сообщений,
        который может выражать ошибочность скачивания сообщений. !!!
        """
        
        sps = SqliteProcessorSpeedup(ms.DB_CONNECTION)
        
        # A. Сначала скачиваем все message_own_id из табл 'tg_messages_proceeded', находим минмальный и максимальный ID в данной таблице
        sql = f"SELECT message_own_id FROM {ms.TB_MSSGS_PROCEEDED_}"
        
        resMainIdList = sps.get_result_from_sql_exec_proc_sps(sql) # Список числовых ID сообщений из таблицы 'tg_messages_proceeded'
        
        print(f"PR_A430 --> resMainIdList = {resMainIdList}")
        
        if isinstance(resMainIdList, list): # Если  есть записи
            # resMainIdList = [0]
            
            # # B. Получить все message_own_id из табл 'tg_auxilary_messages_proceeded', находим минмальный и максимальный ID в данной таблице
            # sql = f"SELECT message_own_id FROM {ms.TB_AUXILARY_MSSGS_PROCEEDED_}"
            
            # resAuxilaryIdList = sps.get_result_from_sql_exec_proc_sps(sql) # Список числовых ID сообщений из таблицы 'tg_auxilary_messages_proceeded'
            
            # print(f"PR_A192 --> resAuxilaryIdList = {resAuxilaryIdList}")
            
            # if isinstance(resAuxilaryIdList, int) : # Если нет записей
            #     resAuxilaryIdList = 0
            
            # totalList = [resMainIdList, resAuxilaryIdList] # Составляем список списков числовых ID из разных таблиц
            
            totalList = [resMainIdList] # Составляем список списков числовых ID из разных таблиц
            
            
            
            # C. Получить минимум - максимум из списка списков числовых ID из разных таблиц
            minMaxList = FunctionsGeneralClass.get_min_max_from_list_of_int_lists(totalList)
            
            
            
            # Получаем разницу дельта из максимального и минимального значений ID сообщений из всех списков из всех таблиц
            resMaxMinIdsDelta = int(minMaxList[1]) - int(minMaxList[0])
            
            
            print(f"PR_A191 --> resMaxMinIdsDelta = {resMaxMinIdsDelta}")
            
        else: 
            resMaxMinIdsDelta = 0
            minMaxList = 0
            
        
        return minMaxList, resMaxMinIdsDelta


    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    ##### XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX  END PRJ_021  XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX

    
    
    
    
    
    
    @staticmethod
    def prepare_table_html_for_bonds_t1(df,  **fkwargs):
        """ 
        LocalFunctionsBda
        Подготовить табличные данные ддля вывода облигаций на странице сайта на основе фрейма df с данными 
        Для формирования сортировки в заголовках, обычной, простой, необходимо 4 параметра:
            - sort_col - название сортируемой колонки
            - sort_asc - направление сортировки в виде 'True'/ 'False' - параметр из строки url, если задана сортировка
            - standartExludingSortFields - список полей, которые должны быть исключены из ссылки в саголовке с сортировкой

        Для формирования ширины колонок при формировании заголовков в <th></th> используется словарь tableColsWidth

        Прим: !! Add lightweight datatables to your project with using the Simple DataTables library. Just add .datatable class name to any table you wish to conver to a datatable
            * https://github.com/fiduswriter/Simple-DataTables 
            Что бы заработал этот пакет нужно прописать tableCode = '<table class="table datatable">' классы в тэге <table>
        """

        # Если есть строки в фрейме,то есть , если есть фрейм
        if isinstance(df , pd.DataFrame):

            tableCode = '<table class="table">'
            # Заголовки таблицы с сокрытием невидимых колонок, которые в названии имеют часть 'HIDDEN' и задаются в словаре ассоциаций названий в settings.py типа COLS_ASSOC_FOR_COMPLEX_BONDS_
            tableHead = TableHtmlManager.prepare_tb_head_advanced_with_color_diff_and_hidden_cols(df, **fkwargs)
            # Тело таблицы с сокрытием невидимых колонок, которые в названии имеют часть 'HIDDEN' и задаются в словаре ассоциаций названий в settings.py типа COLS_ASSOC_FOR_COMPLEX_BONDS_
            tableBody =  TableHtmlManager.prepare_table_body_with_color_diff_and_hidden_cols(df)
            tableCode += tableHead + tableBody
            tableCode += '</table>' 
            
            return tableCode
        
        else :
            return 'В фрейме нет строк'




    @staticmethod
    def prepare_table_html_for_bonds_t1_v2(**fkwargs):
        """ 
        LocalFunctionsBda
        Подготовить табличные данные ддля вывода облигаций на странице сайта на основе фрейма df с данными 
        ПРИМ: Отличие от предыдущей версии в том, что возвращается код без обертки тэгом <table></table>,что бы можно было довставлять какие-то дополнительные ряды, типа
        итогов и пр.
        Для формирования сортировки в заголовках, обычной, простой, необходимо 4 параметра:
            - sort_col - название сортируемой колонки
            - sort_asc - направление сортировки в виде 'True'/ 'False' - параметр из строки url, если задана сортировка
            - standartExludingSortFields - список полей, которые должны быть исключены из ссылки в саголовке с сортировкой

        Для формирования ширины колонок при формировании заголовков в <th></th> используется словарь tableColsWidth

        Прим: !! Add lightweight datatables to your project with using the Simple DataTables library. Just add .datatable class name to any table you wish to conver to a datatable
            * https://github.com/fiduswriter/Simple-DataTables 
            Что бы заработал этот пакет нужно прописать tableCode = '<table class="table datatable">' классы в тэге <table>
        """

        # Если есть строки в фрейме,то есть , если есть фрейм
        if isinstance(fkwargs['df'] , pd.DataFrame):

            # tableCode = '<table class="table">'
            # Заголовки таблицы с сокрытием невидимых колонок, которые в названии имеют часть 'HIDDEN' и задаются в словаре ассоциаций названий в settings.py типа COLS_ASSOC_FOR_COMPLEX_BONDS_
            tableHead = TableHtmlManager.prepare_tb_head_advanced_with_color_diff_and_hidden_cols(fkwargs['df'], **fkwargs)
            # Тело таблицы с сокрытием невидимых колонок, которые в названии имеют часть 'HIDDEN' и задаются в словаре ассоциаций названий в settings.py типа COLS_ASSOC_FOR_COMPLEX_BONDS_
            tableBody =  TableHtmlManager.prepare_table_body_with_color_diff_and_hidden_cols(fkwargs['df'])
            tableCode = tableHead + tableBody
            # tableCode += '</table>' 
            
            return tableCode
        
        else :
            return 'В фрейме нет строк'



    @staticmethod
    def prepare_table_html_for_bonds_t1_v3(df,  **fkwargs):
        """ 
        LocalFunctionsBda
        Подготовить табличные данные ддля вывода облигаций на странице сайта на основе фрейма df с данными 
        ПРИМ: Отличие от предыдущей версии в том, что возвращается код без обертки тэгом <table></table>,что бы можно было довставлять какие-то дополнительные ряды, типа
        итогов и пр.
        Версия 3: Добавлена возможность добавлять фиксированные url-атрибуты и их значения в в формируемую автоматом константную url-строку 
        Для формирования сортировки в заголовках, обычной, простой, необходимо 4 параметра:
            - sort_col - название сортируемой колонки
            - sort_asc - направление сортировки в виде 'True'/ 'False' - параметр из строки url, если задана сортировка
            - standartExludingSortFields - список полей, которые должны быть исключены из ссылки в саголовке с сортировкой

        Для формирования ширины колонок при формировании заголовков в <th></th> используется словарь tableColsWidth

        Прим: !! Add lightweight datatables to your project with using the Simple DataTables library. Just add .datatable class name to any table you wish to conver to a datatable
            * https://github.com/fiduswriter/Simple-DataTables 
            Что бы заработал этот пакет нужно прописать tableCode = '<table class="table datatable">' классы в тэге <table>
        """

        # Если есть строки в фрейме,то есть , если есть фрейм
        if isinstance(df , pd.DataFrame):

            # tableCode = '<table class="table">'
            # Заголовки таблицы с сокрытием невидимых колонок, которые в названии имеют часть 'HIDDEN' и задаются в словаре ассоциаций названий в settings.py типа COLS_ASSOC_FOR_COMPLEX_BONDS_
            tableHead = TableHtmlManager.prepare_tb_head_advanced_with_color_diff_and_hidden_cols_v2(df, **fkwargs)
            # Тело таблицы с сокрытием невидимых колонок, которые в названии имеют часть 'HIDDEN' и задаются в словаре ассоциаций названий в settings.py типа COLS_ASSOC_FOR_COMPLEX_BONDS_
            tableBody =  TableHtmlManager.prepare_table_body_with_color_diff_and_hidden_cols(df)
            tableCode = tableHead + tableBody
            # tableCode += '</table>' 
            
            return tableCode
        
        else :
            return 'В фрейме нет строк'
        
        


    @staticmethod
    def prepare_table_html_for_bonds_t1_v4(dicDecorRes,  **fkwargs):
        """ 
        LocalFunctionsBda
        Подготовить табличные данные ддля вывода облигаций на странице сайта на основе фрейма df с данными 
        ПРИМ: Отличие от предыдущей версии в том, что возвращается код без обертки тэгом <table></table>,что бы можно было довставлять какие-то дополнительные ряды, типа
        итогов и пр.
        Версия 3: Добавлена возможность добавлять фиксированные url-атрибуты и их значения в в формируемую автоматом константную url-строку 
        Версия 4:  Теперь для динамической функции используется такая функция, которая принимает не фрейм , а сквозной словарь декораторов dicDecorRes, в котором содержится как фрейм,
        так и прочие параметры
        Для формирования сортировки в заголовках, обычной, простой, необходимо 4 параметра:
            - sort_col - название сортируемой колонки
            - sort_asc - направление сортировки в виде 'True'/ 'False' - параметр из строки url, если задана сортировка
            - standartExludingSortFields - список полей, которые должны быть исключены из ссылки в саголовке с сортировкой

        Для формирования ширины колонок при формировании заголовков в <th></th> используется словарь tableColsWidth

        Прим: !! Add lightweight datatables to your project with using the Simple DataTables library. Just add .datatable class name to any table you wish to conver to a datatable
            * https://github.com/fiduswriter/Simple-DataTables 
            Что бы заработал этот пакет нужно прописать tableCode = '<table class="table datatable">' классы в тэге <table>
        """

        # Если есть строки в фрейме,то есть , если есть фрейм
        if isinstance(dicDecorRes['df'] , pd.DataFrame):

            # tableCode = '<table class="table">'
            # Заголовки таблицы с сокрытием невидимых колонок, которые в названии имеют часть 'HIDDEN' и задаются в словаре ассоциаций названий в settings.py типа COLS_ASSOC_FOR_COMPLEX_BONDS_
            tableHead = TableHtmlManager.prepare_tb_head_advanced_with_color_diff_and_hidden_cols_v2(dicDecorRes, **fkwargs)
            # Тело таблицы с сокрытием невидимых колонок, которые в названии имеют часть 'HIDDEN' и задаются в словаре ассоциаций названий в settings.py типа COLS_ASSOC_FOR_COMPLEX_BONDS_
            tableBody =  TableHtmlManager.prepare_table_body_with_color_diff_and_hidden_cols(dicDecorRes['df'])
            tableCode = tableHead + tableBody
            # tableCode += '</table>' 
            
            return tableCode
        
        else :
            return 'В фрейме нет строк'
        
        
        
        
        
    @staticmethod
    def prepare_table_html_for_bonds_t1_v5(**dicDecorRes):
        """ 
        LocalFunctionsBda
        Подготовить табличные данные ддля вывода облигаций на странице сайта на основе фрейма df с данными 
        ПРИМ: Отличие от предыдущей версии в том, что возвращается код без обертки тэгом <table></table>,что бы можно было довставлять какие-то дополнительные ряды, типа
        итогов и пр.
        Версия 3: Добавлена возможность добавлять фиксированные url-атрибуты и их значения в в формируемую автоматом константную url-строку 
        Версия 4:  Теперь для динамической функции используется такая функция, которая принимает не фрейм , а сквозной словарь декораторов dicDecorRes, в котором содержится как фрейм,
        так и прочие параметры
        Версия 5: В паарметрах оставлены только именные парметры в качестве **dicDecorRes
        Для формирования сортировки в заголовках, обычной, простой, необходимо 4 параметра:
            - sort_col - название сортируемой колонки
            - sort_asc - направление сортировки в виде 'True'/ 'False' - параметр из строки url, если задана сортировка
            - standartExludingSortFields - список полей, которые должны быть исключены из ссылки в саголовке с сортировкой

        Для формирования ширины колонок при формировании заголовков в <th></th> используется словарь tableColsWidth

        Прим: !! Add lightweight datatables to your project with using the Simple DataTables library. Just add .datatable class name to any table you wish to conver to a datatable
            * https://github.com/fiduswriter/Simple-DataTables 
            Что бы заработал этот пакет нужно прописать tableCode = '<table class="table datatable">' классы в тэге <table>
        """

        # Если есть строки в фрейме,то есть , если есть фрейм
        if isinstance(dicDecorRes['df'] , pd.DataFrame):

            # tableCode = '<table class="table">'
            # Заголовки таблицы с сокрытием невидимых колонок, которые в названии имеют часть 'HIDDEN' и задаются в словаре ассоциаций названий в settings.py типа COLS_ASSOC_FOR_COMPLEX_BONDS_
            tableHead = TableHtmlManager.prepare_tb_head_advanced_with_color_diff_and_hidden_cols_v3(**dicDecorRes)
            # Тело таблицы с сокрытием невидимых колонок, которые в названии имеют часть 'HIDDEN' и задаются в словаре ассоциаций названий в settings.py типа COLS_ASSOC_FOR_COMPLEX_BONDS_
            tableBody =  TableHtmlManager.prepare_custom_table_body_v4(**dicDecorRes)
            tableCode = tableHead + tableBody
            # tableCode += '</table>' 
            
            return tableCode
        
        else :
            return 'В фрейме нет строк'



    @staticmethod
    def prepare_table_html_for_month_payment_matrix(**dicDecorRes):
        """ 
        LocalFunctionsBda
        Подготовить табличные данные ддля вывода облигаций на странице сайта на основе фрейма df с данными 
        ПРИМ: В данном коде таблицы пустые значения ячеек None замещаются на прочерки '-' 
        ПРИМ: Отличие от предыдущей версии в том, что возвращается код без обертки тэгом <table></table>,что бы можно было довставлять какие-то дополнительные ряды, типа
        итогов и пр.
        Для формирования сортировки в заголовках, обычной, простой, необходимо 4 параметра:
            - sort_col - название сортируемой колонки
            - sort_asc - направление сортировки в виде 'True'/ 'False' - параметр из строки url, если задана сортировка
            - standartExludingSortFields - список полей, которые должны быть исключены из ссылки в саголовке с сортировкой

        Для формирования ширины колонок при формировании заголовков в <th></th> используется словарь tableColsWidth

        Прим: !! Add lightweight datatables to your project with using the Simple DataTables library. Just add .datatable class name to any table you wish to conver to a datatable
            * https://github.com/fiduswriter/Simple-DataTables 
            Что бы заработал этот пакет нужно прописать tableCode = '<table class="table datatable">' классы в тэге <table>
        """

        # Если есть строки в фрейме,то есть , если есть фрейм
        if isinstance(dicDecorRes['df'] , pd.DataFrame):

            # tableCode = '<table class="table">'
            # Заголовки таблицы с сокрытием невидимых колонок, которые в названии имеют часть 'HIDDEN' и задаются в словаре ассоциаций названий в settings.py типа COLS_ASSOC_FOR_COMPLEX_BONDS_
            tableHead = TableHtmlManager.prepare_tb_head_advanced_with_color_diff_and_hidden_cols_v3(**dicDecorRes)
            # Тело таблицы с сокрытием невидимых колонок, которые в названии имеют часть 'HIDDEN' и задаются в словаре ассоциаций названий в settings.py типа COLS_ASSOC_FOR_COMPLEX_BONDS_
            tableBody =  TableHtmlManager.prepare_table_body_for_month_payment_matrix(**dicDecorRes)
            tableCode = tableHead + tableBody
            # tableCode += '</table>' 
            
            return tableCode
        
        else :
            return 'В фрейме нет строк'
        
        
        
        
        






    @staticmethod
    def add_summary_rows_to_month_pay_matrix (df):
        """
        Добавить суммирующие, итоговые ряды в таблицы месячных выплат по облигациям (матрицы выплат)
        """
        
        # print(f'GGGGGGGGGGGGGGGGGG   FFFFFFFFFFFFFFFFFFFFFFF   df = {df} ')

        
        # 0. Local const
        MIN_BG_CLR_ = '#FF0000' # Цыет максимума в суммарной выплате купонов
        MAX_BG_CLR_ = '#008000' # Цвет минимума
        #8B0000
        TOTAL_CLR_ = '#8B0000'
        
        addedSpecialRows = []

        # A.  Получить агрегейт по колонкам с месяцами из подготовленного в dsocBondsBought фрейма
        aggrColsList = [
                'Янв',
                'Февр',
                'Март',
                'Апр',
                'Май',
                'Июнь',
                'Июль',
                'Август',
                'Сент',
                'Окт',
                'Нояб',
                'Декаб',
            ]
        
        strAggFunc = 'sum'
        resSerries = BondsMainManager.get_aggregate_by_cols_and_agg_func(df, aggrColsList, strAggFunc)


        # B. Получить минимум и макимальные индексы в серии
        imin = resSerries.idxmin()
        imax = resSerries.idxmax()

        
        dicAccordance = {
            'Янв' : 1,
            'Февр': 2,
            'Март': 3,
            'Апр': 4,
            'Май': 5,
            'Июнь': 6,
            'Июль': 7,
            'Август': 8,
            'Сент': 9,
            'Окт': 10,
            'Нояб': 11,
            'Декаб': 12,
        }
        
        # Вычесть 13% и вывести итоговую строку
        summaryRow13 = '<tr><td><b>ИТОГО -13%:</b></td> <td></td><td></td><td></td>'
        totalYearSumm = 0 # Гоодовой доход от всех выплат , сцммарный по всем месяцам
        for index,colAggr in enumerate(resSerries.items()):
            # print(round(colAggr[1], 2))
            colAggSum = round(float(round(colAggr[1], 2)) - float(round(colAggr[1], 2))*13/100, 1)
            totalYearSumm += colAggSum
            if index == dicAccordance[imin]-1:
                summaryRow13 += f'<td style="color:{MIN_BG_CLR_};"><b><p style="cursor:pointer" title="Показать те облигации, выплаты по которым формируют данную сумму в данном месяце" onclick="window.open(\'http://127.0.0.1:9050/bonds_dj_app/bought_bonds_payments_by_month?payment_month={index+1}\', \'_blank\')">{colAggSum}</p></b></td>'
            elif index == dicAccordance[imax]-1:
                summaryRow13 += f'<td style="color:{MAX_BG_CLR_};"><b><p style="cursor:pointer" title="Показать те облигации, выплаты по которым формируют данную сумму в данном месяце" onclick="window.open(\'http://127.0.0.1:9050/bonds_dj_app/bought_bonds_payments_by_month?payment_month={index+1}\', \'_blank\')">{colAggSum}</p></b></td>'
            else:
                summaryRow13 += f'<td><b><p style="cursor:pointer" title="Показать те облигации, выплаты по которым формируют данную сумму в данном месяце" onclick="window.open(\'http://127.0.0.1:9050/bonds_dj_app/bought_bonds_payments_by_month?payment_month={index+1}\', \'_blank\')">{colAggSum}</p></b></td>'

        summaryRow13 += '</tr>'
        summaryRow13 += '</tr>'
        # print (summaryRow13)
        addedSpecialRows.append(summaryRow13)

        # Сложить Доход от всех месяцев и вывести в TOTAL
        totalYearSummRound = round(totalYearSumm,1)
        summaryRowYearTotal = f'<tr><td><b>TOTAL -13%:</b></td><td style="color:{TOTAL_CLR_};"><b>{totalYearSummRound} р.</b></td>'
        addedSpecialRows.append(summaryRowYearTotal)

        # 6. Добавление еще двух итоговых строк

        monthesLowRow = """<tr><td></td><td></td><td></td><td></td>
        <td><a href="http://127.0.0.1:9050/bonds_dj_app/index_packages_portfolio_by_month_folders?payment_month=1" target = "_blank" title="Показать индексные пакеты и портфолио в разрезе этого месяца"><b>Январь</b></a></td>
        <td><a href="http://127.0.0.1:9050/bonds_dj_app/index_packages_portfolio_by_month_folders?payment_month=2" target = "_blank" title="Показать индексные пакеты и портфолио в разрезе этого месяца"><b>Февраль</b></a></td>
        <td><a href="http://127.0.0.1:9050/bonds_dj_app/index_packages_portfolio_by_month_folders?payment_month=3" target = "_blank" title="Показать индексные пакеты и портфолио в разрезе этого месяца"><b>Март</b></a></td>
        <td><a href="http://127.0.0.1:9050/bonds_dj_app/index_packages_portfolio_by_month_folders?payment_month=4" target = "_blank" title="Показать индексные пакеты и портфолио в разрезе этого месяца"><b>Апрель</b></a></td>
        <td><a href="http://127.0.0.1:9050/bonds_dj_app/index_packages_portfolio_by_month_folders?payment_month=5" target = "_blank" title="Показать индексные пакеты и портфолио в разрезе этого месяца"><b>Май</b></a></td>
        <td><a href="http://127.0.0.1:9050/bonds_dj_app/index_packages_portfolio_by_month_folders?payment_month=6" target = "_blank" title="Показать индексные пакеты и портфолио в разрезе этого месяца"><b>Июнь</b></a></td>
        <td><a href="http://127.0.0.1:9050/bonds_dj_app/index_packages_portfolio_by_month_folders?payment_month=7" target = "_blank" title="Показать индексные пакеты и портфолио в разрезе этого месяца"><b>Июль</b></a></td>
        <td><a href="http://127.0.0.1:9050/bonds_dj_app/index_packages_portfolio_by_month_folders?payment_month=8" target = "_blank" title="Показать индексные пакеты и портфолио в разрезе этого месяца"><b>Август</b></a></td>
        <td><a href="http://127.0.0.1:9050/bonds_dj_app/index_packages_portfolio_by_month_folders?payment_month=9" target = "_blank" title="Показать индексные пакеты и портфолио в разрезе этого месяца"><b>Сентябрь</b></a></td>
        <td><a href="http://127.0.0.1:9050/bonds_dj_app/index_packages_portfolio_by_month_folders?payment_month=10" target = "_blank" title="Показать индексные пакеты и портфолио в разрезе этого месяца"><b>Октябрь</b></a></td>
        <td><a href="http://127.0.0.1:9050/bonds_dj_app/index_packages_portfolio_by_month_folders?payment_month=11" target = "_blank" title="Показать индексные пакеты и портфолио в разрезе этого месяца"><b>Ноябрь</b></a></td>
        <td><a href="http://127.0.0.1:9050/bonds_dj_app/index_packages_portfolio_by_month_folders?payment_month=12" target = "_blank" title="Показать индексные пакеты и портфолио в разрезе этого месяца"><b>Декабрь</b></a></td>
        </tr>"""
        addedSpecialRows.append(monthesLowRow)
        
        
        
        addedSpecialRowsHTML = ''.join(addedSpecialRows)
        
        
        
        return addedSpecialRowsHTML
        
        
        





        













if __name__ == '__main__':
    pass

    # ПРОРАБОТКА: prepare_table_html_for_bonds_type1(df)
    
    # bmm = BondsMainManager(ms.DB_BONDS) 
    
    # dfComplexBonds = bmm.get_complex_bonds_df_with_added_diff_columns(ms.TB_BONDS_CURRENT, ms.TB_OFZ_CURRENT, ms.TB_MUNICIP_CURRENT)
    
    

    
    # # ПРОРАБОТКА: Агрегирование столбцов фрейма -  матрица помесячных выплат по облигациям агрегированная 
    
    # from noocube.bonds_main_manager_speedup import BondsMainManagerSpeedup
    
    # bmms = BondsMainManagerSpeedup(ms.DB_CONNECTION) # Подключение к конекшену
    
    # dfBoughtBonds = bmms.get_bought_bonds_df_with_added_diff_columns()
    
    # print(dfBoughtBonds.dtypes)
    
    # aggrColsList = [
    #         'jan',
    #         # 'feb',
    #         # 'march',
    #         # 'apr',
    #         # 'may',
    #         # 'june',
    #         # 'july',
    #         # 'aug',
    #         # 'sept',
    #         # 'oct',
    #         # 'nov',
    #         # 'dec',
    #     ]

    
    # strAggFunc = 'sum'
    # resSerries = BondsMainManager.get_aggregate_by_cols_and_agg_func(dfBoughtBonds, aggrColsList, strAggFunc)





    
    
    
    
    
    
    
    
    
    
    
    
    
    
    