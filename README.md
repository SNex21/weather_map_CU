# Как тестировали сервис и какие ошибки обработали

1) ввод разных языков: сервис умеет обрабатывать и русский и английский язык, из-за чего не возникает ошибок при вводе на разных языках
2) ввод некорректных данных, если данные не найдены, то сервис обработает ошибку и выдаст ее
3) ввод несуществующего города: если город не существует, сервис тоже обработает эту ситуацию и не сломается

Сервис обработает все ситуации и будет недопускать ошибок, разработчик может проверить ошибки, просмотрев терминал, где логируются :
- тип ошибки
- ответ от api
- ошибка от python

Так разработчик может контролировать сервис и вовремя исправлять ошибки
