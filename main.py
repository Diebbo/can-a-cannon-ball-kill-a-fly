import pybullet as p
import math
import pybullet_data

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

# Run the simulation
p.setRealTimeSimulation(1)
input("Press Enter to exit...")
p.disconnect()
