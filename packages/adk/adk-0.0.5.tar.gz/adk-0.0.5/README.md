# ADK
 A Develop Kit, for easy coding.

## Develop Tools:
### RPC
* **Console Commands**: adk/adk.d config/start, details see "adk -h" for help 
* **RPC config**: adk.set_rpc_config, adk.get_rpc_config, adk.rpc_connect_args
* **adk.TaskManager**, implemented methods ['set', 'get', 'clear', 'get_work_que', 'get_res_que', 'run']
* **adk.start_rpc_server**, base class is multiprocessing.managers.BaseManager
* **adk.start_rpc_worker**, get task from queue(get_work_que()), put result to queue(get_res_que())
* **adk.rpc_client**, get rpc client. ['set', 'get', 'clear'] for cache data, 'run' for submit task to server
* **adk.clt**, a rpc client instance like above, for convenience

### Utils
* **adk.TaskQue**, Task Queue with key-value mapping, priority, speed limit, timeout and callbacks.
* **adk.PriQue**, Priority Queue with mutex lock and speed limit.
* **adk.PriDict**, Priority Dict with mutex lock and speed limit.

## Data types:
### Priority containers
extension of heap, main methods are: push, pop, peek
* **adk.PriorityQueue**, Priority Queue, push(data, priority) 
* **adk.SimplePriorityQueue**, Priority Queue, push(priority) 
* **adk.PriorityDict**, Priority Dict, push(key, data, priority)
* **adk.SimplePriorityDict**, Priority Dict, push(key, priority)
