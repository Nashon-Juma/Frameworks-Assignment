import pandas as pd
import numpy as np
from datetime import datetime
import re

class CORD19Cleaner:
    def __init__(self, df):
        self.df = df.copy()
        self.cleaning_steps = []
    
    def handle_missing_values(self):
        """Handle missing values in important columns"""
        print("=== HANDLING MISSING VALUES ===")
        
        # Record original shape
        original_shape = self.df.shape
        
        # Create a copy before cleaning for comparison
        self.df_cleaned = self.df.copy()
        
        # Handle specific columns
        # For title - we can't work with papers without titles
        self.df_cleaned = self.df_cleaned.dropna(subset=['title'])
        
        # For abstract - fill with empty string
        self.df_cleaned['abstract'] = self.df_cleaned['abstract'].fillna('No abstract available')
        
        # For publish_time - we'll handle this in date processing
        self.df_cleaned = self.df_cleaned[self.df_cleaned['publish_time'].notna()]
        
        # Record cleaning step
        rows_removed = original_shape[0] - self.df_cleaned.shape[0]
        self.cleaning_steps.append(f"Removed {rows_removed} rows with missing critical data")
        
        print(f"Original data: {original_shape[0]} rows")
        print(f"After cleaning: {self.df_cleaned.shape[0]} rows")
        print(f"Rows removed: {rows_removed}")
        
        return self.df_cleaned
    
    def process_dates(self):
        """Convert and extract date information"""
        print("\n=== PROCESSING DATES ===")
        
        # Convert publish_time to datetime
        try:
            self.df_cleaned['publish_time'] = pd.to_datetime(
                self.df_cleaned['publish_time'], errors='coerce'
            )
            
            # Extract year, month, and quarter
            self.df_cleaned['publication_year'] = self.df_cleaned['publish_time'].dt.year
            self.df_cleaned['publication_month'] = self.df_cleaned['publish_time'].dt.month
            self.df_cleaned['publication_quarter'] = self.df_cleaned['publish_time'].dt.quarter
            
            # Remove rows where year extraction failed
            self.df_cleaned = self.df_cleaned[self.df_cleaned['publication_year'].notna()]
            
            self.cleaning_steps.append("Converted publish_time to datetime and extracted year/month/quarter")
            print("Date processing completed successfully")
            
        except Exception as e:
            print(f"Error in date processing: {e}")
        
        return self.df_cleaned
    
    def create_new_features(self):
        """Create new columns for analysis"""
        print("\n=== CREATING NEW FEATURES ===")
        
        # Abstract word count
        self.df_cleaned['abstract_word_count'] = self.df_cleaned['abstract'].apply(
            lambda x: len(str(x).split()) if pd.notna(x) else 0
        )
        
        # Title word count
        self.df_cleaned['title_word_count'] = self.df_cleaned['title'].apply(
            lambda x: len(str(x).split()) if pd.notna(x) else 0
        )
        
        # Has abstract flag
        self.df_cleaned['has_abstract'] = self.df_cleaned['abstract'] != 'No abstract available'
        
        # Source type (simplified)
        self.df_cleaned['source_type'] = self.df_cleaned['source_x'].fillna('Unknown')
        
        self.cleaning_steps.append("Created new features: word counts, flags, and source type")
        print("New features created successfully")
        
        return self.df_cleaned
    
    def get_cleaning_summary(self):
        """Print summary of cleaning steps"""
        print("\n=== CLEANING SUMMARY ===")
        for i, step in enumerate(self.cleaning_steps, 1):
            print(f"{i}. {step}")
        
        print(f"\nFinal dataset shape: {self.df_cleaned.shape}")
        print(f"Missing values in critical columns:")
        print(f"  - Title: {self.df_cleaned['title'].isnull().sum()}")
        print(f"  - Abstract: {self.df_cleaned['abstract'].isnull().sum()}")
        print(f"  - Publication year: {self.df_cleaned['publication_year'].isnull().sum()}")
    
    def get_clean_data(self):
        """Return the cleaned dataframe"""
        return self.df_cleaned
