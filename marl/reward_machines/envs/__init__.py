from gym.envs.registration import register

# ----------------------------------------- Half-Cheetah

register(
    id='Half-Cheetah-RM1-v0',
    entry_point='envs.mujoco_rm.half_cheetah_environment:MyHalfCheetahEnvRM1',
    max_episode_steps=1000,
)
register(
    id='Half-Cheetah-RM2-v0',
    entry_point='envs.mujoco_rm.half_cheetah_environment:MyHalfCheetahEnvRM2',
    max_episode_steps=1000,
)

register(
    id='Point-Goal-RM1-v0',
    entry_point='envs.mujoco_rm.point_goal:MyPointGoalEnvRM1',
    max_episode_steps=1000,
)

register(
    id='Ball-Circle-RM1-v0',
    
    entry_point='envs.mujoco_rm.ballcircle:MyEnvRM1',

    #entry_point='envs.mujoco_rm.point_goal:MyPointGoalEnvRM1',
    max_episode_steps=1000,
)

# ----------------------------------------- WATER
for i in range(11):
    w_id = 'Water-M%d-v0'%i
    w_en = 'envs.water.water_environment:WaterRMEnvM%d'%i
    register(
        id=w_id,
        entry_point=w_en,
        max_episode_steps=600
    )

for i in range(11):
    w_id = 'Water-single-M%d-v0'%i
    w_en = 'envs.water.water_environment:WaterRM10EnvM%d'%i
    register(
        id=w_id,
        entry_point=w_en,
        max_episode_steps=600
    )

# ----------------------------------------- OFFICE
register(
    id='Office-v0',
    entry_point='envs.grids.grid_environment:OfficeRMEnv',
    max_episode_steps=1000
)

register(
    id='Office-single-v0',
    entry_point='envs.grids.grid_environment:OfficeRM3Env',
    max_episode_steps=1000
)

# ----------------------------------------- CRAFT
for i in range(11):
    w_id = 'Craft-M%d-v0'%i
    w_en = 'envs.grids.grid_environment:CraftRMEnvM%d'%i
    register(
        id=w_id,
        entry_point=w_en,
        max_episode_steps=1000
    )

for i in range(11):
    w_id = 'Craft-single-M%d-v0'%i
    w_en = 'envs.grids.grid_environment:CraftRM10EnvM%d'%i
    register(
        id=w_id,
        entry_point=w_en,
        max_episode_steps=1000
    )

register(
    id='MACraft-single-v0',
    entry_point='envs.grids.grid_environment:MACraftRMEnv3M0',
    max_episode_steps=1000
)

for i in range(4):
    w_id = 'MACraft-3agentdcent-M%d-v0'%i
    w_en = 'envs.grids.grid_environment:MACraftRMEnv3M%dDcent'%i
    register(
        id=w_id,
        entry_point=w_en,
        max_episode_steps=1000
    )

for i in range(4):
    w_id = 'MACraft-3agentcent-M%d-v0'%i
    w_en = 'envs.grids.grid_environment:MACraftRMEnv3M%dCent'%i
    register(
        id=w_id,
        entry_point=w_en,
        max_episode_steps=1000
    )
    
register(
    id='MACraft-cent-v0',
    entry_point='envs.grids.grid_environment:MACraftRMEnv3M10Cent',
    max_episode_steps=1000
)

register(
    id='MACraft-dcent-v0',
    entry_point='envs.grids.grid_environment:MACraftRMEnv3M10Dcent',
    max_episode_steps=1000
)

register(
    id='MACraft-dcent-v1',
    entry_point='envs.grids.grid_environment:MACraftRMEnv3M10Dcent1',
    max_episode_steps=1000
)

register(
    id='MACraft-2agentdcent-v0',
    entry_point='envs.grids.grid_environment:MACraftRMEnv2M0Dcent',
    max_episode_steps=1000
)

register(
    id='MACraft-2agentcent-v0',
    entry_point='envs.grids.grid_environment:MACraftRMEnv2M0Cent',
    max_episode_steps=1000
)

register(
    id='MACraft-5agentdcent-v0',
    entry_point='envs.grids.grid_environment:MACraftRMEnv5M0Dcent',
    max_episode_steps=1000
)

register(
    id='MACraft-5agentcent-v0',
    entry_point='envs.grids.grid_environment:MACraftRMEnv5M0Cent',
    max_episode_steps=1000
)

register(
    id='MACraft-Origin-v0',
    entry_point='envs.grids.grid_environment:MACraftOriginalEnv',
    max_episode_steps=1000
)