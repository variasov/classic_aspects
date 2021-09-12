import threading


class CallsStack:

    def __init__(self):
        self._stack = []

    def append(self, obj):
        self._stack.append(obj)

    def pop(self):
        return self._stack.pop()

    def __getitem__(self, item):
        return self._stack[item]

    @property
    def is_empty(self):
        return len(self._stack) == 0

    @property
    def is_first(self):
        return len(self._stack) == 0


class ThreadSafeCallStack(CallsStack, threading.local):
    pass
