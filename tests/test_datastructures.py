import pytest
from email_server.datastructures import Hash_map, merge_sort, Mail_queue


def test_hash_map_empty_lookup():
    hash_map = Hash_map(capacity=8)
    assert hash_map.get("missing") is None


def test_hash_map_zero_and_null_values():
    hash_map = Hash_map(capacity=8)
    hash_map.put("zero", 0)
    hash_map.put("none", None)

    assert hash_map.get("zero") == 0
    assert hash_map.get("none") is None


def test_merge_sort_empty():
    assert merge_sort([]) == []


def test_merge_sort_sorted_output():
    data = [5, 3, 8, 1, 9, 2]
    sorted_data = merge_sort(data)
    assert sorted_data == sorted(data)


def test_merge_sort_large_numbers_over_64_bits():
    big_values = [2**80, 2**64, 2**100]
    sorted_values = merge_sort(big_values)
    assert sorted_values == sorted(big_values)


def test_mail_queue_basic_behavior():
    queue = Mail_queue()
    assert queue.is_empty()

    queue.enqueue(1)
    queue.enqueue(2)
    assert len(queue) == 2

    assert queue.dequeue() == 1
    assert queue.dequeue() == 2
    assert queue.dequeue() is None
    assert queue.is_empty()

