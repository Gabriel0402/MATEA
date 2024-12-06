cd ../reward_machines

for j in `seq 0 5`; 
do
    #python run.py --alg=maqlearning --env=MACraft-5agentdcent-v0 --num_timesteps=2e7 --gamma=0.9 --log_path=../aaai/5agent/dcent/M1/$j --ma --num_agent=5 --dcent
    
    python run.py --alg=maqlearning --env=MACraft-5agentcent-v0 --num_timesteps=2e7 --gamma=0.9 --log_path=../aaai/5agent/cent/M1/$j --ma --num_agent=5	
done
