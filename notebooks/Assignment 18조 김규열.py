import pandas as pd

raw = [
    {"date":"2026-01-01", "time":"09:10", "store":"A", "menu":"Americano", "price":"4,500원", "qty":"2", "paid":"TRUE"},
    {"date":"2026/01/01", "time":"09:12", "store":"A", "menu":"Latte",     "price":"5000",   "qty":1,   "paid":"True"}, # /
    {"date":"2026-01-02", "time":"12:30", "store":"A", "menu":"Latte",     "price":None,     "qty":2,   "paid":"FALSE"},
    {"date":"2026-01-03", "time":"18:05", "store":"B", "menu":"Mocha",     "price":"5500",   "qty":None,"paid":True},
    {"date":"2026-01-03", "time":"18:05", "store":"B", "menu":"Mocha",     "price":"5500",   "qty":None,"paid":True},  # 중복
    {"date":"2026-01-04", "time":"08:55", "store":"B", "menu":"Americano ", "price":"4500",  "qty":"1", "paid":"TRUE"}, # 공백
    {"date":"2026-01-04", "time":"08:58", "store":"A", "menu":"latte",     "price":"5,000",  "qty":"3", "paid":"TRUE"}, # 소문자
]
df = pd.DataFrame(raw)
df

cols = ["date","time","store","menu","price","qty","paid"]
df3= df[cols].copy()
df3["paid"] = df3["paid"].astype(str).str.strip().str.lower()

# paid true
paid_df3 = df3["paid"].isin(["true"])
# selecttrue = df3.loc[paid_df3]

# store A
storeA = df3["store"].isin(["A"])
# selectA = df3.loc[storeA]

# menu clean
df3["menu"]= df3["menu"].str.strip().str.title()

# quantity clean
df3 = df3.rename(columns={"qty":"quantity"})
df3['quantity']= df3['quantity'].astype(str).str.replace(',','',regex=False)
df3['quantity']= pd.to_numeric(df3['quantity'],errors='coerce')

# price clean
df3['price']= (
    df3['price'].astype(str)
    .str.replace(",", "", regex=False)
    .str.replace('원','',regex=False)
    .str.strip()
)
df3['price']= pd.to_numeric(df3['price'],errors='coerce')

# sales create
df3['sales']= df3['price']*df3['quantity']

# clean date, time
df3['date']= df3['date'].astype(str).str.strip().str.replace('/','-', regex=False)
df3['time']= df3['time'].astype(str).str.strip()
df3['wholedate']= pd.to_datetime(df3['date'] +" "+ df3['time'], errors='coerce')

# Clear duplicate
df3 = df3.drop_duplicates()

# result
meeting_table1 = df3.loc[paid_df3 & storeA, ["wholedate","store","menu","price","quantity","sales"]].sort_values(
    by=["wholedate","store"],
    ascending=[True, True]
)

print(meeting_table1)