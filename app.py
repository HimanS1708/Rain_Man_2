#! /usr/bin/env python3

from fastapi import FastAPI
from pydantic import BaseModel
from fastapi.middleware.cors import CORSMiddleware

from algorithm2D import solution as solution2D
from algorithm3D import solution as solution3D

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_credentials=True,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

class Env(BaseModel):
    points: list
    path_points: list
    v_x: float
    v_y: float
    v_z: float
    intensity: float

@app.post("/")
async def process2D(env: Env):
    return solution2D(env.points, env.path_points, env.v_x, env.v_y, env.intensity)
@app.post("/3D")
async def process3D(env: Env):
    return solution3D(env.points, env.path_points, env.v_x, env.v_y, env.v_z, env.v_z, env.intensity)

if __name__ == "__main__":
    pass