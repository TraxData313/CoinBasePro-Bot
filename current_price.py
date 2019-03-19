import cbpro, time, datetime
public_client = cbpro.PublicClient()

current_value_LTC = 0
current_value_ETH = 0
current_value_BTC = 0
ts = time.time()
st = datetime.datetime.fromtimestamp(ts).strftime('%Y-%m-%d %H:%M:%S')
appendFile = open('CurrentPrice.error.log', 'a') # w for write , r for read | wipes the file when opening it!
appendFile.write('\n\nCurrentPrice.error.log started at: ')
appendFile.write(st)
appendFile.write('\n')
appendFile.close()

while True:

    ts = time.time()
    st = datetime.datetime.fromtimestamp(ts).strftime('%Y-%m-%d %H:%M:%S')

    # Read price:
    
    ## LTC-EUR
    try:
        current_value_LTC = public_client.get_product_ticker(product_id='LTC-EUR')
    except:
        print '\n\nERROR added to CurrentPrice.error.log'
        appendFile = open('CurrentPrice.error.log', 'a') # a for append
        appendFile.write('\n')
        appendFile.write(st)
        appendFile.write(' - Error while getting current_value_LTC')
        appendFile.close()
        pass
    try:
        current_value_LTC = str(current_value_LTC['price'])
    except:
        print '\n\nERROR added to CurrentPrice.error.log'
        appendFile = open('CurrentPrice.error.log', 'a') # a for append
        appendFile.write('\n')
        appendFile.write(st)
        appendFile.write(' - Error while setting current_value_LTC to str')
        appendFile.write('\n')
        appendFile.close()
        pass
            
    ## ETH-EUR
    try:
        current_value_ETH = public_client.get_product_ticker(product_id='ETH-EUR')
    except:
        print '\n\nERROR added to CurrentPrice.error.log'
        appendFile = open('CurrentPrice.error.log', 'a') # a for append
        appendFile.write('\n')
        appendFile.write(st)
        appendFile.write(' - Error while getting current_value_ETH')
        appendFile.write('\n')
        appendFile.close()
    try:
        current_value_ETH = str(current_value_ETH['price'])
    except:
        print '\n\nERROR added to CurrentPrice.error.log'
        appendFile = open('CurrentPrice.error.log', 'a') # a for append
        appendFile.write('\n')
        appendFile.write(st)
        appendFile.write(' - Error while setting current_value_LTC to str')
        appendFile.write('\n')
        appendFile.close()
        pass

    ## BTC-EUR
    try:
        current_value_BTC = public_client.get_product_ticker(product_id='BTC-EUR')
    except:
        print '\n\nERROR added to CurrentPrice.error.log'
        appendFile = open('CurrentPrice.error.log', 'a') # a for append
        appendFile.write('\n')
        appendFile.write(st)
        appendFile.write(' - Error while getting current_value_BTC')
        appendFile.write('\n')
        appendFile.close()
    try:
        current_value_BTC = str(current_value_BTC['price'])
    except:
        print '\n\nERROR added to CurrentPrice.error.log'
        appendFile = open('CurrentPrice.error.log', 'a') # a for append
        appendFile.write('\n')
        appendFile.write(st)
        appendFile.write(' - Error while setting current_value_BTC to str')
        appendFile.write('\n')
        appendFile.close()
        pass


    # Write price:
    ## LTC-EUR
    appendFile = open('LTC-EUR.txt', 'w')
    try:
        appendFile.write(current_value_LTC)
    except:
        print 'ERROR writing the price to file - possible site down'
        print 'Check site status at: https://status.gdax.com/'
        appendFile.write('ERROR writing the price to file - possible site down')
    appendFile.close()
    ## ETH-EUR
    appendFile = open('ETH-EUR.txt', 'w')
    try:
        appendFile.write(current_value_ETH)
    except:
        print 'ERROR writing the price to file - possible site down'
        print 'Check site status at: https://status.gdax.com/'
        appendFile.write('ERROR writing the price to file - possible site down')
    appendFile.close()
    ## BTC-EUR
    appendFile = open('BTC-EUR.txt', 'w')
    try:
        appendFile.write(current_value_BTC)
    except:
        print 'ERROR writing the price to file - possible site down'
        print 'Check site status at: https://status.gdax.com/'
        appendFile.write('ERROR writing the price to file - possible site down')
    appendFile.close()


    # Print:
    print
    print
    print
    print st
    print
    print '----------'
    print 'LTC-EUR:'
    print 'Current value:', current_value_LTC
    print '----------'
    print
    print '----------'
    print 'ETH-EUR:'
    print 'Current value:', current_value_ETH
    print '----------'
    print
    print '----------'
    print 'BTC-EUR:'
    print 'Current value:', current_value_BTC
    print '----------'
    
        
    time.sleep(1)
