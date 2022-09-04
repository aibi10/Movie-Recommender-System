import argparse
import os
from pathlib import Path
import shutil
from threading import local
from tqdm import tqdm
import logging
from src.utils.common import read_yaml, create_directories, extracting_name, movies_cast, movies_crew, movies_overview, remove_space, lower_case, stem
import random
import pandas as pd
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.metrics.pairwise import cosine_similarity
import pickle


STAGE = "STAGE_NAME"

logging.basicConfig(
    filename=os.path.join("logs", "running_logs.log"),
    level=logging.INFO,
    format="[%(asctime)s: %(levelname)s: %(module)s]: %(message)s",
    filemode="a"
)


def main(config_path):
    config = read_yaml(config_path)
    try:
        logging.info("file reading started >>>>> ")

        # reading the local directory name
        local_dir = config['data']['local_dir']
        # this is a another folder inside data folder
        data_folder = config['data']['data_folder']
        folder_name = Path(local_dir, data_folder)
        movie_file_name = config['data']['movie_file_name']  # movie csv file

        # credit csv file
        credit_file_name = config['data']['credit_file_name']
        movie_file = Path(folder_name, movie_file_name)
        credit_file = Path(folder_name, credit_file_name)
        movies = pd.read_csv(movie_file)
        credits = pd.read_csv(credit_file)
        logging.info("<<<<< file reading is done")
    except Exception as e:
        logging.info("error occured while reading the file")
        logging.exception(e)

    try:
        logging.info("movie file and credit files are going to be merged")
        column_name = config["data"]["merge_column_name"]
        movies = movies.merge(credits, on=column_name)
        logging.info("files are merged into movies")
    except Exception as e:
        logging.info("some error occured while merging of file")
        logging.exception(e)

    try:
        logging.info("only required columns are taken into consideration")
        movie_id = config['params']['movie_id']
        title = config['params']['title']
        overview = config['params']['overview']
        genres = config['params']['genres']
        keywords = config['params']['keywords']
        cast = config['params']['cast']
        crew = config['params']['crew']

        movies = movies[[movie_id, title, overview,
                         genres, keywords, cast, crew]]

        logging.info("rest of the columns are removed")
    except Exception as e:
        logging.info("some error occured while remving unwanted columns")
        logging.exception(e)

    try:
        logging.info("removing null values >>>>>>")
        null_values = movies.isnull().sum()
        if null_values.empty == False:
            movies.dropna(inplace=True)
        logging.info("null values are removed")

    except Exception as e:
        logging.info("some error occured while removing null values")
        logging.exception(e)

    try:
        logging.info("removing duplicate values if any >>>>")
        duplicate_value = movies.duplicated().sum()
        if duplicate_value != 0:
            movies = movies.drop_duplicates()
        logging.info("duplicates are dropped")

    except Exception as e:
        logging.info("some error occured while removing duplicates")
        logging.exception(e)

    try:
        logging.info("genres names is being extracted")
        movies["genres"] = movies["genres"].apply(extracting_name)
        logging.info("genres names has been extracted")
    except Exception as e:
        logging.info("some error occured while extracting genres names")
        logging.exception(e)

    try:
        logging.info("keywords names is being extracted")
        movies["keywords"] = movies["keywords"].apply(extracting_name)
        logging.info("keywords names is extracted")
    except Exception as e:
        logging.info("some error occured while extracting keywords names")
        logging.exception(e)

    try:
        logging.info("top three cast is being extracted")
        movies["cast"] = movies["cast"].apply(movies_cast)
        logging.info("top three cast is extracted")
    except Exception as e:
        logging.info("some error occured while extracting cast names")
        logging.exception(e)

    try:
        logging.info("Directors and Screenplay names are being extracted")
        movies["crew"] = movies["crew"].apply(movies_crew)
        logging.info("Directors and Screenplay names are extracted")
    except Exception as e:
        logging.info(
            "some error occured while extracting directors and screenplay names")
        logging.exception(e)

    try:
        logging.info("converting string in overview to list")
        movies["overview"] = movies["overview"].apply(movies_overview)
        logging.info("conversion is done")
    except Exception as e:
        logging.info("some error occured while conversion")
        logging.exception(e)

    try:
        logging.info("removing spaces >>>>>>>>>>>>")
        movies['cast'] = movies['cast'].apply(remove_space)
        logging.info("space from cast is removed")
        movies['crew'] = movies['crew'].apply(remove_space)
        logging.info("space from crew is removed")
        movies['genres'] = movies['genres'].apply(remove_space)
        logging.info("space from genres is removed")
        movies['keywords'] = movies['keywords'].apply(remove_space)
        logging.info("space from keywords is removed")
        logging.info("removal of space is done")
    except Exception as e:
        logging.info("some error occured while removing spaces")
        logging.exception(e)

    try:
        logging.info("converting to lower case")
        movies['cast'] = movies['cast'].apply(lower_case)
        logging.info("cast is converted to lowercase")
        movies['crew'] = movies['crew'].apply(lower_case)
        logging.info("crew is converted to lowercase")
        movies['genres'] = movies['genres'].apply(lower_case)
        logging.info("genres is converted to lowercase")
        movies['keywords'] = movies['keywords'].apply(lower_case)
        logging.info("keywords is converted to lowercase")
        movies['overview'] = movies['overview'].apply(lower_case)
        logging.info("overview is converted to lowercase")
        logging.info("conversion is done")
    except Exception as e:
        logging.info("some error occured while conversion")
        logging.exception(e)

    try:
        logging.info("combining 5 columns to 1 columns")
        tags = config['params']['tags']
        movies[tags] = movies[genres] + movies[keywords] + \
            movies[cast] + movies[crew] + movies[overview]
        logging.info("Done!!!")
    except Exception as e:
        logging.info("some error occured while combining")
        logging.exception(e)

    try:
        logging.info("converting the entire dataframe to just 3 columns")
        new_df = movies[[movie_id, title, tags]]
        logging.info("Done!!!")
    except Exception as e:
        logging.info("some error occured while combining")
        logging.exception(e)

    try:
        logging.info("stemming of words in tags column is done")
        new_df["tags"] = new_df["tags"].apply(stem)
        logging.info("Stemming is done!!!")
    except Exception as e:
        logging.info("some error occured while stemming")
        logging.exception(e)

    try:
        cv = CountVectorizer(max_features=5000, stop_words='english')
        vector = cv.fit_transform(new_df['tags']).toarray()
        similarity = cosine_similarity(vector)
        pickle.dump(new_df, open('artifacts/movie_list.pkl', 'wb'))
        pickle.dump(similarity, open('artifacts/similarity.pkl', 'wb'))
    except Exception as e:
        logging.info(e)


if __name__ == "__main__":
    args = argparse.ArgumentParser()
    args.add_argument("--config", "-c", default="configs/config.yaml")
    parsed_args = args.parse_args()

    try:
        logging.info("\n***************************")
        logging.info(f">>>>>>>>>>> stage   {STAGE}   started <<<<<<<<<<")
        main(config_path=parsed_args.config)
        logging.info(f">>>>>>>>> stage  {STAGE}   completed <<<<<<<<<<<")
    except Exception as e:
        logging.exception(e)
        raise e
