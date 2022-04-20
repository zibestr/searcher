# NotYandex Search Engine
## Краткое описание
Поисковой движок позволяет осуществлять поиск 
по контенту сайта, и легко встраивается в ваш сайт/web приложение.
## Установка
Для работы приложения требуется Python 3.9+.  
После клонирования репозитория установите все необходимые модули и библиотеки:
```
    pip install -r requirements.txt
```
Для запуска приложения на Windows используйте:
```
    python main.py
```
MacOS и Linux:
```
    python3 main.py
```
## Модули движка
### Парсер
В движок встроен парсер, который ищет все возможные ссылки на сайте, 
и анализирует их на принадлежность к заданному сайту, не используя внешние ссылки.
Также в репозитории есть файл robots.txt, в который можно добавить, 
или убрать ссылки на страницы сайта.
### Перевернутый Индекс
Это часть приложения является самой главное и позволяет проиндексировать
содержимое найденных страниц сайта и составить перевернутый индекс.
### Обработчик запросов
Для запросов может использоваться как простая словесная форма, так и 
разработанный нашей командой язык запросов. **Подробнее в [документации](docs/index.md)**.  

Этот же модуль осуществляет ранжирование результатов поиска. 
По умолчанию используеутся алгоритм, основанный на TF*IDF 
коэффициенте и учитывающий глубину ссылки 
(чем длиннее путь к файлу, тем ниже будет ранг ссылки, при прочих 
одинаковых факторах). **Подробнее в [документации](docs/index.md)**.

## Документация
### Пользовательская документация
#### Основы
После запуска приложения активируется веб-клиент на порте 5000, 
к которому можно обращаться с помощью API.  
##### Обращение к обработчику запросов
GET запрос по адресу `/api/search/<query>` возвращает результаты поиска
по запросу query в формате json:
```
[
    {
        "title": "Название страницы",
        "text": "Краткое описание страницы",
        "href": '"Ссылка на страницу'"
    },
]
```
При первом запросе на заданном url будет запускаться индексирование сайта,
которые может занять большое количество времени (по несколько минут 
на страницу, в зависимости от количества текста на ней). После индексирования
сайта индекс сохраняется в json формате в [saved indexes](engine/saved%20indexes).
##### Изменение url сайта
POST запрос по адресу `/api/change` с параметром new_url меняет url 
обрабатываемого сайта и возвращает сообщение об успешном/неуспешном 
выполнении запроса в формате json:
```
{
    "message": "Error"
}
```
Или:
```
{
    "message": "Successful"
}
```
#### robots.txt
В файле [robots.txt](engine/robots.txt) можно добавлять url страниц, 
которые нужно проигнорировать или наоборот учесть при поиске.  
Синтаксис файла robots.txt прост:  
- для добавления сайта в исключение используйте:
```
- url
```
- для добавления сайта в дополнительный список:
```
+ url
```
#### Стоп слова
В файле [stop_words.txt](engine/stop_words.txt) лежат стоп слова,
которые игнорируются индексом и обработчиком запросов.  
Чтобы добавить слово, достаточно записать его в файл.
### Язык запросов
#### Правила составления запросов
Поисковик работает только в одном из двух режимах: поиск по фразам и 
продвинутый поиск.
Поиск по фразам активируется при обычном обращение к поисковику, то есть
когда на обработчик подана простая фраза, например: купить утку.  
А продвинутый поиск активируется при соблюдение особого синтаксиса. Если
в поисковом запросе встречаются символы "{" и "}", он переходит в 
сложный режим.  
Сложный запрос делится на части проблелом, а части запроса заключаются в
фигурные скобки. Внутри частей запроса между словами стоят 
спец. символы без пробелов, которые отвечают за вид запроса. Внутри одной 
части запроса могут быть только один вид запроса 
(один и тот же спец. символ).  
Пример запроса:
```
{солнце&луч} {ель|сосна} {!дом}
```
#### Виды запросов
##### Запрос И
Запрос И записывается через символ '&' и ищет страницы, которые содержат
одновременно заданные слова. Запрос может содержать сразу несколько слов. 
Например, запрос: 
```
{участок&земля&площадь&арендовать}
```
Покажет только страницы, на которых есть слова участок, земля, 
площадь и арендовать в любом падеже и форме.
##### Запрос ИЛИ
Запрос ИЛИ записывается через символ '|' и ищет страницы, которые содержат 
хотя бы одно из заданных слов. Запрос может содержать сразу несколько слов.
Например, запрос:
```
{палатка|тент}
```
Покажет только страницы, на которых есть слова палатка или тент
в любом падеже и форме.
##### Запрос НЕТ
Запрос НЕТ записывается через символ '!' и ищет страницы, которые не содержат
заданное слово. Запрос может содержать только одно слово,
но отдельных запросов может быть несколько.
Например, запрос:
```
{!налог}
```
Покажет только страницы, на которых нет слова налог в любом падеже и форме.
### Документация по исходному коду
:point_right: [Ссылка](docs/index.md)