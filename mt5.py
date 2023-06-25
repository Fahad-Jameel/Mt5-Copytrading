import MetaTrader5 as mt5

def get_input():
    volume = float(input("Enter the volume for the order: "))
    set_profit_loss = input("Do you want to set profit and loss levels? (Y/N): ")
    if set_profit_loss.lower() == 'y':
        take_profit = float(input("Enter the take profit level: "))
        stop_loss = float(input("Enter the stop loss level: "))
    else:
        take_profit = 0
        stop_loss = 0
    symbol = input("Enter the currency symbol: ")
    
    return volume, take_profit, stop_loss, symbol

try:
    mt5.initialize()
except mt5.Error as e:
    print(f"MetaTrader5 initialization error: {e}")
    exit(1)

account_credentials = [
   
    # {'login': 98765432, 'password': 'password2', 'server': 'Server2'},
    # Add more accounts here if needed
]

for account in account_credentials:
    try:
        if not mt5.login(account['login'], account['password'], account['server']):
            print(f"Failed to connect to {account['server']} with login {account['login']}")
            continue
    except mt5.Error as e:
        print(f"Login error for {account['server']} with login {account['login']}: {e}")
        continue

    volume, take_profit, stop_loss, symbol = get_input()

    try:
        symbols = mt5.symbols_get()
        if not symbols:
            print(f"No symbols available for {account['server']} with login {account['login']}")
            mt5.shutdown()
            continue
    except mt5.Error as e:
        print(f"Symbol retrieval error for {account['server']} with login {account['login']}: {e}")
        mt5.shutdown()
        continue

    for symbol_info in symbols:
        if symbol_info.name != symbol:
            continue

        order_type = mt5.ORDER_TYPE_BUY if symbol_info.name.endswith('.BUY') else mt5.ORDER_TYPE_SELL

        if symbol_info.name.endswith('.BUY'):
            order_volume = volume * 0.5
        else:
            order_volume = volume

        request = {
            'action': mt5.TRADE_ACTION_DEAL,
            'symbol': symbol_info.name,
            'volume': order_volume,
            'type': order_type,
            'price': symbol_info.last,
            'sl': stop_loss,
            'tp': take_profit,
        }

        try:
            result = mt5.order_send(request)
            if result.retcode != mt5.TRADE_RETCODE_DONE:
                print(f"Failed to place order on {symbol_info.name} for {account['server']} with login {account['login']}")
        except mt5.Error as e:
            print(f"Order placement error for {symbol_info.name} on {account['server']} with login {account['login']}: {e}")

    try:
        mt5.logout()
    except mt5.Error as e:
        print(f"Logout error for {account['server']} with login {account['login']}: {e}")

try:
    mt5.shutdown()
except mt5.Error as e:
    print(f"MetaTrader5 shutdown error: {e}")
