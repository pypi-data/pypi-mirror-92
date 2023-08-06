from dropgen.RDSValue import RDSValue

class RDSNullValue(RDSValue):

    '''
    Allow for null/None objects to be part of the 
    result set
    '''

    def __init__(self, probability=None):
        '''
        The null object makes it possible to have no object
        be returned from an iteration of the loot engine
        * probability -- default value is 1
        '''

        RDSValue.__init__(self, probability, None)

    