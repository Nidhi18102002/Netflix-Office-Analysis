# examine_data.py
# Copy this entire code into a new file called 'examine_data.py'
import pandas as pd
import matplotlib.pyplot as plt

print("=== EXAMINING YOUR DOWNLOADED DATASETS ===\n")

# =============================================
# NETFLIX DATASET EXAMINATION
# =============================================
try:
    print("📽️ NETFLIX DATASET")
    print("-" * 50)
    
    # Load Netflix data
    netflix_df = pd.read_csv('../data/netflix_data.csv')
    
    print(f"✓ Shape: {netflix_df.shape}")
    print(f"✓ Columns: {list(netflix_df.columns)}")
    
    # Check data types and missing values
    print(f"\n📊 Data Info:")
    print(netflix_df.info())
    
    print(f"\n🎬 Content Types:")
    print(netflix_df['type'].value_counts())
    
    print(f"\n📅 Release Year Range:")
    if 'release_year' in netflix_df.columns:
        print(f"From {netflix_df['release_year'].min()} to {netflix_df['release_year'].max()}")
    
    print(f"\n🎭 Top Genres:")
    if 'listed_in' in netflix_df.columns:
        # Get top 5 most common genres
        genres = netflix_df['listed_in'].str.split(', ').explode().value_counts().head()
        print(genres)
    
    print(f"\n🎞️ Sample Movies (first 3):")
    movies = netflix_df[netflix_df['type'] == 'Movie'].head(3)
    for _, movie in movies.iterrows():
        print(f"- {movie['title']} ({movie['release_year']}) - {movie['duration']}")
    
    print(f"\n📺 Sample TV Shows (first 3):")
    tv_shows = netflix_df[netflix_df['type'] == 'TV Show'].head(3)
    for _, show in tv_shows.iterrows():
        print(f"- {show['title']} ({show['release_year']}) - {show['duration']}")

except FileNotFoundError:
    print("❌ netflix_data.csv not found!")
    print("Make sure you renamed 'netflix_titles.csv' to 'netflix_data.csv'")
except Exception as e:
    print(f"❌ Error loading Netflix data: {e}")

print("\n" + "="*70 + "\n")

# =============================================
# THE OFFICE DATASET EXAMINATION  
# =============================================
try:
    print("🏢 THE OFFICE DATASET")
    print("-" * 50)
    
    # Load Office data
    office_df = pd.read_csv('../data/office_data.csv')
    
    print(f"✓ Shape: {office_df.shape}")
    print(f"✓ Columns: {list(office_df.columns)}")
    
    # Check data types and missing values
    print(f"\n📊 Data Info:")
    print(office_df.info())
    
    print(f"\n📺 Episodes per Season:")
    if 'Season' in office_df.columns:
        print(office_df['Season'].value_counts().sort_index())
    
    print(f"\n⭐ Ratings Range:")
    rating_col = None
    for col in ['Ratings', 'ratings', 'rating', 'imdb_rating']:
        if col in office_df.columns:
            rating_col = col
            break
    
    if rating_col:
        print(f"From {office_df[rating_col].min()} to {office_df[rating_col].max()}")
        print(f"Average: {office_df[rating_col].mean():.2f}")
    
    print(f"\n👥 Guest Stars Info:")
    guest_col = None
    for col in ['GuestStars', 'guest_stars', 'Guest Stars']:
        if col in office_df.columns:
            guest_col = col
            break
    
    if guest_col:
        has_guests = office_df[guest_col].notna().sum()
        print(f"Episodes with guest stars: {has_guests}")
        print(f"Episodes without guests: {len(office_df) - has_guests}")
        
        if has_guests > 0:
            print(f"\nSample guest stars:")
            guest_episodes = office_df[office_df[guest_col].notna()].head(3)
            for _, ep in guest_episodes.iterrows():
                episode_col = 'EpisodeNumber' if 'EpisodeNumber' in office_df.columns else 'episode_number'
                if episode_col in office_df.columns:
                    print(f"- Episode {ep[episode_col]}: {ep[guest_col]}")
    
    print(f"\n📈 Viewership Info:")
    viewership_col = None
    for col in ['Viewership', 'viewership', 'viewership_mil', 'Viewership_mil']:
        if col in office_df.columns:
            viewership_col = col
            break
    
    if viewership_col:
        print(f"Average viewership: {office_df[viewership_col].mean():.2f}")
        print(f"Highest: {office_df[viewership_col].max()}")
        print(f"Lowest: {office_df[viewership_col].min()}")
    
    print(f"\n📋 First 3 episodes:")
    print(office_df.head(3))

except FileNotFoundError:
    print("❌ office_data.csv not found!")
    print("Make sure you renamed 'the_office_series.csv' to 'office_data.csv'")
except Exception as e:
    print(f"❌ Error loading Office data: {e}")

print("\n" + "="*70)
print("🎯 NEXT STEPS:")
print("1. If both datasets loaded successfully, you're ready to start!")
print("2. If there are errors, check file names and locations")
print("3. Run the Netflix analysis script next")
print("="*70)