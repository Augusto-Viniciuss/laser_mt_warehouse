#import rospy
from Mambo.src.Drone import Drone
from Turtlebot2.src.Turtle import Turtle

mambo = Drone("?????")
rospy.init_node("follow_route", anonymous = False)
turtle = Turtle()

end_route = False
print("antes da função")
status_turtle = turtle.go_to_shelf()

while not end_route:
    if(status_turtle):
        turtle.stop()
        status_mambo = mambo.fly()

        if(status_mambo):
            turtle.go_to_shelf()
    
    end_route = turtle.check_end_route()
            
mambo.disconnect()

Laser 1 Logistic Multi-Robot