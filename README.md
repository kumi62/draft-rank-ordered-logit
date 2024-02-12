# draft-rank-ordered-logit
A repository containing the code and materials for "Dynamic Prediction of the National Hockey League Draft with Rank-Ordered Logit Models" in the International Journal of Forecasting.

## Data Collection

The objective of the Data Collection phase of this project is to gather:

- Sets of draft rankings published by scouting sites and media outlets leading up to the NHL draft. For example, [this page](https://www.tsn.ca/2022-nhl-draft-rankings-bob-mckenzie-1.1818580) contains a draft ranking set for the 2022 NHL draft from Bob McKenzie, a reporter at TSN (The Sports Network).

- The observed results of past NHL drafts. For example, [this page on hockeydb.com](https://www.hockeydb.com/ihdb/draft/nhl2022e.html) contains the draft results for the 2022 NHL draft.

- Player-specific bios and statistics. For example, [this page on eliteprospects.com](https://www.eliteprospects.com/player/527453/pavel-mintyukov) contains information about Pavel Mintyukov, a prospect for the 2022 NHL draft.

We use a mixture of manual data entry and web scraping via `BeautifulSoup` and `selenium` in Python to collect these data.

The `code/scrapers/ranking_scrapers.py` file contains a handful of examples of how we scrape NHL draft results and ranking sets and the `code/scrapers/update_player_data.py` file contains a scraper for player-specific information from eliteprospects.com. All data collected for this project can be found in the `data/players` and `data/rankings` subdirectories.

## Data Preparation

Upon obtaining the raw data from our Data Collection phase, there are steps required in order to prepare the data for modelling and analyses. Among the key steps in this process are:

- **Player mapping**: Ensure that all players in each ranking set are mapped to a corresponding `player_id`. Matching on names is not always reliable as there are often inconsistencies in player names between ranking sets due to translations, nicknames and misspellings.

- **Create player-level covariates**: In the corresponding paper, we incorporate the three covariates containing player-level information into the model: 1) whether or not the player is an overager, 2) a weighted proportion of games played by the player at the professional men's level, and 3) the player's height, z-scored by position and draft year. In our Data Preparation phase we store these covariates for each player in each ranking set to be used when fitting our model.

- **Structuring data for modelling**: We use Stan in order to fit a Bayesian model to predict the outcome of the NHL draft. Thus, we store all relevant materials for fitting our model in a list in R (the required format for modelling with `rstan`) so that the data is prepared to and ready to be utilized in the Modelling step without any additional preprocessing.

The `code/scripts/data_preparation.R` script contains a step-by-step walkthrough of our Data Preparation phase. Resulting data can be found in the `data/model_input` subdirectory.

## Modelling

With the data prepared, we move on to fitting the rank-ordered logit models described in the corresponding paper:

1. Rank-ordered logit model fit with ranking sets for the 2021 NHL draft, without considering team and agency tendencies.

2. Rank-ordered logit model fit with ranking sets for the 2022 NHL draft, without considering team and agency tendencies.

3. Rank-ordered logit model fit with ranking sets for the 2019-2022 NHL drafts and draft results from the 2019-2021 NHL drafts with player-level covariates and team and agency-level tendency parameters.

Models (1) and (2) are fit in `code/scripts/model_no_covariates.R` with the Stan code for these models found in `code/models/model_no_covariates.stan`. Model (3) is fit in `code/scripts/model_with_covariates.R` with Stan code found in `code/models/model_with_covariates.stan`.

Collectively, these three models take over 36 hours to fit using a 16-core MacBook Pro. The outputted models from these scripts are coded to be stored in the `data/model_output` subdirectory. However, due to storage limits, these were omitted from the repository. See [this Google Drive](https://drive.google.com/drive/folders/16oM5WRBuboXfEcXJztKdY_CD1Wj4TTs9?usp=drive_link) for a copy of models [(1)](https://drive.google.com/file/d/1_lJzuJfO3Y-pVGOUG6i3K9dzpdjwBg4e/view?usp=sharing), [(2)](https://drive.google.com/file/d/1BA5fiz91Z7OnKL_FtjQF0YyN3i54Rq4i/view?usp=sharing) and [(3)](https://drive.google.com/file/d/12O3fP2dlSD9F6M2LU4V3sPpOfGfajAI1/view?usp=sharing) fit using the scripts in this repository.

## Draft Simulations

Upon fitting the models, we use analyze the model parameters and the posterior draws to simulate the NHL draft in various scenarios in the 'Sample Results' sections of `code/scripts/model_no_covariates.R` and `code/scripts/model_with_covariates.R`. These simulations are powered by Stan and the `rstan::gqs` function with the corresponding Stan code found in `code/models/simulations_no_covariates.stan` and `code/models/simulations_with_covariates.stan`.


## Reproducibility

The figures found in the corresponding paper can be reproduced by running the `code/scripts/create_paper_figures.R` script. This leverages the results of the `code/scripts/data_preparation.R`, `code/scripts/model_no_covariates.R` and `code/scripts/model_with_covariates.R` to generate raw copies of all figures. Collectively, these four scripts can be used to generate all models and results described in the corresponding paper.
