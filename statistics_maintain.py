import time, datetime

print('-----------------------------')
print('Statistic Maintenance BOT 1.0')
print('-----------------------------')
'''
- Reads the current price files created by current_price.py
- Adds the new price to the statistics files every 1 minute
'''

# - Current price files to read from:
product_file_LTC = 'LTC-USD.txt'
product_file_ETH = 'ETH-USD.txt'
product_file_BTC = 'BTC-USD.txt'

# - Output files to append the price onto:
fileName_LTC = 'stats_LTC-USD.txt'
fileName_ETH = 'stats_ETH-USD.txt'
fileName_BTC = 'stats_BTC-USD.txt'

# - Parameters:
event_log_file = 'statistics.log'
error_log_file = 'stat_maint_error.log'
update_time = 60

# - Variables:
last_price_LTC = 0
current_price_LTC = 0
last_price_ETH = 0
current_price_ETH = 0
last_price_BTC = 0
current_price_BTC = 0



print()
print()
print("Initiating Statistic Maintenance BOT...")
print("- Appending new price every", update_time, "seconds")

# - Creating error log:
print()
print("Adding entry to the log...")
ts = time.time()
st = datetime.datetime.fromtimestamp(ts).strftime('%Y-%m-%d %H:%M:%S')
appendFile = open(event_log_file, 'a') 
appendFile.write('\n\n\nstatistics_maintain.py started at: ')
appendFile.write(st)
appendFile.write('\n')
appendFile.close()
print("- Done!")


try:
    print()
    print()
    print("Starting loop...")
    while True:
        
        # - Get current time:
        ts = time.time()
        st = datetime.datetime.fromtimestamp(ts).strftime('%Y-%m-%d %H:%M:%S')
        print()
        print()
        print()
        print()
        print()
        print()
        print()
        print()
        print()
        print('Statistic Maintenance BOT is running')
        print("- Appending new price every", update_time, "seconds")
        print("- Last append time:", st)

        # - Read the current prices:
        # -- Read current_price_LTC:
        current_price_LTC = open(product_file_LTC, 'r').read()
        print()
        print("- Reading prices...")
        try:
            current_price_LTC = str(current_price_LTC)
        except Exception as error:
            print("ERROR handler: check error log")
            current_price_LTC = last_price_LTC
            appendFile = open(error_log_file, 'a')
            appendFile.write('\n\n')
            appendFile.write(st)
            appendFile.write(' : ERROR while setting current_price_LTC to str handeled ( current_price_LTC = last_price_LTC ). ')
            appendFile.write('\n- Current price_LTC =')
            appendFile.write(current_price_LTC)
            appendFile.write('\n- Reason: ')
            appendFile.write(str(error))
            appendFile.write('\n- END Reason')
            appendFile.close()
        print("-- LTC price:", current_price_LTC)
        # -- Read current_price_ETH:
        current_price_ETH = open(product_file_ETH, 'r').read()
        try:
            current_price_ETH = str(current_price_ETH)
        except Exception as error:
            print("ERROR handler: check error log")
            current_price_ETH = last_price_ETH
            appendFile = open(error_log_file, 'a')
            appendFile.write('\n\n')
            appendFile.write(st)
            appendFile.write(' : ERROR while setting current_price_ETH to str handeled ( current_price_ETH = last_price_ETH ). ')
            appendFile.write('\n- Current price_ETH =')
            appendFile.write(current_price_ETH)
            appendFile.write('\n- Reason: ')
            appendFile.write(str(error))
            appendFile.write('\n- END Reason')
            appendFile.close()
        print("-- ETH price:", current_price_ETH)
        # -- Read current_price_BTC:
        current_price_BTC = open(product_file_BTC, 'r').read()
        try:
            current_price_BTC = str(current_price_BTC)
        except Exception as error:
            print("ERROR handler: check error log")
            current_price_BTC = last_price_BTC
            appendFile = open(error_log_file, 'a')
            appendFile.write('\n\n')
            appendFile.write(st)
            appendFile.write(' : ERROR while setting current_price_BTC to str handeled ( current_price_BTC = last_price_BTC ). ')
            appendFile.write('\n- Current price_BTC =')
            appendFile.write(current_price_BTC)
            appendFile.write('\n- Reason: ')
            appendFile.write(str(error))
            appendFile.write('\n- END Reason')
            appendFile.close()
        print("-- BTC price:", current_price_BTC)
        print("-- Done!")
        
        
        # - Apend the prices:
        print()
        print("- Appending prices...")
        appendFile = open(fileName_LTC, 'a')
        appendFile.write('\n')
        appendFile.write(current_price_LTC)
        appendFile.close()
        print("-- appending to", fileName_LTC)
        appendFile = open(fileName_ETH, 'a')
        appendFile.write('\n')
        appendFile.write(current_price_ETH)
        appendFile.close()
        print("-- appending to", fileName_ETH)
        appendFile = open(fileName_BTC, 'a')
        appendFile.write('\n')
        appendFile.write(current_price_BTC)
        appendFile.close()
        print("-- appending to", fileName_BTC)
        print("-- Done!")

        
        # - Remember the last prices:
        last_price_LTC = current_price_LTC
        last_price_ETH = current_price_ETH
        last_price_BTC = current_price_BTC
            
        
        # - End loop:
        time.sleep(update_time)
 

# - Crash reporting:
except Exception as error:
    print()
    print()
    print()
    print("********************************")
    print("Shutting down due to an error...")
    print("--- --- ---")
    print("Error:")
    print(str(error))
    print("--- --- ---")
    print("Appending the error to", error_log_file)
    print()
    print("- Done!")
    print("********************************")
    ts = time.time()
    st = datetime.datetime.fromtimestamp(ts).strftime('%Y-%m-%d %H:%M:%S')
    appendFile = open(error_log_file, 'a') 
    appendFile.write('\n\n\nstatistics_maintain.py crashed at: ')
    appendFile.write(st)
    appendFile.write('\n- Reason: ')
    appendFile.write(str(error))
    appendFile.write('\n- END Reason')
    appendFile.close()

















