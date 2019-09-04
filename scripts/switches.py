#!/usr/bin/env python
import rospy,sys
from pimouse_ros.msg import Switches
def get_freq():
	f=rospy.get_param('switches_freq',10);
	try:
		if f <= 0.0:	raise Exception()
	except:
		rospy.logerr("value error: switches_freq")
		sys.exit(1)

	return f 

if __name__=='__main__':
	devfile='/dev/rtswitch'
	rospy.init_node('switches')
	pub = rospy.Publisher('switches',Switches,queue_size=10)
	freq=get_freq()
	rate=rospy.Rate(freq)
	d=Switches()
	d.state='neutral'
	state_change_counter=0
	while not rospy.is_shutdown():
		try:
			with open(devfile+'0','r') as f:
				d.front=True if '0' in f.readline() else False
			with open(devfile+'1','r') as f:
				d.center=True if '0' in f.readline() else False
			with open(devfile+'2','r') as f:
				d.rear=True if '0' in f.readline() else False	

			pub.publish(d)
		except:
			rospy.logerr("cannnot read to "+devfile+"[0,1,2]")

		if d.front: state_change_counter+=1

		if state_change_counter >=5 and not d.front:
			stage_change_counter =0
			if d.state == 'neutral':	d.state='ready'
			elif d.state =='ready':		d.state='run'
			else:				d.state='neutral'

		f=get_freq()
		if f!=freq:
				freq = f
				rate=rospy.Rate(freq)

		rate.sleep()

