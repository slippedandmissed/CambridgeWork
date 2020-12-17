#!/usr/bin/python3.9

import ucamcl
import pandas
import numpy as np
import matplotlib.pyplot as plt
from pylab import rcParams

### 1A
GRADER = ucamcl.autograder('https://markmy.solutions', course='scicomp').subsection('tick2a')

all_data = pandas.read_csv("covid_global_20201213.csv")
covid = all_data.dropna(subset=["Population"])
num_rows = len(covid)

GRADER.submit_answer(GRADER.fetch_question('q1'), num_rows)

ans = all_data[all_data["Population"].isna()][["Country/Region", "Province/State"]].drop_duplicates()

GRADER.submit_answer(GRADER.fetch_question('q2'), ans)

ans = covid.loc[covid["Country/Region"] == "United Kingdom"]["Province/State"].value_counts(dropna=False).to_frame().reset_index().rename(columns={"index":"Province/State", "Province/State": "n"}).sort_values("Province/State")
GRADER.submit_answer(GRADER.fetch_question('q3'), ans)

ans = covid.loc[covid["Country/Region"] == "United Kingdom"]
ans = ans.loc[ans["Province/State"].isna()][["Date", "Confirmed", "Deaths"]]
ans["Date"] = ans["Date"].apply(pandas.to_datetime)
ans["new_confirmed"] = ans["Confirmed"].diff()
ans["new_deaths"] = ans["Deaths"].diff()
ans["smooth_new_confirmed"] = ans.rolling(7, on="Date")["new_confirmed"].mean()

q = GRADER.fetch_question('q4')
want = pandas.DataFrame(q.rows).assign(Date=lambda df: pandas.to_datetime(df.Date))
submit = ans.merge(want)[q.want_cols].assign(Date=lambda df: df.Date.astype(str))
GRADER.submit_answer(q, submit)


rcParams['figure.figsize'] = 13, 5
fig, axs = plt.subplots(2, sharex=True)

axs[0].set_ylabel("daily cases")
axs[0].bar(ans["Date"], ans["new_confirmed"], width=1, color="lightblue")
axs[0].plot(ans["Date"], ans["smooth_new_confirmed"])

axs[1].set_ylabel("daily deaths")
axs[1].bar(ans["Date"], ans["new_deaths"], width=1, color="lightblue")

plt.show()


grouped = covid.groupby("Country/Region")
ans = grouped.apply(lambda x: 1 if any(x["Province/State"].isna()) else 0).reset_index().rename(columns={0: "metropole"})
ans["provinces"] = grouped.apply(lambda x: len(x["Province/State"].drop_duplicates().dropna())).reset_index()[0]
ans = ans.loc[(ans["metropole"] == 0) | (ans["provinces"] > 0)]

GRADER.submit_answer(GRADER.fetch_question('q6'), ans)

case0 = ["Australia", "Canada", "China"]
case1 = ["Denmark", "France", "Netherlands", "United Kingdom"]
neededFromOriginal = ["Country/Region", "Province/State", "Date", "Confirmed", "Deaths"]
special0 = covid.loc[covid["Country/Region"].isin(case0)][neededFromOriginal]
special1 = covid.loc[covid["Country/Region"].isin(case1)][neededFromOriginal]
nonSpecial = covid.loc[~covid["Country/Region"].isin(case0+case1)][neededFromOriginal]

special0 = special0.groupby(["Country/Region", "Date"]).sum().reset_index()
special1 = special1.loc[special1["Province/State"].isna()]

covidc = pandas.concat([special0, special1, nonSpecial])
covidc["Date"] = covidc["Date"].apply(pandas.to_datetime)

population_iso3 = pandas.read_csv("covid_countries_20201213.csv").rename(columns={"Country_Region": "Country/Region", "Province_State": "Province/State"})[["Country/Region", "Province/State", "iso3", "Population"]]

covidc = pandas.merge(covidc, population_iso3, how="left", left_on=["Country/Region", "Province/State"], right_on=["Country/Region", "Province/State"]).sort_values(["Country/Region", "Date"]).drop(["Province/State"], axis=1)

q = GRADER.fetch_question('q7')
want = pandas.DataFrame(q.rows).assign(Date=lambda df: pandas.to_datetime(df.Date))
submit = covidc.merge(want)[q.want_cols].assign(Date=lambda df: df.Date.astype(str))
GRADER.submit_answer(q, {'num_rows': len(covidc), 'details': submit})

### 1B

GRADER = ucamcl.autograder('https://markmy.solutions', course='scicomp').subsection('tick2b')

simplified = covidc.sort_values("Date").drop_duplicates(subset=["Country/Region"], keep="last")[["Country/Region", "Confirmed", "Deaths"]]
ans = simplified.copy()

q = GRADER.fetch_question('q8')
submit = pandas.DataFrame(q.rows).merge(ans)[q.want_cols]
GRADER.submit_answer(q, submit)

first = covidc.loc[covidc["Date"] < '2020-07-15'].sort_values("Date").drop_duplicates(subset=["Country/Region"], keep="last")[["Country/Region", "Confirmed", "Deaths"]]
second = covidc.loc[covidc["Date"] > '2020-07-14'].sort_values("Date").drop_duplicates(subset=["Country/Region"], keep="last")[["Country/Region", "Confirmed", "Deaths"]]
ans = first.merge(second, on="Country/Region", how="outer", suffixes=["1", "2"])
ans["Confirmed2"] = ans["Confirmed2"] - ans["Confirmed1"]
ans["Deaths2"] = ans["Deaths2"] - ans["Deaths1"]
ans["case_multiplier"] = (ans["Deaths1"]/ans["Confirmed1"])/(ans["Deaths2"]/ans["Confirmed2"])
case_multiplier_table = ans

q = GRADER.fetch_question('q9')
submit = pandas.DataFrame(q.rows).merge(ans)[q.want_cols]
GRADER.submit_answer(q, submit)

d = 10

smooth_new_confirmed_window = d # NOTE: the question says this should be 7 but the autograder and quoted values use 10

ans = covidc \
    .drop(["Deaths", "iso3", "Population"], axis=1) \
    .groupby("Country/Region") \
    .apply(lambda x: x.assign(new_confirmed=x["Confirmed"].diff())) \
    .reset_index(drop=True) \
    .groupby("Country/Region") \
    .apply(lambda x: x.assign(new_confirmed=x["new_confirmed"].where(x["Date"] > "2020-07-14", x["new_confirmed"]*case_multiplier_table.loc[case_multiplier_table["Country/Region"] == x["Country/Region"].iloc[0]]["case_multiplier"].iloc[0]))) \
    .reset_index(drop=True) \
    .groupby("Country/Region") \
    .apply(lambda x: x.assign(smooth_new_confirmed=x.rolling(smooth_new_confirmed_window, on="Date")["new_confirmed"].mean())) \
    .reset_index(drop=True) \
    .groupby("Country/Region") \
    .apply(lambda x: x.assign(infected=x.rolling(d, on="Date")["smooth_new_confirmed"].sum())) \
    .reset_index(drop=True) \
    .groupby("Country/Region") \
    .apply(lambda x: x.assign(inc=x["infected"].pct_change()+1)) \
    .reset_index(drop=True) \
    .groupby("Country/Region") \
    .apply(lambda x: x.assign(R=d*(x["inc"] - 1) + 1)) \
    .reset_index(drop=True)

q = GRADER.fetch_question('q10')
want = pandas.DataFrame(q.rows).assign(Date=lambda df: pandas.to_datetime(df.Date))
submit = ans.merge(want)[q.want_cols].assign(Date=lambda df: df.Date.astype(str))
GRADER.submit_answer(q, submit)

rcParams['figure.figsize'] = 13, 13
fig, axs = plt.subplots(4, sharex=True)
fig.suptitle("R versus number infected per 100k")
plt.xlim(10**0.5, 10**3.05)
plt.xscale("log")
plt.xlabel("num. infected per 100k")

double_every_two_weeks = d * (2.0**(1.0/14.0) - 1) + 1
halve_every_two_weeks = d * (0.5**(1.0/14.0) - 1) + 1

max_date = (float_dates := covidc["Date"].astype(int)).max()
min_date = float_dates.min()

for i, country in enumerate(["United Kingdom", "Italy", "Germany", "US"]):
    data = ans.loc[ans["Country/Region"] == country]
    c = (data["Date"].astype(int) - min_date)/(max_date - min_date)
    axs[i].scatter(x:=data["infected"]/covidc.loc[covidc["Country/Region"] == country]["Population"].iloc[0] * 100000, y:=data["R"], marker="+", c=c, cmap=plt.get_cmap("viridis"))
    axs[i].plot(x, y, lw=0.6, c="grey", alpha=0.6)
    axs[i].axhline(y=1, color="grey", alpha=0.5)
    axs[i].axvline(x=10, color="grey", alpha=0.5)
    axs[i].axvline(x=100, color="grey", alpha=0.5)
    axs[i].axvline(x=1000, color="grey", alpha=0.5)
    axs[i].axhspan(halve_every_two_weeks, double_every_two_weeks, alpha=0.1, color="grey")
    axs[i].set_ylim((0, 3))
    axs[i].set_title(country, position=(0.1, 1.0), y=0.8)

plt.show()
