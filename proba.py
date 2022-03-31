import datetime
data = datetime.datetime.today() - datetime.timedelta(1)
print(data.strftime('%Y-%m-%d %H.%M.%S'))