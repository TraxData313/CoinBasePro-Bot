import time, datetime
from time import sleep
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
from utils import println
import pickle


println(10)
print('--------------------------')
print('BOT for statistics testing')
print('--------------------------')
time.sleep(0.5)
'''
NOTES:
- Data in stat files must be from oldest to newest:
1 -> oldest
4 -> previous
2 -> newest
-- If the data is the opposite way, use the reverser_script to reverse it
- 
'''


def saveBot(bot: 'Network Class Obj', pickle_file: 'File name'):
    'Saves the bot to the pickle_file file'
    print("- Saving bot...")
    pickle_out = open(pickle_file, "wb")
    pickle.dump(bot, pickle_out)
    pickle_out.close()
    print("- Done!")
    
def loadBot(pickle_file: 'File name') -> 'Network Obj (bot)':
    'Loads the bot from a pickle file'
    picke_in = open(pickle_file, "rb")
    bot = pickle.load(picke_in)
    return bot

   
#############
# PARAMETERS:
print()
print("Loading parameters...")
# - Test parameters:
variablesFile = "liveTesting_variables.txt" # contains the bot to be used
test_file     = "stats_LTC-USD.txt"
minutes_per_cycle = 60
der_type      = 1    # def=1, 0:standard (new-old), 1:norm (new-old)/old
# - Default parameters:
fee = 0.003       # default = 0.003, fee applied on sell
reward_limit = 1  # default = 1, make sure reward doesn't overflow over the abs(value)
reward_type  = 1   # 0:relu(db), 1:relu(s*der), 2:tahn(db), 3:tahn(s*der)
db_mult      = 3   # for reward, F(mult*db + s*der)
record_reward = 0  # if==1 will create "reward_log.csv" file
profit_point  = 1000
starting_EUR  = 100
# - end
time.sleep(0.5)
print("- Done!")
    
    
##########
# NETWORK:
# - pickle in:
print()
is_loading_existing = str(input("- Do you want to use saved object (1=yes)?: "))
if is_loading_existing == "1":
    pickle_file = input("- File to load from: ")
    bot = loadBot(pickle_file)
    input_size = bot.input_size
    print()
    print("Loaded bot:", bot)
    print("Bot life:", bot.life)
# - Or create a new bot:
else:
    print()
    print("Generating a bot instance...")
    # - Network and its parameters:
    # --Import:
    from networkMod import Network
    # -- Fixed parameters:
    input_size  = int(input("Enter input size (note that 1 place is for state): "))
    output_size = 2
    # -- Layer sizing parameters:
    hidden_count      = int(input("Hidden layer count: "))
    hidden_size       = int(input("Hidden layer size : "))
    # -- Object:
    if der_type == 0:
        bot = Network(input_size,
                      hidden_size,
                      output_size,
                      hidden_count) # input_size + 1 more input for the state
    elif der_type == 1:
        bot = Network(input_size,
                      hidden_size,
                      output_size,
                      hidden_count) # input_size + 1 more input for the state
    # -- Hyper parameters:
    bot.max_EF_resist = int(input("Max EF resist (cell change resistance, def=1k): "))
    bot.D_resist      = int(input("D resist (weight change resistance, def=50): "))
    bot.is_chem_marking = 0
    # - end
    time.sleep(0.5)
    print("- Done!")
    time.sleep(0.1)
    print("- Generated bot:", bot)
# - Save the bot to be used to the variablesFile:
pickle_file = 'Bot_{}-{}x{}_EFr{}_Dr{}_ChMark{}.pickle'.format(bot.input_size,
                                                      bot.hidden_count,
                                                      bot.hidden_size,
                                                      bot.max_EF_resist,
                                                      bot.D_resist,
                                                      bot.is_chem_marking)
print("Picke file used:", pickle_file)
saveFile = open(variablesFile, 'w')
saveFile.write(pickle_file)
saveFile.close()

    
############
# VARIABLES:
print()
print("Initiating variables...")
# - Variables:
EUR           = starting_EUR
coins         = 0
current_price = 0
ballance      = EUR + coins*current_price
ballance_old  = ballance
total_ballance_change = 0
total_reward  = 0
deals         = 0
state         = - 1
total_input_samples = 0
profit        = 0
loops_tested  = 0
for i in range(input_size):
    total_input_samples += (i+1)**2   # stretch is 2 by default
# - end
print("- Input size:", input_size)
print("- Total samples to fill all inputs:", total_input_samples)
print("- Done!")



#############
# STATISTICS:
print()
print("Loading price data...")
# - Ad the path to the statistics:
test_file = "./Stats/" + test_file
# - Create the statistics:
test_data  = open(test_file, 'r').readlines()
test_data_lenght = len(test_data)
# - end
print("- Test data file:", test_file)
print("- Test data lenght:", test_data_lenght, "min (", int(test_data_lenght/1440), "days )")
time.sleep(0.5)
print("- Done!")



###############
# LIVE TESTING:
println(3)
is_ready = str(input("Ready to start testing? "))

while True:

    ###############
    # LOAD THE BOT:
    pickle_file   = 'null'
    variablesList = open(variablesFile, 'r').readlines()
    pickle_file   = variablesList[0]
    bot           = loadBot(pickle_file)
    

    #############
    # STATISTICS:
    
    # - Import the data:
    test_data  = open(test_file, 'r').readlines()
    test_data_lenght = len(test_data)

    print()
    print("Shrinking test data...")
    # - Shrink the test data:
    Prices_list = []
    for i in range(test_data_lenght):
        if i%minutes_per_cycle==0:
            temp_price = float(test_data[-1-i])
            Prices_list.append(temp_price)
    # - end
    print("- New test data samples:", len(Prices_list))
    print("- Each sample is close price for every:", minutes_per_cycle, "'th minute")
    print("- Done!")
    
    # - Recover the current price:
    try:
        current_price = float(Prices_list[0])
    except:
        current_price = float(Prices_list[0].split()[0])

    # - Data processing:
    STAT_list       = [] # list of raw data
    SAMPLE_list     = [] # list of squished data
    STAT_list_old   = []
    SAMPLE_list_old = []
    STAT_list_der   = []
    # -- Build the stat and sample 0:
    for i in range(total_input_samples):
        try:
            temp_float = float(Prices_list[i])
        except:
            temp_float = float(Prices_list[i].split()[0]) 
        STAT_list.append(temp_float)
    at_element = 0
    for i in range(input_size):
        temp_samples = (i+1)**2
        sample = np.mean(STAT_list[at_element:at_element+temp_samples])
        SAMPLE_list.append(sample)
        at_element += temp_samples
    # -- Build the stat and sample 1 (old):
    for i in range(total_input_samples):
        try:
            temp_float = float(Prices_list[i+1])
        except:
            temp_float = float(Prices_list[i+1].split()[0]) 
        STAT_list_old.append(temp_float)
    at_element = 0
    for i in range(input_size):
        temp_samples = (i+1)**2
        sample = np.mean(STAT_list_old[at_element:at_element+temp_samples])
        SAMPLE_list_old.append(sample)
        at_element += temp_samples
    # -- Build the der list:
    if der_type == 0:
        for i in range(input_size):
            STAT_list_der.append(SAMPLE_list[i] - SAMPLE_list_old[i])
    elif der_type == 1:
        for i in range(input_size - 1):
            STAT_list_der.append((SAMPLE_list[i] - SAMPLE_list[i+1])/SAMPLE_list[i+1])


    #########
    # REWARD:
    
    # - Calculate the ballance change in %:
    ballance = EUR + coins*current_price
    ballance_change = ((ballance - ballance_old)/ballance_old)*100
    total_ballance_change += ballance_change
    
    # - Save the old ballance:
    ballance_old = ballance
    
    # - Prepare the reward:
    # -- Reward type:
    if reward_type == 0: # relu
        reward = ballance_change
    elif reward_type == 1: # relu + state*STAT_list_der[-1]
        reward = ballance_change + state*STAT_list_der[-1]
    elif reward_type == 2: # tahn
        pos_exp = np.exp(ballance_change)
        neg_exp = np.exp(-ballance_change)
        reward = (pos_exp - neg_exp) / (pos_exp + neg_exp) 
    
    # -- Make a file with the ballance change:
    if record_reward == 1:
        appendFile = open("reward_log.csv", 'a')
        appendFile.write(str(ballance_change))
        appendFile.write('\n')
        appendFile.close()
        
    # -- Modify reward:
    # NOTE: once recorded the reward, modify it if needed:
    reward = reward*0.1
    
    # -- Overflow catch:
    if reward > reward_limit:
        reward = reward_limit
    elif reward < - reward_limit:
        reward = - reward_limit

    # -- Keep track of the total reward:
    total_reward += reward
    
    # - Provide the reward to the bot:
    bot.rewardAndUpdate(reward)
    
    
    
    ########
    # INPUT:
    # - Create the input vector:
    input_vector = []
    input_vector = STAT_list_der.copy()
    input_vector.append(state)
        
    # - Provide the input to the bot:
    print("Input vector size:", len(input_vector))
    print("Bot:", bot)
    bot.getInputAndPropagate(input_vector)
        
        
    ###################
    # OUTPUT AND TRADE:
        
    # - Get the output:
    output = bot.returnOutputPlace()
    
    # - Sell:
    if output == 0 and coins > 0:
        EUR = (coins*current_price)*(1-fee)
        if EUR > profit_point:
            profit += EUR - profit_point
            EUR = profit_point
        coins = 0
        ballance = EUR + coins*current_price
        deals += 1 
        state = - 1
        
    # - Buy:
    if output == 1 and EUR > 0:
        coins = (EUR/current_price)
        EUR = 0
        ballance = EUR + coins*current_price
        deals += 1 
        state = 1
        
    # - Increase bot life:
    loops_tested += 1
    
        
    #########
    # PRINTS:
    println(5)
    print("DATA:")
    print()
    print("- Raw data 1:")
    print(STAT_list_old)
    print()
    print("- Raw data 0:")
    print(STAT_list)
    print()
    print("- Squished data 1:")
    print(SAMPLE_list_old)
    print()
    print("- Squished data 0:")
    print(SAMPLE_list)
    print()
    print("- Prices der:")
    print(STAT_list_der)
    println(5)
    print("LIVE TESTING")
    ts = time.time()
    st = datetime.datetime.fromtimestamp(ts).strftime('%Y-%m-%d %H:%M:%S')
    print(st)
    print()
    print("PARAMETERS:")
    print(bot)
    print(pickle_file)
    print("Testing on data:", test_file)
    print("Minutes per cycle:", minutes_per_cycle)
    print()
    print("Current stats:")
    print("- Bot life:", bot.life)
    print("- Testing for loops:", loops_tested)
    print("- Current price:", current_price)
    print("- Deals made:", deals)
    print("- EUR:", EUR)
    print("- Coins:", coins)
    print("- Ballance:", ballance)
    print("- Received reward:", total_reward)
    print("- Ballance change%:", total_ballance_change)
    print("- Profit:", profit)
    # - Save the bot:
    saveBot(bot, pickle_file)
    sleep(minutes_per_cycle*60)