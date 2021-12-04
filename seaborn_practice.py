#%%
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.patches as mp
import seaborn as sns

df = pd.read_csv("labeled_data2.csv")
#df.head()

sns.set_style("darkgrid")
#sns.set_context("paper", font_scale=1.2)
#sns.despine(left=True, bottom=True)
# plt.figure(figsize=(8,8))


#Distribution plots
# sns.displot(df["count"], kde=True)
# sns.displot(df["class"], kde=True)
# sns.displot(df["hate_speech"], kde=True)
# sns.displot(df["offensive_language"], kde=True)
# sns.displot(df["neither"], kde=True)


# fig, axes = plt.subplots(1, 3, sharey=False, figsize=(20,5))

# fig.suptitle("How often was something labeled...")
# sns.histplot(df["offensive_language"], ax=axes[1])
# sns.histplot(df["hate_speech"], ax=axes[0])
# sns.histplot(df["neither"], ax=axes[2])


#Jointplots
#sns.violinplot(x="class", y="offensive_language", data=df)


#multiples density

fig, axes = plt.subplots(2, 2, sharey=True, figsize=(20,20))
fig.suptitle("Data Density per Class")
sns.jointplot(ax=axes[0,0], x='class', y='hate_speech', data=df, kind="kde")
axes[0,0].set_title("Hate Speech Density")
sns.jointplot(ax=axes[0,1], x='class', y='offensive_language', data=df, kind="kde")
axes[0,1].set_title("Offensive Language Density")
sns.jointplot(ax=axes[1,0], x='class',y='neither', data=df, kind="kde")
axes[1,0].set_title("Neither Density")


#KDE plots
#sns.kdeplot(df["hate_speech"])

#pairplots

#sns.pairplot(df)
#sns.pairplot(df, hue="class", palette="Blues")

#rugplot
#print(df)
#sns.rugplot(df["count"])


# %%
#################STYLING################
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.patches as mp
import seaborn as sns

df = pd.read_csv("labeled_data2.csv")

sns.set_style("darkgrid")
plt.figure(figsize=(8,8))


sns.jointplot(x="class", y="count", data=df, kind="kde")
# %%



#%%
#################Categorical Data Plotting#################
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.patches as mp
import seaborn as sns

df = pd.read_csv("labeled_data2.csv")
sns.set_style("darkgrid")

#sns.histplot(data=df["class"], estimator=np.median)
#sns.countplot(x="neither", data=df)

fig, axes = plt.subplots(1, 3, sharey=True, figsize=(15, 10))
fig.suptitle("Amounts of Votes in Each Class")
sns.countplot( x='hate_speech', data=df, ax=axes[0])
axes[0].set_title("Hate Speech Votes")
sns.countplot( x='offensive_language', data=df, ax=axes[1])
axes[1].set_title("Offensive Language Votes")
sns.countplot(x='neither', data=df, ax=axes[2])
axes[2].set_title("Neither Votes")



# %%
################### BOXPLOTS #########################
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.patches as mp
import seaborn as sns

df = pd.read_csv("labeled_data2.csv")

sns.boxplot(x="neither", y="count", data=df, hue="class")






# %%
