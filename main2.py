import asyncio
from viam.components.base import Base
from viam.robot.client import RobotClient
from viam.rpc.dial import Credentials, DialOptions
from viam.services.slam import SLAMClient
import numpy as np
async def connect():
    opts = RobotClient.Options.with_api_key(
        api_key='i11ph4btwvdp1kixh3oveex92tmvdtx2',
        api_key_id='8b19e462-949d-4cf3-9f7a-5ce0854eb7b8'
    )
    return await RobotClient.at_address('rover6-main.9883cqmu1w.viam.cloud', opts)
async def get_position(slam):
    position = await slam.get_position()  # This depends on your specific SLAM client
    return position

async def moveToPos(base, slam, x,y,theta):
    currPos = get_position(slam)
    currX = currPos.x
    currY = currPos.y
    currTheta = currPos.theta
    toMove = np.arctan((y-currY)/(x-currX))-currTheta
    dist = np.sqrt((y-currY)**2+(x-currX)**2)
    base.spin(toMove,10)
    base.move_forward(dist,50)
    base.spin(theta-toMove,50)


async def main():
    robot = await connect()
    print('Resources:', robot.resource_names)

    base = Base.from_robot(robot, 'viam_base')
    slam = SLAMClient.from_robot(robot, 'slam-1')  # Initialize SLAM



    #get a set of waypoints to track and populate them
    wp = np.zeros((40,3))
    for i in range(10):
        wp[i][0]=i
        wp[i][2]=90
        wp[i+10][0]=10
        wp[i+10][1]=i
        wp[i+10][2]=180
        wp[i+20][0]=10
        wp[i+20][1]=10-i
        wp[i+20][2]=270
        wp[i+30][0]=0
        wp[i+30][1]=10-i
        wp[i+30][2]=0
    
    #get initial position
    pos = await slam.get_position()
    x = pos.x
    y = pos.y
    theta = pos.theta
    print(x)
    print(y)
    print(theta)
    
    await moveToPos(base,slam,0,0,0)

    await robot.close()

    
    #base_coords = (x0, y0)
    #print(f"Base coordinates: ({x0}, {y0})")
"""
    # Move in a square and maintain base coordinates
    await moveInSquare(roverBase, slam, base_coords)

    await robot.close()
"""

if __name__ == '__main__':
    asyncio.run(main())
