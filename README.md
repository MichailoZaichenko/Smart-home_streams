Написать приложение с двумя потоками

Поток №1
Отображается меню в консоли и ожидается ввод от пользователя. После ввода отображается подменю или выводится информация из файла. Для команд управления использовать Event для второго потока

Меню:
1. Температура/Влажность
    1.1 Текущая # последняя запись в файле
    1.2 Средняя # среднее 6 последних записей
2. Счетчики
    2.1 Электроенергия # показания счетчика, текущий расход
    2.2 Газ # показания счетчика, текущий расход
    2.3 Вода # показания счетчика, текущий расход
3. Котел
    3.1 Состояние # Включен/Выключен, температура, давление
    3.2 Включить # Команда на включение
    3.3 Выключить # Команда на выключение
4. Журнал # все записи из файла

Поток №2
Каждые 5 секунд отправляются GET запросы на сервер (ссылка позже на GitHub) и принимается ответ в видt JSON (формат в файле example.json).
Полученные данные с добавленным дата/время сохраняются в файле (любой формат файла). При возникновении Event отправляет запросы на сервер (ссылка позже на GitHub) 


