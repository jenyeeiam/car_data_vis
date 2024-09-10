import matplotlib.pyplot as plt
import pandas as pd
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

def update(year):
    ax.clear()
    data = model_counts_by_year_country.loc[year]
    countries = data.index
    values = data.values
    bars = ax.barh(countries, values, color=plt.cm.tab20.colors)
    ax.set_xlabel('Number of Models')
    ax.set_title(f'Car Models by Country in {int(year)}')
    plt.gca().invert_yaxis()  # Invert y axis so the largest is on top
    ax.set_xlim(0, model_counts_by_year_country.values.max())  # Set fixed x-axis limit

# Creating animation
ani = FuncAnimation(fig, update, frames=model_counts_by_year_country.index, repeat=False, interval=300)

# To save the animation, uncomment the line below
ani.save('car_models_animation.mp4', writer='ffmpeg', dpi=80)

plt.show()
