import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from wordcloud import WordCloud
from collections import Counter
import re

# Set style for better visualizations
plt.style.use('default')
sns.set_palette("husl")

class CORD19Visualizer:
    def __init__(self, df):
        self.df = df
    
    def plot_publications_over_time(self, save_path='publications_over_time.png'):
        """Plot number of publications over time"""
        plt.figure(figsize=(12, 6))
        
        # Group by year and count
        yearly_counts = self.df['publication_year'].value_counts().sort_index()
        
        # Filter out any invalid years
        yearly_counts = yearly_counts[yearly_counts.index >= 2019]
        
        plt.plot(yearly_counts.index, yearly_counts.values, marker='o', linewidth=2, markersize=8)
        plt.title('COVID-19 Research Publications Over Time', fontsize=16, fontweight='bold')
        plt.xlabel('Publication Year', fontsize=12)
        plt.ylabel('Number of Publications', fontsize=12)
        plt.grid(True, alpha=0.3)
        
        # Add value annotations
        for year, count in yearly_counts.items():
            plt.annotate(f'{count:,}', (year, count), 
                        textcoords="offset points", xytext=(0,10), ha='center')
        
        plt.tight_layout()
        plt.savefig(save_path, dpi=300, bbox_inches='tight')
        plt.show()
        
        return yearly_counts
    
    def plot_top_journals(self, top_n=15, save_path='top_journals.png'):
        """Plot top publishing journals"""
        plt.figure(figsize=(12, 8))
        
        # Get top journals
        journal_counts = self.df['journal'].value_counts().head(top_n)
        
        # Create horizontal bar chart
        bars = plt.barh(range(len(journal_counts)), journal_counts.values)
        plt.yticks(range(len(journal_counts)), journal_counts.index)
        plt.title(f'Top {top_n} Journals Publishing COVID-19 Research', fontsize=16, fontweight='bold')
        plt.xlabel('Number of Publications', fontsize=12)
        
        # Add value labels on bars
        for i, bar in enumerate(bars):
            width = bar.get_width()
            plt.text(width, bar.get_y() + bar.get_height()/2, 
                    f' {width:,}', ha='left', va='center')
        
        plt.tight_layout()
        plt.savefig(save_path, dpi=300, bbox_inches='tight')
        plt.show()
        
        return journal_counts
    
    def generate_word_cloud(self, save_path='wordcloud.png'):
        """Generate word cloud from paper titles"""
        # Combine all titles
        text = ' '.join(self.df['title'].dropna().astype(str))
        
        # Clean text - remove special characters and common words
        stop_words = ['using', 'based', 'study', 'analysis', 'covid', '19', 
                     'sars', 'cov', '2', 'coronavirus', 'pandemic']
        
        # Generate word cloud
        wordcloud = WordCloud(width=800, height=400, 
                             background_color='white',
                             stopwords=stop_words,
                             max_words=100,
                             colormap='viridis').generate(text)
        
        plt.figure(figsize=(12, 6))
        plt.imshow(wordcloud, interpolation='bilinear')
        plt.title('Most Frequent Words in Paper Titles', fontsize=16, fontweight='bold')
        plt.axis('off')
        plt.tight_layout()
        plt.savefig(save_path, dpi=300, bbox_inches='tight')
        plt.show()
    
    def plot_source_distribution(self, save_path='source_distribution.png'):
        """Plot distribution of papers by source"""
        plt.figure(figsize=(10, 6))
        
        source_counts = self.df['source_x'].value_counts().head(10)
        
        plt.pie(source_counts.values, labels=source_counts.index, autopct='%1.1f%%')
        plt.title('Distribution of Papers by Source', fontsize=16, fontweight='bold')
        plt.tight_layout()
        plt.savefig(save_path, dpi=300, bbox_inches='tight')
        plt.show()
        
        return source_counts
    
    def plot_abstract_length_distribution(self, save_path='abstract_length.png'):
        """Plot distribution of abstract lengths"""
        plt.figure(figsize=(12, 6))
        
        # Filter out papers without abstracts
        df_with_abstracts = self.df[self.df['has_abstract']]
        
        plt.hist(df_with_abstracts['abstract_word_count'], bins=50, alpha=0.7, edgecolor='black')
        plt.title('Distribution of Abstract Word Counts', fontsize=16, fontweight='bold')
        plt.xlabel('Word Count')
        plt.ylabel('Number of Papers')
        plt.grid(True, alpha=0.3)
        
        # Add statistics
        mean_length = df_with_abstracts['abstract_word_count'].mean()
        median_length = df_with_abstracts['abstract_word_count'].median()
        
        plt.axvline(mean_length, color='red', linestyle='--', label=f'Mean: {mean_length:.1f}')
        plt.axvline(median_length, color='green', linestyle='--', label=f'Median: {median_length:.1f}')
        plt.legend()
        
        plt.tight_layout()
        plt.savefig(save_path, dpi=300, bbox_inches='tight')
        plt.show()
        
        return mean_length, median_length
    
    def comprehensive_analysis(self):
        """Run all analyses and generate report"""
        print("=== COMPREHENSIVE ANALYSIS REPORT ===")
        
        # Basic statistics
        print(f"Total papers in analysis: {len(self.df):,}")
        print(f"Date range: {self.df['publication_year'].min()} - {self.df['publication_year'].max()}")
        print(f"Papers with abstracts: {self.df['has_abstract'].sum():,} ({self.df['has_abstract'].mean()*100:.1f}%)")
        
        # Run all visualizations
        yearly_counts = self.plot_publications_over_time()
        journal_counts = self.plot_top_journals()
        source_counts = self.plot_source_distribution()
        mean_len, median_len = self.plot_abstract_length_distribution()
        self.generate_word_cloud()
        
        # Print key findings
        print("\n=== KEY FINDINGS ===")
        print(f"Peak publication year: {yearly_counts.idxmax()} with {yearly_counts.max():,} papers")
        print(f"Top journal: {journal_counts.index[0]} with {journal_counts.iloc[0]:,} papers")
        print(f"Top source: {source_counts.index[0]} with {source_counts.iloc[0]:,} papers")
        print(f"Average abstract length: {mean_len:.1f} words")
        print(f"Median abstract length: {median_len:.1f} words")

# Usage example
if __name__ == "__main__":
    # Load cleaned data
    cleaned_df = pd.read_csv('cleaned_metadata.csv')
    
    # Initialize visualizer
    visualizer = CORD19Visualizer(cleaned_df)
    
    # Run comprehensive analysis
    visualizer.comprehensive_analysis()
