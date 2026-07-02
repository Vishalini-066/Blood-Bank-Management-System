# queue_ds.py
# Queue Data Structure — FIFO + list + bool + int
class RequestQueue:

    def __init__(self):
        self.__queue = []    # list — private

    # Add request to back of queue
    def enqueue(self, request):
        self.__queue.append(request)
        print("Request added to queue!")

    # Remove request from front of queue
    def dequeue(self):
        if self.__queue:
            return self.__queue.pop(0)
        return None

    # See who is next without removing
    def peek(self):
        if self.__queue:
            return self.__queue[0]
        return None

    # Check if queue is empty
    def is_empty(self):
        return len(self.__queue) == 0   # bool

    # Count pending requests
    def size(self): 
        return len(self.__queue)        # int

    # Show all pending requests
    def display_queue(self):
        if self.is_empty():
            print("No pending requests!")
            return
        print("\n--- PENDING BLOOD REQUESTS ---")
        for i, req in enumerate(self.__queue):
            print(f"{i+1}. {req['name']} needs "
                  f"{req['blood_group']} x{req['units']} units")