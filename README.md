# derivative
### Авторы: Шамугия Давид, Филимонова Ирина
### Задача по Python. 4 семестр КН Матмех УрФУ
Вход: функция одной переменной, записанная в математической форме
###### (т.е. знаки некоторых операций могут отсутствовать).

Выход: Указание ошибки в записи, если таковая присутствовала, иначе производная от заданной функции.

## Пакет functions

### operators
Модуль с классом `Operator`, описывающим операторы. Также модуль хранит словари с основными математическими операторами и константами.

### expr_parser
Модуль с классом `Parser`, умеющий преобразовывать математические выражения в ОПЗ (Обратная Польская Запись). Принимает в конструктор строковое представление математического выражения. Поле `rpn` экземпляра класса содержит массив с токенами ОПЗ. Также модуль имеет пару кастомных исключений для обработки ошибок, связанных с некорректным вводом математического выражения.

### function
Модуль с классом `Function`, предоставляющий разный функционал для работы с математическими функциями. Принимает в конструктор строковое представление математического выражения. Далее это строковое представление переписывается в ОПЗ, по которому строится AST (Абстрактное синтаксическое дерево).
#### Методы класса `Function`
+ `validate_function(**values)` - Проверяет функцию на запрещенные операции, например деление на ноль в заданной точке. Точка может быть указана не полностью.
+ `simplify()` - Возвращает упрощенную функцию
+ `calculate(**values)` - Считает значение функции в заданной точке. Возвращает функцию. Точка может быть указана не полностью.
+ `derive(variable: str, **values)` - Вычисляет производную функции по заданной переменной и в заданной точке
+ `diff(variable: str)` - Находит производную функции по заданной переменной
