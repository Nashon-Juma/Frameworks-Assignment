import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from datetime import datetime
import warnings
warnings.filterwarnings('ignore')

class CORD19Analyzer:
    def __init__(self, file_path):
        self.file_path = file_path
        self.df = None
        
    def load_data(self):
        """Load the metadata.csv file"""
        try:
            self.df = pd.read_csv(self.file_path)
            print("Data loaded successfully!")
            return True
        except FileNotFoundError:
            print(f"File {self.file_path} not found.")
            return False
        except Exception as e:
            print(f"Error loading data: {e}")
            return False
    
    def basic_exploration(self):
        """Perform basic data exploration"""
        print("=== BASIC DATA EXPLORATION ===")
        print(f"Dataset dimensions: {self.df.shape}")
        print(f"Number of rows: {self.df.shape[0]:,}")
        print(f"Number of columns: {self.df.shape[1]}")
        
        print("\n=== COLUMN NAMES ===")
        print(self.df.columns.tolist())
        
        print("\n=== DATA TYPES ===")
        print(self.df.dtypes)
        
        print("\n=== FIRST 5 ROWS ===")
        print(self.df.head())
        
    def check_missing_values(self):
        """Analyze missing values in the dataset"""
        print("\n=== MISSING VALUES ANALYSIS ===")
        missing_data = self.df.isnull().sum()
        missing_percent = (missing_data / len(self.df)) * 100
        
        missing_df = pd.DataFrame({
            'Column': missing_data.index,
            'Missing_Count': missing_data.values,
            'Missing_Percent': missing_percent.values
        })
        
        missing_df = missing_df[missing_df['Missing_Count'] > 0].sort_values('Missing_Percent', ascending=False)
        
        print("Columns with missing values:")
        print(missing_df)
        
        # Plot missing values
        if len(missing_df) > 0:
            plt.figure(figsize=(12, 6))
            bars = plt.bar(missing_df['Column'][:10], missing_df['Missing_Percent'][:10])
            plt.title('Top 10 Columns with Missing Values (%)')
            plt.xlabel('Columns')
            plt.ylabel('Percentage Missing')
            plt.xticks(rotation=45, ha='right')
            
            # Add value labels on bars
            for bar in bars:
                height = bar.get_height()
                plt.text(bar.get_x() + bar.get_width()/2., height,
                        f'{height:.1f}%', ha='center', va='bottom')
            
            plt.tight_layout()
            plt.savefig('missing_values.png', dpi=300, bbox_inches='tight')
            plt.show()
        
        return missing_df
    
    def basic_statistics(self):
        """Generate basic statistics for numerical columns"""
        print("\n=== BASIC STATISTICS ===")
        print(self.df.describe())
        
        # Check for numerical columns
        numerical_cols = self.df.select_dtypes(include=[np.number]).columns
        print(f"\nNumerical columns: {list(numerical_cols)}")

# Main execution
if __name__ == "__main__":
    # Initialize analyzer
    analyzer = CORD19Analyzer('metadata.csv')
    
    # Load data
    if analyzer.load_data():
        # Perform exploration
        analyzer.basic_exploration()
        missing_df = analyzer.check_missing_values()
        analyzer.basic_statistics()