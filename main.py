import matplotlib.pyplot as plt
import pandas as pd
import numpy as np
from matplotlib.animation import FuncAnimation

# Load your data here
car_data = pd.read_csv('data/raw.csv')

# Data preprocessing
car_data['Year_from'] = car_data['Year_from'].dropna().astype(int)
countries = car_data['country_of_origin'].unique().tolist()
car_data = car_data[car_data['country_of_origin'].isin(countries)]
model_counts_by_year_country = car_data.groupby(['Year_from', 'country_of_origin']).size().unstack(fill_value=0)

# Setting up the figure and axis for animation
fig, ax = plt.subplots(figsize=(10, 8))

def animate(frame):
    year_index = frame // 3
    
    # Stop the animation if we've reached the end of the data
    if year_index >= len(model_counts_by_year_country):
        ani.event_source.stop()
        return

    ax.clear()
    t = (frame % 3) / 3

    if year_index == 0:
        prev_data = np.zeros_like(model_counts_by_year_country.iloc[0])
    else:
        prev_data = model_counts_by_year_country.iloc[year_index - 1]

    current_data = model_counts_by_year_country.iloc[year_index]
    
    # Interpolate between previous and current data
    interpolated_data = prev_data + (current_data - prev_data) * t
    
    countries = current_data.index
    values = interpolated_data.values
    bars = ax.barh(countries, values, color=plt.cm.tab20.colors)
    
    ax.set_xlabel('Number of Models')
    ax.set_title(f'Car Models by Country in {int(model_counts_by_year_country.index[year_index])}')
    plt.gca().invert_yaxis()  # Invert y axis so the largest is on top
    ax.set_xlim(0, model_counts_by_year_country.values.max())  # Set fixed x-axis limit

# Creating animation
frames = len(model_counts_by_year_country) * 3 + 1  # Add 1 to ensure we reach the last frame
ani = FuncAnimation(fig, animate, frames=frames, repeat=False, interval=50)

# To save the animation, uncomment the line below
ani.save('car_models_animation_grow_bars.mp4', writer='ffmpeg', dpi=80)

plt.show()