from dropgen.IRDSObject import IRDSObject

class IRDSTable(IRDSObject):

    '''
    Tables need to inherit from the this interface/abstract class in order to be 
    used with the base implementation RDSTable
    '''

    #
    # Set/Get the number of items that will drop from this table
    # Should be an integer
    #
    @property
    def rds_count(self):
        '''
        Get number of items to drop
        returns: integer/double
        '''
        return self.__rds_count
    
    @rds_count.setter
    def rds_count(self, rds_count):
        '''
        Set number of items to drop
        requires: integer/double
        '''
        self.__rds_count = rds_count   

    #
    # Get the contents of the table
    # Assumption this is an iterable object
    #
    @property
    def rds_contents(self):
        '''
        Get contents
        return: iterable
        '''
        return self.__rds_contents
    
    @rds_contents.setter
    def rds_contents(self, rds_contents):
        '''
        Set contents
        '''
        self.__rds_contents = rds_contents 

    #
    # Get the result of the table
    # Assumption this is an iterable object
    #
    @property
    def rds_result(self):
        '''
        Get results
        return: iterable
        '''
        return self.__rds_result
    
    @rds_result.setter
    def rds_result(self, rds_result):
        '''
        Set contents
        '''
        self.__rds_result = rds_result