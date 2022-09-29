import pyupbit

access = "d"
secret = "d"
upbit = pyupbit.Upbit(access, secret)

my_balance = upbit.get_balances()
print(my_balance)
