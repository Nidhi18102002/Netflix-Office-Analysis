# netflix_analysis_with_names.py
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import matplotlib.patches as patches

print("🎬 NETFLIX MOVIES ANALYSIS - WITH MOVIE NAMES")
print("=" * 60)

# Step 1: Create initial data dictionary
print("\n📊 Step 1: Creating initial friend's data...")
netflix_df_dict = {
    "Year": [2011, 2012, 2013, 2014, 2015, 2016, 2017, 2018, 2019, 2020, 2021],
    "Duration": [103, 101, 99, 100, 100, 95, 95, 96, 93, 90, 88]
}
durations_df = pd.DataFrame(netflix_df_dict)
print("✓ Initial data dictionary created")

# Step 2: Load and process the full dataset
print(f"\n📁 Step 2: Loading and processing Netflix dataset...")
netflix_df = pd.read_csv('../data/netflix_data.csv')
netflix_movies = netflix_df[netflix_df['type'] == 'Movie'].copy()

# Extract numeric duration and clean data
netflix_movies['duration_min'] = netflix_movies['duration'].str.extract('(\d+)').astype(float)
netflix_movies = netflix_movies.dropna(subset=['duration_min'])

# Create subset with relevant columns
movie_columns = ['title', 'country', 'listed_in', 'release_year', 'duration_min']
netflix_movies_subset = netflix_movies[movie_columns].copy()

print(f"✓ {len(netflix_movies_subset)} movies processed")

# Step 3: Assign colors based on genre
def assign_color(genre_string):
    if pd.isna(genre_string):
        return 'black'
    genre_lower = str(genre_string).lower()
    if 'children' in genre_lower or 'kids' in genre_lower:
        return 'red'
    elif 'documentaries' in genre_lower:
        return 'blue'  
    elif 'stand-up' in genre_lower:
        return 'green'
    else:
        return 'black'

netflix_movies_subset['color'] = netflix_movies_subset['listed_in'].apply(assign_color)

# Step 4: Prepare trend analysis data
modern_movies = netflix_movies_subset[netflix_movies_subset['release_year'] >= 2000]
yearly_avg = modern_movies.groupby('release_year')['duration_min'].agg(['mean', 'count']).round(1)
yearly_avg = yearly_avg[yearly_avg['count'] >= 5]

# Step 5: Short movies analysis
short_movies = netflix_movies_subset[netflix_movies_subset['duration_min'] < 60]
short_movies['primary_genre'] = short_movies['listed_in'].str.split(',').str[0].str.strip()
genre_counts = short_movies['primary_genre'].value_counts().head(8)

# Step 6: Find notable movies for annotation
# Longest and shortest movies
longest_movie = netflix_movies_subset.loc[netflix_movies_subset['duration_min'].idxmax()]
shortest_movie = netflix_movies_subset.loc[netflix_movies_subset['duration_min'].idxmin()]

# Sample of interesting short movies
interesting_short = short_movies.head(5)

# Recent popular movies (2015+)
recent_movies = netflix_movies_subset[netflix_movies_subset['release_year'] >= 2015]
sample_recent = recent_movies.sample(n=min(5, len(recent_movies)), random_state=42)

print(f"✓ Data processing complete. Creating visualization with movie names...")

# =============================================================================
# CREATE COMBINED FIGURE WITH ALL PLOTS AND MOVIE NAMES
# =============================================================================

# Create a figure optimized for single page
fig = plt.figure(figsize=(14, 10))
fig.suptitle('Netflix Movies Analysis - Complete Overview', fontsize=10, y=0.98)

# Plot 1: Friend's Initial Data (Top Left)
ax1 = plt.subplot(3, 2, 1)
ax1.plot(durations_df['Year'], durations_df['Duration'], marker='o', linewidth=2, 
         markersize=6, color='red', markerfacecolor='darkred', markeredgecolor='white', markeredgewidth=1)
ax1.set_xlabel('Release Year', fontsize=10)
ax1.set_ylabel('Duration (minutes)', fontsize=10)
ax1.set_title('1. Friend\'s Initial Data (2011-2021)', fontsize=10, color='darkred')
ax1.grid(True, alpha=0.3)
ax1.set_ylim(85, 105)
ax1.tick_params(labelsize=8)

# Plot 2: All Movies with Notable Examples Annotated (Top Right)
ax2 = plt.subplot(3, 2, 2)
scatter1 = ax2.scatter(netflix_movies_subset['release_year'], 
                      netflix_movies_subset['duration_min'], 
                      alpha=0.4, s=8, color='steelblue', edgecolors='none')
ax2.set_xlabel('Release Year', fontsize=10)
ax2.set_ylabel('Duration (minutes)', fontsize=10)
ax2.set_title('2. All Netflix Movies (Notable Examples)', fontsize=10, color='steelblue')
ax2.grid(True, alpha=0.3)
ax2.set_ylim(0, 220)
ax2.tick_params(labelsize=8)

# Annotate longest and shortest movies
ax2.annotate(f'Longest: {longest_movie["title"][:20]}...\n({longest_movie["duration_min"]:.0f} min)', 
            (longest_movie['release_year'], longest_movie['duration_min']),
            xytext=(10, 10), textcoords='offset points', fontsize=7, 
            bbox=dict(boxstyle='round,pad=0.3', facecolor='yellow', alpha=0.7),
            arrowprops=dict(arrowstyle='->', color='black', lw=0.5))

ax2.annotate(f'Shortest: {shortest_movie["title"][:20]}...\n({shortest_movie["duration_min"]:.0f} min)', 
            (shortest_movie['release_year'], shortest_movie['duration_min']),
            xytext=(10, -15), textcoords='offset points', fontsize=7,
            bbox=dict(boxstyle='round,pad=0.3', facecolor='lightblue', alpha=0.7),
            arrowprops=dict(arrowstyle='->', color='black', lw=0.5))

# Plot 3: Color-Coded by Genre with Examples (Middle Left)
ax3 = plt.subplot(3, 2, 3)
colors = netflix_movies_subset['color']
scatter2 = ax3.scatter(netflix_movies_subset['release_year'], 
                      netflix_movies_subset['duration_min'], 
                      c=colors, alpha=0.6, s=12, edgecolors='black', linewidth=0.1)
ax3.set_xlabel('Release Year', fontsize=10)
ax3.set_ylabel('Duration (minutes)', fontsize=10)
ax3.set_title('3. Movies by Genre (Examples Shown)', fontsize=10, color='purple')

# Add legend for color coding
legend_elements = [
    patches.Patch(color='red', label='Children & Family'),
    patches.Patch(color='blue', label='Documentaries'), 
    patches.Patch(color='green', label='Stand-Up'),
    patches.Patch(color='black', label='Other')
]
ax3.legend(handles=legend_elements, loc='upper right', fontsize=8)
ax3.grid(True, alpha=0.3)
ax3.set_ylim(0, 220)
ax3.tick_params(labelsize=8)

# Annotate some genre examples
children_example = netflix_movies_subset[netflix_movies_subset['color'] == 'red'].head(1)
if len(children_example) > 0:
    ex = children_example.iloc[0]
    ax3.annotate(f'Children: {ex["title"][:15]}...', 
                (ex['release_year'], ex['duration_min']),
                xytext=(5, 5), textcoords='offset points', fontsize=7,
                bbox=dict(boxstyle='round,pad=0.2', facecolor='red', alpha=0.3))

doc_example = netflix_movies_subset[netflix_movies_subset['color'] == 'blue'].head(1)
if len(doc_example) > 0:
    ex = doc_example.iloc[0]
    ax3.annotate(f'Documentary: {ex["title"][:15]}...', 
                (ex['release_year'], ex['duration_min']),
                xytext=(5, -15), textcoords='offset points', fontsize=7,
                bbox=dict(boxstyle='round,pad=0.2', facecolor='blue', alpha=0.3))

# Plot 4: Duration Trend Over Time (Middle Right)
ax4 = plt.subplot(3, 2, 4)
ax4.plot(yearly_avg.index, yearly_avg['mean'], marker='o', linewidth=2, 
         markersize=5, color='darkgreen', markerfacecolor='lightgreen', 
         markeredgecolor='darkgreen', markeredgewidth=1)
ax4.set_xlabel('Release Year', fontsize=10)
ax4.set_ylabel('Average Duration (minutes)', fontsize=10)
ax4.set_title('4. Average Duration Trend (2000+)', fontsize=10, color='darkgreen')
ax4.grid(True, alpha=0.3)
ax4.tick_params(labelsize=8)

# Add trend line
z = np.polyfit(yearly_avg.index, yearly_avg['mean'], 1)
p = np.poly1d(z)
ax4.plot(yearly_avg.index, p(yearly_avg.index), "--", color='red', alpha=0.8, linewidth=1.5, 
         label=f'Trend: {z[0]:.1f} min/year')
ax4.legend(fontsize=8)

# Plot 5: Short Movies by Genre with Examples (Bottom Left)
ax5 = plt.subplot(3, 2, 5)
bars = ax5.bar(range(len(genre_counts)), genre_counts.values, 
               color=['#FF6B6B', '#4ECDC4', '#45B7D1', '#96CEB4', '#FECA57', '#FF9FF3', '#54A0FF', '#5F27CD'])
ax5.set_xlabel('Genre', fontsize=10)
ax5.set_ylabel('Number of Short Movies', fontsize=10)
ax5.set_title('5. Short Movies (< 60 min) with Examples', fontsize=10, color='darkorange')
ax5.set_xticks(range(len(genre_counts)))
ax5.set_xticklabels([label[:12] + '...' if len(label) > 12 else label for label in genre_counts.index], 
                    rotation=45, ha='right', fontsize=8)
ax5.grid(True, alpha=0.3, axis='y')
ax5.tick_params(labelsize=8)

# Add value labels and example movie names
for i, (bar, genre) in enumerate(zip(bars, genre_counts.index)):
    height = bar.get_height()
    ax5.text(bar.get_x() + bar.get_width()/2., height + 0.5,
             f'{int(height)}', ha='center', va='bottom', fontsize=8)
    
    # Add example movie for this genre
    genre_examples = short_movies[short_movies['primary_genre'] == genre]['title'].head(1)
    if len(genre_examples) > 0:
        example_title = genre_examples.iloc[0]
        ax5.text(bar.get_x() + bar.get_width()/2., height/2,
                f'{example_title[:10]}...', ha='center', va='center', fontsize=6,
                rotation=90, color='white', weight='bold')

# Plot 6: Recent Movies Examples (Bottom Right)
ax6 = plt.subplot(3, 2, 6)

# Show recent movies with their names
recent_colors = [assign_color(listed) for listed in sample_recent['listed_in']]
scatter6 = ax6.scatter(sample_recent['release_year'], sample_recent['duration_min'], 
                      c=recent_colors, s=100, alpha=0.8, edgecolors='black', linewidth=1)

ax6.set_xlabel('Release Year', fontsize=10)
ax6.set_ylabel('Duration (minutes)', fontsize=10)
ax6.set_title('6. Recent Movies Examples (2015+)', fontsize=10, color='purple')
ax6.grid(True, alpha=0.3)
ax6.tick_params(labelsize=8)

# Annotate each recent movie
for _, movie in sample_recent.iterrows():
    ax6.annotate(f'{movie["title"][:15]}...\n({movie["duration_min"]:.0f}m)', 
                (movie['release_year'], movie['duration_min']),
                xytext=(5, 5), textcoords='offset points', fontsize=6,
                bbox=dict(boxstyle='round,pad=0.2', facecolor='yellow', alpha=0.6),
                ha='left')

# Adjust layout to fit in one page
plt.tight_layout()
plt.subplots_adjust(top=0.93, hspace=0.4, wspace=0.4)

# Show the combined plot
plt.show()

# =============================================================================
# ANALYSIS SUMMARY WITH MOVIE NAMES
# =============================================================================

print(f"\n🎯 COMPREHENSIVE ANALYSIS WITH MOVIE EXAMPLES:")
print("=" * 60)

# Statistical analysis
if len(yearly_avg) > 5:
    recent_years = yearly_avg.index[-5:]
    early_years = yearly_avg.index[:5]
    
    avg_early = yearly_avg.loc[early_years, 'mean'].mean()
    avg_recent = yearly_avg.loc[recent_years, 'mean'].mean()
    
    print(f"📊 Duration Trend Analysis:")
    print(f"  Early period ({early_years[0]}-{early_years[-1]}): {avg_early:.1f} minutes")
    print(f"  Recent period ({recent_years[0]}-{recent_years[-1]}): {avg_recent:.1f} minutes")
    print(f"  Change: {avg_recent - avg_early:+.1f} minutes")
    
    if avg_recent < avg_early:
        print(f"  ✅ CONCLUSION: Movies ARE getting shorter over time!")
    else:
        print(f"  ❌ CONCLUSION: Movies are NOT getting shorter over time")

print(f"\n🎬 Notable Movie Examples:")
print(f"  Longest movie: '{longest_movie['title']}' ({longest_movie['duration_min']:.0f} min, {longest_movie['release_year']})")
print(f"  Shortest movie: '{shortest_movie['title']}' ({shortest_movie['duration_min']:.0f} min, {shortest_movie['release_year']})")

print(f"\n📋 Short Movie Examples (< 60 minutes):")
for _, movie in interesting_short.iterrows():
    genre = movie['primary_genre']
    print(f"  • '{movie['title']}' ({movie['duration_min']:.0f} min) - {genre}")

print(f"\n🆕 Recent Movie Examples (2015+):")
for _, movie in sample_recent.iterrows():
    print(f"  • '{movie['title']}' ({movie['release_year']}) - {movie['duration_min']:.0f} min")

print(f"\n📈 Key Findings:")
print(f"  • Total movies analyzed: {len(netflix_movies_subset):,}")
print(f"  • Short movies (< 60 min): {len(short_movies)} ({len(short_movies)/len(netflix_movies_subset)*100:.1f}%)")
print(f"  • Duration range: {netflix_movies_subset['duration_min'].min():.0f} - {netflix_movies_subset['duration_min'].max():.0f} minutes")
print(f"  • Average duration: {netflix_movies_subset['duration_min'].mean():.1f} minutes")

print(f"\n✅ Analysis with movie names completed!")
print("=" * 60)