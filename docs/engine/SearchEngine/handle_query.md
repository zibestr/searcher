### def handle_query(self, text_query: str) -> list
Принимает текст запрос и обращается к обработчику запросов SearchQueryGenerator
для поиска по запросу. Возвращает список в формате:
```
[
    url1,
    url2,
    url3,
    ...
]
```