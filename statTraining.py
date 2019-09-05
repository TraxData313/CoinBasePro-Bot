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
'''
NOTES:
- Data in stat files must be from oldest to newest:
1 -> oldest
4 -> previous
2 -> newest
-- If the data is the opposite way, use the reverser_script to reverse it
- 
'''


def saveBot(bot: 'Network Class Obj', pickle_out_file: 'File name'):
    'Saves the bot to the pickle_out_file file'
    print("- Saving bot...")
    pickle_out = open(pickle_out_file, "wb")
    pickle.dump(bot, pickle_out)
    pickle_out.close()
    print("- Done!")
    
def loadBot(pickle_in_file: 'File name') -> 'Network Obj (bot)':
    'Loads the bot from a pickle file'
    picke_in = open(pickle_in_file, "rb")
    bot = pickle.load(picke_in)
    return bot
    


#############
# PARAMETERS:
print()
print("Setting parameters...")
# - Test parameters:
train_epochs  = int(input("For how many Epochs to train: "))
train_file    = "stats_LTC-USD.txt"
test_file     = "stats_LTC-USD.txt"
minutes_per_cycle = 60
is_testing    = 0    # if=1 -> will do test after train
der_type      = 1    # def=1, 0:standard (new-old), 1:norm (new-old)/old
# - Default parameters:
fee = 0.003       # default = 0.003, fee applied on sell
reward_limit = 1  # default = 1, make sure reward doesn't overflow over the abs(value)
reward_type  = 1   # 0:relu(db), 1:relu(s*der), 2:tahn(db), 3:tahn(s*der)
db_mult      = 3   # for reward, F(db_mult*db + state*der) // db = ballance_change
record_reward = 0  # if==1 will create "reward_log.csv" file
profit_point  = 10000
starting_EUR  = 100
# - end
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
    
# - Or create new:
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
    bot.max_EF_resist   = int(input("Max EF resist (cell change resistance, def=1k): "))
    bot.D_resist        = int(input("D resist (weight change resistance, def=50): "))
    bot.is_chem_marking = int(input("Use chem marking? (1 or 0): "))
    # - end
    print("- Generated bot:", bot)
    print("- Done!")

# - pickle out file:
pickle_out_file = 'Bot_{}-{}x{}_EFr{}_Dr{}_ChMark{}.pickle'.format(bot.input_size,
                                                                  bot.hidden_count,
                                                                  bot.hidden_size,
                                                                  bot.max_EF_resist,
                                                                  bot.D_resist,
                                                                  bot.is_chem_marking)
print("Picke out file:", pickle_out_file)
saveBot(bot, pickle_out_file)


############
# VARIABLES:
print()
print("Initiating variables...")
# - Variables:
epoch = 0
EUR           = starting_EUR
coins         = 0
current_price = 0
ballance      = EUR + coins*current_price
ballance_old  = ballance
deals         = 0
state         = - 1   # 1=coins, -1=EUR
total_input_samples = 0
profit        = 0
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
train_file = "./Stats/" + train_file
test_file = "./Stats/" + test_file
# - Create the statistics:
train_data = open(train_file, 'r').readlines()
train_data_lenght = len(train_data)
test_data  = open(test_file, 'r').readlines()
test_data_lenght = len(test_data)
# - end
print("- Train data file:", train_file)
print("- Train data lenght:", train_data_lenght, "minutes")
print("- Test data file:", test_file)
print("- Test data lenght:", test_data_lenght, "minutes")
print("- Done!")


print()
print("Shrinking training data...")
# - Shrink the training data:
Prices_list = []
for i in range(train_data_lenght):
    if i%minutes_per_cycle==0:
        temp_price = float(train_data[i])
        Prices_list.append(temp_price)
print("- New training data samples:", len(Prices_list))
print("- Each sample is close price for every:", minutes_per_cycle, "'th minute")
print("- Done!")



# - Statistical data:
total_reward_vector    = []
ending_ballance_vector = []
deals_made_vector      = []
epochs_vector          = []
profit_vector          = []

for epoch in range(train_epochs):

    ########
    # EPOCH:

    print()
    print("Reseting variables...")
    # - Loop variables to reset:
    tick = total_input_samples
    total_reward = 0
    EUR = 100
    coins = 0
    deals = 0
    state         = - 1   # 1=coins, -1=EUR
    current_price = float(Prices_list[0])
    ballance      = EUR + coins*current_price
    ballance_old  = ballance
    total_ballance_change = 0
    profit = 0
    print("- Done!")
    
    println(3)
    print("Training...")

    while tick < len(Prices_list) - 1:
        
        
        #######
        # STAT:
        
        # - Recover the current price:
        try:
            current_price = float(Prices_list[tick])
        except:
            current_price = float(Prices_list[tick].split()[0])

        STAT_list   = [] # list of raw data
        SAMPLE_list = [] # list of squished data
        STAT_list_old   = []
        SAMPLE_list_old = []
        STAT_list_der = []
        # -- Build the stat and sample 0:
        for i in range(total_input_samples):
            try:
                temp_float = float(Prices_list[tick-i])
            except:
                temp_float = float(Prices_list[tick-i].split()[0]) 
                print()
                print(tick-i+2)
                print()
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
                temp_float = float(Prices_list[tick-i-1])
            except:
                temp_float = float(Prices_list[tick-i-1].split()[0]) 
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
            reward = db_mult*ballance_change + state*STAT_list_der[-1]
        elif reward_type == 2: # tahn
            pos_exp = np.exp(ballance_change)
            neg_exp = np.exp(-ballance_change)
            reward = (pos_exp - neg_exp) / (pos_exp + neg_exp) 
        elif reward_type == 3: # tahn+dd
            reward = db_mult*ballance_change + state*STAT_list_der[-1]
            pos_exp = np.exp(reward)
            neg_exp = np.exp(-reward)
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
            
            
        #########
        # PRINTS:
        tick+=1
        if tick%240==0:
            println(5)
            print("TROUBLESHOOTING DATA:")
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
            print()
            print("END BALLANCE VECTOR:")
            print(ending_ballance_vector)
            if len(ending_ballance_vector) > 0:
                print("Average end ballance:", sum(ending_ballance_vector)/len(ending_ballance_vector))
            println(3)
            print("TRAINING...")
            print(bot)
            print(pickle_out_file)
            print("Chem marking:", bool(bot.is_chem_marking))
            print("Train File:", train_file)
            print()
            print("Training for", train_epochs, "epochs...")
            print("Current epoch:", epoch+1)
            print("Training data total ticks:", len(Prices_list))
            print("Current tick:", tick)
            print()
            print("Current stats:")
            print("- Deals made:", deals)
            print("- Ballance:", ballance)
            print("- Current price:", current_price)
            #print("- Received reward:", total_reward)
            
            
    ###################
    # EPOCH END PRINTS:     
    # - Epoch end:
    total_reward_vector.append(total_reward)
    ending_ballance_vector.append(int(ballance))
    deals_made_vector.append(deals)
    epochs_vector.append(epoch+1)
    profit_vector.append(profit)
    println(3)
    print("END BALLANCE VECTOR:")
    print(ending_ballance_vector)
    println(3)
    print("Saving generator to file:")
    print("<", pickle_out_file, ">")
    print("Epoch#", epoch+1)
    print("Deals made:", deals)
    print("Epoch end ballance:", ballance)
    print("Total reward:", total_reward)
    print("Total Ballance change%:", total_ballance_change)
    # - Save the bot:
    saveBot(bot, pickle_out_file)

    
    
if is_testing == 1:
        
    println(3)
    print("Starting Test...")
    #######
    # TEST:

    print()
    print("Shrinking test data...")
    # - Shrink the test data:
    Prices_list = []
    for i in range(test_data_lenght):
        if i%minutes_per_cycle==0:
            temp_price = float(test_data[i])
            Prices_list.append(temp_price)
    print("- New test data samples:", len(Prices_list))
    print("- Each sample is close price for every:", minutes_per_cycle, "'th minute")
    print("- Done!")


    print()
    print("Reseting variables...")
    # - Loop variables to reset:
    tick = total_input_samples
    total_reward = 0
    EUR = 100
    cois = 0
    deals = 0
    state         = - 1   # 1=coins, -1=EUR
    current_price = float(Prices_list[0])
    ballance      = EUR + coins*current_price
    ballance_old  = ballance
    total_ballance_change = 0
    profit = 0
    print("- Done!")


    while tick < len(Prices_list) - 1:
        
        
        #######
        # STAT:
        
        # - Recover the current price:
        try:
            current_price = float(Prices_list[tick])
        except:
            current_price = float(Prices_list[tick].split()[0])
            
        # - Next price:
        next_price = float(Prices_list[tick+1])
        

        STAT_list   = [] # list of raw data
        SAMPLE_list = [] # list of squished data
        STAT_list_old   = []
        SAMPLE_list_old = []
        STAT_list_der = []
        # -- Build the stat and sample 0:
        for i in range(total_input_samples):
            try:
                temp_float = float(Prices_list[tick-i])
            except:
                temp_float = float(Prices_list[tick-i].split()[0]) 
                print()
                print(tick-i+2)
                print()
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
                temp_float = float(Prices_list[tick-i-1])
            except:
                temp_float = float(Prices_list[tick-i-1].split()[0]) 
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
            reward = db_mult*ballance_change + state*STAT_list_der[-1]
        elif reward_type == 2: # tahn
            pos_exp = np.exp(ballance_change)
            neg_exp = np.exp(-ballance_change)
            reward = (pos_exp - neg_exp) / (pos_exp + neg_exp) 
        elif reward_type == 3: # tahn+dd
            reward = db_mult*ballance_change + state*STAT_list_der[-1]
            pos_exp = np.exp(reward)
            neg_exp = np.exp(-reward)
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
        # bot.rewardAndUpdate(reward)
        
        
        
        ########
        # INPUT:
        
        # - Create the input vector:
        input_vector = []
        input_vector = STAT_list_der.copy()
        input_vector.append(state)
            
        # - Provide the input to the bot:
        bot.getInputAndPropagate(input_vector)
            
            
        ###################
        # OUTPUT AND TRADE:
            
        # - Get the output:
        output = bot.returnOutputPlace()
        
        
        bought = 0
        # - Sell:
        if output == 0 and coins > 0:
            EUR = (coins*current_price)*(1-fee)
            if EUR > profit_point:
                profit += EUR - profit_point
                EUR = profit_point
            coins = 0
            ballance = EUR + coins*current_price
            deals += 1 
            state = 1
            bought = 2
            
        # - Buy:
        if output == 1 and EUR > 0:
            coins = (EUR/current_price)
            EUR = 0
            ballance = EUR + coins*current_price
            deals += 1 
            state = - 1
            bought = 1
            
            
        #########
        # PRINTS:
        tick+=1
        if tick%240==0:
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
            println(3)
            print(bot)
            print("Train File:", train_file)
            print()
            print("Training for", train_epochs, "epochs...")
            print("Current epoch:", epoch+1)
            print("Training data total ticks:", len(Prices_list))
            print("Current tick:", tick)
            print()
            if bought == 1:
                print("BUY ORDER DONE!")
            elif bought == 2:
                print("SELL ORDER DONE!")
            print()
            print("Current stats:")
            print("- Current price:", current_price)
            print("- Next price:", next_price)
            print("- Deals made:", deals)
            print("- Ballance:", ballance)
            print("- EUR:", EUR)
            print("- Coins:", coins)
            print("- Received reward:", total_reward)
            print("- Ballance change%:", total_ballance_change)
            print("- Is chem marking:", bot.is_chem_marking)
            print()
            #haltValue = input("ENTER")
        
    
    
    
########################
# ENDING TRAIN AND TEST:
# - Ending print:
println(4)
print()
print("Used data:")
print("- Traing data:", train_file)
print("- Minutes per cycle:", minutes_per_cycle)
print("Epoch#", epoch+1)
print()
print("END BALLANCE VECTOR:")
print(ending_ballance_vector)
print("Deals made:", deals_made_vector[-1])
print("Total reward received:", total_reward_vector[-1])
print("Average end ballance:", sum(ending_ballance_vector)/len(ending_ballance_vector))
if is_testing == 1:
    print()
    print("TEST RESULTS:")
    print("- Test data  :", test_file)
    print("- Deals made:", deals)
    print("- Total reward:", total_reward)
    print("- Total profit:", profit)
    print("- Ending ballance:", ballance)
print()
print("Bot params:")
print(bot)
print("- Is chem marking:", bool(bot.is_chem_marking))
print("- Reward type:", reward_type)
print("- db_mult (for reward_type 1 and 3):", db_mult)
    
    
# - View the data:
print()
view_data = input("Do you want to view learning stats? (1 or 0) ")
view_data = int(view_data)
if view_data == 1:
    plt.xlabel('Epoch #')
    plt.ylabel('Ending ballance')
    #plt.plot(epochs_vector, total_reward_vector, color="green")
    #plt.plot(epochs_vector, deals_made_vector, color="red")
    plt.plot(epochs_vector, ending_ballance_vector, color="blue")
    #plt.plot(epochs_vector, profit_vector, color="blue")
    #green_line = mpatches.Patch(color='green', label='Toral Reward')
    #red_line = mpatches.Patch(color='red', label='Deals Made')
    blue_line = mpatches.Patch(color='blue', label='Ending ballance')
    #blue_line = mpatches.Patch(color='blue', label='Profit')
    #plt.legend(handles=[green_line, red_line, blue_line])
    #plt.legend(handles=[red_line, blue_line])
    plt.legend(handles=[blue_line])
    plt.show() 