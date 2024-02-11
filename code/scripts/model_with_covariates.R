
## SETUP: LOAD PACKAGES, FUNCTIONS AND DATA ------------------------------------

# Ensure the following packages are installed to run script
library(tidyverse)
library(rstan)
library(glue)
library(ggnewscale)
library(gganimate)
library(ggbeeswarm)

# Source required functions and scripts
source("code/functions/simulations/draft_simulator.R")
source("code/functions/simulations/create_static_heatmap.R")
source("code/functions/simulations/create_dynamic_heatmap.R")
source("code/functions/simulations/create_player_cdf.R")
source("code/functions/simulations/create_tendencies_beeswarm.R")

# Load draft data for all years
ranking_data = readr::read_rds("data/model_input/model_rankings_data.Rda")
agency_data = readr::read_csv("data/model_input/model_agencies_data.csv")
model_data = readr::read_rds("data/model_input/model_data_list.Rda")
player_data = readr::read_csv("data/model_input/model_player_data.csv")
draft_results = readr::read_csv("data/model_input/draft_results.csv")



## FIT MODEL FOR 2019-2022 DRAFT WITH TEAM & AGENCY TENDENCIES -----------------

# Load model code
draft_model = rstan::stan_model("code/models/model_with_covariates.stan")

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



## SAMPLE RESULTS I: MODEL PARAMETERS ------------------------------------------

# Extract posterior means
posterior_means = summary(model_fit)$summary %>%
  as.data.frame() %>%
  rownames_to_column("variable")

# Extract posterior summary for theta (player ability parameters)
theta_means = posterior_means %>%
  filter(grepl("theta\\[", variable)) %>%
  bind_cols(player_data %>% arrange(stan_id)) %>%
  select(stan_id, player, everything()) %>%
  arrange(draft_year, desc(mean))

# Plot 95% credible intervals for the top 20 players across all seasons
theta_means %>%
  arrange(desc(mean)) %>%
  head(20) %>%
  ggplot() +
  geom_pointrange(aes(x = mean, xmin = `2.5%`, xmax = `97.5%`, y = factor(player, levels = player), colour = factor(draft_year))) +
  scale_y_discrete(limits = rev) +
  scale_colour_manual(values = c("navy", "blue", "green", "forestgreen")) +
  theme_bw() +
  theme(axis.text = element_text(size = 14), axis.title = element_text(size = 14), title = element_text(size = 14),
        legend.text = element_text(size = 14)) +
  labs(x = "Estimated Player Abilities", y= "", colour = "Draft Year")


# Extract posterior summary for beta
beta_heights_means = posterior_means %>%
  filter(grepl("beta_heights\\[", variable)) %>%
  bind_cols(agency_data %>% arrange(agency_id)) %>%
  select(agency_id, agency_name, everything()) %>%
  arrange(desc(mean))

beta_propsr_means = posterior_means %>%
  filter(grepl("beta_propsr\\[", variable)) %>%
  bind_cols(agency_data %>% arrange(agency_id)) %>%
  select(agency_id, agency_name, everything()) %>%
  arrange(desc(mean))

beta_overage_means = posterior_means %>%
  filter(grepl("beta_overage\\[", variable)) %>%
  bind_cols(agency_data %>% arrange(agency_id)) %>%
  select(agency_id, agency_name, everything()) %>%
  arrange(desc(mean))

create_tendencies_beeswarm(beta_heights_means, beta_propsr_means, beta_overage_means)



## SAMPLE RESULTS II: SIMULATE DRAFT OUTCOMES ----------------------------------

# Run simulations from the start of the 2022 draft
draft_start = draft_simulator(
  model_fit,
  player_data,
  agency_data,
  draft_results,
  picks_made = c(),
  n_picks_shown = 32,
  n_players_shown = 32,
  year = c(2022),
  include_covariates = TRUE,
  is_retrospective = FALSE
)

# Determine player order for heatmap
player_order = draft_start %>%
  group_by(player) %>%
  summarize(
    prob_picked = sum(prob),
    exp_pick = sum(prob * pick)
  ) %>%
  arrange(desc(prob_picked), exp_pick) %>%
  select(player) %>%
  unlist() %>%
  unname()

create_static_heatmap(draft_start, player_order)

# Run simulations after first 3 observed picks of the 2022 draft
draft_obs_top3 = draft_simulator(
  model_fit,
  player_data,
  agency_data,
  draft_results,
  picks_made = c("Juraj Slafkovsky", "Simon Nemec", "Logan Cooley"),
  n_picks_shown = 32,
  n_players_shown = 32,
  year = c(2022),
  include_covariates = TRUE,
  is_retrospective = FALSE
)

create_static_heatmap(draft_obs_top3, player_order)

# Run simulations after most likely first 3 picks of the 2022 draft
draft_prob_top3 = draft_simulator(
  model_fit,
  player_data,
  agency_data,
  draft_results,
  picks_made = c("Shane Wright", "Juraj Slafkovsky", "Logan Cooley"),
  n_picks_shown = 32,
  n_players_shown = 32,
  year = c(2022),
  include_covariates = TRUE,
  is_retrospective = FALSE
)

create_static_heatmap(draft_prob_top3, player_order)

# Run simulations after each pick in the first round and create animation of results
first_round_results = draft_results %>%
  filter(year == 2022 & rank <= 32) %>%
  select(player) %>%
  unlist() %>%
  unname()

draft_first_round = draft_simulator(
  model_fit,
  player_data,
  agency_data,
  draft_results,
  picks_made = first_round_results,
  n_picks_shown = 50,
  n_players_shown = 50,
  year = c(2022),
  include_covariates = TRUE,
  is_retrospective = TRUE
)

dynamic_heatmap = create_dynamic_heatmap(draft_first_round, player_order)

# heatmap_anim = animate(dynamic_heatmap, renderer = ffmpeg_renderer(), fps = 3, duration = 32/3)
# anim_save(paste("figures/dynamic_heatmap_2022_draft.mp4", sep = ""), heatmap_anim)


# Run simulations after first 22 picks to obtain player-level PMF for Tristan Luneau (selected 53rd by Anaheim)
draft_first22 = draft_simulator(
  model_fit,
  player_data,
  agency_data,
  draft_results,
  picks_made = first_round_results[1:22],
  n_picks_shown = 96,
  n_players_shown = 96,
  year = c(2022),
  include_covariates = TRUE,
  is_retrospective = FALSE
)

create_player_cdf(draft_first22, "Tristan Luneau")

