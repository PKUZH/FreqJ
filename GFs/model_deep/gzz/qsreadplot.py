import obspy
import subprocess
import re
import numpy as np
from obspy.core.trace import Trace
from obspy.core.trace import Stats
from functools import reduce
from obspy.core import read
import matplotlib.pyplot as plt
#re.findall 匹配字符串中符合表达式的连续串。'\d+\d*'匹配的是任意位的整数，而'\d+\.?\d*匹配任意位的小鼠'
def rdata(filename,n,e_abbtrueorfalse):
	idofstation=subprocess.Popen(["cat %s"%(filename)+" | awk '{{if(NR==1) print $%d"%(n)+"}}' "],stdout=subprocess.PIPE, shell=True)
	idofstation1=idofstation.stdout.read()
	idofstation2=re.findall(r'\d+\d*',str(idofstation1))
	numoftsample=subprocess.Popen(["cat %s"%(filename)+" | wc -l"],stdout=subprocess.PIPE, shell=True)
	numoftsample1=numoftsample.stdout.read()
	numoftsample2=int(re.findall(r'\d+\d*',str(numoftsample1))[0])-1
	data=subprocess.Popen(["awk '{{if(NR>=2) print $%d"%(n)+"}}' %s"%(filename)],stdout=subprocess.PIPE, shell=True)
	data1=data.stdout.read()
	if (e_abbtrueorfalse=='False'):data2=re.findall(r'-?\d+\.?\d*',str(data1))
	if (e_abbtrueorfalse=='True'):data2=re.findall(r'-?\d+\.?\d*[Ee].?\d+\d*',str(data1))
	if (len(data2)!=numoftsample2):
		print('error in reading data')
		print(idofstation2[0],numoftsample2,np.array(data2))
	else:
#		print(numoftsample2,data2,len(data2))
		data=np.array(data2)
		return idofstation2[0],numoftsample2,data

def rtimedata(filename,n):
	numoftsample=subprocess.Popen(["cat %s"%(filename)+" | wc -l"],stdout=subprocess.PIPE, shell=True)
	numoftsample1=numoftsample.stdout.read()
	numoftsample2=int(re.findall(r'\d+\d*',str(numoftsample1))[0])-1
	starttime=subprocess.Popen(["awk '{{if(NR==2) print $%d"%(n)+"}}' %s"%(filename)],stdout=subprocess.PIPE, shell=True)
	starttime1=starttime.stdout.read()
	starttime2=re.findall(r'-?\d+\.?\d*',str(starttime1))
	endtime=subprocess.Popen(["awk '{{if(NR==%d"%(numoftsample2+1)+") print $%d"%(n)+"}}' %s"%(filename)],stdout=subprocess.PIPE, shell=True)
	endtime1=endtime.stdout.read()
	endtime2=re.findall(r'-?\d+\.?\d*',str(endtime1))
	#print(numoftsample2,starttime2[0],endtime2[0])
	return numoftsample2,starttime2[0],endtime2[0]

def plottogether(filenamepattern):
	stream=obspy.read(filenamepattern)
	print(stream)
	#stream.filter("bandpass",freqmin=0.5,freqmax=)
	#stream.plot(equal_scale=True,type='relative')
	stream.plot(equal_scale=True,type='normal')
	#subprocess.Popen(["ls %s"%(filenamepattern)+" | awk '{{if(NR==1) print $%d"%(n)+"}}' "],stdout=subprocess.PIPE, shell=True)
def main(sourcetype,channel):
	allsourcetype=['ex','fh','fz','cl','ds','ss','seis']
	allchannel=['tr','tz','tt','tv']
	#allchannel='rtzv'
	selectsourcetype=list(set(allsourcetype) & set(sourcetype))
	#selectchannel=list(set(channelid).intersection(set(allchannel)))
	selectchannel=list(set(allchannel) & set(channel))
	fn = lambda x, code='.': reduce(lambda x, y: [str(i)+code+str(j) for i in x for j in y], x)
	print(selectsourcetype,selectchannel)
	selectfilename=fn([selectsourcetype,selectchannel],code='.')
	print('start reading result from ',selectfilename)
	for filename in selectfilename:
		check=subprocess.Popen(["[[ -f %s"%(filename)+" ]] && echo yes"],stdout=subprocess.PIPE, shell=True)
		check1=check.stdout.read()
		if 'yes' not in str(check1): 
			print(filename,' does not exist')
			continue
		stationnum=subprocess.Popen(["cat %s"%(filename)+" | awk '{{if(NR==1) print NF}}' "],stdout=subprocess.PIPE, shell=True)
		stationnum1=stationnum.stdout.read()
		stationnum2=int(re.findall(r'\d+\d*',str(stationnum1))[0])-1
		print(stationnum2)
		[numoftsample,starttime,endtime]=rtimedata(filename,1)
		for i in range(0,stationnum2):
			#[numoftsample,starttime,endtime]=rtimedata(filename,1)
			print(filename,i+2)
			[idofstation,numoftsample,dataofstation]=rdata(filename,i+2,'True')
			stats=Stats()
			stats.npts=numoftsample
			stats.station=str(idofstation)
			stats.sampling_rate=float((numoftsample-1)/(float(endtime)-float(starttime)))
			stats.channel=filename.split('.')[1]
			trace=Trace(data=dataofstation,header=stats)
			trace.write("%s"%(filename)+"_%s"%(str(idofstation))+".SAC",format="SAC")
			print(numoftsample,starttime,endtime,idofstation,numoftsample)
	plottogether('seis.t*_0001.SAC')
main(['fz'],['tz'])
