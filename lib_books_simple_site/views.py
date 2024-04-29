
# Динамическое подключение settings_bdp_main в корне проекта
import sys
sys.path.append('/home/ak/projects/P029_book_lib_site_simple_tg_django/book_lib_site_simple_tg_django')
import lib_books_simple_site.settings_bdp_main as ms # общие установки для всех модулей

# Django
from django.shortcuts import render
from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt



# Noocube
from noocube.django_view_manager_v3 import DjangoViewManager_V3
from noocube.switch import Switch
from noocube.sqlite_processor_speedup import SqliteProcessorSpeedup
from noocube.sqlite_pandas_processor_speedup import SqlitePandasProcessorSpeedup

# locals
from lib_books_simple_site.local_classes.book_library_funcs_bss import BookLibraryFuncsBss

# Third party
import json
from beeprint import pp



def index(request):
    """
    
    """
    
    
    
    # I. НАстройка распечаток названия View (и их прописание вверху и внизу: START & END)
    prStartEnd = {
        'prStart' : 'PR_B499',
        'prEnd' : 'PR_B500',
    }
    # print(f"--> START {prStartEnd['prStart']} --> : {request.resolver_match.view_name}()") # Маркер старта метода для лога в консоли
    



    # print(f"--> END {prStartEnd['prEnd']} --> : {request.resolver_match.view_name}() VAR: ") # Маркер завершения метода для лога в консоли

    # return HttpResponse('ГОТОВО')
    return render(request, 'lib_books_simple_site/index.html')







@csrf_exempt # декоратор необходимый для работы с POST (с формами)
def api_update_bss_options_table (request):
    """ 
    Обновить таблицу БД с опциями (это такие таблицы, которые несут в себе перечни чего-либо)
    Обновить - это значит вставить, если записи нет и обновить данные в записи, в случае ее существования в таблице

    """
    # I. НАстройка распечаток названия View (и их прописание вверху и внизу: START & END)
    prStartEnd = {
        'prStart' : 'PR_B502',
        'prEnd' : 'PR_B503',
    }
    print(f"--> START {prStartEnd['prStart']} --> : {request.resolver_match.view_name}()") # Маркер старта метода для лога в консоли
    
    # III. Инициализация сквозного словаря dicThrough для текущего View на уровне noocube (уровень универсализации) и необходимых функциональных обьектов
    
    dvm = DjangoViewManager_V3(request)
    blfbss = BookLibraryFuncsBss()
    sps = SqliteProcessorSpeedup(ms.DB_CONNECTION)
    # sdm = SysDevelopManager()
    spps = SqlitePandasProcessorSpeedup(ms.DB_CONNECTION) 
    
    # IV. Аналитическая, исполнительная часть и подготовка процедурных фреймов
    
    # Получение  json-формы обьекта опционных таблиц из requestPost
    jsonDbOptionsTables = dvm.dicThrough['requestDicPost'] ['jsonDbOptionsTables']
    
    # A. Перевод json-формы обьекта в обьект: словарь
    
    dicDbOptionsTables = json.loads(jsonDbOptionsTables)
    
    
    
    print(f"PR_B517 --> dicDbOptionsTables")
    pp(dicDbOptionsTables)



    

    
    # B. Цикл по пришедшим данным по опционным таблицам из БД 'labba' c проекта PRJ021 с их дифференциированной обработкой
    
    for tbKey, val in dicDbOptionsTables.items():
    
        # Дифференциация процедур по каждой из таблиц. представленных в словаре dicDbOptionsTables (ключи в этом словаре идентифицируют таблицы в БД, которые надо 
        # проапдейтить данными из словаря)
    
        # C. Дифференцированные процедуры для обновления таблиц: 1. Очищение опционной таблицы 2. Запись по новой всех опционных данных таблицы с заданными их 'id'. 
        # Все таблицы должны стать в полном соотвтетсвии с текущем состоянием тпблиц в БД проекта PRJ021 
        for case in Switch(tbKey):
            
            # Для таблицы 'lib_categories'
            if case('dicTbCategories'): 
                
                print(f"PR_B511 --> SYS LOG: Сделать UPDATE таблиы 'lib_categories' на основе данных в суб-словаре dicTbCategories")
                
                # INI
                dicTbCategories = val
                
                # Перевод поля id в цифровой вид
                
                dicTbCategories = {int(key) : val for key, val in dicTbCategories.items()}
                

                
                # 1. Очищение опционной таблицы  'lib_categories'
                
                sps.truncate_table_mysql_sps(ms.TB_LIB_CATEGORIES)
                print(f"PR_B512 --> SYS LOG: Удалены записи и обнулена таблица 'lib_categories'")
                
                # 2. Запись по новой всех опционных данных таблицы 'lib_categories' из данных словаря dicTbCategories
                # ПРИМ: предварительно удален автоинкремент для id  в табл 'lib_categories' (так как эта таблица, как и другие в этой БД, 
                # лишь проекции первичных таблиц в проекте PRJ021)
                
                blfbss.api_insert_categories_from_dic_tb_data_bss(dicTbCategories)
                
                break
            
            if case('dicTbLibAuthors'): 
                
                print(f"PR_B518 --> SYS LOG: Сделать UPDATE таблиы 'lib_authors' на основе данных в суб-словаре dicTbLibAuthors")
                
                # INI
                dicTbLibAuthors = val
                
                # Перевод поля id в цифровой вид
                
                dicTbLibAuthors = {int(key) : val for key, val in dicTbLibAuthors.items()}
                
                print(f"PR_B509 --> dicTbLibAuthors")
                pp(dicTbLibAuthors)
                
                
                # 1. Очищение опционной таблицы  'lib_authors'
                
                sps.truncate_table_mysql_sps(ms.TB_LIB_AUTHORS)
                print(f"PR_B521 --> SYS LOG: Удалены записи и обнулена таблица 'lib_authors'")
                
                # 2. Запись по новой всех опционных данных таблицы 'lib_categories' из данных словаря dicTbCategories
                # ПРИМ: предварительно удален автоинкремент для id  в табл 'lib_categories' (так как эта таблица, как и другие в этой БД, 
                # лишь проекции первичных таблиц в проекте PRJ021) {_ВСЕ_РАБОТАЕТ_}
                
                # PARS
                
                tbName = ms.TB_LIB_AUTHORS
                
                dicTbAuthorsFields = {
                    
                    'firstName' : 'author_first_name',
                    'secondName' : 'author_second_name',
                    'fullName' : 'author_full_name',
                }
                
                blfbss.api_insert_persons_from_dic_tb_data_bss( tbName, dicTbLibAuthors, dicTbAuthorsFields)

                break
            
            if case('dicTbLibLanguages'): 
                
                print(f"PR_B519 --> SYS LOG: Сделать UPDATE таблиы 'lib_languages' на основе данных в суб-словаре dicTbLibLanguages")
                
                
                # INI
                dicTbLibLanguages = val
                
                # Перевод поля id в цифровой вид
                
                dicTbLibLanguages = {int(key) : val for key, val in dicTbLibLanguages.items()}

                # 1. Очищение опционной таблицы  'lib_languages'
                
                sps.truncate_table_mysql_sps(ms.TB_LIB_LANGUAGES)
                print(f"PR_B530 --> SYS LOG: Удалены записи и обнулена таблица 'lib_languages'")
                
                # 2. Запись по новой всех опционных данных таблицы 'lib_languages' из данных словаря dicTbCategories
                # ПРИМ: предварительно удален автоинкремент для id  в табл 'lib_languages' (так как эта таблица, как и другие в этой БД, 
                # лишь проекции первичных таблиц в проекте PRJ021)
                
                blfbss.api_insert_languages_from_dic_tb_data_bss(dicTbLibLanguages)

                break
            
            if case('dicTbLibNarrators'): 
                
                print(f"PR_B531 --> SYS LOG: Сделать UPDATE таблиы 'lib_narrators' на основе данных в суб-словаре dicTbLibNarrators")
                
                
                # INI
                dicTbLibNarrators = val
                
                # Перевод поля id в цифровой вид
                
                dicTbLibNarrators = {int(key) : val for key, val in dicTbLibNarrators.items()}
                
                print(f"PR_B532 --> dicTbLibNarrators")
                pp(dicTbLibNarrators)
                
                
                # 1. Очищение опционной таблицы  'lib_narrators'
                
                sps.truncate_table_mysql_sps(ms.TB_LIB_NARRATORS)
                print(f"PR_B533 --> SYS LOG: Удалены записи и обнулена таблица 'lib_narrators'")
                
                # 2. Запись по новой всех опционных данных таблицы 'lib_categories' из данных словаря dicTbCategories
                # ПРИМ: предварительно удален автоинкремент для id  в табл 'lib_categories' (так как эта таблица, как и другие в этой БД, 
                # лишь проекции первичных таблиц в проекте PRJ021) {_ВСЕ_РАБОТАЕТ_}
                
                # PARS
                
                tbName = ms.TB_LIB_NARRATORS
                
                dicTbNarratorsFields = {
                    
                    'firstName' : 'narrator_first_name',
                    'secondName' : 'narrator_second_name',
                    'fullName' : 'narrator_full_name',
                }
                
                blfbss.api_insert_persons_from_dic_tb_data_bss( tbName, dicTbLibNarrators, dicTbNarratorsFields)

                break
            
            
            
            if case(): # default
                print('PR_B510 --> Другое')
                break
        



    # Возвращаемые данные методу, запустившему процессы AJAX
    # ret = 'ГОТОВО'
    print(f"--> END {prStartEnd['prEnd']} --> : {request.resolver_match.view_name}()") # Маркер завершения метода для лога в консоли
    
    return HttpResponse()

























