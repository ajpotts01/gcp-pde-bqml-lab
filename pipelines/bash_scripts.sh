bq --location=EU mk --dataset movies_dev
bq load --source_format=CSV --location=EU --autodetect movies_dev.movielens_ratings gs://dataeng-movielens/ratings.csv
bq load --source_format=CSV --location=EU --autodetect movies_dev.movielens_movies_raw gs://dataeng-movielens/movies.csv