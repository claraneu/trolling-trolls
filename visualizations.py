#Annotated Heatmaps; could be useful for amount per day per month or such
#%%
import matplotlib.pyplot as plt
import seaborn as sns
sns.set_theme()

# Load the example flights dataset and convert to long-form
flights_long = sns.load_dataset("flights")
print(flights_long)
flights = flights_long.pivot("month", "year", "passengers")
print(flights)

# Draw a heatmap with the numeric values in each cell
f, ax = plt.subplots(figsize=(9, 6))
sns.heatmap(flights, annot=True, fmt="d", linewidths=.5, ax=ax)

print(flights_long)




#%%
#Bar plot; could be useful for amount of HS-types
import pandas as pd
import numpy as np
import seaborn as sns
import matplotlib.pyplot as plt
import matplotlib.patches as mp
#sns.set_theme(style="whitegrid")

# Initialize the matplotlib figure
#f, ax = plt.subplots(figsize=(6, 15))

# Load the mock tweet dataset
#df = pd.read_csv("labeled_data2.csv")
#print(df)

#create simple barplots
#sns.barplot(x = "offensive_language", y = "number", data = df)
#sns.barplot(x = "class", y = "number", data = df)


#more complex comparative barplot
sns.set_theme(style="whitegrid")

df = pd.read_csv("labeled_data2.csv")

# Draw a nested barplot by type and confidence
g = sns.catplot(
    data=df, kind="bar",
    x="class", y="number", hue="offensive_language",
    ci="sd", palette="dark", alpha=.6, height=6
)
g.despine(left=True)
g.set_axis_labels("", "Number of Tweets")
g.legend.set_title("")



#
# import seaborn as sns
# import matplotlib.pyplot as plt
# sns.set_theme(style="whitegrid")

# # Initialize the matplotlib figure
# f, ax = plt.subplots(figsize=(6, 15))

# # Load the example car crash dataset
# crashes = sns.load_dataset("car_crashes").sort_values("total", ascending=False)
# print(crashes)
# # Plot the total crashes
# sns.set_color_codes("pastel")
# sns.barplot(x="total", y="abbrev", data=crashes,
#             label="Total", color="b")

# # Plot the crashes where alcohol was involved
# sns.set_color_codes("muted")
# sns.barplot(x="alcohol", y="abbrev", data=crashes,
#             label="Alcohol-involved", color="b")

# # Add a legend and informative axis label
# ax.legend(ncol=2, loc="lower right", frameon=True)
# ax.set(xlim=(0, 24), ylabel="",
#        xlabel="Automobile collisions per billion miles")
# sns.despine(left=True, bottom=True)






#%%
#Small multiple time series; compares time, time, amount
import seaborn as sns

sns.set_theme(style="dark")
flights = sns.load_dataset("flights")

# Plot each year's time series in its own facet
g = sns.relplot(
    data=flights,
    x="month", y="passengers", col="year", hue="year",
    kind="line", palette="crest", linewidth=4, zorder=5,
    col_wrap=3, height=2, aspect=1.5, legend=False,
)

# Iterate over each subplot to customize further
for year, ax in g.axes_dict.items():

    # Add the title as an annotation within the plot
    ax.text(.8, .85, year, transform=ax.transAxes, fontweight="bold")

    # Plot every year's time series in the background
    sns.lineplot(
        data=flights, x="month", y="passengers", units="year",
        estimator=None, color=".7", linewidth=1, ax=ax,
    )

# Reduce the frequency of the x axis ticks
ax.set_xticks(ax.get_xticks()[::2])

# Tweak the supporting aspects of the plot
g.set_titles("")
g.set_axis_labels("", "Passengers")
g.tight_layout()



# %%
