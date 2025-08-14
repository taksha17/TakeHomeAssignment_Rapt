import pandas as pd
import statsmodels.api as sm
import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np

# Loading the dataset
file_path = 'testdata (1).csv'
df = pd.read_csv(file_path)

# Section1: Initialzing with data cleaning and pre preparing the data dropping the rows with missing data
df['revenue'] = pd.to_numeric(df['revenue'], errors='coerce')
df['top'] = pd.to_numeric(df['top'], errors='coerce')
df.dropna(inplace=True)

#Seaction2: Trying to accomplish Task 1 
#Task 1: Simple Linear Regression 
print("--- Simple Linear Regression ---")

sns.set_style("whitegrid")
plt.figure(figsize=(10, 6))
sns.scatterplot(data=df, x='top', y='revenue', alpha=0.6)
plt.title('Figure 1: Revenue vs. Time on Page scatter graph', fontsize=10)
plt.xlabel('Time on Page (Top)', fontsize=10)
plt.ylabel('Revenue', fontsize=10)
plt.savefig('revenue_vs_top_scatterplotgraph.png', dpi=300)

# Trying to fit and summarize the simple model
X_simple = sm.add_constant(df['top'])
y = df['revenue']
model_simple = sm.OLS(y, X_simple).fit()
print(model_simple.summary())
#Task1 seems to be accomplished, the model's fitting in perfectly without errors
#End of Section 1 

#Section2: Trying to accomplish Task 2
#Task 2: Multiple Linear Regression 
print("\n--- Multiple Linear Regression ---")

#Convert 'site' to a category
df['site'] = df['site'].astype('category')

# Create dummy variables for categorical columns
df_dummies = pd.get_dummies(df, columns=['browser', 'platform', 'site'], drop_first=True)

# Here the "pd.get_dummies create's columns with boolean data. While logically, this are same as working with 1's and 0's, 
# but the my version of statsmodels library pops error as I might need to explicitly conver these into integer column's of 1's and 0's"
# Lets identify the columns that are boolean and convert them
for col in df_dummies.columns:
    if df_dummies[col].dtype == 'bool':
        df_dummies[col] = df_dummies[col].astype(int)

# Defining independent and dependent variables
X_multiple = df_dummies[['top', 'browser_safari', 'platform_mobile', 'site_2', 'site_3', 'site_4']]
X_multiple = sm.add_constant(X_multiple)
y_multiple = df_dummies['revenue']

# Sanity check of data types before fitting the model
# print("\nFinal data types for Multiple Regression:")
# print(X_multiple.dtypes)

# Fitting the multiple regression model
model_multiple = sm.OLS(y_multiple, X_multiple).fit()

# Printing the final summary
print(model_multiple.summary())

#Task 2 accomplished
#End Of Section2