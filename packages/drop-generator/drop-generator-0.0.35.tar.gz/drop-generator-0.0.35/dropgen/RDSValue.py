from dropgen.IRDSValue import IRDSValue

class RDSValue(IRDSValue):

    def __init__(self, probability, value, unique=None, always=None, enabled=None):
        '''
        Initialize the value object. 
          * probability -- number (required)
          * value - object (required -- None is ok)
        Optional values:
         * unique - boolean (default false)
         * always - boolean (default false)
         * enabled - boolean (default true)
        
        '''
        
        #Check the required values first
        self.rds_probability = probability
        self.rds_value = value
                
        #Check optional keys and set defaults, if needed
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
