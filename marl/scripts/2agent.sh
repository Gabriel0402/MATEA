cd ../reward_machines

for j in `seq 0 5`; 
do
    python run.py --alg=maqlearning --env=MACraft-2agentdcent-v0 --num_timesteps=1e7 --gamma=0.9 --log_path=../aaai/2agent/dcent/M1/$j --ma --num_agent=2 --dcent	
    
    python run.py --alg=maqlearning --env=MACraft-2agentcent-v0 --num_timesteps=1e7 --gamma=0.9 --log_path=../aaai/2agent/cent/M1/$j --ma --num_agent=2	
done
