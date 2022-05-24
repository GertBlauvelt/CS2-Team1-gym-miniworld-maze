import numpy as np
import math
from gym import spaces
from ..miniworld import MiniWorldEnv, Room
from ..entity import ImageFrame, MeshEnt, Box, Key, Ball, COLOR_NAMES

class ThreeRooms(MiniWorldEnv):
    """
    Two small rooms connected to one large room
    """

    def __init__(self, **kwargs):
        super().__init__(
            max_episode_steps=400,
            **kwargs
        )

        # Allow only the movement actions
        self.action_space = spaces.Discrete(self.actions.move_forward+1)

    def _gen_world(self):
        # Top room
        room0 = self.add_rect_room(
            min_x=-7, max_x=7,
            min_z=0.5 , max_z=7
        )
        # Bottom-left room
        room1 = self.add_rect_room(
            min_x=-7, max_x=-1,
            min_z=-7, max_z=-0.5
        )
        # Bottom-right room
        room2 = self.add_rect_room(
            min_x=1 , max_x=7,
            min_z=-7, max_z=-0.5
        )
        
        self.room3 = self.add_rect_room(
            min_x=-2 , max_x=2,
            min_z=8, max_z=12,
            floor_tex='slime'
        )

        # Connect the rooms with portals/openings
        self.connect_rooms(room0, room1, min_x=-5.25, max_x=-2.75)
        self.connect_rooms(room0, room2, min_x=2.75, max_x=5.25)
        self.connect_rooms(room0, self.room3, min_x=-2, max_x=2)
           
        # Start low duckies
        for i in range(7, 10):
            self.place_entity(
                MeshEnt(
                    mesh_name='duckie',
                    height=0.7
                ),
                pos = np.array([0.5*i, 0.4, 5])
            )
        
        # Middle line of duckies in biggest room
        for i in range(1, 10):
            self.place_entity(
                MeshEnt(
                    mesh_name='duckie',
                    height=0.6
                ),
                pos = np.array([1, 0, 0.5*i])
            )
            
        for i in range(1, 10):
            self.place_entity(
                MeshEnt(
                    mesh_name='duckie',
                    height=0.6
                ),
                pos = np.array([1, 0.6, 0.5*i])
            )
            
        #Second line of duckies
        for i in range(5, 15):
            self.place_entity(
                MeshEnt(
                    mesh_name='duckie',
                    height=0.6
                ),
                pos = np.array([3, 0, 0.5*i])
            )
            
        for i in range(5, 15):
            self.place_entity(
                MeshEnt(
                    mesh_name='duckie',
                    height=0.6
                ),
                pos = np.array([3, 0.6, 0.5*i])
            )
        
        #green square
        self.place_entity(Box(color='green'))
        
        #blue sphere
        self.place_entity(Ball(color='blue'))
        
        #song attached to an object
        
        #dinosaur
        self.place_entity(MeshEnt(mesh_name='office_chair', height=2, static=True))
        
        #random object of our choosing
        self.place_entity(MeshEnt(mesh_name='tree', height=1, static=True))
        
        #billboard with an outside image
         # Putney logo image on the wall
        self.entities.append(ImageFrame(
            pos=[4, 1.35, 7],
            dir=math.pi/2,
            width=1.8,
            tex_name='putneylogo'
        ))
        
        #purple cube *or* pyramid
        self.place_entity(Box(color='purple'))


        self.place_agent(
            room=0,
            min_x=4,
            max_x=4,
            min_z=6,
            max_z=6.5
        )

    def step(self, action):
        obs, reward, done, info = super().step(action)
        
        if self.room3.point_inside(self.agent.pos):
            reward = 0
            done = True

        return obs, reward, done, info
