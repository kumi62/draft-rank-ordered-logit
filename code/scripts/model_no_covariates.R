
## SETUP: LOAD PACKAGES, FUNCTIONS AND DATA ------------------------------------

# Ensure the following packages are installed to run script
library(tidyverse)
library(rstan)
library(glue)

# Source required functions
source("code/functions/simulations/draft_simulator.R")
source("code/functions/simulations/create_static_heatmap.R")
source("code/functions/simulations/create_dynamic_heatmap.R")
source("code/functions/simulations/create_player_cdf.R")

# Load 2021 draft data
player_data_21 = readr::read_csv("data/model_input/model_player_data_2021.csv")
ranking_data_21 = readr::read_rds("data/model_input/model_rankings_data_2021.Rda")
agency_data_21 = readr::read_csv("data/model_input/model_agencies_data_2021.csv")
model_data_21 = readr::read_rds("data/model_input/model_data_list_2021.Rda")
draft_results_21 = readr::read_csv("data/model_input/draft_results_2021.csv")

# Load 2022 draft data
player_data_22 = readr::read_csv("data/model_input/model_player_data_2022.csv")
ranking_data_22 = readr::read_rds("data/model_input/model_rankings_data_2022.Rda")
agency_data_22 = readr::read_csv("data/model_input/model_agencies_data_2022.csv")
model_data_22 = readr::read_rds("data/model_input/model_data_list_2022.Rda")
draft_results_22 = readr::read_csv("data/model_input/draft_results_2022.csv")



## FIT MODEL FOR 2021 AND 2022 DRAFTS ------------------------------------------

# Load model code
draft_model = rstan::stan_model("code/models/model_no_covariates.stan")

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



## SAMPLE RESULTS I: MODEL PARAMETERS ------------------------------------------

# Extract posterior means
posterior_means_22 = summary(model_fit_22)$summary %>%
  as.data.frame() %>%
  rownames_to_column("variable")

# Extract posterior summary for theta (player ability parameters)
theta_means_22 = posterior_means_22 %>%
  filter(grepl("theta\\[", variable)) %>%
  bind_cols(player_data_22 %>% arrange(stan_id)) %>%
  select(stan_id, player, everything()) %>%
  arrange(draft_year, desc(mean))

# Plot 95% credible intervals for the top 32 players
theta_means_22 %>%
  arrange(desc(mean)) %>%
  head(32) %>%
  ggplot() +
  geom_pointrange(aes(x = mean, xmin = `2.5%`, xmax = `97.5%`, y = factor(player, levels = player))) +
  scale_y_discrete(limits = rev) +
  theme_bw() +
  theme(axis.text = element_text(size = 14), axis.title = element_text(size = 14), title = element_text(size = 14),
        legend.text = element_text(size = 14)) +
  labs(x = "Estimated Player Abilities", y= "", colour = "Draft Year")



## SAMPLE RESULTS II: SIMULATE DRAFT OUTCOMES ----------------------------------

# Run simulations from the start of the 2021 draft
draft_2021 = draft_simulator(
  model_fit_21,
  player_data_21,
  agency_data_21,
  draft_results_21,
  picks_made = c(),
  n_picks_shown = 32,
  n_players_shown = 32,
  year = c(2021),
  include_covariates = FALSE,
  is_retrospective = FALSE
)

# Determine player order for heatmap
player_order_21 = draft_2021 %>%
  group_by(player) %>%
  summarize(
    prob_picked = sum(prob),
    exp_pick = sum(prob * pick)
  ) %>%
  arrange(desc(prob_picked), exp_pick) %>%
  select(player) %>%
  unlist() %>%
  unname()

create_static_heatmap(draft_2021, player_order_21)


# Run simulations from the start of the 2022 draft
draft_2022 = draft_simulator(
  model_fit_22,
  player_data_22,
  agency_data_22,
  draft_results_22,
  picks_made = c(),
  n_picks_shown = 32,
  n_players_shown = 32,
  year = c(2022),
  include_covariates = FALSE,
  is_retrospective = FALSE
)

# Determine player order for heatmap
player_order_22 = draft_2022 %>%
  group_by(player) %>%
  summarize(
    prob_picked = sum(prob),
    exp_pick = sum(prob * pick)
  ) %>%
  arrange(desc(prob_picked), exp_pick) %>%
  select(player) %>%
  unlist() %>%
  unname()

create_static_heatmap(draft_2022, player_order_22)

# Run simulations after first 3 observed picks of the 2022 draft
draft_2022_obs_top3 = draft_simulator(
  model_fit_22,
  player_data_22,
  agency_data_22,
  draft_results_22,
  picks_made = c("Juraj Slafkovsky", "Simon Nemec", "Logan Cooley"),
  n_picks_shown = 32,
  n_players_shown = 32,
  year = c(2022),
  include_covariates = FALSE,
  is_retrospective = FALSE
)

create_static_heatmap(draft_2022_obs_top3, player_order_22)

# Run simulations after most likely first 3 picks of the 2022 draft
draft_2022_prob_top3 = draft_simulator(
  model_fit_22,
  player_data_22,
  agency_data_22,
  draft_results_22,
  picks_made = c("Shane Wright", "Juraj Slafkovsky", "Logan Cooley"),
  n_picks_shown = 32,
  n_players_shown = 32,
  year = c(2022),
  include_covariates = FALSE,
  is_retrospective = FALSE
)

create_static_heatmap(draft_2022_prob_top3, player_order_22)

# Run simulations after first 14 picks to obtain player-level PMF for Wyatt Johnston (selected 53rd by Anaheim)
first_3_rounds_2021_results = draft_results %>%
  filter(year == 2021 & rank <= 96) %>%
  select(player) %>%
  unlist() %>%
  unname()

draft_first22 = draft_simulator(
  model_fit_21,
  player_data_21,
  agency_data_21,
  draft_results_21,
  picks_made = first_3_rounds_2021_results[1:14],
  n_picks_shown = 96,
  n_players_shown = 96,
  year = c(2021),
  include_covariates = FALSE,
  is_retrospective = FALSE
)

create_player_cdf(draft_first22, "Wyatt Johnston")
