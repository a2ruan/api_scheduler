import redis, time
import dill
import uuid
import json

class redis_priority_queue:
    # PriorityQueue implementation using redis sorted sets
    
    def __init__(self, **kwargs):
        self.ip = kwargs.get("ip",None)
        self.port = kwargs.get("port",None)
        self.mode = kwargs.get("mode",None) # Setting mode to cluster will allow connection to a redis cluster
        self.connection = None
        self.initialize_connection(mode=self.mode)

    def get_queue_names(self, match:str=None):
        key_names = []
        queue_names = []
        for key in self.connection.scan_iter(match=match,count=10000):
            name = str(key,'utf-8')
            if "_config_info" in name: pass
            else: key_names.append(str(key,"utf-8"))
        key_names.sort()
        if "" in key_names: key_names.remove("")
        for key in key_names: 
            print(key)
            queue_length = 0
            queue_length = self.get_size(key)
            queue_names.append({"label":key,"queue_size":queue_length})
        return queue_names

    def get_queues(self, match:str = None):
        """Get a list of queue names based on a search pattern.  This only works for priority queues created using this class's self.get function

        Args:
            match (str, optional): The search pattern used to determine which keys are returned
        
        Returns (dict): A dictionary containing the key value pairs, where the key is the priority queue name and the value is the priority queue contents.
        """
        queue_data = {}
         # Return keys in batches of 10,000.  Note: Add _type = "zset" in the future.  Redis 5.0 still has bug that disallows type filtering.
        for key in self.connection.scan_iter(match=match,count=10000):
            print(key)
            if "_config_info" in str(key): pass
            else:
                try:
                    queue_data[key.decode("utf-8")] = self.get(key)
                except Exception as e:
                    print(f"Unable to retrieve {key} due to {e}")
            
        return queue_data
    
    def initialize_connection(self, mode:str = "cluster"):
        """Initializes the connection with a redis node or cluster
        Args:
            mode: String that indicates whether to connect to a cluster or node
        Returns:
            True if connection is initialized, else False
        """
        try:
            if self.connection != None: # Do not re-initialize connection if connection already exists
                pass
                #print("Connection is already initialized.")
            elif mode == "cluster":
                self.connection = redis.RedisCluster(host=self.ip, port=self.port)
            elif mode == "node":
                self.connection = redis.Redis(host=self.ip, port=self.port)
            else: return False
            return True
        except redis.ConnectionError:
            return False
    
    def clear(self, name:str) -> bool:
        """Clears all items in the priority queue

        Args:
            name (str): priority queue name

        Returns:
            bool: True if queue has been cleared, otherwise False
        """
        try:
            self.connection.zremrangebyrank(name,0,-1)
        except redis.ConnectionError:
            return False
        return True
    
    def set_priority(self, name:str, index:int, score:float) -> bool:
        """Modify the priority of an element based on its index in the queue

        Args:
            name (str): priority queue name
            index (int): The index of the element who
            score (float): The priority of the element at the specified index

        Returns:
            bool: True if the priority has been modified successfully, else false
        """
        try:
            source_item = self.connection.zrange(name, index, index) # Obtain the key associated at source index
            self.connection.zadd(name,{source_item[0]:score})   # Update the score
        except redis.ConnectionError as connectionerror:
            print(connectionerror)
            return False
        except IndexError as indexerror:
            print(f"Error code: {indexerror}")
            return False
        return True
    
    def drag(self, name:str, source_index:int=None, target_index:int=None) -> bool:
        try:
            num_elements = self.connection.zcard(name)
            if source_index > num_elements or target_index > num_elements: return False
            source_item = self.connection.zrange(name, source_index, source_index) # Obtain the key associated at source index
            #source_score = self.connection.zscore(name, source_item[0])
            target_item = self.connection.zrange(name, target_index, target_index) # Obtain the key associated at source index
            target_score = self.connection.zscore(name, target_item[0])

            # If dragging downwards in priority:
            # Condition 1: If target index is the last element in the list, simply add 0.01 to the score priority
            if target_index == (num_elements-1) and source_index < target_index: new_source_score = target_score + 0.01

            # Condition 2: If the target index is not the last element in the list, set the priority to the average of the priority at locations [target_index, target_index+1]
            elif target_index != (num_elements-1) and source_index < target_index: 
                target_index_offset_p1 = self.connection.zrange(name, target_index+1, target_index+1) # Obtain the key associated at target index + 1
                target_index_offset_p1_score = self.connection.zscore(name, target_index_offset_p1[0])
                new_source_score = (target_score + target_index_offset_p1_score)/2

            # If dragging upwards in priority:
            # Condition 3: If target index is the first element of the list, simply subtract 0.01 from the score priority of the source index
            elif target_index == 0 and source_index > target_index: new_source_score = target_score - 0.01

            # Condition 4: If the target index is not the first element in the list, set the priority to the average of the priority at locatons [target_index, target_index-1]
            elif target_index != 0 and source_index > target_index:
                target_index_offset_n1 = self.connection.zrange(name, target_index-1, target_index-1) # Obtain the key associated at target index - 1
                target_index_offset_n1_score = self.connection.zscore(name, target_index_offset_n1[0])
                new_source_score = (target_score + target_index_offset_n1_score)/2
            else: return False
            self.connection.zadd(name,{source_item[0]:new_source_score})
        except Exception as e:
            print(e)
            return False
        

    def swap(self, name:str, source_index:int=None, target_index:int=None) -> bool:
        """Swaps two elements in the priority queue based on rank (index)

        Args:
            name (str): priority queue name
            source_index (int, optional): The index of the first element to be swapped (swapped with the element at the target index)
            target_index (int, optional): The index of the second element to be swapped (swapped with the element at source index)

        Returns:
            bool: True if the swap was successful, otherwise False
        """
        try:
            source_item = self.connection.zrange(name, source_index, source_index) # Obtain the key associated at source index
            source_score = self.connection.zscore(name, source_item[0])
            target_item = self.connection.zrange(name, target_index, target_index) # Obtain the key associated at source index
            target_score = self.connection.zscore(name, target_item[0])
            
            # Update the scores via swapping
            self.connection.zadd(name,{source_item[0]:target_score})
            self.connection.zadd(name,{target_item[0]:source_score})
        except redis.ConnectionError as connectionerror:
            print(connectionerror)
            return False
        except IndexError as indexerror:
            print(f"Error code: {indexerror}")
            return False
        return True
        
    def rem(self,name:str, index:int=None) -> bool:
        """Removes an element from the priority queue based on index
        
        Args:
            name (str): priority queue name
            index (int, optional): Position of the element in the redis sorted set to be removed (index starts at 0)
        
        Returns:
            bool: True if item has been deleted, otherwise False
        """
        priority_queue = self.get(name)
        if len(priority_queue) < index: return False
        self.connection.zremrangebyrank(name, index, index)
        return True
    
    def edit(self, name:str, obj:object, id:str=None) -> bool:
        """Edits the json contents based on uuid value"""
        self.initialize_connection(mode=self.mode)
        print(name)
        # Get all elements in the sorted set and determine if there are any matching the input uuid
        sorted_set_data = self.get(name)
        for i,job in enumerate(sorted_set_data):
            print(str(job.get("uuid")).replace("-",""))
            if id in str(job.get("uuid","NONE")).replace("-",""):
                print("Found!")
                try:

                    print(obj)
                    print(type(obj))
                    print("Attempting to convert to dict")
                    
                    #print(json.loads(obj))
                    #print(type(json.loads(obj)))
                    #print(type(eval(obj)))
                    print("BP1")
                    candidate_json = json.loads(obj)
                    print("BP10")
                    if isinstance(candidate_json,dict):
                        payload = dill.dumps({
                            "uuid":job.get("uuid"),
                            "key":"default",
                            "value":candidate_json,
                        })
                        print("Removing!"*100)
                        self.rem(name,index=i)
                        print("Pushing!"*100)
                        self.connection.zadd(name,{payload:job.get("score",time.time())})
                    else:
                        print("Object is not a dictionary!  Not editing!")
                    return True
                
                except Exception as conversion_error:
                    print("Conversion Error!")
                    print(conversion_error)
                    return False
                
                payload = dill.dumps({
                    "uuid":id,
                    "key":"default",
                    "value":obj,
                })


        return False

    def add(self,name:str, obj:object, score:float = None):
        """Adds a python object to a redis sorted set.
        
        Args:
            name (str): priority queue name
            obj: An object that will be serialized and added to the redis sorted set
            score: 
                Float value that determines the object's position in the redis sorted set
                If the score is not initialized, then the score with be set to the priority queue's current maximum score + 1
        
        Returns: N/A
        """ 
        self.initialize_connection(mode=self.mode)
        payload = dill.dumps({
            "uuid":uuid.uuid4(),
            "key":"default",
            "value":obj,
            #"status":"queued"
        })
        
        if score == None:
            # Case 1: If an element in the queue has a score greater than the current time, the next score is that max score + 1
            # Case 2: If no elements in the queue has a score greater than the current time, the next score is the current time
            score = max(self.get_max_score(name) + 0.01,round(time.time(),3)) 
            self.connection.zadd(name,{payload:score})
        else:
            self.connection.zadd(name,{payload:score})
            
    def get_max_score(self, name:str) -> float:
        """Gets the maximum score in the priority queue

        Args:
            name (str): _description_
            
        Returns:
            float: Maximum score.  If no elements found, 0 is returned
        """
        queue_list = self.get(name)
        if len(queue_list) > 0:
            return queue_list[-1]["score"]
        else:
            return 0 # This means this is the first element of the queue

    def get_size(self, name:str):
        """Returns number of elements in sorted set"""
        
        num_elements = 0
        try:
            score_limit = 1000000000000
            num_elements = self.connection.zcount(name, -score_limit, score_limit)
        except Exception as queue_undefined:
            print(queue_undefined)
        return num_elements

    def get(self, name:str):
        """Returns all elements of a sorted set as a dictionary
        
        Args:
            name (str): priority queue name
            obj: An object that will be serialized and added to the redis sorted set
            score: Float value that determines the object's position in the redis sorted set
        
        Returns:
            list: List of python objects ordered by score.  If the score is the same, lexographic order is used
        """
        self.initialize_connection(mode=self.mode)
        sorted_set = self.connection.zrange(name,0,-1, withscores=True)
        output = []
        for i, set in enumerate(sorted_set):
            try:
                deserialized_data = dill.loads(set[0])
                score = set[1]
                output.append(
                    {
                        "uuid":deserialized_data["uuid"],
                        "key":deserialized_data["key"],
                        "value":deserialized_data["value"],                    
                        "score":score,
                        #"status":deserialized_data["status"]
                    }
                )
            except KeyError as keyerror:
                pass
        return output

    def pop_min(self, name:str):
        try:
            sorted_set_element = self.connection.zpopmin(name)
            return dill.loads(sorted_set_element[0][0])
        except IndexError:
            return {} # Returns empty if no longer found
    
if __name__ == "__main__":
    redis_queue_manager = redis_priority_queue(ip="10.6.131.238", port=7000, mode="cluster")
    start_time = time.time()
    test_instances = 5
    racks = 10
    for i in range(test_instances):
        print(f"Adding {i}")
        for i in range(racks):
            redis_queue_manager.add(f"RACK_A{str(i)}",{"hello_world":f"A{i}","type":f"rack{i}"})
    print(f"It took {str((time.time()-start_time)*1000)}ms to push {str(test_instances)} instances to redis.  Latency is {str((time.time()-start_time)*1000/test_instances)}ms")
    queue = redis_queue_manager.get("RACK_A2")
    for item in queue:
        print(item)
    
    redis_queue_manager.get_max_score("RACK_A2")
    
    print("Removing item at location index 2 (3rd item)")
    redis_queue_manager.rem("RACK_A2",2)
    queue = redis_queue_manager.get("RACK_A2")
    print("New Priority Queue")
    for item in queue:
        print(item)
    
    print("Swapping items 0 and 2 (1st and 3rd element)")
    redis_queue_manager.swap("RACK_A2",0,2)
    queue = redis_queue_manager.get("RACK_A2")
    print("New Priority Queue")
    for item in queue:
        print(item)
    
    # Scanning for keys
    start_time = time.time()
    queue_names = redis_queue_manager.get_queues(match="RACK*")
    for queue in queue_names:
        print(queue)
        print(queue_names[queue])
    print(f"It took {str(time.time()-start_time)}s to retrieve all racks from the cluster")
    
    print("Testing pop min")
    queue_names = redis_queue_manager.get_queues(match="RACK*")
    for queue in queue_names:
        if queue == "RACK_A2":
            print(queue)
            print(len(queue_names[queue]))
            print(queue_names[queue])
    print("Popping")
    element = redis_queue_manager.pop_min("RACK_A2")
    queue_names = redis_queue_manager.get_queues(match="RACK*")
    for queue in queue_names:
        if queue == "RACK_A2":
            print(queue)
            print(len(queue_names[queue]))
            print(queue_names[queue])
    print("Popped item")
    print(element)
            
    
    print("Clearing entire priority queue")
    for i in range(racks):
        redis_queue_manager.clear(f"RACK_A{str(i)}")
    queue = redis_queue_manager.get("RACK_A2")
    print("New Priority Queue")
    for item in queue:
        print(item)
        
    

    

"""
for i in range(10000):
    
    # Example with inserting dictionaries (hashes)
    dict_out = {
        f"test{str(i)}":f"bar{str(i)}"
    }
    r.hmset(f'foo{str(i)}_dict', dict_out)
    out2 = r.hgetall(f'foo{str(i)}_dict')
    print(out2)
    
    
    # Example with getting key value pairs (string)
    r.set(f'foo{str(i)}', f"bar{str(i)}")
    out = r.get(f'foo{str(i)}')
    print(out)
"""
