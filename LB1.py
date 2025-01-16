import requests
import matplotlib.pyplot as plt
from datetime import datetime, timedelta


def get_exchange_rates(start_date, end_date):
    base_url = "https://bank.gov.ua/NBUStatService/v1/statdirectory/exchange"
    date_format = "%Y%m%d"
    current_date = start_date
    rates = []

    while current_date <= end_date:
        date_str = current_date.strftime(date_format)
        url = f"{base_url}?date={date_str}&json"
        try:
            response = requests.get(url)
            response.raise_for_status()  # Перевіряє статус коду
            data = response.json()
            rates.append({"date": current_date.strftime("%Y-%m-%d"), "rates": data})
        except requests.exceptions.RequestException as e:
            print(f"Error fetching data for {date_str}: {e}")
        except ValueError:
            print(f"Invalid JSON response for {date_str}")

        current_date += timedelta(days=1)

    return rates


# Отримуємо курси за останній тиждень
end_date = datetime.today()
start_date = end_date - timedelta(days=7)
exchange_rates = get_exchange_rates(start_date, end_date)

for day in exchange_rates:
    print(f"Date: {day['date']}")
    for rate in day['rates']:
        if rate['cc'] in ['USD', 'EUR']:  # Наприклад, виводимо тільки USD і EUR
            print(f"Currency: {rate['cc']} | Rate: {rate['rate']:.2f}")


def plot_exchange_rates(exchange_rates, currency_codes):
    dates = []
    rates_dict = {code: [] for code in currency_codes}  # Словник для зберігання курсів для кожної валюти

    for day in exchange_rates:
        dates.append(day["date"])
        for rate in day["rates"]:
            if rate["cc"] in currency_codes:
                rates_dict[rate["cc"]].append(rate["rate"])

    plt.figure(figsize=(10, 5))

    # Побудова графіків для кожної валюти
    for code in currency_codes:
        plt.plot(dates, rates_dict[code], marker='o', label=code)

    plt.xlabel("Date")
    plt.ylabel("Exchange Rate (UAH)")
    plt.title("Exchange Rate Trend")
    plt.legend()
    plt.grid(True)
    plt.show()


# Виклик функції для побудови графіка для USD та EUR
plot_exchange_rates(exchange_rates, ["USD", "EUR"])
