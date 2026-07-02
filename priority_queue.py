# priority_queue.py
import heapq
import itertools

class PriorityRequestQueue:
    """
    Priority Queue for blood requests.
    Lower priority number = more urgent (0 = emergency, 1 = urgent, 2 = normal)
    """

    def __init__(self):
        self.__heap = []
        self.__counter = itertools.count()   # tie-breaker so requests
                                              # with same priority stay FIFO

    # Add request with a priority level
    def enqueue(self, request, priority=2):
        count = next(self.__counter)
        heapq.heappush(self.__heap, (priority, count, request))
        print(f"Request added with priority {priority}!")

    # Remove and return the most urgent request
    def dequeue(self):
        if self.__heap:
            priority, count, request = heapq.heappop(self.__heap)
            return request
        return None

    # See the most urgent request without removing
    def peek(self):
        if self.__heap:
            return self.__heap[0][2]
        return None

    # Check if queue is empty
    def is_empty(self):
        return len(self.__heap) == 0

    # Count pending requests
    def size(self):
        return len(self.__heap)

    # Show all pending requests, most urgent first
    def display_queue(self):
        if self.is_empty():
            print("No pending requests!")
            return
        sorted_items = sorted(self.__heap)
        for priority, count, request in sorted_items:
            print(f"[Priority {priority}] {request}") 

if __name__ == "__main__":
    pq = PriorityRequestQueue()
    pq.enqueue("Patient A - Accident case", priority=0)
    pq.enqueue("Patient B - Routine checkup", priority=2)
    pq.enqueue("Patient C - Surgery needed", priority=1)

    print("\n--- Queue Contents ---")
    pq.display_queue()

    print("\n--- Dispatching ---")
    while not pq.is_empty():
        print("Serving:", pq.dequeue())