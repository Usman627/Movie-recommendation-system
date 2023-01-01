import pandas as pd
from scipy.sparse import csr_matrix
from sklearn.neighbors import NearestNeighbors

# Read in the data
df = pd.read_csv("ratings.csv")

# Create a pivot table of users and items
ratings_pivot = df.pivot_table(index='userId', columns='movieId', values='rating')

# Convert the pivot table to a sparse matrix
ratings_matrix = csr_matrix(ratings_pivot.values)

# Create the NearestNeighbors model and fit it to the matrix
model = NearestNeighbors(metric='cosine', algorithm='brute')
model.fit(ratings_matrix)


# Write a function to make recommendations
def recommend(user_id, num_recommendations):
    # Get the user's ratings
    user_ratings = ratings_pivot.loc[user_id].dropna()

    # Get the indices of the movies the user has rated
    user_rated_movie_indices = user_ratings.index

    # Get the distance and indices of the nearest neighbors
    distances, indices = model.kneighbors(ratings_pivot.loc[user_id].values.reshape(1, -1),
                                          n_neighbors=num_recommendations + 1)

    # Create a list of recommendations
    recommendations = []

    # Iterate over the nearest neighbors
    for i in range(0, len(distances.flatten())):
        # Get the index of the neighbor
        neighbor_index = indices.flatten()[i]

        # If the neighbor is not the user and the neighbor has not been rated by the user
        if neighbor_index != user_id and ratings_pivot.index[neighbor_index] not in user_rated_movie_indices:
            # Add the movie to the recommendations list
            recommendations.append(ratings_pivot.index[neighbor_index])

    # Return the recommendations
    return recommendations


# Test the function
recommendations = recommend(1, 10)
print(recommendations)