import pybullet as p
import math
import pybullet_data
import time

# Initialize PyBullet
physicsClient = p.connect(p.GUI)
p.setGravity(0, 0, -9.81)
p.setAdditionalSearchPath(pybullet_data.getDataPath())
# Load the ground plane
planeId = p.loadURDF("plane.urdf")

# Position for the cannon
x, y = 0, 0
z = 0.25  # Half the height of the base cylinder

startPos = [x, y, z]

# Orient the cannon to point along the x-axis
# No additional rotation needed as the URDF model is already correctly oriented
startOrientation = p.getQuaternionFromEuler([0, 0, 0])

# Load the cannon
cannonId = p.loadURDF("models/cannon.urdf", startPos, startOrientation)

# Add debug lines to visualize axes
p.addUserDebugLine([0, 0, 0], [1, 0, 0], [1, 0, 0], 5)  # X-axis (red)
p.addUserDebugLine([0, 0, 0], [0, 1, 0], [0, 1, 0], 5)  # Y-axis (green)
p.addUserDebugLine([0, 0, 0], [0, 0, 1], [0, 0, 1], 5)  # Z-axis (blue)

# Create a separate cannonball
cannonball_radius = 0.1
cannonball_mass = 5.0
visualShapeId = p.createVisualShape(shapeType=p.GEOM_SPHERE, radius=cannonball_radius, rgbaColor=[0, 0, 0, 1])
collisionShapeId = p.createCollisionShape(shapeType=p.GEOM_SPHERE, radius=cannonball_radius)
cannonballId = p.createMultiBody(baseMass=cannonball_mass,
                                 baseInertialFramePosition=[0, 0, 0],
                                 baseCollisionShapeIndex=collisionShapeId,
                                 baseVisualShapeIndex=visualShapeId,
                                 basePosition=[x + 2.1, y, z])  # Position the ball just in front of the cannon barrel

# Add a debug parameter for fire speed
fire_speed = p.addUserDebugParameter("Fire Speed", 0, 100, 50)
x_angle = p.addUserDebugParameter("Angle X Axis", 0, 90, 45)
y_angle = p.addUserDebugParameter("Angle Y Axis", 0, 90, 45)

# Simulation loop
simulation_time = 20  # seconds
dt = 1./240.  # Time step of 1/240 seconds (240 Hz)
steps = int(simulation_time / dt)

for i in range(steps):
    # Check if spacebar is pressed to fire the cannon
    keys = p.getKeyboardEvents()
    if 32 in keys and keys[32] == 3:  # 32 is the ASCII code for spacebar, 3 means 'released'
        current_speed = p.readUserDebugParameter(fire_speed)
        current_x_angle = p.readUserDebugParameter(x_angle)
        current_y_angle = p.readUserDebugParameter(y_angle)
        # Calculate the velocity vector of the cannonball
        vx = current_speed * math.cos(math.radians(current_x_angle))
        vy = current_speed * math.cos(math.radians(current_y_angle))
        vz = 0
        p.resetBaseVelocity(cannonballId, [vx, vy, vz])
        print(f"Firing cannon with speed: {current_speed} m/s, angle: ({current_y_angle}, {current_x_angle})  degrees")

    # check if cannonball is out of bounds
    pos, _ = p.getBasePositionAndOrientation(cannonballId)
    if pos[0] > 10 or pos[1] > 10 or pos[2] < 0:
        print("Cannonball out of bounds")
        p.resetBasePositionAndOrientation(cannonballId, [x + 2.1, y, z], [0, 0, 0, 1])
    
    # Step the simulation
    p.stepSimulation()
    
    # Get cannonball position and velocity
    pos, orn = p.getBasePositionAndOrientation(cannonballId)
    vel, _ = p.getBaseVelocity(cannonballId)
    
    # Print cannonball status every 60 steps (about 4 times per second)
    if i % 60 == 0:
        print(f"Time: {i*dt:.2f}s, Position: {pos}, Velocity: {vel}")
    
    time.sleep(dt)  # to run simulation in real-time

p.disconnect()
