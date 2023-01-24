class DatabaseObject:
    '''Adds ActiveRecord-like methods to a Model'''

    def __init__(self):
        pass

    def update(self, attrs={}):
        keys = list(attrs.keys())
        for key in keys:
            if hasattr(self, key):
                setattr(self, key, attrs[key])

    def global_id(self):
        '''Create an ambiguous Global ID for use with external applications'''
        pass
