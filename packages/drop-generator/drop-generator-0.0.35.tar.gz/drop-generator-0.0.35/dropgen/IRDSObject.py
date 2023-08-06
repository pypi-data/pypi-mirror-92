from abc import ABC, abstractmethod

class IRDSObject (ABC):

    '''
    This abstact class contains the properties, methods, etc an object must 
    have to be a valid dropgen result object.
    '''

    #
    # Set/Get the probability for this object to be (part of) the result
    #
    @property
    def rds_probability(self):
        '''
        Get probability
        returns: integer/double
        '''
        return self.__rds_probability
    
    @rds_probability.setter
    def rds_probability(self, rds_probability):
        '''
        Set probability
        requires: integer/double
        '''
        self.__rds_probability = rds_probability   

    #
    # Set/Get whether this object may be contained only once in the result set
    #
    @property
    def rds_unique(self):
        '''
        Get uniqueness -- -- drop only once?
        returns: boolean
        '''
        return self.__rds_unique

    @rds_unique.setter 
    def rds_unique(self, rds_unique):
        '''
        Set uniqueness -- drop only once?
        requires: boolean
        '''
        self.__rds_unique = rds_unique


    #
    # Set/Get whether this object will always be part of the result set
    # (Probability is ignored when this flag is set to true)
    #
    @property 
    def rds_always(self):
        '''
        Get whether to always drop
        returns: boolean
        '''
        return self.__rds_always
    
    @rds_always.setter
    def rds_always(self, rds_always):
        '''
        Set whether to always drop
        requires: boolean
        '''
        self.__rds_always = rds_always

    #
    # Set/Get whether this object can be dropped now.
    #
    @property 
    def rds_enabled(self):
        '''
        Get whether to drop now
        returns: boolean
        '''
        return self.__rds_enabled
    
    @rds_enabled.setter
    def rds_enabled(self, rds_enabled):
        '''
        Set whether to drop now
        requires: boolean
        '''
        self.__rds_enabled = rds_enabled

    #
    # Set/Get the table this Object belongs to.
    # Note to inheritors: This property has to be auto-set when
    # an item is added to a table via the AddEntry method.
    #
    @property 
    def rds_table(self):
        '''
        Get the table this Object belongs to
        returns: object
        '''
        return self.__rds_table
    
    @rds_table.setter
    def rds_table(self, rds_table):
        '''
        set the table this Object belongs to
        requires: object
        '''
        self.__rds_table = rds_table 
    
    #
    # Abstract/Interface methods here
    #

    @abstractmethod
    def on_rds_pre_result_eval(self, **kwargs):
        '''
        What if anything to do before the result is returned
        '''
        pass    
    
    @abstractmethod
    def on_rds_hit(self, **kwargs):
        '''
        What if anything to do while the results are
        being generated/returned.
        '''
        pass


    @abstractmethod
    def on_rds_post_result_eval(self, **kwargs):
        '''
        What if anything to do after the results 
        have been received.
        '''
        pass


