import time, datetime

print
print
print
print '--------------------------------'
print 'Statistic Gather and Maintan BOT'
print '--------------------------------'
time.sleep(3)


# PARAMETERS:
# - How long statistics should be [sec]:
stat_total_time = 604800    # example: 604800 sec = 7 days
# - What the refresh rate should be [sec]:
stat_refresh_rate = 60      # seconds



# - What is the product:
product_LTC = 'LTC'
product_ETH = 'ETH'
product_BTC = 'BTC'
product_file_LTC = 'LTC-EUR.txt'
product_file_ETH = 'ETH-EUR.txt'
product_file_BTC = 'BTC-EUR.txt'
# ---------
# Declaration:
last_price_LTC = 0
current_price_LTC = 0
STATS_LTC = [0]
last_price_ETH = 0
current_price_ETH = 0
STATS_ETH = [0]
last_price_BTC = 0
current_price_BTC = 0
STATS_BTC = [0]
# ---------
# Variables:
# - Enough time for stats to fill trigger [loops]:
stat_ready_loops = stat_total_time / stat_refresh_rate
# - Dummy variable to track loops:
ticker = 1
# - Stat is full triggers:
stat_is_ready_LTC = 0 # 0=notFull / 1=Full
stat_is_ready_ETH = 0 # 0=notFull / 1=Full
stat_is_ready_BTC = 0 # 0=notFull / 1=Full
# ---------
# Create the fileName:
fileName_LTC =  'stat_LTC.txt'
fileName_ETH =  'stat_ETH.txt'
fileName_BTC =  'stat_BTC.txt'
# Create error.log file:
ts = time.time()
st = datetime.datetime.fromtimestamp(ts).strftime('%Y-%m-%d %H:%M:%S')
appendFile = open('Stat.error.log', 'a') 
appendFile.write('\n\n\nStatistics.error.log started at: ')
appendFile.write(st)
appendFile.write('\n')
appendFile.close()


while True:

# - get timestamp:
    ts = time.time()
    st = datetime.datetime.fromtimestamp(ts).strftime('%Y-%m-%d %H:%M:%S')

    

# - Get current_price_LTC:
    current_price_LTC = open(product_file_LTC, 'r').read()
    try:
        current_price_LTC = str(current_price_LTC)
    except:
        current_price_LTC = last_price_LTC
        appendFile = open('Stat.error.log', 'a')
        appendFile.write('\n\n')
        appendFile.write(st)
        appendFile.write(' : ERROR while setting current_price_LTC to str handeled ( current_price_LTC = last_price_LTC ). ')
        appendFile.write('\n- Current price_LTC =')
        appendFile.write(current_price_LTC)
        appendFile.close()

# - Get current_price_ETH:
    current_price_ETH = open(product_file_ETH, 'r').read()
    try:
        current_price_ETH = str(current_price_ETH)
    except:
        current_price_ETH = last_price_ETH
        appendFile = open('Stat.error.log', 'a')
        appendFile.write('\n\n')
        appendFile.write(st)
        appendFile.write(' : ERROR while setting current_price_LTC to str handeled ( current_price_ETH = last_price_ETH ). ')
        appendFile.write('\n- Current price_ETH =')
        appendFile.write(current_price_ETH)
        appendFile.close()

# - Get current_price_BTC:
    current_price_BTC = open(product_file_BTC, 'r').read()
    try:
        current_price_BTC = str(current_price_BTC)
    except:
        current_price_BTC = last_price_BTC
        appendFile = open('Stat.error.log', 'a')
        appendFile.write('\n\n')
        appendFile.write(st)
        appendFile.write(' : ERROR while setting current_price_LTC to str handeled ( current_price_BTC = last_price_BTC ). ')
        appendFile.write('\n- Current price_BTC =')
        appendFile.write(current_price_BTC)
        appendFile.close()
        

# - Create statistics file_LTC:
    if (stat_is_ready_LTC == 0):        # <- Stat not ready - gather data
        STATS_LTC.append(current_price_LTC)
    elif (stat_is_ready_LTC == 1):      # <- Stat ready - update data
        STATS_LTC.pop(0)
        STATS_LTC.append(current_price_LTC)

# - Create statistics file_ETH:
    if (stat_is_ready_ETH == 0):        # <- Stat not ready - gather data
        STATS_ETH.append(current_price_ETH)
    elif (stat_is_ready_ETH == 1):      # <- Stat ready - update data
        STATS_ETH.pop(0)
        STATS_ETH.append(current_price_ETH)

# - Create statistics file_BTC:
    if (stat_is_ready_BTC == 0):        # <- Stat not ready - gather data
        STATS_BTC.append(current_price_BTC)
    elif (stat_is_ready_BTC == 1):      # <- Stat ready - update data
        STATS_BTC.pop(0)
        STATS_BTC.append(current_price_BTC)
        
        
        

# - Export statistical data to a file LTC:
    if (stat_is_ready_LTC == 1):             # <- Stat ready - maintain stat file
        print
        print
        print st
        print 'Maintaining stat file:', fileName_LTC
        print
        # - Dummies for the string:
        i = 0       # <- set i = 0
        text = ''   # <- set text = 0
        # - Build the text string to write to the file:
        while (i < stat_ready_loops):  
            temp_text = str(STATS_LTC[i]) + '\n'
            i = i + 1
            text = text + temp_text
        saveFile = open(fileName_LTC, 'w')   # <- open the file
        saveFile.write(text)             # <- write the string
        saveFile.close()                 # <- close the file
    elif (stat_is_ready_LTC == 0):           # if Stat not ready -> pass/wait
        print st
        print 'Gathering statistics data for:', fileName_LTC
        print
        pass


# - Export statistical data to a file ETH:
    if (stat_is_ready_ETH == 1):             # <- Stat ready - maintain stat file
        print 'Maintaining stat file:', fileName_ETH
        print
        # - Dummies for the string:
        i = 0       # <- set i = 0
        text = ''   # <- set text = 0
        # - Build the text string to write to the file:
        while (i < stat_ready_loops):  
            temp_text = str(STATS_ETH[i]) + '\n'
            i = i + 1
            text = text + temp_text
        saveFile = open(fileName_ETH, 'w')   # <- open the file
        saveFile.write(text)             # <- write the string
        saveFile.close()                 # <- close the file
    elif (stat_is_ready_ETH == 0):           # if Stat not ready -> pass/wait
        print st 
        print 'Gathering statistics data for:', fileName_ETH
        print
        pass
        

# - Export statistical data to a file BTC:
    if (stat_is_ready_BTC == 1):             # <- Stat ready - maintain stat file
        print 'Maintaining stat file:', fileName_BTC
        print
        # - Dummies for the string:
        i = 0       # <- set i = 0
        text = ''   # <- set text = 0
        # - Build the text string to write to the file:
        while (i < stat_ready_loops):  
            temp_text = str(STATS_BTC[i]) + '\n'
            i = i + 1
            text = text + temp_text
        saveFile = open(fileName_BTC, 'w')   # <- open the file
        saveFile.write(text)             # <- write the string
        saveFile.close()                 # <- close the file
    elif (stat_is_ready_BTC == 0):           # if Stat not ready -> pass/wait
        print st
        print 'Gathering statistics data for:', fileName_BTC
        print
        print 'Time remaining [sec]:', (stat_ready_loops - ticker + 1)*stat_refresh_rate
        print
        pass

        

# - Tick and track when stat is ready (+1 to make sure):
    if (ticker > stat_ready_loops):
        stat_is_ready_LTC = 1
        stat_is_ready_ETH = 1
        stat_is_ready_BTC = 1
    elif (ticker <= stat_ready_loops):
        stat_is_ready_LTC = 0
        stat_is_ready_ETH = 0
        stat_is_ready_BTC = 0
        ticker = ticker + 1



    last_price_LTC = current_price_LTC
    last_price_ETH = current_price_ETH
    last_price_BTC = current_price_BTC
    time.sleep(stat_refresh_rate)











