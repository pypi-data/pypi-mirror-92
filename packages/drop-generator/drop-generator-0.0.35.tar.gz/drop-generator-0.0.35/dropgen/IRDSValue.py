from dropgen.IRDSObject import IRDSObject

class IRDSValue(IRDSObject):

    '''
    Use this in case of varying value of a particular 
    item can be dropped.  i.e. gold coins
    '''

    #
    # Set/Get the value of an item that can be dropped
    #
    @property
    def rds_value(self):
        '''
        Get the value of an item
        '''
        return self.__rds_value
    
    @rds_value.setter
    def rds_value(self, rds_value):
        '''
        Set the value of an item
        requires: integer/double
        '''
        self.__rds_value = rds_value 