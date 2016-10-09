
# Coursera

Данный скрипт:
* находит все репозитории на сайте [Курсер'ы][], случайнымобрабом выбирает из них 20 курсов;
* по каждому курсу вытгиваются: название, язык, дата начала, количество недель и средняя оценка;
* полученные данные сохраняются в XLSX-файл, имя файла можно задать через аргумент в консоли.

## Запуск

Введите в терминале:

    python3.5 coursera.py

## Зависимости

Скрипт написан на языке Python 3, поэтому требует его наличия.

Для выполнения скрипта должны быть установлены модули [requests][], [beautifulsoup4][], [openpyxl][].

## Поддержка

Если у вас возникли сложности или вопросы по использованию скрипта, создайте 
[обсуждение][] в данном репозитории или напишите на электронную почту 
<IvanovVI87@gmail.com>.

## Документация

Документацию к модулю requests можно получить по [ссылке1][].

Документацию к модулю beautifulsoup4 можно получить по [ссылке2][].

Документацию к модулю openpyxl можно получить по [ссылке3][].

[Курсер'ы]: https://www.coursera.org
[requests]: https://pypi.python.org/pypi/requests/2.11.1
[beautifulsoup4]: https://pypi.python.org/pypi/beautifulsoup4
[openpyxl]: https://pypi.python.org/pypi/openpyxl
[обсуждение]: https://github.com/santax666/10_coursera/issues
[ссылке1]: http://docs.python-requests.org/en/master/
[ссылке2]: https://www.crummy.com/software/BeautifulSoup/bs4/doc/
[ссылке3]: http://openpyxl.readthedocs.io/en/default/
