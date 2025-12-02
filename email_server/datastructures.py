from collections import deque
from typing import Any, List, Tuple, Optional, Callable


class Hash_map:
    def __init__(self, capacity: int = 1024):
        self.capacity = capacity
        self.buckets: List[List[Tuple[Any, Any]]] = [[] for _ in range(capacity)]
        self.size = 0

    def _bucket_index(self, key: Any) -> int:
        return hash(key) % self.capacity

    def put(self, key: Any, value: Any) -> None:
        index = self._bucket_index(key)
        bucket = self.buckets[index]
        for i, (k, _) in enumerate(bucket):
            if k == key:
                bucket[i] = (key, value)
                return
        bucket.append((key, value))
        self.size += 1

    def get(self, key: Any) -> Optional[Any]:
        index = self._bucket_index(key)
        bucket = self.buckets[index]
        for k, v in bucket:
            if k == key:
                return v
        return None

    def remove(self, key: Any) -> None:
        index = self._bucket_index(key)
        bucket = self.buckets[index]
        for i, (k, _) in enumerate(bucket):
            if k == key:
                del bucket[i]
                self.size -= 1
                return


def merge_sort(sequence: List[Any], key: Optional[Callable[[Any], Any]] = None) -> List[Any]:
    if len(sequence) <= 1:
        return sequence
    mid = len(sequence) // 2
    left = merge_sort(sequence[:mid], key=key)
    right = merge_sort(sequence[mid:], key=key)
    return _merge(left, right, key=key)


def _merge(left: List[Any], right: List[Any], key: Optional[Callable[[Any], Any]]) -> List[Any]:
    result: List[Any] = []
    i = j = 0
    while i < len(left) and j < len(right):
        left_val = key(left[i]) if key else left[i]
        right_val = key(right[j]) if key else right[j]
        if left_val <= right_val:
            result.append(left[i])
            i += 1
        else:
            result.append(right[j])
            j += 1
    result.extend(left[i:])
    result.extend(right[j:])
    return result


class Mail_queue:
    def __init__(self):
        self._queue = deque()

    def enqueue(self, item: Any) -> None:
        self._queue.append(item)

    def dequeue(self) -> Optional[Any]:
        if self.is_empty():
            return None
        return self._queue.popleft()

    def is_empty(self) -> bool:
        return len(self._queue) == 0

    def __len__(self) -> int:
        return len(self._queue)

