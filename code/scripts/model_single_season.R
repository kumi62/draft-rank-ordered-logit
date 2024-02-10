
## STEP 0: LOAD PACKAGES, FUNCTIONS AND DATA -----------------------------------

# Ensure the following packages are installed to run script
library(tidyverse)
library(rstan)

# Load 2021 draft data
player_data_21 = readr::read_csv("data/model_input/model_player_data_2021.csv")
ranking_data_21 = readr::read_rds("data/model_input/model_rankings_data_2021.Rda")
agencies_21 = readr::read_csv("data/model_input/model_agencies_data_2021.csv")
model_data_21 = readr::read_rds("data/model_input/model_data_list_2021.Rda")

# Load 2022 draft data
player_data_22 = readr::read_csv("data/model_input/model_player_data_2022.csv")
ranking_data_22 = readr::read_rds("data/model_input/model_rankings_data_2022.Rda")
agencies_22 = readr::read_csv("data/model_input/model_agencies_data_2022.csv")
model_data_22 = readr::read_rds("data/model_input/model_data_list_2022.Rda")



## STEP 1: FIT MODEL FOR 2021 AND 2022 DRAFTS ----------------------------------

# Load model code
draft_model = rstan::stan_model("code/models/model_single_season.stan")

# Draw posterior samples from the 2021 draft model
model_fit_21 = rstan::sampling(
  draft_model,
  data = model_data_21,
  iter = 4500,
  warmup = 2000,
  chains = 4,
  cores = 14
)

# Save model fit for 2021 draft
readr::write_rds(model_fit_21, "data/model_output/model_2021.Rda")

# Draw posterior samples from the 2022 draft model
model_fit_22 = rstan::sampling(
  draft_model,
  data = model_data_22,
  iter = 4500,
  warmup = 2000,
  chains = 4,
  cores = 14
)

# Save model fit for 2022 draft
readr::write_rds(model_fit_22, "data/model_output/model_2022.Rda")



## STEP 2: RUN DRAFT SIMULATIONS -----------------------------------------------





