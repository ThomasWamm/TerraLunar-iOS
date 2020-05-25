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
print(f'Sum = {sum}')
print(f'Ran {loops:1,d} loops in {elapsed:3,.1f} seconds, so {(loops/elapsed):3,.0f} loops per second.')

'''
Results on different devices: 
	iPad Air2	      4,556k loops/s
	iPhoneX		      9,338k loops/s
	iPod6           3,421k loops/s
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

