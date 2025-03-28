import rclpy
from rclpy.node import Node
from geometry_msgs.msg import Twist
from turtlesim.srv import SetPen, Spawn, Kill
import math
import time

class TurtleDraw(Node):
    def __init__(self):
        super().__init__('turtle_draw')
        self.publisher_ = self.create_publisher(Twist, '/turtle1/cmd_vel', 10)
        self.pen_client = self.create_client(SetPen, '/turtle1/set_pen')
        self.spawn_client = self.create_client(Spawn, 'spawn')
        self.kill_client = self.create_client(Kill, 'kill')    


    def set_pen(self, r=255, g=255, b=255, width=2, off=False):
        while not self.pen_client.wait_for_service(timeout_sec=1.0):
            self.get_logger().info('Waiting for pen service...')
        req = SetPen.Request()
        req.r = r
        req.g = g
        req.b = b
        req.width = width
        req.off = off
        self.pen_is_down = not off
        self.pen_client.call_async(req)

    def turn(self, angle):
        msg = Twist()
        msg.angular.z = math.radians(angle)
        self.publisher_.publish(msg)
        time.sleep(abs(angle) / 90.0)  # Approximate turn timing
        msg.angular.z = 0.0
        self.publisher_.publish(msg)
        time.sleep(0.5)

    def draw_line(self, distance, speed=1.0):
        msg = Twist()
        msg.linear.x = speed
        self.publisher_.publish(msg)
        time.sleep(distance/speed)
        msg.linear.x = 0.0
        self.publisher_.publish(msg)
        

    def draw_sq(self,side):
         for _ in range(4):
            self.draw_line(side)
            self.turn(90)

    def draw_circle(self, radius, speed=1.0):
        """Draw circle around specified center coordinates with given radius"""
        """
            Write your logic for drawing circle here.
            Below is a code segment just to guide you, how to execute your logic
        """
        """# Set up circular motion
        angular_speed = speed / radius
        duration = ((2 * math.pi * radius) / speed)
        
        # Execute movement
        msg = Twist()
        msg.linear.x = speed
        msg.angular.z = angular_speed
        self.publisher_.publish(msg)
        time.sleep(duration)
        msg.linear.x=0.0
        msg.angular=0.0
        self.publisher_.publish(msg)"""
        circumference = 2 * math.pi * radius
        speed = 1.0
        angular_speed = speed / radius
        duration = (circumference/speed)
        msg = Twist()
        msg.linear.x = speed
        msg.angular.z = angular_speed
        
        self.get_logger().info(f'Drawing circle with radius {radius}')
        start_time = self.get_clock().now().seconds_nanoseconds()[0]
        while self.get_clock().now().seconds_nanoseconds()[0] - start_time < duration:
            self.publisher_.publish(msg)
            time.sleep(0.1)
 
        msg.linear.x = 0.0
        msg.angular.z = 0.0
        self.publisher_.publish(msg)
    def pen_up(self):
        self.set_pen(off=True)

    def pen_down(self):
        self.set_pen(off=False)

def structure(args=None):
    msg=Twist()
    td = TurtleDraw()
    td.pen_down()
    td.turn(60)
    #square
    td.draw_line(3)
    td.turn(90)
    td.draw_line(3)
    td.turn(90)
    td.draw_line(3)
    td.turn(90)
    td.draw_line(3)
    td.turn(90)
    #Sq done
    for _ in range(4):
        td.draw_line(0.75)
        td.turn(-90)
        td.draw_line(3)
        td.turn(180)
        td.draw_line(0.5)
        td.turn(90)
        td.draw_circle(0.5)
        td.turn(-90)
        td.draw_line(0.5)
        td.turn(-90)
        td.draw_line(0.5)
        td.turn(90)

def main(args=None):
    rclpy.init(args=args)
    turtle_draw = TurtleDraw()
    #Sample template to execute functions
    #turtle_draw.pen_down()
    #turtle_draw.draw_line(4,9) 
    #turtle_draw.pen_up()
    #turtle_draw.draw_circle()
    structure()
    
    turtle_draw.destroy_node()
    rclpy.shutdown()

if __name__ == '__main__':
    main()