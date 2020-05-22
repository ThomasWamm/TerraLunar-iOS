# How fast does Python loop on my gadgets?

import time

print('Running...')

starttime = time.process_time()
sum = 0
loops = int(1e8)

for i in range(loops):
	sum += i

endtime = time.process_time()
elapsed = endtime - starttime
print('Sum = {sum}')
print(f'Ran {loops:1,d} loops in {elapsed:3,.1f} seconds, so {(loops/elapsed):3,.0f} loops per second.')

'''
Results on different devices: 
	iPad Air2	      Ran 100,000,000 loops in 24.4 seconds, so 4,094,389 loops per second.
	iPhoneX		      Ran 100,000,000 loops in 10.7 seconds, so 9,338,982 loops per second.
	iPod6           
	Dell Optiplex   
	Dell laptop     
	HP laptop       
	Dell Mini       
	iMac_2007       
	Rpi4  
	Rpi3blk
	Rpi3clr
	Rpi0w
'''

