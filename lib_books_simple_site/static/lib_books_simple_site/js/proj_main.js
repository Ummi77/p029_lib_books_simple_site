




// JS159^^ - GENERAL FIFFERENCIATOR OF LOADING PAGES OR STARTER !!!!
// Запускает какие-то jquery функции в зависимости от загрузки какой-то заданной странице сайта или View. 
// Что бы включался стартовый дифференциатор необходимо в url параметрах иметь: '?diff_starter=True'


$(document).ready(function(){

    // Get url attr value  
    const queryString = window.location.search;
    const urlParams = new URLSearchParams(queryString);
    const diff_starter = urlParams.get('diff_starter'); // html-фтрибут в url браузера alfa_id

    // alert(diff_starter)

    if (diff_starter == 'True') {

        // Get url attr value
        url = window.location.href
        var u_parts = url.split('?')

        var puth_parts = u_parts[0].split('/')

        var p_qn = puth_parts.length

        var curr_view = puth_parts[p_qn - 1]

        switch (curr_view) {
            case 'book_authors_editor':
                // alert( 'PR_B390 --> Diff starter: from View -> book_authors_editor()' );






                break;
            case 4:
                alert( 'В точку!' );
                break;
            case 5:
                alert( 'Перебор' );
                break;
            default:
                alert( "Нет таких значений" );
            }


    } // if (start_diff == 'True') {


})





// JS114^^   ajax Подгрузить и высветить список авторов для редактирования и присваивания авторов для книги

$(document).ready(function(){

    // var alfa_id = 1; // alfaId книги, которое надо взять из url
    // alert()
    // Get url attr value
    const queryString = window.location.search;
    const urlParams = new URLSearchParams(queryString);
    const alfa_id = urlParams.get('alfa_id');

    $("#show_authors_editor").on("click", function() {

        $(".attr_editor").css({display:'none'}); // выкд.чение всех СЕКЦИЙ вообще

        $('#authors_editor').css({display:'block'});

        $('#book_authors_editor').css({display:'block'}); // включение секции общего редактирования авторов в book_authors_editor.html

        // выполняем  ajax запрос - обновить список авторов в модуле редактирвоания
        $.ajax(
            {
                type: "GET",
                url: "get_html_checkboxes_authors_list_block_ajax" ,
                data: {
                    "alfa_id" : alfa_id, 
            
                },
            }
            
            )
        .always(function(data) { //Выполнить при успешном выполнении ajax запроса
            // alert( data2);
            $('#authors_container').html(data)
        })

        .fail(function(data) { //Выполнить при успешном выполнении ajax запроса
            alert('PR_B374 --> ajax fail');
        });

        // $(this).trigger("click"); // Нажать на сылку програмно. что бы прокрутить вниз до якоря и показать редактор

    } );
})

// END JS114^^   ajax Подгрузить и высветить список авторов для редактирования и присваивания авторов для книги








// JS132^^   ajax Подгрузить и высветить список дикторов для редактирования и присваивания дикторов для книги

$(document).ready(function(){

    // var alfa_id = 1; // alfaId книги, которое надо взять из url

    // Get url attr value
    const queryString = window.location.search;
    const urlParams = new URLSearchParams(queryString);
    const alfa_id = urlParams.get('alfa_id');

    $("#show_book_narrators_editor").on("click", function() {

        // alert()

        // Скрыть все блоки кодов и высветить только #narrators_editor
        $(".attr_editor").css({display:'none'});
        $('#narrators_editor').css({display:'block'});

        // alert()


        sendData = {
            alfa_id : alfa_id,
        }
        

        $.get("get_html_checkboxes_narrators_list_block_ajax", sendData) 

        .done(function(data) { //Выполнить при успешном выполнении ajax запроса
            // alert( data2);
            $('#narrators_container').html(data)
        })

        .fail(function(data) { //Выполнить при успешном выполнении ajax запроса
            alert('JS132^^ -> ajax fail');
        });


    } );
})

// END JS132^^   ajax Подгрузить и высветить список дикторов для редактирования и присваивания дикторов для книги


















// JS120^^   ajax Подгрузить и высветить список статусов книги для редактирования и присваивания статусов для книги


$(document).ready(function(){

    // var alfa_id = 1; // alfaId книги, которое надо взять из url

    // Get url attr value
    const queryString = window.location.search;
    const urlParams = new URLSearchParams(queryString);
    const alfa_id = urlParams.get('alfa_id');

    $("#show_book_statuses_editor").on("click", function() {

        $(".attr_editor").css({display:'none'});

        $('#book_statuses_editor').css({display:'block'});

        // выполняем  ajax запрос - обновить список авторов в модуле редактирвоания
        $.ajax(
            {
                type: "GET",
                url: "get_html_checkboxes_book_statuses_list_block_ajax" ,
                data: {
                    "alfa_id" : alfa_id, 
                },
            }
            
            )
        .always(function(data) { //Выполнить при успешном выполнении ajax запроса
            // alert( data2);
            $('#book_statuses_container').html(data)
        })

        .fail(function(data) { //Выполнить при успешном выполнении ajax запроса
            alert('ajax fail');
        });

    } );
})

// END JS120^^   ajax Подгрузить и высветить список статусов книги для редактирования и присваивания статусов для книги







// JS127^^   ajax Подгрузить и высветить список категорий книги для редактирования и присваивания категорий для книги

$(document).ready(function(){


    // Get url attr value
    const queryString = window.location.search;
    const urlParams = new URLSearchParams(queryString);
    const alfa_id = urlParams.get('alfa_id');

    $("#show_book_categories_editor, #book_categs_checkboxes_restore").on("click", function() {

        $(".attr_editor").css({display:'none'});

        $('#book_categories_editor').css({display:'block'});



        // выполняем  ajax запрос - обновить список авторов в модуле редактирвоания
        $.ajax(
            {
                type: "GET",
                url: "get_html_checkboxes_book_caategories_list_block_ajax" ,
                data: {
                    "alfa_id" : alfa_id, 
                },
            }
            
            )
        .done(function(data) { //Выполнить при успешном выполнении ajax запроса
            // alert( data2);
            $('#lib_categories_ajax_container').html(data)
        })

        .fail(function(data) { //Выполнить при успешном выполнении ajax запроса
            alert('PR_A630 --> ajax fail in JS127');
        });

    } );
})

// END JS127^^   ajax Подгрузить и высветить список категорий книги для редактирования и присваивания категорий для книги










// // JS116^^   Высветить редактор автора книги при нажатии на редактировать автора


// $(document).ready(function(){
//     $("#open_author_editor").on("click", function() {

//         var chosen_chbox_data = $(".chb_book_authors:checked").map(function(index,domElement) {
//             var firstn = $(domElement).attr('firstn') // атрибут с данными по имени автора в текущем элементе checkbox
//             var scndn = $(domElement).attr('scndn') // фамилия автора
//             var elVal = $(domElement).val()
//             var res = [elVal, firstn, scndn];
//             return res; //  TODO: суммирует все результаты в один список. а надо, что бы был список списков. иначе все неразборчиво попадает в один список
//         }).get(); 

//         // alert(chosen_chbox_data.length)
        
//         // Если выбран больше. чем один checkbox
//         if (chosen_chbox_data.length > 3) { // TODO: дико дубовая реализация, потом исправить. 3 занчения данных соотвтетсвуют одному выбранному checkbox
//             alert('PR_A497 --> SYS LOG: Выбрано более одного автора')
//         }

//         else if (chosen_chbox_data.length < 1) { // TODO: дико дубовая реализация, потом исправить. 3 занчения данных соотвтетсвуют одному выбранному checkbox
//             alert('PR_A510 --> SYS LOG: Не выбрано ни одного автора')
//         }

//         else {

//             $(".attr_editor").css({display:'none'}); // Выключить все прочие редакторы

//             $('#edit_author').css({display:'block'});  // Включить редактор автора
    
//             // $(this).trigger("click"); // Нажать на сылку програмно. что бы прокрутить вниз до якоря и показать редактор

//             // присваиваем значения в редактируемые поля, а так же в hidden поле с  шв fdnjhf
//             $('#author_id').val(chosen_chbox_data[0]); 
//             $('#author_first_name').val(chosen_chbox_data[1]);
//             $('#author_second_name').val(chosen_chbox_data[2]);

//         }


//     });
// })

// // END JS116^^  контекстное меню правого нажатия мышки курсора   $(this)





// JS134^^   Высветить редактор диктора книги при нажатии на редактировать автора


$(document).ready(function(){
    $("#open_narrator_editor").on("click", function() {

        var chosen_chbox_data = $(".chb_book_narrators:checked").map(function(index,domElement) {
            var firstn = $(domElement).attr('firstn') // атрибут с данными по имени автора в текущем элементе checkbox
            var scndn = $(domElement).attr('scndn') // фамилия автора
            var elVal = $(domElement).val()
            var res = [elVal, firstn, scndn];
            return res; //  TODO: суммирует все результаты в один список. а надо, что бы был список списков. иначе все неразборчиво попадает в один список
        }).get(); 

        // alert(chosen_chbox_data.length)
        
        // Если выбран больше. чем один checkbox
        if (chosen_chbox_data.length > 3) { // TODO: дико дубовая реализация, потом исправить. 3 занчения данных соотвтетсвуют одному выбранному checkbox
            alert('PR_A745 --> SYS LOG: Выбрано более одного диктора')
        }

        else if (chosen_chbox_data.length < 1) { // TODO: дико дубовая реализация, потом исправить. 3 занчения данных соотвтетсвуют одному выбранному checkbox
            alert('PR_A746 --> SYS LOG: Не выбрано ни одного диктора')
        }

        else {

            $(".attr_editor").css({display:'none'}); // Выключить все прочие редакторы

            $('#edit_narrator').css({display:'block'});  // Включить редактор автора
    
            // $(this).trigger("click"); // Нажать на сылку програмно. что бы прокрутить вниз до якоря и показать редактор

            // присваиваем значения в редактируемые поля, а так же в hidden поле с  шв fdnjhf
            $('#narrator_id').val(chosen_chbox_data[0]); 
            $('#narrator_first_name').val(chosen_chbox_data[1]);
            $('#narrator_second_name').val(chosen_chbox_data[2]);

        }


    });
})

// END JS134^^  контекстное меню правого нажатия мышки курсора   $(this)










// JS142^^   Высветить редактор одного заданного аудио-тома книги при нажатии на сроку в перечне аудио-томов в модуле редактирования книги


$(document).ready(function(){
    $(".open_audio_volume_editor").on("click", function() {

        // alert("POINT A")

        $(".attr_editor").css({display:'none'}); // Выключить все прочие редакторы

        $('#edit_audio_volume').css({display:'block'});  // Включить редактор автора

        // присваиваем значения в редактируемые поля, а так же в hidden поле с  id аудио-книги

        // INI
        var volume_id = $(this).attr('volume_id')
        var volume_file_name = $(this).html()

        // var volume_title = $('#volume_title_li span').html()

        var volume_title = $('#volume_title_li_span_' + volume_id).html()

        $('#audio_volume_id').val(volume_id); 

        $('#volume_file_name_inp').val(volume_file_name); 

        $('#volume_title_inp').val(volume_title); 

        window.open('#edit_audio_volume', "_self"); // Якорь

    });
})

// END JS142^^  контекстное меню правого нажатия мышки курсора   $(this)







// JS143^^  сохранить изменения в редактируемом аудио-томе
$(document).ready(function () {

    $("#sbtn_edit_audio_volume_form").click(function(event){

        var answer = window.confirm("PR_A837 --> Сейчас будут сохранены изменения в редактируемом аудио-томе книги: " +  ". Вы хотите сохранить изменения?");
        if (answer) {

            // Get url attr value
            const queryString = window.location.search;
            const urlParams = new URLSearchParams(queryString);
            const alfa_id = urlParams.get('alfa_id');

            // данные по полям формы плюс любые добавочные кастомные параметры для POST
            // ПРИМ: Название атрибутов задаем в соотвтетсвии с полями таблицы 'lib_book_audio_volumes' в которой эти поля будут апдейтится
            var sendData = { 
                id: $("#audio_volume_id").val(), // селектор для поля из форма по id поля
                volume_file_name: $("#volume_file_name_inp").val(), 
                volume_title: $("#volume_title_inp").val(), 
                };
                // AJAX  запрос
                // Переводим список в стринг, а потом снова распарсиваем его , получая выбранные id 
                $.post("save_book_audio_volume_edited_data", sendData) // Передача данных через AJAX (этот оператор - синоним .ajax )

                .done(function() {

                    var id = $("#audio_volume_id").val(); // селектор для поля из форма по id поля
                    var volume_title_changed = $("#volume_title_inp").val();

                    alert('PR_A838 --> Изменения успешно сохранены в БД!');

                    //Обновление измененного тайтла аудио-тома. Прим: Название файла не меняем. Н оесли понадобится - таким же образом как и тайтдл
                    $("#volume_title_li_span_" + id).html(volume_title_changed);

                    // // AJAX  запрос внутири первичного AJAX-запроса
                    // //Обновление списка аудио-томов книги в модуле редактора книги через AJAX (внутри данного AJAX)
                    // $.get("get_book_volumes_html_ul_block_for_edit", {alfa_id : alfa_id}) // Передача данных через AJAX (этот оператор - синоним .ajax )
                    // .done(function(data) {

                    //     // Обновить список аудио-томов книги в модуле редактора книги через AJAX
                    //     $("#book_volumes_ul_for_edit").html(data)

                    // })
                    // .fail(function() {
                    //     alert("PR_A839 --> Вложенный AJAX запрос для AJAX-перезагрузки блока с кодом с перечнем адио-томов книги в модуле редактирования!!! ")
                    // })

                })

                .fail(function() {
                    alert('PR_A840 --> Сбой в работе AJAX. Изменения не были сохранены в БД');
                })


        }

    });
    
});

// END JS143^^ сохранить изменения в заданном категрии (название категрии) после его редактирования в теблице 

















// JS122^^   Высветить редактор статуса книги при нажатии на редактировать статус (открывается редактор статуса, который выделен был в списке )


$(document).ready(function(){
    $("#open_book_status_editor").on("click", function() {

        var chosen_chbox_data = [];
        $(".chb_book_statuses:checked").each(function(i) {

            // chosen_chbox_values.push($(this).val());
            var book_status_id = $(this).val()
            var status_name = $(this).attr('status_name') 

            chosen_chbox_data.push({
                key:   book_status_id,
                value: status_name
            });

        });

        // alert(JSON.stringify(chosen_chbox_data) )
        
        // Если выбран больше. чем один checkbox
        if (chosen_chbox_data.length > 1) { // TODO: дико дубовая реализация, потом исправить. 3 занчения данных соотвтетсвуют одному выбранному checkbox
            alert('PR_A528 --> SYS LOG:  выбран более, чем один элемент checkbox')
        }

        else if (chosen_chbox_data.length < 1) { // TODO: дико дубовая реализация, потом исправить. 3 занчения данных соотвтетсвуют одному выбранному checkbox
            alert('PR_A529 --> SYS LOG: Не выбрано ни одного элемента checkbox')
        }

        else {

            $(".attr_editor").css({display:'none'}); // Выключить все прочие редакторы

            $('#edit_book_status').css({display:'block'});  // Включить редактор автора
    
            // $(this).trigger("click"); // Нажать на сылку програмно. что бы прокрутить вниз до якоря и показать редактор

            // // присваиваем значения в редактируемые поля, а так же в hidden поле с  шв fdnjhf
            $('#book_status_id').val(chosen_chbox_data[0]['key']); 
            $('#book_status').val(chosen_chbox_data[0]['value']);
            // $('#author_second_name').val(chosen_chbox_data[2]);

            }

    });
})

// END JS122^^  контекстное меню правого нажатия мышки курсора   $(this)







// JS129^^   Высветить редактор категории книги при нажатии на редактировать категорию (открывается редактор категории, который выделен был в списке )


$(document).ready(function(){
    $("#open_book_category_editor").on("click", function() {

        // alert()

        var chosen_chbox_data = [];
        $(".chb_book_categories:checked").each(function(i) {

            // alert()

            // chosen_chbox_values.push($(this).val());
            var book_category_id = $(this).val()
            var category_name = $(this).attr('category_name') 

            // alert(category_name)

            chosen_chbox_data.push({
                key:   book_category_id,
                value: category_name
            });

            // alert(chosen_chbox_data)

        });

        // alert(f"chosen_chbox_data = {chosen_chbox_data}")

        // alert(JSON.stringify(chosen_chbox_data) )
        
        // Если выбран больше. чем один checkbox
        if (chosen_chbox_data.length > 1) { // TODO: дико дубовая реализация, потом исправить. 3 занчения данных соотвтетсвуют одному выбранному checkbox
            
            alert('PR_A528 --> SYS LOG:  выбран более, чем один элемент checkbox')
        }

        else if (chosen_chbox_data.length < 1) { // TODO: дико дубовая реализация, потом исправить. 3 занчения данных соотвтетсвуют одному выбранному checkbox
            alert('PR_A529 --> SYS LOG: Не выбрано ни одного элемента checkbox')
        }

        else {

            

            $(".attr_editor").css({display:'none'}); // Выключить все прочие редакторы

            $('#edit_book_category').css({display:'block'});  // Включить редактор категории
    
            // // присваиваем значения в редактируемые поля, а так же в hidden поле с  шв fdnjhf
            $('#book_category_id').val(chosen_chbox_data[0]['key']); 
            $('#book_category').val(chosen_chbox_data[0]['value']);

            }

    });
})

// END JS129^^  Высветить редактор категории книги при нажатии на редактировать категорию (открывается редактор категории, который выделен был в списке )












// JS117^^  перехватить событие нажатия кнопки заданной формы и AJAX - отправить форму с редактируемыми данными по автору для сохранения изменений 
// в табл lib_authors

    $(document).ready(function () {





        $("#save_edit_author_butt").click(function () { // Перехват событи формы, заданной по селектору




        // alert()
        // данные по полям формы плюс любые добавочные кастомные параметры для POST
        var formData = { 
            author_id: $("#author_id").val(), // селектор для поля из форма по id поля
            author_first_name: $("#author_first_name").val(), 
            author_second_name: $("#author_second_name").val(), 
            ajax: "True", //  для запуска ajax концовки во view, а не рендеринг (кастомный добавочный параметр)
            // alfa_id: alfa_id,
        };


        var answer = window.confirm("PR_A530 --> Сейчас будут сохранены изменения в ФИО автора: " +  ". Вы хотите сохранить изменения в ФИО автора?");
        if (answer) {

        // Get url attr value  
            const queryString = window.location.search;
            const urlParams = new URLSearchParams(queryString);
            const alfa_id = urlParams.get('alfa_id'); // html-фтрибут в url браузера alfa_id


            $.ajax({
                type: "POST",
                url: "save_book_author_edited_data",
                data: formData,
                dataType: "text", // Если возврат идет в обычном тексте или вообще нет возврата, то этот оператор надо закоментить или дать значение text 
                encode: true, // ?
                //context: this, // ?
                success: (data) => { // тут можно выполнять работу с полученными данными. Позволяет разделить успешное и неуспешное завершение ajax 
                    // alert(data)
                    // window.location.reload(true);
                    // $(".attr_editor").css({display:'none'}); // Выключить все прочие редакторы

                    $('#authors_editor').css({display:'block'});  // Включить Authors Edit Section в книжном редакторе автворов

                    $('#second_edit_any_author').css({display:'block'});  // Включить Authors Edit Section в общем редакторе авторов

                    // alert(data)

                        // выполняем еще один ajax запрос внутри первого ajax - обновить список авторов в модуле редактирвоания get_html_checkboxes_authors_list_block_ajax
                        $.ajax( 
                            {
                                type: "GET",
                                url: "get_html_checkboxes_authors_list_block_ajax" ,
                                data: {
                                    "alfa_id" : alfa_id, // html-атрибут при запросе а модуль  url

                                },
                            }
                        )

                        .done(function(data2) {
                            // alert( data2);
                            $('#authors_container').html(data2)
                        });


                },
                error: (error) => {
                    alert("AJAX JQERY ERROR in View: save_book_author_edited_data()");
                }

            });
        } //  if (answer) {

        });
    });

// END JS117^^  перехватить событие нажатия кнопки заданной формы и AJAX - отправить форму с редактируемыми данными по автору для сохранения изменений 






// JS135^^  перехватить событие нажатия кнопки заданной формы и AJAX - отправить форму с редактируемыми данными по диктору для сохранения изменений 
// в табл lib_narrators

$(document).ready(function () {

    // Get url attr value  
    const queryString = window.location.search;
    const urlParams = new URLSearchParams(queryString);
    const alfa_id = urlParams.get('alfa_id'); // html-фтрибут в url браузера alfa_id



    $("#edit_narrators_form").submit(function (event) { // Перехват событи формы, заданной по селектору

    // alert()
    // данные по полям формы плюс любые добавочные кастомные параметры для POST
    var formData = { 
        narrator_id: $("#narrator_id").val(), // селектор для поля из форма по id поля
        narrator_first_name: $("#narrator_first_name").val(), 
        narrator_second_name: $("#narrator_second_name").val(), 
        ajax: "True", //  для запуска ajax концовки во view, а не рендеринг (кастомный добавочный параметр)
        // alfa_id: alfa_id,
    };

    $.ajax({
        type: "POST",
        url: "save_book_narrator_edited_data",
        data: formData,
        dataType: "text", // Если возврат идет в обычном тексте или вообще нет возврата, то этот оператор надо закоментить или дать значение text 
        encode: true, // ?
        //context: this, // ?
        success: (data) => { // тут можно выполнять работу с полученными данными. Позволяет разделить успешное и неуспешное завершение ajax 
            // alert(data)
            // window.location.reload(true);
            $(".attr_editor").css({display:'none'}); // Выключить все прочие редакторы

            $('#narrators_editor').css({display:'block'});  // Включить Authors Edit Section

                // выполняем еще один ajax запрос внутри первого ajax - обновить список авторов в модуле редактирвоания get_html_checkboxes_authors_list_block_ajax
                $.ajax( 
                    {
                        type: "GET",
                        url: "get_html_checkboxes_narrators_list_block_ajax" ,
                        data: {
                            "alfa_id" : alfa_id, // html-атрибут при запросе а модуль  url

                        },
                    }
                )



                .done(function(data2) {
                    // alert( data2);
                    $('#narrators_container').html(data2)
                });


        },
        error: (error) => {
            alert("JS135^^ ->  AJAX JQERY ERROR in View: save_book_narrator_edited_data()");
        }

    }).done(function (data) { // тут можно выполнять работу с полученными данными
        // console.log(data);
        // alert(data)
    }),
    
    event.preventDefault(); // to prevent the form from behaving by default by reloading the page on submission
    });
});

// END JS135^^  перехватить событие нажатия кнопки заданной формы и AJAX - отправить форму с редактируемыми данными по автору для сохранения изменений 










// JS123^^  сохранить изменения в заданном статусе (название статуса) после его редактирования в теблице lib_book_statuses

$(document).ready(function () {

    // Get url attr value  
    // const queryString = window.location.search;
    // const urlParams = new URLSearchParams(queryString);
    // const alfa_id = urlParams.get('alfa_id'); // html-фтрибут в url браузера alfa_id


    $("#sbtn_edit_book_status_form").click(function(event){

        var answer = window.confirm("PR_A530 --> Сейчас будут сохранены изменения в данных заданного статуса: " +  ". Вы хотите сохранить изменения в названии статуса?");
        if (answer) {

            // Get url attr value
            const queryString = window.location.search;
            const urlParams = new URLSearchParams(queryString);
            const alfa_id = urlParams.get('alfa_id');

            //     // AJAX  запрос

            // данные по полям формы плюс любые добавочные кастомные параметры для POST
            var formData = { 
                book_status_id: $("#book_status_id").val(), // селектор для поля из форма по id поля
                book_status: $("#book_status").val(), 
                };

                // Переводим список в стринг, а потом снова распарсиваем его , получая выбранные id 
                $.post("save_book_status_edited_data", formData) // Передача данных через AJAX (этот оператор - синоним .ajax )

                .done(function() {

                    alert('PR_A531 --> Изменения успешно сохранены в БД!');

                    $(".attr_editor").css({display:'none'}); // Выключить все прочие редакторы

                    $('#book_statuses_editor').css({display:'block'});  // Включить Authors Edit Section

                    //Обновление списка статусов в модуле редактирования статусов через AJAX (внутри данного AJAX)
                    $.get("get_html_checkboxes_book_statuses_list_block_ajax", {alfa_id : alfa_id}) // Передача данных через AJAX (этот оператор - синоним .ajax )
                    .done(function(html_data_block) {

                        // alert(html_data_block)
                        // Обновить список статусов после сохранения изменения в одном из ешо элементов
                        $("#book_statuses_container").html(html_data_block)

                    })
                    .fail(function() {
                        alert("PR_A533 --> Вложенный AJAX запрос для получение обновленного кода списка статусов прошел со сбоем!!! ")
                    })

                })

                .fail(function() {
                    alert('PR_A532 --> Сбой в работе AJAX. Изменения не были сохранены в БД');
                })


        }

    });
    
});
    








// JS130^^  сохранить изменения в заданном категрии (название категрии) после его редактирования в теблице 
$(document).ready(function () {

    $("#sbtn_edit_book_category_form").click(function(event){

        var answer = window.confirm("PR_A646 --> Сейчас будут сохранены изменения в данных заданной категории: " +  ". Вы хотите сохранить изменения в названии категории?");
        if (answer) {

            

            // Get url attr value
            const queryString = window.location.search;
            const urlParams = new URLSearchParams(queryString);
            const alfa_id = urlParams.get('alfa_id');

            

            //     // AJAX  запрос

            // данные по полям формы плюс любые добавочные кастомные параметры для POST
            var formData = { 
                book_category_id: $("#book_category_id").val(), // селектор для поля из форма по id поля
                book_category: $("#book_category").val(), 
                ifTransferChecked : $("#transfer_to_categ_vocabulary").is(":checked"),
                };

                // alert('ПРОВЕРКА')

                // Переводим список в стринг, а потом снова распарсиваем его , получая выбранные id 
                $.post("save_book_category_edited_data", formData) // Передача данных через AJAX (этот оператор - синоним .ajax )

                .done(function() {

                    alert('PR_A647 --> Изменения успешно сохранены в БД!');

                    $(".attr_editor").css({display:'none'}); // Выключить все прочие редакторы

                    $('#book_categories_editor').css({display:'block'});  // Включить Authors Edit Section

                    //Обновление списка категорий в модуле редактирования статусов через AJAX (внутри данного AJAX)
                    $.get("get_html_checkboxes_book_categories_list_block_ajax", {alfa_id : alfa_id}) // Передача данных через AJAX (этот оператор - синоним .ajax )
                    .done(function(html_data_block) {

                        // alert(html_data_block)
                        // Обновить список статусов после сохранения изменения в одном из ешо элементов
                        // $("#book_categories_container").html(html_data_block);
                        var book_category_id = $("#book_category_id").val();
                        var book_category = $("#book_category").val();
                        // alert(book_category)
                        // Простановка измененного названия категории в списке (куда нажали, то меняется)
                        $("[key_val_js148=" + book_category_id + "]").html(book_category);
                        // alert(book_category)
                        $("[key_val_js149=" + book_category_id + "]").html(book_category);


                    })
                    .fail(function() {
                        alert("PR_A648 --> Вложенный AJAX запрос для получение обновленного кода списка категорий прошел со сбоем!!! ")
                    })

                })

                .fail(function() {
                    alert('PR_A649 --> Сбой в работе AJAX. Изменения не были сохранены в БД');
                })


        }

    });
    
});

// END JS130^^ сохранить изменения в заданном категрии (название категрии) после его редактирования в теблице 













// JS115^^  Ajax jQuery универсальная фильтрация записей в стандартных процессинговых фреймах по задаваемым колонкам
// Модуль View  определяется из атрибута фильтрационного окна trg_view= "<Название целевого View>"
// Фильтрационное окно input определяется классом 'gen_filter_inp'. id фильтрационного поля - не важно
// Контейнер приема ajax-результата : Может быть любым, но обязательно id контейнера должен быть прописан 
// в атрибуте фльтрационнного окна так: ajax_container="<id контейнера>" 
// ПРИМ: Важно, что бы функиця формирования html-кода (резльтата по ajax) в подобных entity была идентична своим подобиям
// ПРИМ: Важно - название целевого View должно быть задано в атрибуте окна фильтрации с названием:  trg_view= "<Название целевого View>"
$( ".gen_filter_inp" ).on( "input", function() {

    // Analyse target url-nick depends on current url
    var curl = window.location.href;
    // Name of view equal to nick of url by default

    // Название целевого View, который формирует необходимый выход html-кода
    var trg_view =  $(this).attr('trg_view')

    // view_name = curl.split("/").pop().split("?")[0] 
    // alert(trg_view)

    // Get url attr value
    const queryString = window.location.search;
    const urlParams = new URLSearchParams(queryString);
    const alfa_id = urlParams.get('alfa_id');

    // Контейнер (должен быть прописан в фильтрационном поле input с классом 'gen_filter_inp')
    var ajax_container = $(this).attr('ajax_container')

    $.ajax({
    url: trg_view, // модуль View
    type: "GET",
    data: {
        "ajax": "True",
        "srch_str" : $(this).val(), // получаем значение из <input>
        "alfa_id" : alfa_id, 
    },
    
    //context: this, 
    success: (data) => {
        $('#' + ajax_container).html(data); // Вставить полученный с view html code for table to .div_container

    },
    error: (error) => {
        alert('AJAX JQERY ERROR in index.html -> $( "#tb_gen_srch" ).on( "input", function() ');
    }
    });
});






// JS119^^  Ajax сохранить выбор авторов (по списку checkboxes) для книги в табл lib_books_authors в модуле редактирования книги во view: edit_book_complect()
// При нажатии на 'Сохранить выбор для книги' отправить данные формы по Ajax в модуль: save_book_authors_choosen

$(document).ready(function(){



        $("#btn_save_book_chosen_authors").click(function(event){



            var authSeconds = [];
            $(".chb_book_authors:checked").each(function(i) {
                authSeconds.push($(this).attr('scndn'));
            });

            authSecondsStr = authSeconds.toString()

            // alert(authSecondsStr)


            var answer = window.confirm("PR_A542 --> Сейчас книге будут присвоены следующие авторы: " + authSecondsStr + ". Вы хотите присвоить книге данных авторов?");
            if (answer) {
                // Get url attr value
                const queryString = window.location.search;
                const urlParams = new URLSearchParams(queryString);
                const alfa_id = urlParams.get('alfa_id');


                var data = [];
                $(".chb_book_authors:checked").each(function(i) {
                    data.push($(this).val());
                });
                
                // Дубовая реализация, но решение. Другие пока никак не решаются. Можно еще попробовать сериализацию, что уже делалось ранее
                // Смысл в том, что переводим список в стринг, а потом снова распарсиваем его , получая выбранные id 
                // TODO: Понять, как передать массив через ajax. Почему-то при отправке на вью из html-аргумента этого получаем только последний выбранный элемент ???
                // data =  JSON.stringify(data)
                $.post("save_book_authors_choosen", {chkd_authors_ids:JSON.stringify(data), alfa_id:alfa_id}) // Передача данных через AJAX (этот оператор - синоним .ajax )

                .done(function() {

                    alert('PR_A543 --> Книге успешно присвоены выбранные авторы!');

                    // выполняем еще один ajax запрос внутри первого ajax - обновить список авторов в модуле редактирвоания get_html_checkboxes_authors_list_block_ajax
                    $.get( 
                        {
                            type: "GET",
                            url: "get_html_checkboxes_authors_list_block_ajax" ,
                            data: {
                                "alfa_id" : alfa_id, // html-атрибут при запросе а модуль  url

                            },
                        }
                    )

                    .done(function(data2) {
                        // alert( data2);
                        $('#authors_container').html(data2)
                    });


                });
            };
        });
    
});

// END JS119^^  Ajax сохранить выбор авторов (по списку checkboxes) для книги в табл lib_books_authors в модуле редактирования книги во view: edit_book_complect()







// JS124^^  Ajax сохранить выбор статусов (по списку checkboxes) для книги в табл lib_books_statuses (то есть присвоить книге выбранные из списка статусы)
// При нажатии на 'Сохранить выбор для книги' отправить данные формы по Ajax в модуль: save_book_authors_choosen

$(document).ready(function(){



    $("#btn_save_book_chosen_statuses").click(function(event){

        // alert()

        var bookStatusName = [];
        $(".chb_book_statuses:checked").each(function(i) {
            // alert()
            bookStatusName.push($(this).attr('status_name'));
        });

        var bookStatusNameStr = bookStatusName.toString()


        var answer = window.confirm("PR_A539 --> Сейчас книге будут присвоены следующие статусы: " + bookStatusNameStr + ". Вы хотите присвоить книге данные статусы?");
        if (answer) {
            // Get url attr value
            const queryString = window.location.search;
            const urlParams = new URLSearchParams(queryString);
            const alfa_id = urlParams.get('alfa_id');


            var data = [];
            $(".chb_book_statuses:checked").each(function(i) {
                data.push($(this).val());
            });
            
            // Дубовая реализация, но решение. Другие пока никак не решаются. Можно еще попробовать сериализацию, что уже делалось ранее
            // Смысл в том, что переводим список в стринг, а потом снова распарсиваем его , получая выбранные id 
            // TODO: Понять, как передать массив через ajax. Почему-то при отправке на вью из html-аргумента этого получаем только последний выбранный элемент ???
            data = data.toString() 
            $.post("save_book_statuses_choosen", {chkd_statuses_ids:data, alfa_id:alfa_id}) // Передача данных через AJAX (этот оператор - синоним .ajax )

            .done(function() {
                alert('PR_A541 --> Книге успешно присвоены выбранные статусы!');
            });
        };
    });

});

// END JS124^^  Ajax сохранить выбор авторов (по списку checkboxes) для книги в табл lib_books_authors в модуле редактирования книги во view: edit_book_complect()








// JS128^^  Ajax сохранить выбор категорий (по списку checkboxes) для книги в табл lib_books_categories (то есть присвоить книге выбранные из списка категории)
// При нажатии на 'Сохранить выбор для книги' отправить данные формы по Ajax в модуль: 

$(document).ready(function(){



    $("#btn_save_book_chosen_categories").click(function(event){

        // alert()

        var bookCategoryName = [];
        $(".checkboxb_js149:checked").each(function(i) {
            // alert()
            bookCategoryName.push($(this).attr('category_name'));
        });

        var bookCategoryNameStr = bookCategoryName.toString()


        var answer = window.confirm("PR_A632 --> Сейчас книге будут присвоены следующие категории: " + bookCategoryNameStr + ". Вы хотите присвоить книге данные категории?");
        if (answer) {
            // Get url attr value
            const queryString = window.location.search;
            const urlParams = new URLSearchParams(queryString);
            const alfa_id = urlParams.get('alfa_id');


            var data = [];
            $(".checkboxb_js149:checked").each(function(i) {
                data.push($(this).val());
            });
            
            // Дубовая реализация, но решение. Другие пока никак не решаются. Можно еще попробовать сериализацию, что уже делалось ранее
            // Смысл в том, что переводим список в стринг, а потом снова распарсиваем его , получая выбранные id 
            // TODO: Понять, как передать массив через ajax. Почему-то при отправке на вью из html-аргумента этого получаем только последний выбранный элемент ???
            data = data.toString()

            // alert(data)

            // AJAX-отправка -> $.post...
            $.post("save_book_categories_choosen", {chkd_categories_ids:data, alfa_id:alfa_id}) // Передача данных через AJAX (этот оператор - синоним .ajax )

            .done(function() {
                alert('PR_A633 --> Книге успешно присвоены выбранные категории!');
            });
        };
    });

});

// END JS128^^  Ajax сохранить выбор авторов (по списку checkboxes) для книги в табл lib_books_authors в модуле редактирования книги во view: edit_book_complect()








// JS125^^  Перезагрузить таблицу с книгами, но с фильтрацией по выбранному статусу (а так же, возможно, исключая выбранный статус)



$(document).ready(function(){


    $("#filter_by_status").change(function () {
        
        var filter_by = this.value;



        url = window.location.href
        var u_parts = url.split('?') 

        var url_with_filter = u_parts[0] + '?filt_status=' + filter_by

        // alert(filter_by)

        window.open(url_with_filter, "_self");
        
    });

    




});


// END JS125^^  Перезагрузить таблицу с книгами, но с фильтрацией по выбранному статусу (а так же, возможно, исключая выбранный статус)





// JS126^^  нажатие на кнопку : Сохранить-присвоить статус 'ALLOWED_TO_PUBLIC' тем книгам, чекюоксы которых в таблице выбраны
// View: save_status_allowed_publish_to_books_chosen()


$(document).ready(function(){


    $("#save_statuses_btn").click(function () {
        

        var answer = window.confirm("PR_A851 --> сейчас будут охранены зафиксированные на странице статусы в checkboxes: " + ". Вы хотите выполнить эту операцию?");
        if (answer) {
        
            // Данные по выбранным книгам
            var checked_data = [];
            $(".chb_allow_to_publick:checked").each(function(i) {
                checked_data.push($(this).val());
                
            });

            // Данные по невыранным книгам
            var unchecked_data = [];
            $(".chb_allow_to_publick:not(:checked)").each(function(i) {
                // alert($(this).val())
                unchecked_data.push($(this).val());
                
            });

            // alert(unchecked_data)
            
            $.post("save_status_allowed_publish_to_books_chosen", {books_ids_checked:JSON.stringify(checked_data), books_ids_unchecked:JSON.stringify(unchecked_data)}) // Передача данных через AJAX (этот оператор - синоним .ajax )

            .done(function() {
                url = window.location.href
                window.open(url, "_self"); // перезагрузить страницу для проверки фиксации статусов в БД
            });

        }

    });

});

// END JS126^^  нажатие на кнопку : Сохранить-присвоить статус 'ALLOWED_TO_PUBLIC' тем книгам, чекюоксы которых в таблице выбраны







// JS131^^ Удаление выбранных категорий в списки библиотечных категори, а так же возможных связей с книгами, которые уже существуют

$(document).ready(function(){

    $("#delete_chosen_lib_categories").click(function () {
        
        var chosen_chbox_data = [];
        $(".checkboxb_js148:checked").each(function() {

            // alert('POINT A')

            // chosen_chbox_values.push($(this).val());
            var book_status_id = $(this).val() 

            // alert(book_status_id)

            chosen_chbox_data.push(book_status_id);
        });

        // alert(JSON.stringify(chosen_chbox_data) )
        
        // // Если выбран больше. чем один checkbox
        // if (chosen_chbox_data.length > 1) { // TODO: дико дубовая реализация, потом исправить. 3 занчения данных соотвтетсвуют одному выбранному checkbox
        //     alert('PR_A713 --> SYS LOG:  выбран более, чем один элемент checkbox')
        // }

        if (chosen_chbox_data.length < 1) { // TODO: дико дубовая реализация, потом исправить. 3 занчения данных соотвтетсвуют одному выбранному checkbox
            alert('PR_A714 --> SYS LOG: Не выбрано ни одного элемента checkbox')
        }

        else { 

            // alert()
            var answer = window.confirm("PR_A710 --> Сейчас будет произведено удаление категории : " +  ". Вы хотите удалить данную категорию книги?");
            if (answer) {


                // Get url attr value
                const queryString = window.location.search;
                const urlParams = new URLSearchParams(queryString);
                const alfa_id = urlParams.get('alfa_id');

                // параметры для передачи через AJAX POST
                var sendData = { 
                    alfa_id : alfa_id,
                    chosen_categ_ids: JSON.stringify(chosen_chbox_data), 
                    };

                    //AJAX POST
                    $.post("delete_book_category", sendData)

                    .done(function() {

                        alert('PR_A711 --> Категория успешно удалена!');

                        // $(".attr_editor").css({display:'none'}); // Выключить все прочие редакторы

                        // $('#book_categories_editor').css({display:'block'});  // Включить Authors Edit Section

                        //Обновление списка категорий в модуле редактирования статусов через AJAX (внутри данного AJAX)
                        $.get("book_categories_editor", {ajax : 'True'}) // Передача данных через AJAX (этот оператор - синоним .ajax )
                        .done(function(html_data_block) {

                            // alert(html_data_block)
                            // Обновить список категорий после сохранения изменения в одном из его элементов
                            $("#lib_categories_ajax_container").html(html_data_block)

                        })
                    })

                    .fail(function() {
                        alert("JS131^^--> AJAX запрос прошел со сбоем!!! ")
                    })

            }

        }

    });

});


// END JS131^^ Удаление категории книги и ее связей









// JS137^^ Удалить зарегестрировнный книжный комплект или псевдо-книгу. 
// ПРИМ: Возможно и в предшествующих таблицах стадий, что бы не было повтора)
// View: delete_lib_registered_book_complect_or_pseudo_book()


$(document).ready(function(){


    $(".del_reg_book_complect").click(function () {
        
        var alfaId = $(this).attr('alfa_id')

        var sendData = { 
            alfa_id: alfaId, 
            };

            // AJAX 
            $.post("delete_lib_registered_book_complect_or_pseudo_book", sendData) // Передача данных через AJAX (этот оператор - синоним .ajax )

            .done(function() {


            })
            
            .fail(function() {


            });   

    });

});


// END JS137^^  Удаленить зарегестрировнный книжный комплект или псевдо-книгу.











// JS133^^ -  открыть источник сообщения в телеграме


$(document).ready(function(){


    $("#open_book_tg_source").click(function () {

        // Считать атрибут оригинальнойссылки на сообщение в ТГ-канале
        var srcTgLink = $(this).attr('srcTgLink')
        // открыть ссылку в новом браузер-окне-фолдере
        window.open(srcTgLink);

    });

});




// END JS133^^ -  открыть источник сообщения в телеграме











// JS136^^ -  открыть редактор категорий при нажатии на поле в таблице с перечнем категорий 


$(document).ready(function(){


    $(".tbrd_edit_categ_view01").click(function () {

        // Считать атрибут оригинальнойссылки на сообщение в ТГ-канале
        var balfa_id = $(this).attr('balfa_id')

        var categEditorLink = 'http://127.0.0.1:6070/telegram_monitor/edit_book_complect?alfa_id=' + balfa_id + '#book_categories_editor'
        // открыть ссылку в новом браузер-окне-фолдере
        var x = window.open(categEditorLink);

        // Псевдо-нажать на #show_book_narrators_editor
        // $( "#show_book_narrators_editor" ).trigger( "click" );

        window.setTimeout(function(){
            // do whatever you want to do   
            // $( "#show_book_narrators_editor" ).trigger( "click" );
            x.document.getElementById("show_book_categories_editor").click();
            
            }, 600);


    });

});




// END JS136^^ -  открыть источник сообщения в телеграме





// JS138^^ запустить Очистить таблицы ТГ сообщений

$(document).ready(function(){
    $(".clear_url").click(function () {
        var url = $(this).attr('hrefd')
        var action = $(this).html()
        var answer = window.confirm("PR_A809 --> " + action + "?");
        if (answer) {
            window.open(url, '_self');
        }
    });
});

// END JS138^^ 








// JS141^^ Popup TEST {STANDART}
// opener: $( ".show_book_volums_icon" ) - класс внутри селектора
// Function to show and hide the popup ~ https://jqueryui.com/dialog/#animated

    $(document).ready(function(){

        $(".show_book_volums_icon").click(function () {
            
            var alfaId = $(this).attr('alfa_id')
    
            var sendData = { 
                alfa_id: alfaId, 
                };
    
                // AJAX 
                $.post("obtain_book_audio_volums_data_to_html_block_ajax", sendData) // Передача данных через AJAX (этот оператор - синоним .ajax )
    
                .done(function(data) {
    
                    // Popup prepare
                    $("#popupBookVolumes").html(data)

                    // popup start
                        $( "#popupBookVolumes" ).dialog({

                            minWidth: 600, // ширина popup ~ http://127.0.0.1:6070/telegram_monitor/show_lib_books_to_allow_public_repositories_downloading
                            autoOpen: false,
                            show: {
                            effect: "blind",
                            duration: 10
                            },
                            hide: {
                            effect: "explode",
                            duration: 300
                            }
                        });

                        // Открыть popup окно
                        $( "#popupBookVolumes" ).dialog( "open" );
    
                })
                
                .fail(function() {

                });   
        });
    
    });


// END JS141^^ Popup TEST {STANDART}





    // JS144^^
    $(document).ready(function(){

        $(".reload_message_icon").click(function () {


            var mpid = $(this).attr('mpid')
            // alert(mpid)

            var sendData = { 
                mpid: mpid, 
                };
    
                // // AJAX 
                // $.get("reload_mistaken_messages_from_tg_chanel", sendData) // Передача данных через AJAX (этот оператор - синоним .ajax )
    
                // .done(function(data) {

                //     // alert(data)

                // })
                // .fail(function() {
                //     alert("FAIL AJAX")

                // }); 

        });
    
    });




    // JS145^^
    // Обработка сообщений: telegram_monitor/show_mssg_downloaded_errors.html
    $(document).ready(function(){


        $("#execute_btn_va001").click(function () {
            
    
    
            var chosen_chbox_data = [];
            $(".chb_mssg_execute_va001:checked").each(function(i) {
    
                // chosen_chbox_values.push($(this).val());
                var mssg_tbid = $(this).val()
    
                chosen_chbox_data.push(mssg_tbid);
    
            });

            var execute_type = $("#choose_execute_va001").val()


            // alert(execute_type)

            // параметры для передачи через AJAX POST
            var sendData = { 
                chosen_chbox_data : JSON.stringify(chosen_chbox_data),
                execute_type: execute_type, 
                };

                // alert(sendData)

            $.post("execute_proccessing_of_error_messages", sendData) // Передача данных через AJAX (этот оператор - синоним .ajax )

            .done(function() {
                // url = window.location.href
                // window.open(url, "_self"); // перезагрузить страницу для проверки фиксации статусов в БД
            })

            .fail(function() {

                alert('AJAX FAIL')

            });

        });
    
    });







// JS147^^  Ajax jQuery Универсальный метод фильтрации массива данных в стандартных процессинговых фреймах по задаваемым колонкам
// ПРИМ: контейнер, куда подгружаются данные, должен иметь id = lib_categories_ajax_container (какой-то уникальный id посложнее), поисковый инпут фильтрации должен быть id="data_filter"
// Селектор тоже должен быть уникальный и посложнее
// в поисковом окне должен быть задан целевая вьюха в виде атрибута 'target_view':
// [<input  type="text" id="lib_categories_data_filter" target_view="book_categories_editor"  value="">]
// Прим: функция используется тиз разных модулей с немног оразными настройками. поэтому это не индивидуальная функция
$( "#lib_categories_data_filter" ).on( "input", function() {


    // параметры для VIEW: get_html_checkboxes_book_caategories_list_block_ajax
    const queryString = window.location.search;
    const urlParams = new URLSearchParams(queryString);
    const alfa_id = urlParams.get('alfa_id');


    // alert('POINT A')

    // Analyse target url-nick depends on current url
    var curl = window.location.href;
    // Name of view equal to nick of url by default
    // var view_name = curl.split("/").pop().split("?")[0] 

    // целевая вьюха 
    var view_name = $(this).attr('target_view')


    
    $.ajax({
    url: view_name, // ссылка через ник-ссылки в urls.py
    type: "GET",
    data: {
        "ajax": "True",
        "srch_str" : $('#lib_categories_data_filter').val(), // получаем значение из <input>
        "alfa_id" : alfa_id,
    },
    
    //context: this, 
    success: (data) => {
        // alert(data)
        $('#lib_categories_ajax_container').html(data); // Вставить полученный с view html code for table to .div_container
    },

    error: (error) => {
        alert('AJAX JQERY ERROR:' + error);
    }
    });
});






// JS148^^  вывод на редактирование элемента списка категорий книг
// ПРИМ: Обе функции JS149^^ и  JS148^^ настроены на один и тот же метод и алгоритм.
$(document).ready(function(){

    // $( ".spn_class_js148" ).on( "click", function() {
    $('body').on('click','.spn_class_js148',function(){

        $("#second_edit_any_category").css({display:'block'});
        $('#second_add_new_category').css({display:'none'});

        var categ_id = $(this).attr('key_val_js148')

        // alert(categ_id)

        // id категории в скрытом поле
        $("#book_category_id").val(categ_id) 
        // Название выбраннйо категории
        $("#book_category").val($(this).html())

    });

});





// // JS149^^ Подгрузка вторичного модуля редактирования катгории в модуле редактирования, при нажатии на одну из ктаегорий или навигационный элемент в навигаторе
// https://stackoverflow.com/questions/17715274/jquery-click-function-doesnt-work-after-ajax-call - перегрузка элементов, которые имели
// event handler через AJAX. $('body') -> может быть любой статичный элемент на странице
// ПРИМ: Обе функции JS149^^ и  JS148^^ настроены на один и тот же метод и алгоритм.
$(document).ready(function(){
    $('body').on('click','.spn_class_js149', function(){


        $("#second_edit_any_category").css({display:'block'});
        $('#second_add_new_category').css({display:'none'});


        var categ_id = $(this).attr('key_val_js149')

        // alert(categ_id)

        // id категории в скрытом поле
        $("#book_category_id").val(categ_id) 
        // Название выбраннйо категории
        $("#book_category").val($(this).html())

    });
});




// JS150^^ - Очистить фильтр категорий в модуле редактирования категорий и на стра редактирования категорий книги


$(document).ready(function(){
    $("#categ_filter_clear").click(function () {
        
        $("#lib_categories_data_filter").val(''); 
        $("#lib_categories_data_filter").trigger("input")

    });
});





// JS151^^ - В списке категорий в модуле редактирования категорий или в модуле редактирования категорий книги
// сделать  unchecked всем выбранным элементам
$(document).ready(function(){
    $('#categ_checkboxes_clear').click(function () { 
    $('.checkboxb_js149, .checkboxb_js148').each( 
        function (index, checkbox) { 
            if (index != 0) { 
                checkbox.checked = false; 
            } 
        }); 
    });
});






// JS152^^ - скрыть суб-блок для редактиоования одной выбранной категории с  id="second_edit_any_category"
// Высветить суб-блок с добавлением новой категории с id="second_add_new_category" 


$(document).ready(function(){
    $('#create_new_category').click(function () { 

        $("#second_edit_any_category").css({display:'none'});
        $('#second_add_new_category').css({display:'block'});

    });
});





// JS153^^ - Создать новую категорию в табл lib_categories и вывести обновленный список категорий на страницу

$(document).ready(function(){

    $("#butt_create_new_categ_JS153").click(function () {
        
        var new_category = $("#new_category_JS153").val()

        var answer = window.confirm("PR_B359 --> Сейчас будет создана новая категория: " + new_category + ". Вы хотите создать новую категорию?");
        if (answer) {

                // Get url attr value
                const queryString = window.location.search;
                const urlParams = new URLSearchParams(queryString);
                const alfa_id = urlParams.get('alfa_id');
                    
                // параметры для передачи через AJAX POST
                var sendData = { 
                    new_category : new_category,
                    alfa_id : alfa_id,
                    };

                    // alert(sendData)

                $.get("add_new_lib_category", sendData) // Передача данных через AJAX (этот оператор - синоним .ajax )

                .done(function(data) {

                    alert('SYS LOG: Категория создана')

                    $('#lib_categories_ajax_container').html(data)

                })

                .fail(function() {

                    alert('AJAX FAIL')

                });

            }

    });

});







// JS154^^ - Удалить выбранные категории в модуле редактирования категорий 

$(document).ready(function(){

    $("#execute_btn_va001").click(function () {
        
        var chosen_chbox_data = [];
        $(".chb_mssg_execute_va001:checked").each(function(i) {

            // chosen_chbox_values.push($(this).val());
            var mssg_tbid = $(this).val()

            chosen_chbox_data.push(mssg_tbid);

        });

        var execute_type = $("#choose_execute_va001").val()

        // alert(execute_type)

        // параметры для передачи через AJAX POST
        var sendData = { 
            chosen_chbox_data : JSON.stringify(chosen_chbox_data),
            execute_type: execute_type, 
            };

            // alert(sendData)

        $.post("execute_proccessing_of_error_messages", sendData) // Передача данных через AJAX (этот оператор - синоним .ajax )

        .done(function() {
            // url = window.location.href
            // window.open(url, "_self"); // перезагрузить страницу для проверки фиксации статусов в БД
        })

        .fail(function() {

            alert('AJAX FAIL')

        });

    });

});





// JS155^^ - вывод на редактирование автора при нажатии на его ФИО в блоке редактирования авторов
// делегируем eventhandler to body, так как список с авторами может ajax-перегружаться

$(document).ready(function(){
    $('body').on('click','.edit_li_chbox_author_fio', function(){


        $('#second_add_new_author').css({display:'none'});
        $("#second_edit_any_author").css({display:'block'});

        var firstn = $(this).attr('firstn') // атрибут с данными по имени автора в текущем элементе checkbox
        var scndn = $(this).attr('scndn') // фамилия автора
        var auth_id = $(this).attr('auth_id') // id автора в таблице регистрации автора

        // alert(auth_id)

        // присваиваем значения в редактируемые поля, а так же в hidden поле
        $('#author_id').val(auth_id); 
        $('#author_first_name').val(firstn);
        $('#author_second_name').val(scndn);


    });
});






// JS156^^ - Высветить подраздел добавки нового автора в блоке редактирования авторов
// templates/telegram_monitor/lib_edit/book_edit_page.html
//  


$(document).ready(function(){
    $('#btn_create_new_author').click(function () { 

        $("#second_edit_any_author").css({display:'none'});
        $('#second_add_new_author').css({display:'block'});

    });
});





// JS157^^ - Добавить нового автора в библиотеку в табл lib_authors в блоке редактирования авторов книг 

$(document).ready(function(){

    $("#add_new_author_butt").click(function () {
        



    var auth_first_name = $("#new_author_first_name").val()
    var auth_second_name = $("#new_author_second_name").val()

    var answer = window.confirm("PR_B402 --> Сейчас в библиотеку будет добавлен новый автор: \n" + auth_second_name + " " + auth_first_name +  " \nВы хотите добавить нового автора?");
    if (answer) {

        // alert(execute_type)

        // параметры для передачи через AJAX POST
        var sendData = { 
            auth_first_name : auth_first_name,
            auth_second_name: auth_second_name, 
            };

            // alert(sendData)

        $.get("add_new_lib_author", sendData) // Передача данных через AJAX (этот оператор - синоним .ajax )

        .done(function() {
            // url = window.location.href
            // window.open(url, "_self"); // перезагрузить страницу для проверки фиксации статусов в БД

                 // выполняем еще один ajax запрос внутри первого ajax - обновить список авторов в модуле редактирвоания get_html_checkboxes_authors_list_block_ajax
                // Get url attr value  
                const queryString = window.location.search;
                const urlParams = new URLSearchParams(queryString);
                const alfa_id = urlParams.get('alfa_id'); // html-фтрибут в url браузера alfa_id
            
                // Обновление списка ul на странице
                $.get( 
                    {
                        url: "get_html_checkboxes_authors_list_block_ajax" ,
                        data: {
                            "alfa_id" : alfa_id, // html-атрибут при запросе а модуль  url
                        },
                    }
                )

                .done(function(data) {
                    $('#authors_container').html(data)

                });

        })

        .fail(function() {

            alert('PR_B387 --> JS157^^: AJAX FAIL')

        });

    } // if (answer) {

    });

});







// JS158^^ - Удалить выбранных авторов в модуле редактирования общего списка авторов  и перезагрузить список обновленных авторов 
// в библиотеке

$(document).ready(function(){

    $("#delete_chosen_lib_authors").click(function () {

        // alert("#delete_chosen_lib_authors")
        
        var chosen_author_tbids = [];
        $(".chb_book_authors:checked").each(function(i) {

            // id автора в табл 'lib_authors'
            var author_tbid = $(this).val()

            chosen_author_tbids.push(author_tbid);

        });


        
        // alert(execute_type)
        var chosen_author_tbids_strfy = JSON.stringify(chosen_author_tbids)

        // параметры для передачи через AJAX POST
        var sendData = { 
            chosen_author_tbids_del : chosen_author_tbids_strfy,
            //execute_type: execute_type, 
            };


        var answer = window.confirm("PR_B403 --> Сейчас  из библиотеки будут удалены авторы с tbids: \n" + chosen_author_tbids_strfy +  " \nВы хотите удалить этих авторов?");
        if (answer) {

                // alert(chosen_author_tbids)

            $.post("delete_chosen_authors_from_lib", sendData) // Передача данных через AJAX (этот оператор - синоним .ajax )

                .done(function() {
                    // url = window.location.href
                    // window.open(url, "_self"); // перезагрузить страницу для проверки фиксации статусов в БД


                    // Обновление списка ul на странице
                    $.get( 
                        {
                            url: "get_html_checkboxes_authors_list_block_ajax" ,
                            data: {},
                        }
                    )

                    .done(function(data) {
                        $('#authors_container').html(data)

                    });



                })

                .fail(function() {

                    alert('PR_B392 --> JS158: AJAX FAIL')

                });

        }

    });

});




// JS160^^ - Высветить блок добавления нового диктора в библиотеке в модуле редактирования дикторов

$(document).ready(function(){

    $("#btn_add_new_lib_narrator").click(function () {
        
    // alert('btn_add_new_lib_narrator')

    $("#second_edit_any_narrator").css({display:'none'});
    $('#second_add_new_narrator').css({display:'block'});



    });

});




// JS161^^ - добавить нового диктора в библиотеке в модуле редактирования дикторов
$(document).ready(function(){

    $("#add_new_narrator_butt").click(function () {
        
        var new_narrator_first_name = $("#new_narrator_first_name").val()
        var new_narrator_second_name = $("#new_narrator_second_name").val()

        // параметры для передачи через AJAX POST
        var sendData = { 
            narrator_first_name : new_narrator_first_name,
            narrator_second_name: new_narrator_second_name, 
            };

            $.get("add_new_lib_narrator", sendData) // Передача данных через AJAX (этот оператор - синоним .ajax )

            .done(function() {

                // alert('AJAX JS161^^ add_new_lib_narrator -> DONE');

                // выполняем еще один ajax запрос внутри первого ajax - обновить список дикторов в модуле редактирвоания get_html_checkboxes_authors_list_block_ajax
                // Get url attr value  
                const queryString = window.location.search;
                const urlParams = new URLSearchParams(queryString);
                const alfa_id = urlParams.get('alfa_id'); // html-фтрибут в url браузера alfa_id
                
                // Обновление списка ul на странице
                $.get( 
                    {
                        url: "get_html_checkboxes_narrators_list_block_ajax" ,
                        data: {
                            "alfa_id" : alfa_id, // html-атрибут при запросе а модуль  url
                        },
                    }
                )

                .done(function(data) {
                    // alert('SECOND AJAX Обновление списка')
                    $('#narrators_container').html(data)

                })

                .fail (function(data) {
                    alert('SECOND AJAX Обновление списка дикторов WRONG !!!!')
                    
                });
    
            })
    
            .fail(function() {
    
                alert('PR_B387 --> JS161^^: AJAX FAIL')
    
            });
    
    });

});








// JS162^^ - Высветить блок редактирования диктора и вставить его данные , при нажатии на его ФИО

// class span - spn_li_narrator


$(document).ready(function(){

    $('body').on('click','.spn_li_narrator', function(){

    // alert('spn_li_narrator')

    $("#second_add_new_narrator").css({display:'none'});
    $('#second_edit_any_narrator').css({display:'block'});

    
    // Значения текущих парметров диктора из спана с ФИО 
    var curr_narr_first_name = $(this).attr('firstn')
    var curr_narr_second_name = $(this).attr('scndn')
    var narrator_tbid = $(this).attr('narrator_tbid')

    // alert(narrator_tbid)

    // Присвоить значения в поля редактирования диктора, включая скрытое поле с tbid
    $('#narrator_first_name').val(curr_narr_first_name)
    $('#narrator_second_name').val(curr_narr_second_name)
    $('#narrator_id').val(narrator_tbid)

    
    });

});




// JS163^^ - Сохранить изменения в редактируемом дикторе в модуле редактирования дикторов 
// (как по заданной книге, так и в общем редакторе)

$(document).ready(function(){

    $("#btn_save_edited_narrator").click(function () {

        // const queryString = window.location.search;
        // const urlParams = new URLSearchParams(queryString);
        // const alfa_id = urlParams.get('alfa_id');

        // Данные в редактируемых полях  input в блоке редактирования дикторв
        var narrator_first_name = $('#narrator_first_name').val()
        var narrator_second_name = $('#narrator_second_name').val()
        var narrator_tbid = $('#narrator_id').val()

        // alert('PR_B418 --> narrator_tbid = ' + narrator_tbid)

        $.get( 
            {
                url: "update_edited_narrator" ,
                data: {
                    // "alfa_id" : alfa_id, // html-атрибут при запросе а модуль  url
                    'narrator_first_name' : narrator_first_name,
                    'narrator_second_name' : narrator_second_name,
                    'narrator_tbid' : narrator_tbid,
                },
            }
        )

        .done(function(data) {

                // Обновление списка ul на странице
                $.get( 
                    {
                        url: "get_html_checkboxes_narrators_list_block_ajax" ,
                        data: {
                            // "alfa_id" : alfa_id, // html-атрибут при запросе а модуль  url
                        },
                    }
                )

                .done(function(data) {
                    // alert('SECOND AJAX Обновление списка')
                    $('#narrators_container').html(data)

                })

                .fail (function(data) {
                    alert('PR_B440 JS163^^ -> SECOND AJAX Обновление списка дикторов WRONG !!!!')
                    
                }); //  $.get( 
                // END Обновление списка ul на странице

        })

        .fail(function(data) {
            alert("PR_B419 --> AJAX JS163^^ went WRONG!!!");
        });


        

    });

});











// JS164^^ - Сохранение выбора дикторов по книге





$(document).ready(function(){

    $("#btn_save_book_chosen_narrator").click(function () {


        var data = [];
        $(".chb_book_narrators:checked").each(function(i) {
            data.push($(this).val());
            // alert($(this).val())
        });

        var chkd_narrators_ids = JSON.stringify(data)

        // alert(chkd_narrators_ids)


        const queryString = window.location.search;
        const urlParams = new URLSearchParams(queryString);
        const alfa_id = urlParams.get('alfa_id');



        $.post("save_book_narrators_choosen", {chkd_narrators_ids : chkd_narrators_ids, alfa_id:alfa_id}) // Передача данных через AJAX (этот оператор - синоним .ajax )

        .done(function() {

                // Обновление списка ul на странице
                $.get("get_html_checkboxes_narrators_list_block_ajax", sendData) 

                .done(function(data) { //Выполнить при успешном выполнении ajax запроса
                    // alert( data2);
                    $('#narrators_container').html(data)
                })
        
                .fail(function(data) { //Выполнить при успешном выполнении ajax запроса
                    alert('JS164^^ -> ajax fail');
                });
                // END Обновление списка ul на странице


        })

        .fail(function() {

            alert('PR_B438 JS164^^ -> AJAX FAIL')

        })

    });

});









// JS165^^ - операции при нажатии на название источника в модлуе присвоения репозиториев источнику 

$(document).ready(function(){


    $(".spn_li_orig_source").on("click", function() {

        var curr_orig_source_id = $(this).attr('orig_source_id')
        var curr_orig_source_name = $(this).html()

        // 1. Присвоить параметры текущего источника тэгу с id="current_source" 
        $("#current_source").attr("curr_source_id", curr_orig_source_id)

        // 2. вывести название источника в заголовок текущего источника
        $("#current_source").html(curr_orig_source_name)


        // 3. AJAX - Обновление списка репозиториев, присвоенных данному источнику с выбранными репозиториями как checked
        var send_data = {
            orig_source_id : curr_orig_source_id,
            'ajax' : 'True',
        }
        
        $.get("set_source_repositories_editor", send_data) // Передача данных через AJAX (этот оператор - синоним .ajax )

            .done(function(data) {

                // 4. Обновить список ul для репозиториев с checked значениями, которы еприсвоены данному источнику
                $('#repositories_container').html(data)

            })

            .fail(function() {

                alert('PR_B463 JS165^^ -> AJAX FAIL')

            })


    });

});






// JS166^^ - Сохранить выбор репозиториев для текущего источника в табл 'lib_sources_assigned_repositories'
$(document).ready(function(){


    $("#save_source_repository_options").on("click", function() {

        var answer = window.confirm("PR_B467 --> Сейчас будут сохранены выборы по checkboxes репозиториев для заданного источника: \n" + " \nВы хотите сохранить выборы репозториев для текущего источника?");
        if (answer) {

            // 1. Снять данные текущего источника из тэга с id="current_source" 
            var curr_orig_source_id = $('#current_source').attr('curr_source_id')

            // 2. Считать все выбранные чекбоксы репозиториев в массив
            var checkedRepositors = [];
            $(".chb_assigned_repositories:checked").each(function(i) {
                checkedRepositors.push($(this).val());
                // alert($(this).val())
            });

            var checked_reposit_ids = JSON.stringify(checkedRepositors)

            // alert(checked_reposit_ids)

            // 3. Отправить данные в View: save_choosen_repositories_for_orig_source

            var send_data = {
                checked_reposit_ids : checked_reposit_ids, 
                curr_orig_source_id : curr_orig_source_id
            }

            $.post("save_choosen_repositories_for_orig_source", send_data) // Передача данных через AJAX (этот оператор - синоним .ajax )

                .done(function() {


                })

                .fail(function() {

                    alert('PR_B453 JS166^^ -> AJAX FAIL')

                })

        } // if (answer) {

    });

});








// JS168^^ - Высветить редактирование книги по целевым репозиториям
$(document).ready(function(){


    $("#show_book_target_repositories_editor").on("click", function() {

        // alert()

        const queryString = window.location.search;
        const urlParams = new URLSearchParams(queryString);
        const alfa_id = urlParams.get('alfa_id');



            $(".attr_editor").css({display:'none'});
            $('#book_assigned_repositories_editor').css({display:'block'});

            send_data = {
                alfa_id : alfa_id,
                ajax : 'True',
            }

            $.get("set_lib_book_repositories_editor", send_data) // Передача данных через AJAX (этот оператор - синоним .ajax )

                .done(function(ret_data) {

                    
                    // alert('GOOD!')

                    $("#repositories_container").html(ret_data)

                })

                .fail(function() {

                    alert('PR_B487 JS168^^ -> AJAX FAIL')

                })



    });

});










// JS169^^ - Сохранить выбор целевых репозиториев для заданнйо книги
$(document).ready(function(){


    $("#save_book_repositories_options").on("click", function() {

        // alert()

        const queryString = window.location.search;
        const urlParams = new URLSearchParams(queryString);
        const alfa_id = urlParams.get('alfa_id');

        var answer = window.confirm("PR_B498 JS169^^ --> Сейчас будут сохранены выборы по checkboxes репозиториев для заданной книги с bookAlfaId = " + alfa_id + " \nВы хотите сохранить выборы репозториев для данной книги?");
        if (answer) {

        // Считать все выбранные чекбоксы репозиториев в массив
        var checkedRepositors = [];
        $(".chb_assigned_repositories:checked").each(function(i) {
            checkedRepositors.push($(this).val());
            // alert($(this).val())
        });

        var checked_reposit_ids = JSON.stringify(checkedRepositors)


        send_data = {
            alfa_id : alfa_id,
            ajax : 'True',
            checked_reposit_ids : checked_reposit_ids,
        }

        $.post("save_choosen_repositories_for_lib_book", send_data) // Передача данных через AJAX (этот оператор - синоним .ajax )

            .done(function() {

                
                // alert('GOOD!')


            })

            .fail(function() {

                alert('PR_B488 JS169^^ -> AJAX FAIL')

            })

        } //if (answer) {

    });

});




















