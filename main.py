from zeep import Client
import csv
from time import sleep


def print_info(client, account):
    """Prints the account information"""

    how_much_to_finish = client.service.howMuchToFinish(account)
    balance = client.service.balance(account)
    print("How much to finish:", how_much_to_finish)
    print("Balance:", balance)


def gather_data(client):
    """Gathers data from the server and writes it to a CSV file"""

    stocks = client.service.list()
    print("Stocks:", stocks)
    with open("stocks.csv", "w", newline="", encoding="utf-8") as csvfile:
        writer = csv.writer(csvfile)
        writer.writerow(stocks)
        while True:
            prices = []
            for stock in stocks:
                price = client.service.info(stock)
                prices.append(price)
            writer.writerow(prices)
            csvfile.flush()
            print("Prices:", prices)
            sleep(1)


def make_money(client, account):
    while True:
        balance = client.service.balance(account)
        cs_price = client.service.info("CS")

        # Buy at 500 or lower
        if cs_price <= 500:
            # Calculate how many shares to buy
            shares_to_buy = balance // cs_price
            if shares_to_buy > 0:
                print("Buying", shares_to_buy, "shares of CS")
                # Buy the shares
                client.service.buy(account, "CS", shares_to_buy)

        # Sell at 700 or higher
        if cs_price >= 700:
            # Calculate how many shares to sell (all of them)
            shares_to_sell = client.service.own(account, "CS")
            if shares_to_sell > 0:
                print("Selling", shares_to_sell, "shares of CS")
                client.service.sell(account, "CS", shares_to_sell)

        # Print account info
        print_info(client, account)
        sleep(1)


def main():
    client = Client("http://andromeda.fi.muni.cz/~xbatko/homework2?wsdl")

    # Create account
    # account = client.service.createAccount("567769@mail.muni.cz")
    account = "42e3c7c5-1bd6-4757-920f-48cd8a2685fd"
    print_info(client, account)

    # Uncomment the following line to gather data
    # gather_data(client)

    # Uncomment the following line to make money
    # make_money(client, account)


if __name__ == "__main__":
    main()
