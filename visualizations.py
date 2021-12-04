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
#Grouped Barplots
import pandas as pd
import numpy as np
import seaborn as sns
import matplotlib.pyplot as plt
import matplotlib.patches as mp
sns.set_theme(style="whitegrid")

df = pd.read_csv("labeled_data2.csv")
print(df.head())

# Draw a nested barplot by species and sex
# g = sns.catplot(
#     data=df, kind="bar",
#     x=df["class"], y=df["class"].value_counts(), hue=df["count"],
#     ci="sd", palette="dark", alpha=.6, height=6
# )
# g.despine(left=True)
# g.set_axis_labels("", "Tweet Count")
# g.legend.set_title("")




#%%
#Bar plot; could be useful for amount of HS-types
import pandas as pd
import numpy as np
import seaborn as sns
import matplotlib.pyplot as plt
import matplotlib.patches as mp
sns.set_theme(style="whitegrid")

# Initialize the matplotlib figure
#f, ax = plt.subplots(figsize=(6, 15))

# Load the mock tweet dataset
df = pd.read_csv("labeled_data2.csv")

#create simple barplots doesnt work because it doesn't count 0s and weirdly 2s
#sns.barplot(x = df["class"], y = df.value_counts("class"))

#sns.plot(kind=bar, x = df["class"], y = df.value_counts("class"))

#This was a test to see what value value_counts counts, and they are correct. Error must be somewhere else
#test = df.value_counts("class")
#test_frame = pd.DataFrame(test)
#print(test)

#Three bar plots next to each other; this one's correct
#sns.countplot(x="class", data = df)

#counts of votes per total count
#sns.barplot(x = df["offensive_language"], y = df.value_counts("count"))
sns.barplot(x="count", y=df.value_counts("count"), data=df)

###########create separate dataframe that contains the counts for class occurrences in df##########
# count class occurrences in csv file and store in dictionary
# class_count = {}
# for n in df["class"]:
#     class_count[n] = class_count.get(n, 0) + 1
# #print(class_count)

# #I don't know, but it works
# classes = class_count.items()
# class_list = list(classes)

# #create dataframe from list
# class_frame = pd.DataFrame(class_list)
# class_frame.columns=["class", "class_count"]

# #sort dataframe by classes from 0 to 2
# class_frame.sort_values(by=["class"])

# #rename indexes from 0 to 1 because they got shuffled by sort (doesn't work)
# class_frame.index=["0", "1", "2"]
# print(class_frame)

# sns.barplot(x="class", y="class_count", data=class_frame)
##############################






#%%
#Small multiple time series; compares time, time, amount
import pandas as pd
import numpy as np
import seaborn as sns
import matplotlib.pyplot as plt
import matplotlib.patches as mp

sns.set_theme(style="dark")

df = pd.read_csv("labeled_data2.csv")

# Plot each year's time series in its own facet
g = sns.relplot(
    data=df,
    x="class", y="count", col="offensive_language", hue="offensive_language",
    kind="line", palette="crest", linewidth=4, zorder=5,
    col_wrap=3, height=2, aspect=1.5, legend=False,
)

# Iterate over each subplot to customize further
for year, ax in g.axes_dict.items():

    # Add the title as an annotation within the plot
    ax.text(.8, .85, year, transform=ax.transAxes, fontweight="bold")

    # Plot every year's time series in the background
    sns.lineplot(
        data=flights, x="class", y="count", units="offensive_language",
        estimator=None, color=".7", linewidth=1, ax=ax,
    )

# Reduce the frequency of the x axis ticks
ax.set_xticks(ax.get_xticks()[::2])

# Tweak the supporting aspects of the plot
g.set_titles("")
g.set_axis_labels("", "Class")
g.tight_layout()



# %%
