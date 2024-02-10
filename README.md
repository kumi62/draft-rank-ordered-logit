# draft-rank-ordered-logit
A repository containing the code and materials for "Dynamic Prediction of the National Hockey League Draft with Rank-Ordered Logit Models"

## Data Collection

The objective of the Data Collection phase of this project is to gather:

- Sets of draft rankings published by scouting sites and media outlets leading up to the NHL draft.

- The observed results of past NHL drafts.

- Player-specific bios and statistics.

We use a mixture of manual data entry and web scraping via `BeautifulSoup` and `selenium` in Python to collect these data.

The `code/scrapers/ranking_scrapers.py` file contains a handful of examples of how we scrape NHL draft results and ranking sets and the `code/scrapers/update_player_data.py` file contains a scraper for player-specific information from eliteprospects.com. All data collected for this project can be found in the `data/players` and `data/rankings` subdirectories.

## Data Preparation

Upon obtaining the raw data from our Data Collection phase, there are steps required in order to prepare the data for modelling and analyses. Among the key steps in this process are:

- **Player mapping**: Ensure that players in ranking sets are mapped to a corresponding `player_id`. Matching on names is not always reliable as translations, nicknames and misspellings may lead to player names being difficult to map from one ranking set to another.

- **Create player-level covariates**: In the corresponding paper, we incorporate the three covariates containing player-level information into the model: 1) whether or not the player is an overager, 2) a weighted proportion of games played by the player at the professional men's level, and 3) the player's height, z-scored by position and draft year. In our Data Preparation phase we store these covariates for each player in each ranking set to be used when fitting our model.

- **Structuring data for modelling**: We use Stan in order to fit a Bayesian model to predict the outcome of the NHL draft. Thus, we store all relevant materials for fitting our model in a list (the required format for modelling with `rstan`) so that the data is prepared to and ready to be utilized in the Modelling step without any additional preprocessing.

The `code/scripts/data_preparation.R` script contains a step-by-step walkthrough of our Data Preparation phase. Resulting data can be found in the `data/model_input` subdirectory.

## Modelling

With the data prepared, we move on to fitting the rank-ordered logit models described in the corresponding paper:

1. Rank-ordered logit model fit with ranking sets for the 2021 NHL draft, without considering team and agency tendencies.

2. Rank-ordered logit model fit with ranking sets for the 2022 NHL draft, without considering team and agency tendencies.

3. Rank-ordered logit model fit with ranking sets for the 2019-2022 NHL drafts and draft results from the 2019-2021 NHL drafts with player-level covariates and team and agency-level tendency parameters.

Models (1) and (2) are fit in `code/scripts/model_single_season.R` with the Stan code for these models found in `code/models/model_single_season.stan`. Model (3) is fit in `code/scripts/model_multiple_seasons.R` with Stan code found in `code/models/model_multiple_seasons.stan`.

The outputted models from these scripts are stored in the `data/model_output` subdirectory. However, due to storage limits, these were omitted from the repository.

## Draft Simulations




## Reproducibility

The models and results found in the corresponding paper can be reproduced by running the `code/scripts/model_single_season.R` and `code/scripts/model_multiple_seasons.R` scripts.

