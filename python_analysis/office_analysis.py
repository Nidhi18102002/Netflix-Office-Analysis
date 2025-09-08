# office_analysis_with_names.py
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
from matplotlib.lines import Line2D
import matplotlib.patches as patches

print("🏢 THE OFFICE ANALYSIS - WITH EPISODE NAMES")
print("=" * 55)

# Step 1: Load and prepare data
print("\n📁 Step 1: Loading and preparing The Office dataset...")
office_df = pd.read_csv('../data/office_data.csv')

# Create episode number column
if 'Unnamed: 0' in office_df.columns:
    office_df['episode_number'] = office_df['Unnamed: 0'] + 1
else:
    office_df['episode_number'] = range(1, len(office_df) + 1)

# Set up guest stars analysis
guest_col = 'GuestStars'
has_guest_col = 'has_guest'
office_df[has_guest_col] = office_df[guest_col].notna()

# Scale ratings for color coding
min_rating = office_df['Ratings'].min()
max_rating = office_df['Ratings'].max()
office_df['scaled_rating'] = (office_df['Ratings'] - min_rating) / (max_rating - min_rating)

# Define color and size mapping functions
def get_rating_color(scaled_rating):
    if scaled_rating < 0.25:
        return 'red'
    elif scaled_rating < 0.50:
        return 'orange'
    elif scaled_rating < 0.75:
        return 'lightgreen'
    else:
        return 'darkgreen'

def get_marker_size(has_guest):
    return 180 if has_guest else 20  # Reduced sizes for better page fit

# Apply mappings
office_df['color'] = office_df['scaled_rating'].apply(get_rating_color)
office_df['marker_size'] = office_df[has_guest_col].apply(get_marker_size)

print(f"✓ Dataset processed: {len(office_df)} episodes")
print(f"✓ Episodes with guest stars: {office_df[has_guest_col].sum()}")

# Find notable episodes for annotation
most_watched = office_df.loc[office_df['Viewership'].idxmax()]
highest_rated = office_df.loc[office_df['Ratings'].idxmax()]
guest_episodes = office_df[office_df[has_guest_col] == True]
most_watched_guest = guest_episodes.loc[guest_episodes['Viewership'].idxmax()] if len(guest_episodes) > 0 else None
top_5_episodes = office_df.nlargest(5, 'Viewership')

# =============================================================================
# CREATE COMBINED FIGURE WITH EPISODE NAMES
# =============================================================================

# Create a figure optimized for single page
fig = plt.figure(figsize=(14, 10))
fig.suptitle('The Office Analysis - Complete Overview with Episode Names', fontsize=10, y=0.98)

# Plot 1: Main Project Visualization with Episode Names (Top - spans 2 columns)
ax1 = plt.subplot(3, 2, (1, 2))
scatter = ax1.scatter(office_df['episode_number'], 
                     office_df['Viewership'], 
                     c=office_df['color'], 
                     s=office_df['marker_size'],
                     alpha=0.7,
                     edgecolors='black',
                     linewidth=0.3)

ax1.set_title("Popularity, Quality, and Guest Appearances on the Office", 
              fontsize=10, pad=15, color='navy')
ax1.set_xlabel("Episode Number", fontsize=10)
ax1.set_ylabel("Viewership (Millions)", fontsize=10)
ax1.tick_params(labelsize=8)

# Annotate top episodes with names
for i, (_, ep) in enumerate(top_5_episodes.iterrows()):
    if i < 3:  # Only annotate top 3 to avoid clutter
        guest_indicator = "👥" if ep[has_guest_col] else ""
        ax1.annotate(f'{ep["EpisodeTitle"][:20]}...\n{guest_indicator}({ep["Viewership"]:.1f}M)', 
                    (ep['episode_number'], ep['Viewership']),
                    xytext=(5, 5 + i*15), textcoords='offset points', fontsize=7,
                    bbox=dict(boxstyle='round,pad=0.3', facecolor='yellow', alpha=0.7),
                    arrowprops=dict(arrowstyle='->', color='black', lw=0.5))

# Create legend for main plot
legend_elements = [
    Line2D([0], [0], marker='o', color='w', markerfacecolor='red', 
           markersize=6, label='Rating < 0.25', markeredgecolor='black'),
    Line2D([0], [0], marker='o', color='w', markerfacecolor='orange', 
           markersize=6, label='0.25 ≤ Rating < 0.50', markeredgecolor='black'),
    Line2D([0], [0], marker='o', color='w', markerfacecolor='lightgreen', 
           markersize=6, label='0.50 ≤ Rating < 0.75', markeredgecolor='black'),
    Line2D([0], [0], marker='o', color='w', markerfacecolor='darkgreen', 
           markersize=6, label='Rating ≥ 0.75', markeredgecolor='black'),
    Line2D([0], [0], marker='o', color='w', markerfacecolor='gray', 
           markersize=8, label='With Guest', markeredgecolor='black'),
    Line2D([0], [0], marker='o', color='w', markerfacecolor='gray', 
           markersize=3, label='No Guest', markeredgecolor='black')
]
ax1.legend(handles=legend_elements, loc='upper right', fontsize=8)
ax1.grid(True, alpha=0.3)

# Plot 2: Viewership by Season with Notable Episodes (Middle Left)
ax2 = plt.subplot(3, 2, 3)
season_stats = office_df.groupby('Season').agg({
    'Viewership': ['mean', 'max'],
    'EpisodeTitle': 'first'
}).round(2)

season_viewership = season_stats[('Viewership', 'mean')]
season_colors = plt.cm.viridis(np.linspace(0, 1, len(season_viewership)))

bars2 = ax2.bar(season_viewership.index, season_viewership.values, 
                color=season_colors, alpha=0.8, edgecolor='black', linewidth=0.5)
ax2.set_xlabel('Season', fontsize=10)
ax2.set_ylabel('Average Viewership (Millions)', fontsize=10)
ax2.set_title('2. Average Viewership by Season', fontsize=10, color='darkblue')
ax2.grid(True, alpha=0.3, axis='y')
ax2.tick_params(labelsize=8)

# Add value labels on bars
for bar in bars2:
    height = bar.get_height()
    ax2.text(bar.get_x() + bar.get_width()/2., height + 0.1,
             f'{height:.1f}', ha='center', va='bottom', fontsize=8)

# Plot 3: Guest Stars Impact with Examples (Middle Right)
ax3 = plt.subplot(3, 2, 4)
guest_stats = office_df.groupby(has_guest_col).agg({
    'Viewership': 'mean',
    'Ratings': 'mean'
}).round(2)

categories = ['No Guests', 'With Guests']
viewership_means = [guest_stats.loc[False, 'Viewership'], guest_stats.loc[True, 'Viewership']]
rating_means = [guest_stats.loc[False, 'Ratings'], guest_stats.loc[True, 'Ratings']]

x_pos = np.arange(len(categories))
width = 0.35

# Create dual y-axis
ax3_twin = ax3.twinx()

bars3_1 = ax3.bar(x_pos - width/2, viewership_means, width, 
                  label='Viewership', color='steelblue', alpha=0.8)
bars3_2 = ax3_twin.bar(x_pos + width/2, rating_means, width, 
                       label='Rating', color='orange', alpha=0.8)

ax3.set_xlabel('Episode Type', fontsize=10)
ax3.set_ylabel('Avg Viewership (M)', fontsize=10, color='steelblue')
ax3_twin.set_ylabel('Avg Rating', fontsize=10, color='orange')
ax3.set_title('3. Guest Stars Impact', fontsize=10, color='purple')
ax3.set_xticks(x_pos)
ax3.set_xticklabels(categories)
ax3.grid(True, alpha=0.3)
ax3.tick_params(labelsize=8)
ax3_twin.tick_params(labelsize=8)

# Add value labels
for i, (bar1, bar2) in enumerate(zip(bars3_1, bars3_2)):
    ax3.text(bar1.get_x() + bar1.get_width()/2., bar1.get_height() + 0.1,
             f'{viewership_means[i]:.1f}M', ha='center', va='bottom', fontsize=8)
    ax3_twin.text(bar2.get_x() + bar2.get_width()/2., bar2.get_height() + 0.05,
                  f'{rating_means[i]:.1f}', ha='center', va='bottom', fontsize=8)

# Plot 4: Top Episodes with Names (Bottom Left)
ax4 = plt.subplot(3, 2, 5)
top_episodes_plot = office_df.nlargest(8, 'Viewership')

# Create horizontal bar chart for better name visibility
y_pos = np.arange(len(top_episodes_plot))
colors_top = ['red' if guest else 'blue' for guest in top_episodes_plot[has_guest_col]]

bars4 = ax4.barh(y_pos, top_episodes_plot['Viewership'], color=colors_top, alpha=0.8, edgecolor='black', linewidth=0.5)

# Customize episode names
episode_labels = []
for _, ep in top_episodes_plot.iterrows():
    guest_marker = "👥" if ep[has_guest_col] else "👤"
    label = f"E{ep['episode_number']} {ep['EpisodeTitle'][:15]}... {guest_marker}"
    episode_labels.append(label)

ax4.set_yticks(y_pos)
ax4.set_yticklabels(episode_labels, fontsize=7)
ax4.set_xlabel('Viewership (Millions)', fontsize=10)
ax4.set_title('4. Top Episodes with Names', fontsize=10, color='darkgreen')
ax4.grid(True, alpha=0.3, axis='x')
ax4.tick_params(labelsize=8)

# Add viewership values
for i, (bar, viewership) in enumerate(zip(bars4, top_episodes_plot['Viewership'])):
    ax4.text(bar.get_width() + 0.1, bar.get_y() + bar.get_height()/2,
             f'{viewership:.1f}M', ha='left', va='center', fontsize=7)

# Plot 5: Guest Stars Analysis with Names (Bottom Right)
ax5 = plt.subplot(3, 2, 6)

# Show guest star episodes with their names
if len(guest_episodes) > 0:
    top_guest_episodes = guest_episodes.nlargest(6, 'Viewership')
    
    # Create scatter plot
    scatter5 = ax5.scatter(top_guest_episodes['episode_number'], 
                          top_guest_episodes['Viewership'], 
                          c='red', s=80, alpha=0.8, edgecolors='black', linewidth=0.5)
    
    ax5.set_xlabel('Episode Number', fontsize=10)
    ax5.set_ylabel('Viewership (Millions)', fontsize=10)
    ax5.set_title('5. Top Guest Star Episodes', fontsize=10, color='maroon')
    ax5.grid(True, alpha=0.3)
    ax5.tick_params(labelsize=8)
    
    # Annotate guest episodes with guest names
    for i, (_, ep) in enumerate(top_guest_episodes.iterrows()):
        if i < 4:  # Only show top 4 to avoid clutter
            guest_names = str(ep[guest_col]).split(',')[0].strip() if pd.notna(ep[guest_col]) else "Guest"
            ax5.annotate(f'{ep["EpisodeTitle"][:12]}...\n{guest_names[:15]}...', 
                        (ep['episode_number'], ep['Viewership']),
                        xytext=(5, 5 + i*8), textcoords='offset points', fontsize=6,
                        bbox=dict(boxstyle='round,pad=0.2', facecolor='lightcoral', alpha=0.7),
                        arrowprops=dict(arrowstyle='->', color='black', lw=0.3))

# Adjust layout to fit in one page
plt.tight_layout()
plt.subplots_adjust(top=0.93, hspace=0.4, wspace=0.4)
plt.show()

# =============================================================================
# DETAILED ANALYSIS RESULTS WITH NAMES
# =============================================================================

print(f"\n🎯 COMPREHENSIVE ANALYSIS WITH EPISODE NAMES:")
print("=" * 55)

# Find most watched episodes
most_watched = office_df.loc[office_df['Viewership'].idxmax()]
guest_episodes = office_df[office_df[has_guest_col] == True]

print(f"🏆 Most Watched Episode Overall:")
print(f"  Episode {most_watched['episode_number']}: '{most_watched['EpisodeTitle']}'")
print(f"  Season {most_watched['Season']} | {most_watched['Viewership']} million viewers")
print(f"  Rating: {most_watched['Ratings']} | Has guests: {most_watched[has_guest_col]}")

if len(guest_episodes) > 0:
    most_watched_guest = guest_episodes.loc[guest_episodes['Viewership'].idxmax()]
    print(f"\n⭐ Most Watched Episode WITH Guest Stars:")
    print(f"  Episode {most_watched_guest['episode_number']}: '{most_watched_guest['EpisodeTitle']}'")
    print(f"  Season {most_watched_guest['Season']} | {most_watched_guest['Viewership']} million viewers")
    print(f"  Rating: {most_watched_guest['Ratings']}")
    print(f"  Guest stars: {most_watched_guest[guest_col]}")
    
    # Extract guest names
    guest_names = str(most_watched_guest[guest_col]).split(',')
    guest_names = [name.strip() for name in guest_names if name.strip()]
    
    print(f"\n🎭 ANSWER TO PROJECT QUESTION:")
    if guest_names:
        print(f"One guest star in the most watched Office episode was: {guest_names[0]}")
    
    print(f"\n🎭 All guest stars in this episode:")
    for i, guest in enumerate(guest_names, 1):
        print(f"  {i}. {guest}")

# Top 5 episodes with names
print(f"\n🏆 Top 5 Most Watched Episodes:")
top_5 = office_df.nlargest(5, 'Viewership')
for i, (_, ep) in enumerate(top_5.iterrows(), 1):
    guest_status = "👥 With guests" if ep[has_guest_col] else "👤 No guests"
    guest_info = f" ({str(ep[guest_col]).split(',')[0].strip()})" if ep[has_guest_col] and pd.notna(ep[guest_col]) else ""
    print(f"  {i}. Episode {ep['episode_number']:3d}: '{ep['EpisodeTitle']}'")
    print(f"     {ep['Viewership']:5.1f}M viewers | ⭐{ep['Ratings']:.1f} | {guest_status}{guest_info}")

# Guest episodes with names
if len(guest_episodes) > 0:
    print(f"\n👥 Top Guest Star Episodes:")
    top_guest_eps = guest_episodes.nlargest(5, 'Viewership')
    for i, (_, ep) in enumerate(top_guest_eps.iterrows(), 1):
        guest_names = str(ep[guest_col]).split(',')
        main_guest = guest_names[0].strip() if guest_names else "Unknown"
        print(f"  {i}. Episode {ep['episode_number']:3d}: '{ep['EpisodeTitle']}'")
        print(f"     {ep['Viewership']:5.1f}M viewers | Guest: {main_guest}")

# Season breakdown with notable episodes
print(f"\n📺 Season Breakdown with Notable Episodes:")
for season in range(1, 10):
    season_eps = office_df[office_df['Season'] == season]
    if len(season_eps) > 0:
        best_ep = season_eps.loc[season_eps['Viewership'].idxmax()]
        guest_count = season_eps[has_guest_col].sum()
        print(f"  Season {season}: {len(season_eps)} episodes, {guest_count} with guests")
        print(f"    Best: '{best_ep['EpisodeTitle']}' ({best_ep['Viewership']:.1f}M viewers)")

# Statistical summary
print(f"\n📊 Statistical Summary:")
with_guests = office_df[office_df[has_guest_col] == True]
without_guests = office_df[office_df[has_guest_col] == False]

print(f"  📺 Total episodes: {len(office_df)}")
print(f"  👥 Episodes with guests: {len(with_guests)} ({len(with_guests)/len(office_df)*100:.1f}%)")
print(f"  📈 Avg viewership (with guests): {with_guests['Viewership'].mean():.2f} million")
print(f"  📈 Avg viewership (no guests): {without_guests['Viewership'].mean():.2f} million")
print(f"  ⭐ Avg rating (with guests): {with_guests['Ratings'].mean():.2f}")
print(f"  ⭐ Avg rating (no guests): {without_guests['Ratings'].mean():.2f}")

print(f"\n✅ Analysis with episode and guest names completed!")
print("All visualizations now include actual episode titles and guest star names!")
print("=" * 55)