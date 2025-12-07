import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from wordcloud import WordCloud
import numpy as np

# Set page configuration
st.set_page_config(
    page_title="CORD-19 Data Explorer",
    page_icon="🔬",
    layout="wide",
    initial_sidebar_state="expanded"
)

class CORD19App:
    def __init__(self):
        self.df = None
        
        self.load_data()
    
    def load_data(self):
        """Load the cleaned dataset"""
        try:
            self.df = pd.read_csv('cleaned_metadata.csv')
            # Convert publication_year to integer for filtering
            self.df['publication_year'] = self.df['publication_year'].astype(int)
        except FileNotFoundError:
            st.error("Cleaned data file not found. Please run the data cleaning script first.")
            st.stop()
    
    def setup_sidebar(self):
        """Setup sidebar with filters and controls"""
        st.sidebar.title("🔬 CORD-19 Explorer")
        st.sidebar.markdown("Explore COVID-19 research publications")
        
        # Year range filter
        min_year = int(self.df['publication_year'].min())
        max_year = int(self.df['publication_year'].max())
        
        st.sidebar.subheader("Publication Year Filter")
        year_range = st.sidebar.slider(
            "Select year range:",
            min_value=min_year,
            max_value=max_year,
            value=(min_year, max_year)
        )
        
        # Journal filter
        st.sidebar.subheader("Journal Filter")
        top_journals = self.df['journal'].value_counts().head(10).index.tolist()
        selected_journals = st.sidebar.multiselect(
            "Select journals:",
            options=top_journals,
            default=top_journals[:3] if top_journals else []
        )
        
        # Abstract availability filter
        st.sidebar.subheader("Abstract Filter")
        has_abstract = st.sidebar.radio(
            "Abstract availability:",
            options=['All', 'With Abstract', 'Without Abstract']
        )
        
        return year_range, selected_journals, has_abstract
    
    def apply_filters(self, year_range, selected_journals, has_abstract):
        """Apply filters to the dataset"""
        filtered_df = self.df.copy()
        
        # Apply year filter
        filtered_df = filtered_df[
            (filtered_df['publication_year'] >= year_range[0]) & 
            (filtered_df['publication_year'] <= year_range[1])
        ]
        
        # Apply journal filter
        if selected_journals:
            filtered_df = filtered_df[filtered_df['journal'].isin(selected_journals)]
        
        # Apply abstract filter
        if has_abstract == 'With Abstract':
            filtered_df = filtered_df[filtered_df['has_abstract'] == True]
        elif has_abstract == 'Without Abstract':
            filtered_df = filtered_df[filtered_df['has_abstract'] == False]
        
        return filtered_df
    
    def display_overview(self, filtered_df):
        """Display overview statistics"""
        st.title("CORD-19 Data Explorer")
        st.markdown("Simple exploration of COVID-19 research papers")
        
        # Key metrics
        col1, col2, col3, col4 = st.columns(4)
        
        with col1:
            st.metric("Total Papers", f"{len(filtered_df):,}")
        
        with col2:
            st.metric("Papers with Abstracts", 
                     f"{filtered_df['has_abstract'].sum():,}",
                     f"{filtered_df['has_abstract'].mean()*100:.1f}%")
        
        with col3:
            st.metric("Date Range", 
                     f"{filtered_df['publication_year'].min()}-{filtered_df['publication_year'].max()}")
        
        with col4:
            avg_abstract_len = filtered_df[filtered_df['has_abstract']]['abstract_word_count'].mean()
            st.metric("Avg Abstract Length", f"{avg_abstract_len:.1f} words")
    
    def plot_publications_chart(self, filtered_df):
        """Plot publications over time"""
        st.subheader("Publications Over Time")
        
        yearly_counts = filtered_df['publication_year'].value_counts().sort_index()
        
        fig, ax = plt.subplots(figsize=(10, 4))
        ax.plot(yearly_counts.index, yearly_counts.values, marker='o', linewidth=2)
        ax.set_title('Publications by Year')
        ax.set_xlabel('Year')
        ax.set_ylabel('Number of Publications')
        ax.grid(True, alpha=0.3)
        
        st.pyplot(fig)
    
    def plot_top_journals_chart(self, filtered_df):
        """Plot top journals"""
        st.subheader("Top Publishing Journals")
        
        journal_counts = filtered_df['journal'].value_counts().head(10)
        
        fig, ax = plt.subplots(figsize=(10, 5))
        journal_counts.plot(kind='barh', ax=ax)
        ax.set_title('Top 10 Journals')
        ax.set_xlabel('Number of Publications')
        
        st.pyplot(fig)
    
    def generate_word_cloud_chart(self, filtered_df):
        """Generate word cloud"""
        st.subheader("Word Cloud - Paper Titles")
        
        text = ' '.join(filtered_df['title'].dropna().astype(str))
        
        if text.strip():
            wordcloud = WordCloud(width=800, height=400, 
                                background_color='white',
                                max_words=100,
                                colormap='viridis').generate(text)
            
            fig, ax = plt.subplots(figsize=(10, 5))
            ax.imshow(wordcloud, interpolation='bilinear')
            ax.axis('off')
            ax.set_title('Most Frequent Words in Titles')
            
            st.pyplot(fig)
        else:
            st.info("No data available for word cloud generation.")
    
    def show_data_sample(self, filtered_df):
        """Show sample of the data"""
        st.subheader("Sample Data")
        
        # Select columns to display
        display_columns = ['title', 'journal', 'publication_year', 'abstract_word_count', 'source_x']
        available_columns = [col for col in display_columns if col in filtered_df.columns]
        
        if available_columns:
            st.dataframe(
                filtered_df[available_columns].head(100),
                use_container_width=True,
                height=400
            )
        else:
            st.warning("No columns available to display.")
    
    def run(self):
        """Run the Streamlit application"""
        # Setup sidebar and get filters
        year_range, selected_journals, has_abstract = self.setup_sidebar()
        
        # Apply filters
        filtered_df = self.apply_filters(year_range, selected_journals, has_abstract)
        
        # Display overview
        self.display_overview(filtered_df)
        
        # Create two columns for charts
        col1, col2 = st.columns(2)
        
        with col1:
            self.plot_publications_chart(filtered_df)
            self.plot_top_journals_chart(filtered_df)
        
        with col2:
            self.generate_word_cloud_chart(filtered_df)
            
            # Additional statistics
            st.subheader("Quick Statistics")
            if not filtered_df.empty:
                st.write(f"**Year Range:** {filtered_df['publication_year'].min()} - {filtered_df['publication_year'].max()}")
                st.write(f"**Total Journals:** {filtered_df['journal'].nunique()}")
                st.write(f"**Average Title Length:** {filtered_df['title_word_count'].mean():.1f} words")
                st.write(f"**Most Common Source:** {filtered_df['source_x'].mode().iloc[0] if not filtered_df['source_x'].mode().empty else 'N/A'}")
        
        # Show data sample
        self.show_data_sample(filtered_df)
        
        # Footer
        st.markdown("---")
        st.markdown(
            "**CORD-19 Dataset** | COVID-19 Open Research Dataset Challenge "
            "| Created for educational purposes"
        )

# Run the app
if __name__ == "__main__":
    app = CORD19App()
    app.run()
