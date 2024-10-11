from sklearn.model_selection import train_test_split
from sklearn.linear_model import LinearRegression
from sklearn.metrics import mean_squared_error
import pandas as pd
from analysis import merge_datasets, normalize_data, load_data, clean_data

def build_and_train_model(merged_df):
    # One-hot encode categorical features: 'type' and 'supermarket'
    merged_df = pd.get_dummies(merged_df, columns=['type', 'supermarket'], drop_first=True)
    
    # Select the features and target variable
    X = merged_df[['units', 'sales_province'] + [col for col in merged_df.columns if col.startswith('type_') or col.startswith('supermarket_')]]
    y = merged_df['amount']
    
    # Split the data
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
    
    # Train the model
    model = LinearRegression()
    model.fit(X_train, y_train)
    
    # Make predictions
    y_pred = model.predict(X_test)
    
    # Evaluate the model
    mse = mean_squared_error(y_test, y_pred)
    print(f'Mean Squared Error: {mse}')

if __name__ == '__main__':
    items, supermarkets, sales, promotions = load_data()
    items, supermarkets, sales, promotions = clean_data(items, supermarkets, sales, promotions)
    merged_df = merge_datasets(items, supermarkets, sales, promotions)
    merged_df = normalize_data(merged_df)
    build_and_train_model(merged_df)
