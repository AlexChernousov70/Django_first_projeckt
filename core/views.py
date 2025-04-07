from django.shortcuts import render
from django.http import HttpResponse


masters = [
    {"id": 1, "name": "Эльдар 'Бритва' Рязанов"},
    {"id": 2, "name": "Зоя 'Ножницы' Космодемьянская"},
    {"id": 3, "name": "Борис 'Фен' Пастернак"},
    {"id": 4, "name": "Иннокентий 'Лак' Смоктуновский"},
    {"id": 5, "name": "Раиса 'Бигуди' Горбачёва"},
]

# Список возможных услуг барбершопа
services = [
    "Стрижка под 'Горшок'",
    "Укладка 'Взрыв на макаронной фабрике'",
    "Королевское бритье опасной бритвой",
    "Окрашивание 'Жизнь в розовом цвете'",
    "Мытье головы 'Душ впечатлений'",
    "Стрижка бороды 'Боярин'",
    "Массаж головы 'Озарение'",
    "Укладка 'Ветер в голове'",
    "Плетение косичек 'Викинг'",
    "Полировка лысины до блеска"
]

# Статусы заявок
STATUS_NEW = 'новая'
STATUS_CONFIRMED = 'подтвержденная'
STATUS_CANCELLED = 'отмененная'
STATUS_COMPLETED = 'выполненная'

# Тестовые данные заявок
orders = [
    {
        "id": 1,
        "client_name": "Пётр 'Безголовый' Головин",
        "services": ["Стрижка под 'Горшок'", "Полировка лысины до блеска"],
        "master_id": 1,
        "date": "2025-03-20",
        "status": STATUS_NEW
    },
    {
        "id": 2,
        "client_name": "Василий 'Кудрявый' Прямиков",
        "services": ["Укладка 'Взрыв на макаронной фабрике'"],
        "master_id": 2,
        "date": "2025-03-21",
        "status": STATUS_CONFIRMED
    },
    {
        "id": 3,
        "client_name": "Афанасий 'Бородач' Бритвенников",
        "services": ["Королевское бритье опасной бритвой", "Стрижка бороды 'Боярин'", "Массаж головы 'Озарение'"],
        "master_id": 3,
        "date": "2025-03-19",
        "status": STATUS_COMPLETED
    },
    {
        "id": 4,
        "client_name": "Зинаида 'Радуга' Красильникова",
        "services": ["Окрашивание 'Жизнь в розовом цвете'", "Укладка 'Ветер в голове'"],
        "master_id": 4,
        "date": "2025-03-22",
        "status": STATUS_CANCELLED
    },
    {
        "id": 5,
        "client_name": "Олег 'Викинг' Рюрикович",
        "services": ["Плетение косичек 'Викинг'", "Стрижка бороды 'Боярин'"],
        "master_id": 5,
        "date": "2025-03-23",
        "status": STATUS_NEW
    },
    {
        "id": 6,
        "client_name": "Геннадий 'Блестящий' Лысенко",
        "services": ["Полировка лысины до блеска", "Массаж головы 'Озарение'"],
        "master_id": 1,
        "date": "2025-03-24",
        "status": STATUS_CONFIRMED
    },
    {
        "id": 7,
        "client_name": "Марина 'Рапунцель' Косичкина",
        "services": ["Укладка 'Ветер в голове'", "Мытье головы 'Душ впечатлений'"],
        "master_id": 2,
        "date": "2025-03-25",
        "status": STATUS_CANCELLED
    },
    {
        "id": 8,
        "client_name": "Федор 'Кучерявый' Завитушкин",
        "services": ["Укладка 'Взрыв на макаронной фабрике'", "Массаж головы 'Озарение'", "Мытье головы 'Душ впечатлений'"],
        "master_id": 3,
        "date": "2025-03-26",
        "status": STATUS_COMPLETED
    },
    {
        "id": 9,
        "client_name": "Елизавета 'Корона' Царевна",
        "services": ["Королевское бритье опасной бритвой"],
        "master_id": 4,
        "date": "2025-03-27",
        "status": STATUS_NEW
    },
    {
        "id": 10,
        "client_name": "Добрыня 'Богатырь' Никитич",
        "services": ["Стрижка бороды 'Боярин'", "Плетение косичек 'Викинг'", "Массаж головы 'Озарение'"],
        "master_id": 5,
        "date": "2025-03-28",
        "status": STATUS_COMPLETED
    }
]

def landing(request):
    context = {
        'masters': masters,
        'services': services,
    }

    return render(request, 'landing.html', context)

def thanks(request):
    return render(request, 'thanks.html')

def orders_list(request):
    context = {
        'orders': orders
    }
    return render(request, 'orders_list.html', context)

def order_detail(request, order_id):
    try:
        order = [o for o in orders if o["id"] == order_id][0]
    except IndexError:
        # Если заказ не найден, возвращаем 404 - данные не найдены
        return HttpResponse(status=404)
    master_id = order["master_id"]
    master = next(m for m in masters if m["id"] == master_id)
    context = {"order": order, "master": master}
    return render(request, 'order_detail.html', context)