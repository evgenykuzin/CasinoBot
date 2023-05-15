docker stop jopsbank
docker rm jopsbank
docker rmi jopsbank-bot
docker rmi cr.yandex/crpmuk69odu46tddhh7q/jekajops21/jopsbank:1.1
docker-compose down --remove-orphans
docker-compose up -d
docker start jopsbank
docker tag jopsbank-bot cr.yandex/crpmuk69odu46tddhh7q/jekajops21/jopsbank:1.1
docker rmi jopsbank-bot
docker run cr.yandex/crpmuk69odu46tddhh7q/jekajops21/jopsbank:1.1