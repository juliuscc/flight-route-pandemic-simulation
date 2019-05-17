MAX_STEPS_IN_SIMULATION = 300

PORTION_OF_POPULATION_EXPOSED = 0.5
PORTION_OF_POPULATION_INFECTED = 0.2
BETA_KEEP_LOCAL_STATE_FRACTION = 0.5


# omega = 0
SEIR_RATE_RECOVERY = 0

# natural death 255 days
SEIR_RATE_NATURAL_DEATH = 0

# natural birth nu = mu
SEIR_RATE_NATURAL_BIRTH = SEIR_RATE_NATURAL_DEATH

# latent period 1.2 days sigma^-1
SEIR_PERIOD_LATENT = 1 / 1.2

# infected period gamma = sigma for the influenza
SEIR_INFECTED_PERIOD = 1 / 1.2

# transmission coefficient beta 1.66 days
SEIR_TRANSMISSION_COEFFICIENT = 1 / 1.66

# h = 0.1
SEIR_TIME_STEP = 0.5

##################################
# MEASLES
##################################
# SEIR_PERIOD_LATENT = 0.143

# TUBERCULOSIS
SEIR_PERIOD_LATENT = 0.000310               # sigma
SEIR_INFECTED_PERIOD = 0.123111             # gamma
SEIR_TRANSMISSION_COEFFICIENT = 0.326655    # beta
