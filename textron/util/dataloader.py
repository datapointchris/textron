import logging
from glob import glob

import pandas as pd

from textron.util import databases
from textron import CONFIG


def load_scraped_csv(self, scraped_dir):
    df = pd.DataFrame()
    for label in self.class_labels:
        csv_files = sorted(glob(f'{scraped_dir}/*{label}*.csv'))
        if len(csv_files) < 1:
            raise ValueError(f'No data for "{label}"')
        for csv_file in csv_files:
            data = pd.read_csv(csv_file)
            df = pd.concat([df, data], ignore_index=True)
    return df


# === NOTE === # this bypasses the 'execute_read_query' function in the databases module...
def load_sqlite(self, database, query):
    db = databases.Sqlite()
    connection = db.create_connection(database)

    placeholders = ','.join('?' for label in self.class_labels)

    ### FIX ###
    # this query needs to be explicitely given in each notebook
    # to allow for different databases
    subreddit_query = f"""
    SELECT
        title,
        subreddit,
        date
    FROM subreddits
    WHERE subreddit IN (%s);""" % str(placeholders)

    cursor = connection.cursor()
    cursor.execute(subreddit_query, self.class_labels)

    column_names = [description[0] for description in cursor.description]
    data = cursor.fetchall()
    df = pd.DataFrame(data=data, columns=column_names)
    df = df.drop_duplicates(subset='title')
    for label in self.class_labels:
        if len(df[df['subreddit'] == label]) == 0:
            raise ValueError(f'No data for "{label}"')
    return df


def load_mongo(self):
    db = databases.Mongo()
    return db.create_connection()


def load_postgres(self):
    db = databases.Postgres()
    return db.create_connection()


def load_mysql(self):
    db = databases.Mysql()
    return db.create_connection()
