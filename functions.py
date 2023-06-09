# -*- coding: utf-8 -*-
"""functions

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1AJZzxsH34GBu9dpxLvl25jB-bPiSxQvH
"""

# Commented out IPython magic to ensure Python compatibility.
import pandas as pd
import seaborn as sns
import numpy as np
import matplotlib.pyplot as plt
import scipy.stats as stats
import statsmodels.api as sm
import statsmodels.formula.api as smf
import plotly.express as px
import plotly.graph_objs as go
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score, recall_score, precision_score, f1_score, confusion_matrix
from sklearn.feature_selection import SelectKBest, chi2
from sklearn import linear_model
from sklearn import metrics
from sklearn.linear_model import LinearRegression
from sklearn.metrics import mean_squared_error
from sklearn import ensemble
from sklearn.model_selection import cross_val_score
from mpl_toolkits.mplot3d import Axes3D
import folium
from folium.plugins import HeatMap
import warnings
# %matplotlib inline

kc_df = pd.read_csv('kc_house_data.csv')
kc_df.head()

def null_values():
  total_null = 0
  for null_count in kc_df.isnull().sum():
      total_null += null_count
  print(f"There are total {total_null} null values in the data")
null_values()

def adjustedR2(r2,n,k):
    return r2-(k-1)/(n-k)*(1-r2)

def get_rmse(model, name):
      model.fit(X_train, Y_train)
      score = np.sqrt(-cross_val_score(model, X_test, Y_test, scoring="neg_mean_squared_error", cv = 10))
      score_mean = score.mean()
      results[name] = score_mean

#Data Preprocessing
kc_df = kc_df.dropna()
kc_df = kc_df.drop(labels=['date', 'lat', 'long'], axis= 1)
kc_df.info()

#Results and Findings

#Data Visualization for variables affect on Price of properties

#property values by zipcode calculation
def dv_variable_graph():
  kc_top5_price = kc_df.groupby("zipcode")["price"].mean().sort_values(ascending = False)[:5]
  kc_mean_price = kc_df.price.mean()
  #top5 neighborhood label for plot
  area_labels = ["Medina", "Bellevue", "Mercer Island",
               "Madison Park", "Capitol Hill"]
  #plotting the data
  plt.subplots(figsize=(8,4))
  sns.barplot(x=kc_top5_price.index, y=kc_top5_price, order=kc_top5_price.index, palette="Blues_d") #blue for seahawks!
  plt.xticks(np.arange(5), area_labels, rotation=75, size=8) #relabel x with list above
  plt.hlines(kc_mean_price, -.5 ,4.5, colors="darkgoldenrod", label="Average Price") #plot average price horizontal line
  #annotating the graph
  plt.xlabel("Neighborhoods", size=14)
  plt.ylabel("Prices ($1mil)", size=14)
  plt.title("Neighborhoods with Highest Property Price", size=16, y=1.08)
  plt.legend()
  plt.show()

#Data Visualization on property condition's affect on price
def dv_condition_graph():
  condition_mean = kc_df.groupby("condition")["price"].mean()
  condition_median = kc_df.groupby("condition")["price"].median()
  condition_score = np.arange(1,6)
  #set subplot data
  fig, ax = plt.subplots(figsize=(8,4))
  ax2 = ax.twinx() #set ax2 on same x axis as ax
  ax3 = ax.twinx() #same as above, for hline
  width = 0.5
  #creating barplot
  ax.bar(x=condition_score, height=condition_median, width=width,
       label="Median Price", color="midnightblue", alpha=0.8)
  ax2.bar(x=condition_score, height=condition_mean, width=width,
        label="Mean Price", color="royalblue", alpha=0.8)
  #horizontal line for mean price
  kc_mean_price = kc_df.price.mean()
  ax3.hlines(kc_mean_price, .7 ,5.3, colors="red", label="Average Price")
  #set ylimit to the same scale and display only 1
  ax.set_ylim(0,1.2*condition_mean.max())
  ax2.set_ylim(0,1.2*condition_mean.max())
  ax3.set_ylim(0,1.2*condition_mean.max())
  ax2.yaxis.set_visible(False) #hide the 2nd axis
  ax3.yaxis.set_visible(False)
  #setting legend positions
  ax.legend(bbox_to_anchor=(0,0,1,1), loc="upper left")
  ax2.legend(bbox_to_anchor=(0,-.1,1,1), loc="upper left")
  ax3.legend(bbox_to_anchor=(0,0,1,1), loc="upper right")
  #annotating the graph
  ax.set_ylabel("Average Prices ($)", size=14)
  ax.set_xlabel("Condition Score", size=14)
  plt.title("Average Property Value per Condition", size=16, y=1.08)
  plt.legend()
  plt.show()

#Data Visualization on basement and renovation affect on price
def dv_basement():
    basement = kc_df[(kc_df["sqft_basement"] > 0)]
    basement_mean = basement.price.mean()
    no_basement = kc_df[(kc_df["sqft_basement"] == 0)]
    no_basement_mean = no_basement.price.mean()
    #mean values to plot
    renovated = kc_df[(kc_df["yr_renovated"] > 0)]
    renovated_mean = renovated.price.mean()
    not_renovated = kc_df[(kc_df["yr_renovated"] == 0)]
    not_renovated_mean = not_renovated.price.mean()
    #prepare plot labels
    label_basement = ["Basement", "No basement"]
    values_basement = [basement_mean, no_basement_mean]
    label_renovation = ["Renovated", "No Renovation"]
    values_renovation = [renovated_mean, not_renovated_mean]
    #setting the graph
    fig, ax = plt.subplots(1, 2, figsize=(14,4))
    sns.barplot(ax=ax[0], x=label_basement, y=values_basement, palette="Blues_r")
    sns.barplot(ax=ax[1], x=label_renovation, y=values_renovation, palette="Blues_r")
    kc_mean_price = kc_df.price.mean()
    ax[0].hlines(kc_mean_price, -.5 ,1.5, colors="coral", label="Average Price") #plot average price horizontal line
    ax[1].hlines(kc_mean_price, -.5 ,1.5, colors="coral", label="Average Price") #plot average price horizontal line
    #Annotating the graph
    ax[0].set_ylabel("Average Prices ($)", size=12)
    ax[0].set_title("Average Property Value", size=14)
    ax[0].set_ylim(0,1.1*renovated_mean)
    ax[0].legend()
    ax[1].set_ylabel("Average Prices ($)", size=12)
    ax[1].set_title("Average Property Value", size=14)
    ax[1].set_ylim(0,1.1*renovated_mean)
    ax[1].legend()
    
    plt.suptitle("Affect of Basement and Renovation on Property Value", size=16, y=1.02)
    plt.show()

df= pd.read_csv("kc_house_data.csv")

#Correlation Matrix

def cormat():
  features = ['price','bedrooms','bathrooms','sqft_living','sqft_lot','floors','waterfront',
            'view','condition','grade','sqft_above','sqft_basement','yr_built','yr_renovated',
            'zipcode','lat','long','sqft_living15','sqft_lot15']
  mask = np.zeros_like(df[features].corr(), dtype=np.bool) 
  mask[np.triu_indices_from(mask)] = True 
  
  f, ax = plt.subplots(figsize=(16, 12))
  plt.title('Correlation Matrix',fontsize=25)
  sns.heatmap(df[features].corr(),linewidths=0.25,vmax=0.7,square=True,cmap="rocket",
            linecolor='w',annot=True,annot_kws={"size":8},mask=mask,cbar_kws={"shrink": .9});

def linear_reg():
  #Simple Linear Regression
  train_data,test_data = train_test_split(df,train_size = 0.8,random_state=3)
  
  lr = linear_model.LinearRegression()
  X_train = np.array(train_data['sqft_living'], dtype=pd.Series).reshape(-1,1)
  y_train = np.array(train_data['price'], dtype=pd.Series)
  lr.fit(X_train,y_train)
  
  X_test = np.array(test_data['sqft_living'], dtype=pd.Series).reshape(-1,1)
  y_test = np.array(test_data['price'], dtype=pd.Series)
  
  pred = lr.predict(X_test)
  rmsesm = float(format(np.sqrt(metrics.mean_squared_error(y_test,pred)),'.3f'))
  rtrsm = float(format(lr.score(X_train, y_train),'.3f'))
  rtesm = float(format(lr.score(X_test, y_test),'.3f'))
  cv = float(format(cross_val_score(lr,df[['sqft_living']],df['price'],cv=5).mean(),'.3f'))
  
  print ("Average Price for Test Data: {:.3f}".format(y_test.mean()))
  print('Intercept: {}'.format(lr.intercept_))
  print('Coefficient: {}'.format(lr.coef_))
  
  evaluation = pd.DataFrame({'Model': [],
                           'Details':[],
                           'Root Mean Squared Error (RMSE)':[],
                           'R-squared (training)':[],
                           'Adjusted R-squared (training)':[],
                           'R-squared (test)':[],
                           'Adjusted R-squared (test)':[],
                           '5-Fold Cross Validation':[]})
  r = evaluation.shape[0]
  evaluation.loc[r] = ['Simple Linear Regression','-',rmsesm,rtrsm,'-',rtesm,'-',cv]
  evaluation

def renovation():
  df = pd.read_csv("kc_house_data.csv")
  df_dm= df.copy()
  # just take the year from the date column
  df_dm['sales_yr']=df_dm['date'].astype(str).str[:4]
  
  # add the age of the buildings when the houses were sold as a new column
  df_dm['age']=df_dm['sales_yr'].astype(int)-df_dm['yr_built']
  # add the age of the renovation when the houses were sold as a new column
  df_dm['age_rnv']=0
  df_dm['age_rnv']=df_dm['sales_yr'][df_dm['yr_renovated']!=0].astype(int)-df_dm['yr_renovated'][df_dm['yr_renovated']!=0]
  df_dm['age_rnv'][df_dm['age_rnv'].isnull()]=0
  # partition the age into bins
  bins = [-2,0,5,10,25,50,75,100,100000]
  labels = ['<1','1-5','6-10','11-25','26-50','51-75','76-100','>100']
  df_dm['age_binned'] = pd.cut(df_dm['age'], bins=bins, labels=labels)
  # partition the age_rnv into bins
  bins = [-2,0,5,10,25,50,75,100000]
  labels = ['<1','1-5','6-10','11-25','26-50','51-75','>75']
  df_dm['age_rnv_binned'] = pd.cut(df_dm['age_rnv'], bins=bins, labels=labels)
  
  # histograms for the binned columns
  f, axes = plt.subplots(1, 2,figsize=(15,5))
  p1=sns.countplot(df_dm['age_binned'],ax=axes[0])
  for p in p1.patches:
    height = p.get_height()
    p1.text(p.get_x()+p.get_width()/2,height + 50,height,ha="center")   
  p2=sns.countplot(df_dm['age_rnv_binned'],ax=axes[1])
  sns.despine(left=True, bottom=True)
  for p in p2.patches:
    height = p.get_height()
    p2.text(p.get_x()+p.get_width()/2,height + 200,height,ha="center")
  
  axes[0].set(xlabel='Age')
  axes[0].yaxis.tick_left()
  axes[1].yaxis.set_label_position("right")
  axes[1].yaxis.tick_right()
  axes[1].set(xlabel='Renovation Age');
  
  # transform the factor values to be able to use in the model
  df_dm = pd.get_dummies(df_dm, columns=['age_binned','age_rnv_binned'])

def best_feature():
  kc_df1 = pd.read_csv("kc_house_data.csv")
  kc_df1 = kc_df1.drop(['date', 'lat', 'long', 'id'], axis =1)
  
  bestfeatures = SelectKBest(score_func=chi2, k=8)
  y = kc_df1['price']
  X = kc_df1.drop("price", axis=1)
  fit = bestfeatures.fit(X, y)
  scores = pd.DataFrame(fit.scores_)
  columns = pd.DataFrame(X.columns)
  featureScores = pd.concat([columns,scores],axis=1)
  featureScores.columns = ['Variables', 'Score']
  print(featureScores)

best_feature()

