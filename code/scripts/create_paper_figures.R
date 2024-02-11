
## SETUP: LOAD PACKAGES, FUNCTIONS, MODELS AND DATA ----------------------------

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

# Load 2021 draft data and model, fit without covariates
player_data_21 = readr::read_csv("data/model_input/model_player_data_2021.csv")
ranking_data_21 = readr::read_rds("data/model_input/model_rankings_data_2021.Rda")
agency_data_21 = readr::read_csv("data/model_input/model_agencies_data_2021.csv")
model_data_21 = readr::read_rds("data/model_input/model_data_list_2021.Rda")
draft_results_21 = readr::read_csv("data/model_input/draft_results_2021.csv")
model_fit_21 = readr::read_rds("data/model_output/model_2021.Rda")

# Load 2022 draft data and model, fit without covariates
player_data_22 = readr::read_csv("data/model_input/model_player_data_2022.csv")
ranking_data_22 = readr::read_rds("data/model_input/model_rankings_data_2022.Rda")
agency_data_22 = readr::read_csv("data/model_input/model_agencies_data_2022.csv")
model_data_22 = readr::read_rds("data/model_input/model_data_list_2022.Rda")
draft_results_22 = readr::read_csv("data/model_input/draft_results_2022.csv")
model_fit_22 = readr::read_rds("data/model_output/model_2022.Rda")

# Load draft data and model, fit with covariates between 2019-2022
ranking_data = readr::read_rds("data/model_input/model_rankings_data.Rda")
agency_data = readr::read_csv("data/model_input/model_agencies_data.csv")
model_data = readr::read_rds("data/model_input/model_data_list.Rda")
player_data = readr::read_csv("data/model_input/model_player_data.csv")
draft_results = readr::read_csv("data/model_input/draft_results.csv")
model_fit = readr::read_rds("data/model_output/model_full.Rda")



## FIGURE 1: POSTERIOR SUMMARIES FOR PLAYER ABILITY PARAMETERS (THETA) ---------

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
figure1 = theta_means_22 %>%
  arrange(desc(mean)) %>%
  head(32) %>%
  ggplot() +
  geom_pointrange(aes(x = mean, xmin = `2.5%`, xmax = `97.5%`, y = factor(player, levels = player))) +
  scale_y_discrete(limits = rev) +
  theme_bw() +
  theme(axis.text = element_text(size = 14), axis.title = element_text(size = 14), title = element_text(size = 14),
        legend.text = element_text(size = 14)) +
  labs(x = "Estimated Player Abilities", y= "", colour = "Draft Year")

ggsave("figures/figure1.png", figure1, height = 6, width = 7, dpi = 300)



## FIGURE 2a: PLAYER-PICK PMF FOR 2021 DRAFT WITHOUT COVARIATES ----------------

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

# Determine player order for player-pick pmf
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

# Create player-pick pmf
figure2a = create_static_heatmap(draft_2021, player_order_21)

ggsave("figures/figure2a.png", figure2a, width = 10, height = 8)



## FIGURE 2b: PLAYER-PICK PMF FOR 2022 DRAFT WITHOUT COVARIATES ----------------

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

# Determine player order for player-pick pmf
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

# Create player-pick pmf
figure2b = create_static_heatmap(draft_2022, player_order_22)

ggsave("figures/figure2b.png", figure2b, width = 10, height = 8)



## FIGURE 3a: PLAYER-PICK PMF FOR 2022 AFTER OBSERVED TOP 3 --------------------

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

# Create player-pick pmf
figure3a = create_static_heatmap(draft_2022_obs_top3, player_order_22)

ggsave("figures/figure3a.png", figure3a, width = 10, height = 8)



## FIGURE 3b: PLAYER-PICK PMF FOR 2022 AFTER EXPECTED TOP 3 --------------------

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

# Create player-pick pmf
figure3b = create_static_heatmap(draft_2022_prob_top3, player_order_22)

ggsave("figures/figure3b.png", figure3b, width = 10, height = 8)



## FIGURE 4: TEAM AND AGENCY TENDENCY PARAMETER MEANS (BETA) -------------------

# Extract posterior means
posterior_means = summary(model_fit)$summary %>%
  as.data.frame() %>%
  rownames_to_column("variable")

# Extract posterior means for height tendency parameter
beta_heights_means = posterior_means %>%
  filter(grepl("beta_heights\\[", variable)) %>%
  bind_cols(agency_data %>% arrange(agency_id)) %>%
  select(agency_id, agency_name, everything()) %>%
  arrange(desc(mean))

# Extract posterior means for weighted proportion of games as Sr level tendency parameter
beta_propsr_means = posterior_means %>%
  filter(grepl("beta_propsr\\[", variable)) %>%
  bind_cols(agency_data %>% arrange(agency_id)) %>%
  select(agency_id, agency_name, everything()) %>%
  arrange(desc(mean))

# Extract posterior means for overager tendency parameter
beta_overage_means = posterior_means %>%
  filter(grepl("beta_overage\\[", variable)) %>%
  bind_cols(agency_data %>% arrange(agency_id)) %>%
  select(agency_id, agency_name, everything()) %>%
  arrange(desc(mean))

# Create a beeswarm plot of the posterior means for these parameters, split by teams vs agencies
figure4 = create_tendencies_beeswarm(beta_heights_means, beta_propsr_means, beta_overage_means)

ggsave("figures/figure4.png", figure4, width = 12, height = 20)



## FIGURE 5: PLAYER-PICK PMF FOR THE 2022 DRAFT WITH COVARIATES ----------------

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

# Create player-pick pmf
figure5 = create_static_heatmap(draft_start, player_order)

ggsave("figures/figure5.png", figure5, width = 10, height = 8)



## FIGURE 6: WYATT JOHNSTON CDF IN 2021 DRAFT AFTER FIRST 14 PICKS -------------

# Extract first 14 picks of the 2021 NHL draft
first_14_picks_2021 = draft_results %>%
  filter(year == 2021 & rank <= 14) %>%
  select(player) %>%
  unlist() %>%
  unname()

# Run simulations after first 14 picks to obtain player-level PMF for Wyatt Johnston (selected 53rd by Anaheim)
draft_first22 = draft_simulator(
  model_fit_21,
  player_data_21,
  agency_data_21,
  draft_results_21,
  picks_made = first_14_picks_2021,
  n_picks_shown = 96,
  n_players_shown = 96,
  year = c(2021),
  include_covariates = FALSE,
  is_retrospective = FALSE
)

# Create CDF for Wyatt Johnston at pick 15
figure6 = create_player_cdf(draft_first22, "Wyatt Johnston")

ggsave("figures/figure6.png", figure6, dpi = 400, height = 5, width = 10)
