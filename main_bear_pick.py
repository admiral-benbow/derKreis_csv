import pandas as pd


pd.set_option("display.max_columns", None)

table = pd.read_csv("table.csv", delimiter=";", encoding="PTCP154", engine="python")
# for i in table.iterrows():
#     print(i)
print(table.head())


# some_hell = table["ƒата и врем€ записи"]
# date_hell = pd.to_datetime(some_hell)
# print(date_hell)