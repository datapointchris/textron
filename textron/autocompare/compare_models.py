import argparse
import datetime
import logging
import logging.handlers
import time

import pandas as pd
from sklearn.metrics import roc_auc_score
from sklearn.model_selection import RandomizedSearchCV, train_test_split
from sklearn.pipeline import make_pipeline
from tqdm import tqdm

# --- Absolute Import Fix --- #
# Use this if script needs to be run standalone
import os
import sys
from dotenv import find_dotenv
sys.path.append(os.path.dirname(find_dotenv()))

from textron import CONFIG
from textron.util import dataloader
from textron.autocompare import grid_models
from textron.util.helpers import Labeler, function_timer

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)
formatter = logging.Formatter(
    '%(asctime)s:%(name)s:%(message)s', datefmt='%m/%d/%Y %I:%M:%S %p')
file_handler = logging.handlers.RotatingFileHandler(filename=CONFIG.LOGS_DIR / 'compare_models.log',
                                                    maxBytes=10000000,
                                                    backupCount=10)
file_handler.setFormatter(formatter)
logger.addHandler(file_handler)


@function_timer
def main():
    df = dataloader.data_selector(class_labels, data_source)
    X = df['title']
    y = df['subreddit']

    labeler = Labeler()
    labeler.fit(y)
    y = labeler.transform(y)

    X_train, X_test, y_train, y_test = train_test_split(X, y, random_state=7)

    preprocessors = grid_models.preprocessors
    estimators = grid_models.estimators
    date = str(datetime.datetime.now().strftime('%Y-%m-%d_%H%M'))
    now = datetime.datetime.now()

    model_comparison_df = pd.DataFrame(columns=[
        'preprocessor',
        'estimator',
        'best_train_score',
        'best_test_score',
        'time_weighted_score',
        'roc_auc',
        'train_test_variance',
        'fit_time_seconds',
        'predict_time_seconds',
        'best_params',
        'subreddits',
        'date'
    ])

    for est in tqdm(estimators.values()):
        for prep in preprocessors.values():
            logger.info(f"Fitting model with {prep.get('name')} and {est.get('name')}")
            print(f"Fitting model with {prep.get('name')} and {est.get('name')}")
            try:
                pipe = make_pipeline(
                    prep.get('preprocessor'),
                    est.get('estimator'))
                pipe_params = dict()
                pipe_params.update(prep.get('pipe_params'))
                pipe_params.update(est.get('pipe_params'))
                model = RandomizedSearchCV(pipe,
                                           param_distributions=pipe_params,
                                           n_iter=n_iter,
                                           cv=3,
                                           verbose=1,
                                           n_jobs=-1
                                           )
                model.fit(X_train, y_train)
            except Exception as e:
                logger.exception(f'ERROR BUILDING AND TRAINING MODEL: {e}')
                continue

            train_score = model.score(X_train, y_train)
            predict_start_time = time.time()
            test_score = model.score(X_test, y_test)
            predict_elapsed_time = time.time() - predict_start_time
            if hasattr(model, 'predict_proba'):
                y_proba = model.predict_proba(X_test)
                roc_auc = roc_auc_score(y_test, y_proba, multi_class="ovr")

            subreddits = (', ').join(labeler.classes_)
            time_weighted_score = test_score / (model.refit_time_ + predict_elapsed_time) * 1000
            train_test_score_variance = (train_score - test_score) / train_score

            # add the model result to the df
            model_comparison_df.loc[len(model_comparison_df)] = [
                prep.get('name'),
                est.get('name'),
                round(train_score, 3),
                round(test_score, 3),
                round(time_weighted_score, 3),
                round(roc_auc, 3) if roc_auc else 'na',
                round(train_test_score_variance, 3),
                round(model.refit_time_, 3),
                round(predict_elapsed_time, 3),
                model.best_params_,
                subreddits,
                now
            ]

    logger.info('Saving comparison df to CSV')
    try:
        model_comparison_df.to_csv(
            f'{CONFIG.MODEL_COMPARE_DIR}/{date}.csv')
    except FileNotFoundError:
        logger.exception('ERROR SAVING MODEL:')
    except UnboundLocalError:
        logger.exception('No compare_df saved.  Error fitting models:')


# ========================= MAIN ========================= #

if __name__ == "__main__":
    logger.info('PROGRAM STARTED -- "compare_models"')
    parser = argparse.ArgumentParser(
        prog='Model Comparison for Text Classification',
        description='''
            Compare models using preprocessors and estimators speficied in `grid_models.py`
            Specify class labels or default is random 8 labels from full list specified in `grid_models.py`
        '''
    )
    parser.add_argument('--class_labels', action='store', nargs='+', default=grid_models.class_labels_random,
                        help='Class labels to pull from database and use for model comparison')
    parser.add_argument('--data_source', action='store', choices=['csv', 'sqlite', 'postgres', 'mongo', 'mysql'],
                        default='sqlite', help='Source to get data from')
    parser.add_argument('--n_iter', action='store', default=100,
                        help='Number of iterations to use for RandomizedSearchCV, default is 100')

    args = parser.parse_args()
    class_labels = args.class_labels
    data_source = args.data_source
    n_iter = int(args.n_iter)

    logger.info(f'Class Labels: {class_labels}')
    logger.info(f'Data Source: {data_source}')
    logger.info(f'Number of Iterations: {n_iter}')

    main_start = time.time()
    main()
    logger.info(f'Total Run Time: {round((time.time() - main_start) / 60, 2)} minutes')
    logger.info('PROGRAM FINISHED')
