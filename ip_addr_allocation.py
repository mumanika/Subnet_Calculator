import socket
import binascii
import sys
import ipaddress
import os.path

def subnetTheNetwork(netId,k):
	subnetList=list(netId.subnets(new_prefix=32-k))
	return subnetList
	
def calculateK(hostReq):
	k=1
	while True:
		if 2**k < hostReq+2:
			k=k+1
			continue
		else:
			break	
	return k
	
def retrieveList():
	subnetList=[]
	with open("Subnet_List.txt","r") as f:
		Contents=f.readlines()
		
		for x in Contents:
			value=ipaddress.IPv4Network(unicode(x[:-1],'utf-8'),strict=False)
			subnetList.append(value)
			
	f.close()
	return list(subnetList)


def retrieveAssignedList():
	subnetList=[]
	with open("Subnet_List_Assigned.txt","r") as f:
		Contents=f.readlines()
		
		for x in Contents:
			value=ipaddress.IPv4Network(unicode(x[:-1],'utf-8'),strict=False)
			subnetList.append(value)
			
	f.close()
	return list(subnetList)
	
def writeList(subnetList):
	with open("Subnet_List.txt","w") as f:
		for x in subnetList:
			f.write('%s\n' % x)
		f.close()	
		
def appendList(subnet):
	with open("Subnet_List_Assigned.txt","a+") as f:
		f.write('%s\n' % subnet)
		f.close()
		
def overlapAssigned(subnetTemp):
	assignedList=retrieveAssignedList()
	for x in assignedList:
		if subnetTemp.overlaps(x):
			return True
		else:
			continue
	
def subnetFunction(subnet, subnetList, prefix_length_diff):
	new_subnets=list(subnet.subnets(prefixlen_diff=prefix_length_diff))
	for x in subnetList:
		new_subnets.append(x)
	return new_subnets
	
	
	
useExistingFlag=False
if os.path.exists('Subnet_List.txt'):
	useExistingFlag=True		
		
print "Enter the network IP address with the class:\nEg. 1.2.3.4/12"
userIpString=unicode(raw_input("IP Address:").strip().replace(' ',''),'utf-8')
netId=ipaddress.IPv4Network(userIpString,strict=False)

print "Enter the number of hosts that are required:"
hostReq=int(raw_input("Hosts:"))
if hostReq is 0:
	print "Host number cannot be zero! Please enter a non-zero value."
	sys.exit(0)

subnet=[]
subnetTemp=[]

if useExistingFlag:
	subnetList=retrieveList()

	if not(netId.supernet_of(subnetList[0])):
		print "Please delete/save in another the existing files from the directory where the program is stored.\nThis will allow the program to allocate addresses with the new network ID."

	elif hostReq <= len(list(subnetList[0].hosts())) and (netId.supernet_of(subnetList[0])):
		new_k=calculateK(hostReq)
		old_k=32-subnetList[0].prefixlen
		if old_k==new_k:
			subnet=subnetList.pop(0)
			print "The subnet that the customer can use is: ", subnet
			writeList(subnetList)
			appendList(subnet)
		else: 
			subnetTemp=subnetList.pop(0)
			subnetList = subnetFunction(subnetTemp, subnetList, old_k-new_k)
			subnet=subnetList.pop(0)
			print "The subnet that the customer can use is: ", subnet
			writeList(subnetList)
			appendList(subnet)
	
	elif hostReq > len(list(subnetList[0].hosts())) and (netId.supernet_of(subnetList[0])):
		new_k=calculateK(hostReq)
		old_k=32-subnetList[0].prefixlen
		#print new_k, old_k
		subnetTemp=[]
		subnet=[]
		supernet=[]
		for x in subnetList:
			subnetTemp=x.supernet(prefixlen_diff=new_k-old_k)
			if overlapAssigned(subnetTemp):
				continue
			else:
				supernet=subnetTemp
				subnet=x
				subnetList.remove(subnet)
				break
		print "The subnet that the customer can use is: ", supernet
		for x in subnetList:
			#print x
			if x.subnet_of(supernet):
				subnetList.remove(x)
		writeList(subnetList)
		appendList(supernet)
					
else: 
	k=calculateK(hostReq)
	subnetList=subnetTheNetwork(netId,k)
	subnet=subnetList.pop(0)	
	print "The subnet that the customer can use is: ", subnet
	writeList(subnetList)
	appendList(subnet)
	
		
		

	
	







