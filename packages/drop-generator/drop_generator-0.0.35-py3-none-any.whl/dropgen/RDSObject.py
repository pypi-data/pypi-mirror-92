from dropgen.IRDSObject import IRDSObject 

class RDSObject(IRDSObject):
    '''
    Generic implementation of the IRDSObject interface
    '''
    def __init__(self, probability=None, unique=None, always=None, enabled=None):
        '''
        Possible parameters:
         * probability - number (default 1)
         * unique - boolean (default false)
         * always - boolean (default false)
         * enabled - boolean (default true)
        
        
        '''
        
      
        if probability is not None:
            self.rds_probability = probability
        else:
            self.rds_probability = 1
               
        if unique is not None:
            self.rds_unique = unique
        else: 
            self.rds_unique = False

        if always is not None:
            self.rds_always = always
        else: 
            self.rds_always = False

        if enabled is not None:
            self.rds_enabled = enabled
        else: 
            self.rds_enabled = True






    #
    # IRDSObject method implementation
    # All of them do nothing (for now)
    #

    def on_rds_pre_result_eval(self, **kwargs):
        '''
        Do nothing
        '''
        pass    
    
    
    def on_rds_hit(self, **kwargs):
        '''
        Do nothing
        '''
        pass


    def on_rds_post_result_eval(self, **kwargs):
        '''
        Do nothing
        '''
        pass