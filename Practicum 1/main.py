class CounterClass:
    count = 0 

    def __init__(self):
        CounterClass.count += 1
        print(f"An object has been created.")

    def __del__(self):
        CounterClass.count -= 1
        print(f"The object has been deleted.")

obj1 = CounterClass()
obj2 = CounterClass()
obj3 = CounterClass()

print(f'Current number of objects: {CounterClass.count}')

del obj1 
print(f'After deletion: {CounterClass.count}')

del obj2 
print(f'After the second deletion: {CounterClass.count}')
