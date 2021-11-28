from pathlib import Path, PurePath

ROOT_DIR = Path(__file__).resolve().parent.parent

# Top Level Directories
DATA_DIR = ROOT_DIR / 'data'
LOGS_DIR = ROOT_DIR / 'logs'
TESTS_DIR = ROOT_DIR / 'tests'
IMAGES_DIR = ROOT_DIR / 'images'

# Data Directories
BEST_MODELS_DIR = ROOT_DIR / 'best_models'
MODEL_COMPARE_DIR = DATA_DIR / 'compare_df'
DATABASE_DIR = DATA_DIR / 'databases'
SCRAPED_DIR = DATA_DIR / 'scraped'

if __name__ == '__main__':
    print('Running as Main Directory')
    print(f'ROOT DIR: {ROOT_DIR}')


# ========================= USER DEFINED ========================= #

# All paths should be relative to the ROOT_DIR
