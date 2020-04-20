import matplotlib.pyplot as plt
from Environment import *
from Learner import *
from CTSLearner import *
from Hungarian import *


n_arms = 4 # WHAT THE HELL DO I HAVE TO DO WITH PROBABILITIES?
p = np.array([0.15, 0.1, 0.1,0.35])  # probabilities for each arm (probability of obtaining 1 as a sample (Bernoulli lies in {0,1})à
opt = p[3]  # This is the optimal arm (0.35 is the greatest) --> My guess

T = 300  # Time Horizon
X = 1  #number of arms of the superarm
n_experiments = 1    # number of experiments
arraysRewards = []
ts_rewards_per_experiment = []
gr_rewards_per_experiment = []

for e in range(n_experiments): #number of experiments
    idx = getArmsFromMatching()  # RUN THE HUNGARIAN FOR THE FIRST TIME
   # n_arms = len(idx)
    print("experiment number: ",e)
    print("array of indexes", idx)

    env = Environment(n_arms=n_arms, probabilities=p)
    cts_learner = CTSLearner(n_arms)

    for t in range(T):   # T = time orizon
        for x in range(len(idx)): #here we pull every arm of the superarm
            if(idx[x] != 0): #the arms with index 0 are not in the superarm
                print("index", idx[x]*x)
               # pulled_arm =  idx[x]*x   #THIS IS THE INDEX OF THE ARM NEEDED TO PULL
                pulled_arm = cts_learner.pull_arm()  #IT WAS THIS WAY
                print(pulled_arm)
               # if (pulled_arm > 3):
                #    pulled_arm = 1   #FOR SOME REASON THE EVIROMENT IS NOT HANDLING INDEX > 3
                reward = env.round(pulled_arm) #assign the reward of the pulled arm, THE ENVIROMENT IS GIVING ME THE REWARD
                print("reward of the arm", reward)
                cts_learner.update(pulled_arm, reward) #update the values in the ts_learner
                arraysRewards.append(reward) #THE ARRAY THAT WE ARE GOING TO PASS TO THE HUNGARIAN WITH THE REWARDS OF THE ARMS
               # ---- THE PROBLEM IS THAT THE REWARD HERE IS JUST 0/1  
    # ----- NOW I DO HAVE TO PASS THE REWARD BACK TO HUNGARIAN -------------
            idx = getArmsFromMatching()  # RUN THE HUNGARIAN AND GET THE SUPERARMS

    ts_rewards_per_experiment.append(cts_learner.collected_rewards)


# Regret = T*opt - sum_t(rewards_t)

plt.figure(0)
plt.xlabel("t")
plt.ylabel("Regret")


# Calculate the instantaneous regret for each t for each experiment
# Note: regret_t = optimal_arm_value - pulled_arm_value
# Note: a positive regret is "bad", a negative regret is "good"
regrets = opt - ts_rewards_per_experiment

# Calculate the average regret for each iteration t
# Note that we are conducting n_experiments so we need the average over all the experiments for each iteration t
# Note that axis=0 means that you are averaging over each iteration t (over the column)
avg_regrets = np.mean(regrets, axis=0)

# Avg_Regret = T*opt - sum_t(value_t)
# Note that we have already calculated the average regret (opt-value)
# So we only need to cumulatively sum the array containing the avg_regret for each itearation t
# np.cumsum(array) returns an array with item at position i equal to the sum of the items at previous positions (pos i included)
avg_regret = np.cumsum(avg_regrets)
# Plot
plt.plot(avg_regret, 'r')

# The same is done for Greedy_Learner
plt.plot(np.cumsum(np.mean(opt-gr_rewards_per_experiment, axis=0)), 'g')

plt.legend(["TS"])
plt.show()

