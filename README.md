Приложение справшивает нужные параметры и выгружает данные либо в csv, либо в базу данных Postgres. Я тестировал подключение к бд через контейнер postgres запущенный с такими параметрами
docker run --name my-postgres \
  -e POSTGRES_USER=admin \
  -e POSTGRES_PASSWORD=password \
  -e POSTGRES_DB=db \
  -p 5432:5432 \
  -v pgdata:/var/lib/postgresql/data \
  -d postgres:latest
Можно вводить разыне даты, будет выгружать этот интервал
