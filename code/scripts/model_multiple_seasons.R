
## STEP 0: LOAD PACKAGES, FUNCTIONS AND DATA -----------------------------------

# Ensure the following packages are installed to run script
library(tidyverse)
library(rstan)

# Load 2021 draft data
ranking_data = readr::read_rds("data/model_input/model_rankings_data.Rda")
agencies = readr::read_csv("data/model_input/model_agencies_data.csv")
model_data = readr::read_rds("data/model_input/model_data_list.Rda")
player_data = readr::read_csv("data/model_input/model_player_data.csv")



## STEP 1: FIT MODEL FOR 2019-2022 DRAFT WITH TEAM & AGENCY TENDENCIES ---------

# Load model code
draft_model = rstan::stan_model("code/models/model_multiple_seasons.stan")

# Draw posterior samples from the model
model_fit = rstan::sampling(
  draft_model,
  data = model_data,
  iter = 4500,
  warmup = 2000,
  chains = 4,
  cores = 14
)

# Save model fit
readr::write_rds(model_fit, "data/model_output/model_full.Rda")

