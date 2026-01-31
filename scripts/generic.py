#!/usr/bin/env python3

import numpy as np
import matplotlib.pyplot as plt

import rclpy
from rclpy.node import Node
from rclpy.qos import QoSProfile, QoSDurabilityPolicy
from rclpy.clock import Clock

from std_msgs.msg import Float32MultiArray
from visualization_msgs.msg import Marker
from rosflight_msgs.msg import SimState
from roscopter_msgs.srv import AddWaypoint
from rosflight_msgs.msg import GNSS
NodeName = 'sensorToWaypoints'

SensorMsgType = Float32MultiArray
SensorTopicName = 'sensors/walls_sensor'



class Autopilot(Node):

    def __init__(self):
        super().__init__(NodeName)
        # self.clock = self.get_clock()
        # self.init_time = self.clock.now()
        # self.min_distance = []
        # self.walls = []
        # self.karl = None
        # self.finished = False

        #node state
        self.nesw = []
        self.prevDirection = 0
        self.position
        self.altitude = 5
        self.req = AddWaypoint.Request()
        self.req.wp.w= [0.0,0.0,self.altitude]
        self.req.wp.psi=0

        #needs to know previous direction it came from.
        #needs to know if we've arrived at a waypoint
        #needs to know if 

        # Quality of service profile to collect walls
        qos_profile = QoSProfile(
            depth=20,
            durability=QoSDurabilityPolicy.TRANSIENT_LOCAL
        )
        # # Publisher and subscribers
        #listen for sensor inputs
        self.sensor_sub = self.create_subscription(SensorMsgType, SensorTopicName, self.getDistances, 10)

        self.waypoint_pub = self.create_client(AddWaypoint,"path_planner/add_waypoint")
        while not self.waypoint_pub.wait_for_service(timeout_sec=1.0):
            self.get_logger().info('service not available, waiting again...')
        print("should be able to communicate with service")
        self.waypoint_pub.call_async(self.req)
        #needs to listen for if the quadrotor is at a waypoint
        self.stateSub = self.create_subscription(SimState, 'sim/truth_state', self.positionCallback, 10)

        print("initialization complete")


    def getDistances(self, msg):
        n = ("n", msg.data[0])
        e = ("e", msg.data[1])
        s = ("s", msg.data[2])
        w = ("w", msg.data[3])
        self.nesw = [n,e,s,w]
        # print("NESW: ", self.nesw)
        if self.closeToWaypoint():
             self.nextWaypoint = self.calcNextWaypoint()

    def positionCallback(self, msg):
        print("got data on current state!")
        print(msg.pose.postion)
        self.position = msg.pose.position
    
    def closeToWaypoint(self):
         pos = self.position
         point = self.nextWaypoint
         return np.sqrt(pos.x**2 + pos.y**2) <= 2
         
    def calcNextWaypoint(self):
         pos = self.position
         directions = self.nesw.copy() # make a copy so I don't mutate important data
         directions.sort(key=lambda item: item[1], reverse=True) #sort directions so furthest is index 1
         #based off previous direction, check if the furthest direction to go is which way

         
         
    




def DistToCoords(nesw):
        print("calculating coords for next waypoint")
        #take distances in each direction, and determine which way(s) haven't been traveled, and return a waypoint to
        #travel towards that is new. 
        return np.array([0,0,0,0])

    

def main(args=None):
    rclpy.init(args=args)
    node = Autopilot()
    rclpy.spin(node)
    rclpy.shutdown()

if __name__ == '__main__':
    main()