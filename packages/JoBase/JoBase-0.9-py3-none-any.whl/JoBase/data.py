import arcade, os

class List:
    
    def __init__(self, *objects):
        self.array = list(objects)
            
    def __len__(self):
        return len(self.array)
    
    def __iter__(self):
        return iter(self.array)
    
    def __str__(self):
        return str(self.array)
    
    def __repr__(self):
        return repr(self.array)    

    def __getitem__(self, key):
        return self.array[key]
    
    def __setitem__(self, key, value):
        self.array[key] = value
    
    def draw(self):
        for element in self.array:
            if 'draw' in dir(element):
                element.draw()
                
    def append(self, element):
        element.array = self
        self.array.append(element)
        
    def remove(self, element):
        element.array = None
        self.array.remove(element)
    
    def add(self, element):
        # It does exactly the same thing as append.
        self.append(element)
        
    def collide(self, other):
        return collide(self.boundary(), other.boundary())    
        
    def boundary(self):
        boundaries = []
        
        for item in self.array:
            boundaries.append(item.boundary())
            
        return {'list': boundaries,
                'type': 'list'}
    
class Content:
    
    def __init__(self, array, name):
        self.array = list(array)
        self.name = name
        
    def __getitem__(self, key):
        return self.array[key]    
        
    def __setitem__(self, key, value):
        self.array[key] = value
        
        file = open(self.name, 'r')
        array = file.readlines()
        file.close()
        
        array[key] = str(value) + '\n'
                
        file = open(self.name, 'w')
        file.writelines(array)
        file.close()
    
    def __iter__(self):
        return iter(self.array)
    
    def __str__(self):
        return str(self.array)
    
    def __repr__(self):
        return repr(self.array)
    
    def __len__(self):
        return len(self.array)
    
    def append(value):
        self.array.append(value)
    
class File:
    
    def __init__(self, name: str = 'text_file.txt'):
        # Python automatically creates a new text file if it doesn't exist.

        if not os.path.isfile(name):
            file = open(name, 'w').close()
        
        self._name = name
        self.content = Content(self.read(), name)
        
    def clear(self):
        open(self.name, 'w').close()
        self.content.array = []
    
    def add(self, *items):
        file = open(self.name, 'a')
        
        for item in items:
            file.write(str(item) + '\n')
            self.content.append(item)
            
        file.close()
        
    def write(self, *items):
        file = open(self.name, 'w')
        self.content.array = []
        
        for item in items:
            file.write(str(item) + '\n')
            self.content.append(item)
            
        file.close()
        
    def delete(self):
        os.remove(self.name)
        del self
        
    def read(self):
        file = open(self.name, 'r')
        
        read = file.readlines()
        array = []
    
        for element in read:
            element = element.strip()
        
            if element.replace('.', '', 1).isdigit():
                element = eval(element)
            
            array.append(element)
        
        file.close()
    
        return array
    
    def _get_name(self):
        return self._name
    
    def _set_name(self, name: str):
        self.content.name = name
        os.rename(self._name, name)
        self._name = name
        
    name = property(_get_name, _set_name)

class Sound:
    
    def __init__(self, name: str = 'collect.wav'):
        self.name = name
        self.sound = arcade.load_sound(name)
        
    def play(self):
        arcade.play_sound(self.sound)
        
    def loop(self):
        pass