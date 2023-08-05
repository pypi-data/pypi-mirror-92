$.i18n().load({
    "sr-Cyrl": {
        "msg_activecode_error_title": "Грешка",
        "msg_activecode_description_title": "Опис",
        "msg_activecode_to_fix_title": "Да исправите",
        "msg_activecode_load_history": "Учитај историју",
        "msg_activecode_audio_tour": "Аудио тура",
        "msg_activecode_loaded_code": "Ваш изворни код је учитан.",
        "msg_activecode_no_saved_code": "Не постоји сачуван код.",
        "msg_activecode_run_code": "Покрени програм",
        "msg_activecode_show_feedback": "Прикажи резултат",
        "msg_activecode_show_code": "Прикажи код",
        "msg_activecode_hide_code": "Затвори код",
        "msg_activecode_show_codelens": "Корак по корак",
        "msg_activecode_show_in_codelens": "Корак по корак",
        "msg_activecode_hide_codelens": "Затвори режим корак по корак",
        "msg_activecode_play_task": "Прикажи пример",
        "msg_activecode_help": "Прикажи помоћ",
        "msg_activecode_copy": "Ископирај",

        "msg_activecode_parse_error": "Синтаксна грешка (грешка у парсирању) значи да Пајтон не разуме синтаксу у линији на коју порука о грешци указује. Типични примери овакве грешке су заборављена двотачка код 'if' или 'for' наредбе или заборављена запета између аргумената код позива функције",
        "msg_activecode_parse_error_fix": "Да бисте исправили синтаксну грешку треба пажљиво да погледате линију вашег програма на коју указује порука о грешци и можда претходну линину вашег програма. Проверите да ли су поштована сва правила синтаксе Пајтона.",
        "msg_activecode_type_error": "Грешка у типу најчешће настаје када се у изразу покуша комбиновање два објекта чији типови се не могу комбиновати. На пример степеновање стринга",
        "msg_activecode_type_error_fix": "Да бисте исправили грешку у типу највероватније треба да прођете кроз свој програм и уверите се да променљиве имају типове које очекујете од њих. Може бити корисно да одштампате сваку променљиву тако да будете сигурни да су њихове вредности онакве какве мислите да јесу.",
        "msg_activecode_name_error": "Грешка у имену скоро увек значи да сте користили променљиву пре него што је она добила вредност. Често је то једноставна словна грешка, па пажљиво проверите да ли сте тачно написали име.",
        "msg_activecode_name_error_fix": "Проверите десне стране наредби доделе вредности и позиве ваших функција, ово је највероватније место за проналажење грешака у имену.",
        "msg_activecode_value_error": "Грешка у вредности се најчешће јавља када проследите параметар функцији а функција на том месту очекује други тип вредности.",
        "msg_activecode_value_error_fix": "Порука о грешци вам даје прилично добар савет о имену функције као и вредности која није одговарајућа. Пажљиво погледајте поруку о грешци и вратите се на променљиву која садржи проблематичну вредност.",
        "msg_activecode_attribute_error": "Ова порука о грешци вам говори да објекат са леве стране тачке нема атрибут или метод са десне стране.",
        "msg_activecode_attribute_error_fix": "Најчешћа варијанта ове поруке је да објекат 'undefined' нема атрибут 'X'. То вам говори да објекат са леве стране тачке није оно што мислите. Пратите вредности променљиве уназад и одштампајте их на различитим местима док не откријете где постаје 'undefined'. Такође проверите да је тачно написан назив атрибута са десне стране тачке.",
        "msg_activecode_token_error": "Ова грешка најчешће указује на то да сте заборавили десну заграду или сте заборавили да затворите наводнике.",
        "msg_activecode_token_error_fix": "Проверите сваку линију свог програма и уверите се да су ваше заграде и наводници упарени.",
        "msg_activecode_time_limit_error": "Ваш програм ради предуго. Програми се обично изврше за мање од 10 секунди. Ово указује да је ваш програм можда у бесконачној петљи. ",
        "msg_activecode_time_limit_error_fix": "Додајте неке наредбе за штампање да бисте утврдили да ли је ваш програм у бесконачној петљи. Ако није, можете повећати време извршавања са sys.setExecutionLimit(msecs)",
        "msg_activecode_general_error": "Ваш програм ради предуго. Програми се обично изврше за мање од 30 секунди. То указује да је ваш програм вероватно у бесконачној петљи.",
        "msg_activecode_general_error_fix": "Додајте неке наредбе за штампање да бисте утврдили да ли је ваш програм у бесконачној петљи. Ако није, можете повећати време извршавања са sys.setExecutionLimit(msecs)",
        "msg_activecode_syntax_error": "Ова порука указује да Пајтон не може да схвати синтаксу одређене наредбе. Неки примери су додела вредности константи (литералу) или позиву функције",
        "msg_activecode_syntax_error_fix": "Проверите ваше наредбе доделе вредности и уверите се да је лева страна доделе променљива, а не функција или константа (литерал).",
        "msg_activecode_index_error": "Ова порука значи да покушавате да приступите елементу ван граница листе или ниске (стринга). На пример, ако ваша листа садржи 3 елемента и покушате да приступите елементу на позицији 3 или већој.",
        "msg_activecode_index_error_fix": "Ова порука се понекад појављује зато што сте промашили за један. Запамтите да је први елемент у листи или нисци (стрингу) на позицији 0. У листи дужине 3 последњи исправан индекс је 2",
        "msg_activecode_uri_error": "",
        "msg_activecode_uri_error_fix": "",
        "msg_activecode_import_error": "Ова порука о грешци указује да покушавате да увезете модул који не постоји (наредба import)",
        "msg_activecode_import_error_fix": "Проблем може бити у томе да сте погрешно написали назив модула. Може се десити и да покушавате да увезете модул који постоји у 'правом' Пајтону, али не постоји овде. Ако је то случај, пошаљите захтев за додавање модула.",
        "msg_activecode_reference_error": "Ово је највероватније интерна грешка, посебно ако порука помиње конзолу.",
        "msg_activecode_reference_error_fix": "Покушајте да освежите веб страницу и ако грешка и даље постоји, пошаљите извештај о грешци заједно са својим програмом",
        "msg_activecode_zero_division_error": "Ово вам говори да покушавате да делите нулом. Вероватно вредност променљиве у имениоцу израза дељења има вредност 0",
        "msg_activecode_zero_division_error_fix": "Можда је потребно да пре дељења додате у програм проверу помоћу if наредбе да именилац није 0, или треба да преиспитате своје претпоставке о дозвољеним вредностима променљивих, можда је нека претходна наредба неочекивано доделила вредност нула дотичној променљивој.",
        "msg_activecode_range_error": "Прекорачена је највећа дозвољена величина стека позива (call stack).",
        "msg_activecode_range_error_fix": "Веома је вероватно да нисте намеравали да заузмете толики простор на стеку позива. Прекорачење стека се обично дешава када функција неконтролисано позива саму себе. Ако сте у поглављу о рекурзији, проверите да ли сте добро идентификовали основни случај.",
        "msg_activecode_internal_error": "Интерна грешка може значити да сте нашли баг у нашем Пајтону",
        "msg_activecode_internal_error_fix": "Пријавите ову грешку заједно са својим програмом као баг.",
        "msg_activecode_indentation_error": "Ова грешка настаје када нисте исправно увукли наредбе (лоша индентација). Ово се најчешће дешава као део if, for, while или def наредбе.",
        "msg_activecode_indentation_error_fix": "Проверите ваше if, for, while и def наредбе да бисте били сигурни да су линије испод њих исправно увучене. Други начин да добијете ову поруку је ако при копирању и лепљењу кода случајно оставите неке делове кода тамо где више не припадају.",
        "msg_activecode_not_implemented_error": "Ова грешка настаје када покушате да користите уграђену функцију Пајтона која није имплементирана у овој верзији Пајтона у прегледачу.",
        "msg_activecode_not_implemented_error_fix": "За сада је једини начин да се ово поправи да не користите функцију. Можда постоје заобилазнице. Ако вам је заиста потребна ова уграђена функција, онда пријавите грешку и реците нам како покушавате да користите функцију.",

        "msg_activecode_file_not_found": "Фајл није пронађен: '$1'",
        "msg_activecode_no_file_or_dir": "[Errno 2] Нема таквог фајла или директоријума: '$1'",
        "msg_activecode_starting": "Кликните дугме 'покрени' да започнете $1",
        "msg_activecode_playing": "Покрећем $1",
        "msg_activecode_loading_audio": "Учитавам аудио. Молим сачекајте. Ако тура не почне ускоро кликните на 'Заустави туру' и покушајте поново.",
        "msg_activecode_pause_current_audio": "Паузирајте текући аудио",
        "msg_activecode_pause_audio": "Паузирајте аудио",
        "msg_activecode_play_paused_audio": "Покрените паузирани аудио",
        "msg_activecode_audio_paused": "$1 је паузиран. Кликните на дугме 'покрени' да наставите туру.",
        "msg_activecode_input_prg": "Улаз за програм",
        "msg_activecode_were_compiling_err": "Дошло је до грешака при компајлирању вашег кода. Погледајте ниже",
        "msg_activecode_time_limit_exc": "Прекорачено је време за ваш програм",
        "msg_activecode_server_err": "Дошло је до грешке на серверу: $1 $2",
        "msg_activecode_compiling_running": "Компајлирам и покрећем ваш код...",
        "msg_activecode_server_comm_err": "Грешка у комуникацији са сервером.",
        "msg_activecode_save_run": "Покрени програм", //"Сачувај и покрени програм"
        "msg_activecode_reset": "Врати на почетак"
    }
});
