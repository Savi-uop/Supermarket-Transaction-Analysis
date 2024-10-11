import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.preprocessing import StandardScaler
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LinearRegression
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import mean_squared_error, accuracy_score

def load_data():
    # Load datasets
    items_df = pd.read_csv('C:/Users/user/DS Projects/Supermarket Transaction Analysis/data/Item.csv')
    supermarkets_df = pd.read_csv('C:/Users/user/DS Projects/Supermarket Transaction Analysis/data/Supermarkets.csv')
    sales_df = pd.read_csv('C:/Users/user/DS Projects/Supermarket Transaction Analysis/data/Sales.csv')
    promotion_df = pd.read_csv('C:/Users/user/DS Projects/Supermarket Transaction Analysis/data/Promotion.csv')
    
     # Rename columns to ensure consistency
    sales_df.rename(columns={'Supermarket': 'supermarket'}, inplace=True)
    supermarkets_df.rename(columns={'Supermarket': 'supermarket'}, inplace=True)
    
    return items_df, supermarkets_df, sales_df, promotion_df

def clean_data(items_df, supermarkets_df, sales_df, promotion_df):
    # Drop duplicates
    items_df.drop_duplicates(inplace=True)
    supermarkets_df.drop_duplicates(inplace=True)
    sales_df.drop_duplicates(inplace=True)
    promotion_df.drop_duplicates(inplace=True)
    
    # Fill missing values
    sales_df = sales_df.ffill()
    
    return items_df, supermarkets_df, sales_df, promotion_df

def explore_data(items_df, supermarkets_df, sales_df, promotion_df):
    # Preview the datasets
    print("Items Data:")
    print(items_df.head())
    print("\nSupermarkets Data:")
    print(supermarkets_df.head())
    print("\nSales Data:")
    print(sales_df.head())
    print("\nPromotion Data:")
    print(promotion_df.head())

    # Check for missing values
    print("\nMissing Values in Items Data:\n", items_df.isnull().sum())
    print("\nMissing Values in Supermarkets Data:\n", supermarkets_df.isnull().sum())
    print("\nMissing Values in Sales Data:\n", sales_df.isnull().sum())
    print("\nMissing Values in Promotion Data:\n", promotion_df.isnull().sum())

if __name__ == '__main__':
    # Load and clean the data
    items, supermarkets, sales, promotions = load_data()
    items, supermarkets, sales, promotions = clean_data(items, supermarkets, sales, promotions)

    # Print confirmation of data loading and cleaning
    print("Data Loaded and Cleaned")

    # Explore the data
    explore_data(items, supermarkets, sales, promotions)