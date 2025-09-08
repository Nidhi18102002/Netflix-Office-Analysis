# powerbi_data_preparation.py
import pandas as pd
import numpy as np

print("📊 PREPARING DATA FOR POWER BI & TABLEAU")
print("=" * 50)

# Load Netflix data
netflix_df = pd.read_csv('../data/netflix_data.csv')
netflix_movies = netflix_df[netflix_df['type'] == 'Movie'].copy()

# Clean and prepare Netflix data
netflix_movies['duration_min'] = netflix_movies['duration'].str.extract('(\d+)').astype(float)
netflix_movies = netflix_movies.dropna(subset=['duration_min'])

# Add derived columns for better BI visualization
netflix_movies['is_short_movie'] = netflix_movies['duration_min'] < 60
netflix_movies['decade'] = (netflix_movies['release_year'] // 10) * 10

# Categorize genres
def categorize_genre(genre_string):
    if pd.isna(genre_string):
        return 'Unknown'
    genre_lower = str(genre_string).lower()
    if 'children' in genre_lower:
        return 'Children & Family'
    elif 'documentaries' in genre_lower:
        return 'Documentaries'
    elif 'stand-up' in genre_lower:
        return 'Stand-Up Comedy'
    elif 'drama' in genre_lower:
        return 'Drama'
    elif 'comedy' in genre_lower:
        return 'Comedy'
    else:
        return 'Other'

netflix_movies['genre_category'] = netflix_movies['listed_in'].apply(categorize_genre)

# Duration categories
netflix_movies['duration_category'] = netflix_movies['duration_min'].apply(lambda x:
    'Very Short (< 60)' if x < 60 else
    'Short (60-90)' if x < 90 else
    'Medium (90-120)' if x < 120 else
    'Long (120+)')

# Save for Power BI/Tableau
netflix_powerbi = netflix_movies[[
    'title', 'release_year', 'duration_min', 'genre_category', 
    'is_short_movie', 'decade', 'duration_category', 'country', 'rating'
]].copy()

netflix_powerbi.to_csv('../data/netflix_powerbi.csv', index=False)
print(f"✓ Netflix data prepared: {len(netflix_powerbi)} movies")

# Load and prepare Office data
office_df = pd.read_csv('../data/office_data.csv')

if 'Unnamed: 0' in office_df.columns:
    office_df['episode_number'] = office_df['Unnamed: 0'] + 1
else:
    office_df['episode_number'] = range(1, len(office_df) + 1)

# Prepare Office data for BI
office_df['has_guest_stars'] = office_df['GuestStars'].notna()
office_df['scaled_rating'] = (office_df['Ratings'] - office_df['Ratings'].min()) / (office_df['Ratings'].max() - office_df['Ratings'].min())

# Rating categories
office_df['rating_category'] = office_df['scaled_rating'].apply(lambda x:
    'Low' if x < 0.25 else
    'Medium-Low' if x < 0.50 else
    'Medium-High' if x < 0.75 else
    'High')

# Viewership categories  
office_df['viewership_category'] = office_df['Viewership'].apply(lambda x:
    'Low (< 5M)' if x < 5 else
    'Medium (5-8M)' if x < 8 else
    'High (8M+)')

office_powerbi = office_df[[
    'episode_number', 'Season', 'EpisodeTitle', 'Ratings', 'Viewership',
    'has_guest_stars', 'rating_category', 'viewership_category', 'GuestStars'
]].copy()

office_powerbi.to_csv('../data/office_powerbi.csv', index=False)
print(f"✓ Office data prepared: {len(office_powerbi)} episodes")

print("\n✅ Data preparation complete!")
print("Files created:")
print("  - ../data/netflix_powerbi.csv")
print("  - ../data/office_powerbi.csv")
print("\n🚀 Ready for Power BI and Tableau!")