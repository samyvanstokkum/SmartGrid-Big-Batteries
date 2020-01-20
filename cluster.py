# Make a list for each amount of possible batteries.
# So a list for 3 batteries
# one for 4 try:

# Make the segments and link the centroid to the closest

# Take a random combination of batteries that satisfy the houses total usage. Do that 100 times and choose the best configuration.
# can the algo find the best clusters when you give constraints of the batteries.

# try clustering with all different combination. different k different batteries. only save the best configurations

# once you have a cluster, you can link the houses and make an area. In the area you can try random positions for the battery aswell.
from house import House
import csv
import numpy as np
import matplotlib.pyplot as plt
from sklearn.cluster import KMeans


def load_district():
    with open(f'Houses&Batteries/district2_houses.csv') as in_file:
        reader = csv.DictReader(in_file)

        district = []
        for house_id, row in enumerate(reader, 1):
            x = eval(row['x'])
            y = eval(row[' y'])
            output = eval(row[' max output'])
            house = House(house_id, x, y, output)
            district.append(house)

        return district


def get_clusters(district):
    points = []
    for house in district:
        coordinate = [house.x, house.y]
        points.append(coordinate)
    points = np.array(points)

    # Create a kmeans object
    kmeans = KMeans(n_clusters=5)

    # Fit the kmeans object to the dataset
    labels = kmeans.fit_predict(points)

    clusters = kmeans.cluster_centers_
    # clusters.astype(int)

    return labels, points, clusters


def plot_clusters(labels, points, clusters):
    battery_colors = ["#007AFF", "#34C859",
                      "#5857D6", "#FF9600", "#FF2E55", "#AF52DE"]
    house_colors = ["#A3CFFF", "#A0F5B5",
                    "#9594E9", "#FFD496", "#FFAABA", "#E5B1FF"]
    for i in range(len(clusters)):
        # Plot the clusters
        plt.scatter(points[labels == i, 0],
                    points[labels == i, 1], color=house_colors[i])
        # Plot the cluster centers
        plt.scatter(clusters[i, 0], clusters[i, 1],
                    marker="s", s=30, color=battery_colors[i])

    # Show the plot
    plt.show()


if __name__ == "__main__":
    district = load_district()
    labels, points, clusters = get_clusters(district)
    print(clusters)
    plot_clusters(labels, points, clusters)
