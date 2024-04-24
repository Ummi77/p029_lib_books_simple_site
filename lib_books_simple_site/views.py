from django.shortcuts import render

# Create your views here.










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








