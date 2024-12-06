cd ../reward_machines
for i in `seq 0 3`; 
do
	for j in `seq 0 5`; 
	do
		python run.py --alg=maqlearning --env=MACraft-3agentdcent-M$i-v0 --num_timesteps=2e7 --gamma=0.9 --log_path=../aaai/3agent/dcent/M$i/$j --ma --num_agent=3 --dcent	

		python run.py --alg=maqlearning --env=MACraft-3agentcent-M$i-v0 --num_timesteps=2e7 --gamma=0.9 --log_path=../aaai/3agent/cent/M$i/$j --ma --num_agent=3 	 	
	done
done