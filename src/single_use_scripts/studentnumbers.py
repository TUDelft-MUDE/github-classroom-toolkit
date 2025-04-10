import pandas as pd
from matplotlib import pyplot as plt

df = pd.read_csv('cli/classlists/CLASSLIST_3RD.csv')

min_value = df['OrgDefinedId'].min()
max_value = df['OrgDefinedId'].max()
values = df['OrgDefinedId'].tolist()

def plot_distribution(data, min_value, max_value, bins=100):
    """
    Plots a histogram of the given data within the specified min and max range.

    :param data: List of numbers.
    :param min_value: Minimum value of the range.
    :param max_value: Maximum value of the range.
    :param bins: Number of bins for the histogram.
    """
    # Filter the data to be within the min and max range
    filtered_data = [x for x in data if min_value <= x <= max_value]

    if not filtered_data:
        print("No data points fall within the specified range.")
        return

    # Plot the histogram
    plt.hist(filtered_data, bins=bins, range=(min_value, max_value), edgecolor='black', color='skyblue')
    plt.title(f'Distribution of Data (Range: {min_value} to {max_value})')
    plt.xlabel('Value')
    plt.ylabel('Frequency')
    plt.grid(True)
    plt.show()


plot_distribution(values, min_value, max_value, 40_000)