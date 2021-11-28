# To - Do

## scraping.ipynb

- [ ]  Delete this file after adding to docs (post Sphinx)

## suicidewatch.py

- [ ] Get comments with posts
- [ ] Change SQL to store in different db
- [ ]  Set Linux Cron job for auto scrape


## Project Files

- [ ]  
- [x]  


## Additions

- [ ]  Dump data into MongoDB also?
- [ ]  Find more sources of data
- [ ]  Stacking models
        https://openscoring.io/blog/2020/01/02/stacking_sklearn_lightgbm_xgboost/


## Problems / Issues / Lack of Knowledge

- [x] Functions for engineering / bare code for EDA and analysis?
- [ ] UNIT TESTING
- [x] .ipynb vs .py - Keep them both? `demo.ipynb`?
        - I think this is solved with using Sphinx for documentation instead of having a demo jupyter notebook for every .py file.
        - https://www.sphinx-doc.org/en/master/


# Bugs

## scraping.py

- [x] scraper returns less than 10 posts when sort is set to anything other than 'new'
        - fixed this with using for loop set to 40 pages, since limit is 1000 anyway
- [ ] 

