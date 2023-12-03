# api_scheduler

## Dictionary Priority Queue Scheduler

The dictionary priority queue scheduler is for scheduling dictionaries using redis priority queues (sorted sets).  
Each queue (defined by a string) contains a list of dictionaries ordered by rank, where a higher priority corresponds to a lower rank number.
The dictionary can be any JSON compliant data structure comprised of python primitives only.

## Backend
<img src="/docs/img/priority_queue_architecture.PNG" alt="ArduNet Banner" width="800px" height="auto">

The backend (Scheduler Server) is powered using FastAPI, and is used as a middleware to communicate between the Redis cluster and headless endpoints or the frontend UI.
Supported operations include:
1. Removing, adding, reordering dictionaries within a queue
2. Creating or deleting Queues
3. Modifying the dictionary contents

## Frontend
<img src="/docs/img/queue_preview.PNG" alt="ArduNet Banner" width="800px" height="auto">
The front end is powered using React.js, and is used as an interface to modify the priority queue and its dictionary contents. 

### Dynamic Reordering via Drag
<img src="/docs/img/reorder.gif" alt="ArduNet Banner" width="300px" height="auto">

### Adding new Queues
<img src="/docs/img/add_queues.gif" alt="ArduNet Banner" width="300px" height="auto">

### Appending new Dictionaries to Queue
<img src="/docs/img/add_edit_to_queue.gif" alt="ArduNet Banner" width="300px" height="auto">

### Adding custom Dictionaries to Queue
<img src="/docs/img/add_custom_dict.gif" alt="ArduNet Banner" width="300px" height="auto">

## REST API Commands
All items in the priority queue service can be accessed through REST API.  The IP is the server IP of the scheduler server, and the port is the port located in /api_scheduler_backend/start_server.bat

| Endpoint  | Purpose |
| ------------- | ------------- |
| /queue-dict/{queue_name}  | Gets a list of dictionaries corresponding to queue = {queue_name}  |
| /edit?name={queue_name}&id={rank}&json={obj}  | Modifies the dictionary at order {rank} in queue {queue_name} and replaces it with the new object {obj}    |
| /clear?name={queue_name}  | Clears all scheduled dictionaries in queue {queue_name} |
| /set_priority?name={queue_name}&index={rank}&score={new_score}  | Modifies the score of the dictionary at index {rank} in queue {queue_name}.  This will cause the item to be reordered.  |
| /rem?name={queue_name}&index={rank}  | Removes the dictionary at index {rank} in queue {queue_name} |
| /swap?name={queue_name}&source_index={rank1}&target_index={rank2}  | Swaps the two dictionaries at index {rank1} and {rank2} |
| /drag?name={queue_name}&source_index={rank1}&target_index={rank2}  | Reorders the dictionary at index {rank1} to {rank2} |
| /add?name={queue_name}&data={dict_data}  | Adds a dictionary {dict_data} to the end of the queue {queue_name} |
| /get?name={queue_name}  | Returns a list of queued dictionaries, ordered by priority (desc) |
| /queue_names  | Returns a list all queue names and the number of dictionaries in each queue (sorted sets only) |
| /pop?name={queue_name}  | Pops the first dictionary (with highest priority) from the list |
| /queues  | Returns all data from all queues, as a list of dictionaries |


## What are Dictionary Priority Queues?
Dictionary priority queues are dictionaries ordered by a priority number (rank). These queues are stored using redis sorted sets. 