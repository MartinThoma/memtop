#!/usr/bin/env python

#Memtop - prints applications that consumes most of RAM
#Tested with python 2.7 and 3.x
#Contact: tiborb95 at gmail dot com, any comments appreciated
#version 1.0.1
#changes since 0.9.0: compatibility with python3, fixed bug causing that 
# * grepping was not possible due to binary (&invisible) characters in output
# * added "more" information about swapping and memory+swap use
# * logging to a file added
#
#data structures uses:
#key_pid  - dictionary adjusted_mem:PID
#pid_omem - dictionary PID:Old Memory
#pid_mem  - dictionary PID:Memory


from os import listdir,getlogin,getenv,path,sysconf,sysconf_names
from subprocess import Popen, PIPE
from time import sleep, strftime, localtime, time
from getopt import getopt, GetoptError
from sys import exit, argv, stdout, version_info
from re import compile
from string import printable
from shutil import move
import signal


# GLOBAL VARIABLES
_rows=10        #number of programs to list
_period=15   #default period
_format="graph"
_more=False
_log=False
pid_omem={}     #dictionary PID:mem
oldMemUsage=0  #number
_firstiteration=True
_curtime=0
_oldtime=0
_oldpswpin=0
_oldpswpout=0
_oldpgpgin=0
_oldpgpgout=0
_swapinsec=0
_swapoutsec=0
_pageinsec=0
_pageoutsec=0
_oldIOwait=0
_IOwaitprc=0
_logfile="memtop.log"


# FUNCTIONS

def signal_handler(signal, frame):
	stdout.flush() 
	print ("\nSIGINT signal received. Quitting...")
	stdout.flush() 
	exit(0)
signal.signal(signal.SIGINT, signal_handler)

def getCommandOutput(command):
	tmp = Popen(command,shell=True,stdout=PIPE)
	output = tmp.communicate()[0]#.rstrip().rstrip().rstrip()
	return output

def formatMemNumb(memory):
	#shortening memory to include suffix MB or kB)
	if int(memory) >= 1048576:
		memOutput = str(round(float(memory)/1048576,1)) + " MB"
	elif int(memory) >= 1024:
		memOutput = str(round(float(memory)/1024,1)) + " kB"
	else:
		memOutput = str(memory) +" B"
	return memOutput

def graphFormat(newMem,oldMem):
	#graphically shows changes in memory consumption
	global _firstiteration
	
	if _firstiteration:
		output="  n/a   "
	elif newMem - oldMem > 50000000:
		output="   +++++"
	elif newMem - oldMem > 20000000:
		output="   ++++ "
	elif newMem - oldMem > 5000000:
		output="   +++  "
	elif newMem - oldMem > 1000000:
		output="   ++   "
	elif newMem - oldMem > 50000:
		output="   +    "
	elif oldMem - newMem > 10000000:
		output="---     "
	elif oldMem - newMem > 2000000:
		output=" --     "
	elif oldMem - newMem > 100000:
		output="  -     "
	else:
		output="        "
	return output


def getCurMemUse():
	#return utilization of memory
	#http://lwn.net/Articles/28345/
	
	inactive=0
	lines = open("/proc/meminfo", 'r').readlines()
	emptySpace = compile('[ ]+')
	for line in lines:
		if "MemTotal" in line:
			memtotal = float(emptySpace.split(line)[1])
		if "SwapFree" in line:
			swapfree = float(emptySpace.split(line)[1])
		if "SwapTotal" in line:
			swaptotal = float(emptySpace.split(line)[1])
		if "MemFree" in line:
			memfree = float(emptySpace.split(line)[1])
		if "Cached" in line and not "SwapCached" in line:
			cached = float(emptySpace.split(line)[1])

	ramoccup    = 1.0 - (memfree+cached)/memtotal
	if swaptotal==0:
		swapoccup=0
	else:
 		swapoccup   = 1.0 - swapfree/swaptotal
	strramoccup = str(round(ramoccup*100.0,1))
	strswapoccup= str(round(swapoccup*100.0,1))
	
	return float(memtotal),strramoccup,strswapoccup


def usage():
	print ("")
	print ("   MEMTOP is command line utility (python script)\
 to help user to find out \
what applications uses biggest portions of the memory (RAM+swap), sorted in decreasing order. \
It lists private/writeable memory only, that is without shared memory. \
Typical use is when you need to reduce the overall RAM consumption or when you \
encounter performance problems.")
	print ("   Version 1.0")
	print ("   Memtop gets data from /proc/ virtual filesystem.")
	print ("   Home: http://code.google.com/p/memtop/ ")
	print ("")
	print ("   Available switches:")
	print (" -p/--period=  waittime between iterations in minutes")
	print (" -s/--show=    either graph or numb, it selects the way \
how data mainly for previous period are presented.")
	print (" -l/--lines=   number of processes reported")
	print (" -m/--more    additional info about memory utilization and swaping/paging")
	print (" -L/--log     saves basic data into logfile")
	print (" -h/--help     ")
	print ("")
	print ("   You can contact me at tiborb95 at gmail dot com"+'\033[0m')
	

def getPrivateMem(pid):
	sum=0;
	for line in open("/proc/" + str(pid) + "/maps", "rb").readlines():
		line=line.decode("ascii")
		if not line[21] == "p":
			continue
		if not line [19] == "w":
			continue
	
		start=int(line[:8],16)
		end=int(line[9:17],16)
		sum=sum+end-start

	return sum


def checkSwapping():

	global _firstiteration
	global _curtime
	global _oldtime
	global _oldpswpin
	global _oldpswpout
	global _oldpgpgin
	global _oldpgpgout
	global _swapinsec
	global _swapoutsec
	global _pageinsec
	global _pageoutsec
	global _oldIOwait
	global _IOwaitprc
	global _jiffy
	global _more
	
	if not path.exists("/proc/vmstat"):
		print ("   ERROR: file /proc/vmstat not found....")
		return
	if not path.exists("/proc/stat"):
		print ("   ERROR: file /proc/stat not found...")
		return

	emptySpace = compile('[ ]+')

	for line in open("/proc/vmstat").readlines():	
		if "pswpin" in line:
			pswpin  = int(emptySpace.split(line)[1])
		if "pswpout" in line:
			pswpout = int(emptySpace.split(line)[1])
		if "pgpgin" in line:
			pgpgin  = int(emptySpace.split(line)[1])
		if "pgpgout" in line:
			pgpgout = int(emptySpace.split(line)[1])
		_curtime=time()
		
	IOwait  = int(open("/proc/stat").readlines()[0].split()[5])
	cpucount= int(sysconf(sysconf_names['SC_NPROCESSORS_ONLN']))
	_jiffy  = int(sysconf(sysconf_names['SC_CLK_TCK']))

		
	if not _firstiteration:

		timediff   = _curtime-_oldtime
		_swapinsec = ( pswpin  - _oldpswpin ) /timediff
		_swapoutsec= ( pswpout - _oldpswpout) /timediff
		_pageinsec = ( pgpgin  - _oldpgpgin ) /timediff
		_pageoutsec= ( pgpgout - _oldpgpgout) /timediff
		_IOwaitprc = ( IOwait  - _oldIOwait ) *100 / _jiffy / (cpucount * timediff)
		if _more:
			print ("   Swapping: "+str(round(_swapinsec,1))+" / "+str(round(_swapoutsec,1))+\
			", Paging: "+str(round(_pageinsec,1))+" / "+ str(round(_pageoutsec,1))+\
			" (in/out / sec). CPU I/O wait: "+str(round(_IOwaitprc,1))+" %")
	
	_oldpswpin=pswpin
	_oldpswpout=pswpout
	_oldpgpgin=pgpgin
	_oldpgpgout=pgpgout
	_oldtime=_curtime
	_oldIOwait=IOwait
	
def check_py_version():
	try:
		if version_info>=(2,7):
			return
	except:
		pass
	print (" ")
	print (" ERROR - memtop needs python version at least 2.7")
	print ("Chances are that you can install newer version from your repositories, or even that you have some newer version installed yet.")
	print ("(one way to find out which versions are installed is to try following: 'which python2.7' , 'which python3' and so...)")
	print (" ")
	exit()
	
	
###################################
######## BODY: INITIALIZATION #####
###################################

check_py_version()

try:
	opts,args = getopt(argv[1:], "p:s:l:hmL", \
	["period=","show=","lines=","help","more","log"])
	for opt, arg in opts:
		if opt in ("-p", "--period"):
			try:
				_period = int(arg)
				if _period<1:
					_period=1
			except:
				print ("WARNING: Using default iteration time: "+str(_period)+" min")
		if opt in ("-m", "--more"):
			_more=True
		if opt in ("-L", "--log"):
			_log=True
		if opt in ("-l", "--lines"):
			try:
				_rows = int(arg)
			except:
				print ("WARNING: Using default number of lines:"+str(_rows))
		if opt in ("-s", "--show"):
			try:
				if arg in ('graph','Graph','graf','graphic'):
					_format = "graph"
				elif arg in ('numb','Numb','num'):
					_format = "numb"
				else:
					_format = "graph"
					print ("WARNING: Wrong type of total RAM use \
presentation, using default")

			except:
				print ("WARNING: Using default format for old values:"+ str(_format))
		if opt in ("-h", "--help"):
			usage()
			exit()

except GetoptError:
	print (" ")
	print  ('\033[0m'+'\033[95m'+" ! You entered incorrect switches to the script. Please \
read help (will be printed out in a while.)"+'\033[37;32m')
	sleep(2)
	usage()
	sleep(6)
	print ("")
	print ('\033[0m'+'\033[95m'+" ! ! ! Continuing in 15 seconds, but some switches \
can be ignored altogether..."+'\033[0m')
	print ("")
	sleep(15)

# who am I?
user = getCommandOutput("whoami || echo failed")
user=user.decode()
# following two methods are not reliable
if user == "failed":
	try:
		user = getenv('USER').decode()
	except:
		pass
if user == "failed":
	print (" ! Failed to find out the current user")


#preparing logfile
if _log:
	try:   #the destination might not be writeable
		if path.isfile(_logfile):
				move(_logfile, _logfile+".old")
		lfile = open(_logfile, 'a')  
		lfile.write("##Date     time   wrtble ram   swap     pgin   pgout   IOw TopApp:PID wrtbl(KB) command\n")
		lfile.close()
	except:
		print (" \033[0m \033[95m ERROR: Failed to prepare/create the log file in current directory!\033[0m")
		_log=False

###########################################
#######      BODY: LOOPING       ##########
###########################################

while 1:
	memD={}				#key(~memory):real memory
	keys=()				#list of keys (to be listed by size)
	key_pid={}				#key(~memory):PID
	pid_mem={}			#dictionary of PID to cur memory, redefining to empty it
	margin = 0.0001     #this is ugly workaround to make sure there are no same numbers
	totalMemByPmap = 0
	oldMemDtmp = {}  	# dictionary of mem. in previous iteration PID:mem
	processes=0			#count of identified processes

	for dir in listdir('/proc'):     # first we will identify number of processes
		try: #elimination non-numerical dirs
			int(dir)                 #dir = PID
		except:
			continue

		#calculating private memory in /proc/$PID/maps file
		try:
			realMem= getPrivateMem(dir)
		except:   #process probably doesnt exist anymore
			continue
		
		totalMemByPmap = totalMemByPmap + int(realMem)

		#creating key, this is basically real memory plus
		# a very small number
		key1 = int(realMem) + margin
		key_pid[key1]=dir
		pid_mem[dir]=realMem		
		margin = margin + 0.0001
	#now we have all memory data for current iteration


	#creating list of keys - sorted
	keys = key_pid.keys()
	keys=sorted(keys,reverse=True)
	processes=len(keys)
	#print (key_pid)

	##############  printing ##################
	
	# finding terminal lenght (doing it every iteration)
	try:
		width=int(getCommandOutput("stty size | awk '{print $2}'"))
	except:
		width=80
	if width < 46:
		print ('\033[0m'+'\033[95;1m'+" ! Terminal width "+str(width)+" not sufficient, 46 is minimum...."+'\033[0m')
		width= 46

	#calculating widht of individual columns
	col1,col2,col3 = 8,11,11
	col4=int((width-col1-col2-col3-2)/2)
	col5=width -col1-col2-col3-col4


	# # # printing header
	if _format == "numb":
		a="previous |"
	elif _format == "graph":
		a="change  |"
	curtime=strftime("%d %b %H:%M:%S", localtime())[-col5:]
	print ("\033[0m\033[1m{:>{a}s}{:>{b}s}{:<{c}s}{:>{d}s}".format("PID |","private/writ. mem |","command",curtime,a=col1,b=col2+col3,c=col4,d=col5))
	wtime=str("(waiting "+str(_period)+" min.)")[-col5:]
	trunc="(might be truncated)"[:col4]
	print ("{:>{a}s}{:>{b}s}{:>{c}s}{:<{d}s}{:>{e}s}\033[0m".format("|","current |",a,trunc,wtime,\
	a=col1,b=col2,c=col3,d=col4,e=col5))


	# # # printing body (lines with processes)
	printedlines=0		#just count printed lines
	#print ("processes:" +processes)
	for item in keys[0:processes]:
		
		#print ("Doing: "+item)
		#gettind command and shortening if needed
		try:
			pid=key_pid[item]
			cmdfile=str("/proc/"+str(pid)+"/cmdline")
			f=open(cmdfile,'r')
			command = open(cmdfile, "rt").read().replace("\0"," ")[:col4+col5]
			f.close()
		except:
			continue
		
		#print (command)
		#getting formatted value of current memory usage
		curMem=pid_mem[pid]
		try:
			oldMem=pid_omem[pid]
		except:
			oldMem=0


		curMemStr=formatMemNumb(curMem)
		if _format == "numb":
			s2=formatMemNumb(oldMem)+" |"
		elif _format == "graph":
			s2=graphFormat(curMem,oldMem)+" |"

		s0=str(key_pid[item]+" |")
		s1=str(curMemStr+" |")
		command = ''.join(s for s in command if s in printable)  #getting rid of binary characters
		
		print ("{:>{a}s}{:>{b}s}{:>{c}s}{:<{d}s}".format(s0,s1,s2,command,a=col1,b=col2,c=col3,d=col4+col5))
		
		if _log and printedlines ==0:
			outline_comm=" {:>7s} {:>9.0f}  {:20s}".format(pid,round(curMem/1024,0),command)
		
		printedlines=printedlines+1
		if printedlines>=_rows:
			break


	# # # printing footer - info on overall cpu utilization
	totalMem,ramuse,swapuse=getCurMemUse()
	totalMemByPmapKB = int(round(totalMemByPmap / 1000, 1))
	curMemUsage = round(totalMemByPmapKB*100/float(totalMem),1)

	if _format == "numb":
		print ("{:>18s}{:>4.1f}{:s}{:5.1f}{:<1s}".format("Writeable/RAM: ",curMemUsage,"%     (old value: ",oldMemUsage,"%)"))
	elif _format == "graph":
		onePrc = width / 280.0
		firstLen=int(round(min(curMemUsage,100) * onePrc))
		if curMemUsage>100:
			secondLen=int(round((curMemUsage-100) * onePrc))
		else:
			secondLen=0
		#print curMemUsage, onePrc, firstLen , secondLen
		bar=str('='*firstLen+str('#'*secondLen))
		print ("{:>18s}{:s}{:>6.1f}{:s}".format("Writeable/RAM: ", bar,curMemUsage,"%"))
		
	else:
		print (" ! Unexpected data presentation format - internall error, quitting...")
		exit()

	if _more:
		print ("   RAM use without cached pages: "+ramuse+"% , SWAP use: "+swapuse+"%")
	if _more or _log:
		checkSwapping()
	
	
	# print warning if user is not root
	if "root" not in user:
		print ("")
		print ("     \033[0m \033[95m WARNING: Running without ROOT CREDENTIALS, data might be incomplete...\033[0m")

	oldMemUsage = curMemUsage
	pid_omem=pid_mem.copy()
	print ("")

	_firstiteration=False

	stdout.flush()  #because of problems when piping output. But might be not needed

	#writing logfile
	if _log:
		lfile = open(_logfile, 'a') 
		outline_time=strftime("%d/%m/%Y")+" "+strftime("%H:%M")+" "
		outline_ram=" {:>5s} {:>5s} {:>5s}".format(str(curMemUsage),str(ramuse),str(swapuse))
		outline_pg=" {:>8.2f}{:>8.2f}{:>6.1f}".format(_pageinsec,_pageoutsec,_IOwaitprc)
		lfile.write(outline_time+ outline_ram+outline_pg+ outline_comm+"\n")
		lfile.close()


	sleep(_period*60-2)
