import os
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
from data_processing import load_data, clean_data

def merge_datasets(items_df, supermarkets_df, sales_df, promotion_df):
    # Rename columns to ensure consistency
    sales_df.rename(columns={'Supermarket': 'supermarket'}, inplace=True)
    supermarkets_df.rename(columns={'Supermarket': 'supermarket_No'}, inplace=True)
    supermarkets_df.rename(columns={'supermarket_No': 'supermarket'}, inplace=True)

    # Rename the 'supermarkets' column in promotion_df to 'supermarket' to match other DataFrames
    promotion_df.rename(columns={'supermarkets': 'supermarket'}, inplace=True)

    # Rename 'province' columns to distinguish them before merging
    sales_df.rename(columns={'province': 'sales_province'}, inplace=True)
    promotion_df.rename(columns={'province': 'promotion_province'}, inplace=True)

    # Debug: Print columns before merging
    print("Sales Data Columns:", sales_df.columns)
    print("Supermarkets Data Columns:", supermarkets_df.columns)
    print("Promotion Data Columns:", promotion_df.columns)

    # Merge sales and items data on 'code'
    merged_df = pd.merge(sales_df, items_df, on='code', how='left')
    
    # Debug: Print columns after first merge
    print("Merged Data Columns (after merging sales and items):", merged_df.columns)

    # Check for 'supermarket' in merged_df
    print("Supermarket values in merged_df:", merged_df['supermarket'].unique() if 'supermarket' in merged_df.columns else "Not available")
    
    # Merge with supermarkets data on 'supermarket'
    if 'supermarket' in merged_df.columns and 'supermarket' in supermarkets_df.columns:
        merged_df = pd.merge(merged_df, supermarkets_df, on='supermarket', how='left')
    else:
        print("Error: 'supermarket' column not found in one of the DataFrames.")
        print("Merged DataFrame Columns:", merged_df.columns)
        print("Supermarkets DataFrame Columns:", supermarkets_df.columns)
        return None
    
    # Merge with promotion data
    if 'supermarket' in merged_df.columns and 'week' in merged_df.columns:
        if 'supermarket' in promotion_df.columns:
            merged_df = pd.merge(merged_df, promotion_df, on=['code', 'supermarket', 'week'], how='left')
        else:
            print("Error: 'supermarket' column not found in promotion_df.")
            return None
    else:
        print("Error: Required columns for merging with promotions not found.")
        return None

    return merged_df

def normalize_data(merged_df):
    # Check if 'sales_province' and 'promotion_province' exist before normalization
    if 'sales_province' in merged_df.columns:
        merged_df['sales_province'] = merged_df['sales_province'].astype('category').cat.codes
    else:
        print("Error: 'sales_province' column not found in merged_df.")
    
    if 'promotion_province' in merged_df.columns:
        merged_df['promotion_province'] = merged_df['promotion_province'].astype('category').cat.codes
    else:
        print("Error: 'promotion_province' column not found in merged_df.")
    
    return merged_df

def create_output_directory():
    output_dir = '../output'
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)

def analyze_sales(merged_df):
    create_output_directory()
    weekly_sales = merged_df.groupby('week')['amount'].sum().reset_index()
    plt.figure(figsize=(10, 5))
    sns.lineplot(data=weekly_sales, x='week', y='amount')
    plt.title('Weekly Sales Analysis')
    plt.savefig('../output/weekly_sales_analysis.png')
    plt.show()

def analyze_promotions(merged_df):
    create_output_directory()
    
    # Separate promoted and non-promoted sales
    promoted_sales = merged_df[merged_df['feature'].notna()]
    non_promoted_sales = merged_df[merged_df['feature'].isna()]
    
    # Debug: Print the number of promoted and non-promoted sales
    print(f"Number of Promoted Sales: {len(promoted_sales)}")
    print(f"Number of Non-Promoted Sales: {len(non_promoted_sales)}")
    
    plt.figure(figsize=(10, 5))
    sns.barplot(x=['Promotions', 'No Promotions'], y=[promoted_sales['amount'].sum(), non_promoted_sales['amount'].sum()])
    plt.title('Sales Comparison: Promotions vs. No Promotions')
    plt.savefig('../output/promotions_vs_no_promotions.png')
    plt.show()

if __name__ == '__main__':
    items, supermarkets, sales, promotions = load_data()
    items, supermarkets, sales, promotions = clean_data(items, supermarkets, sales, promotions)
    merged_df = merge_datasets(items, supermarkets, sales, promotions)
    
    if merged_df is not None:
        merged_df = normalize_data(merged_df)
        analyze_sales(merged_df)
        analyze_promotions(merged_df)
