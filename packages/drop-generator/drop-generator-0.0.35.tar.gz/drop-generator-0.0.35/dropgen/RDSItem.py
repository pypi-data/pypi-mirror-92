from dropgen.RDSObject import RDSObject

class RDSItem(RDSObject):

    '''
    Create a basic item to add to a table.
    '''

    def __init__(self, name, probability=None, unique=None, always=None, enabled=None):
        '''
        Requireed:
        * name - What is item called?

        Possible parameters:
        * probability - number (default 1)
        * unique - boolean (default false)
        * always - boolean (default false)
        * enabled - boolean (default true) 

        '''
        self.name = name
        RDSObject.__init__(self, probability, unique, always, enabled)



    def __str__(self):
        return self.name

