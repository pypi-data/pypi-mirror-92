from dropgen.IRDSTable import IRDSTable
from dropgen.RDSNullValue import RDSNullValue

from functools import reduce

import random
 
class RDSTable(IRDSTable):

    def __init__(self, contents=None, count=None, probability=None, unique=None, always=None, enabled=None):
        '''
        Initialize the table.  
        Default values:
          * contents: empty list (members are expected to implement IRDSObject interface)
          * count: (Default - 1) How many items should be dropped
          * probability: (Default - 1) What is the probability of something being dropped from this table
          * unique: (Default - False) If set to true, any item in this table or subtables can only be dropped once
          * always: (Default - False) If set to true, an item will always drop. Probability disabled.
          * enabled: (Default - True) If set to True, the item has a chance to drop.

        '''
        if contents is not None:
            self.rds_contents = list(contents)
        else:
            self.rds_contents = self.clear_contents()

        if count is not None:
            self.rds_count = count
        else:
            self.rds_count = 1

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
    # Manage contents of the table
    #
    
    def clear_contents(self):
        '''
        Create an empty list for the table.
        '''
        return []

      

    def add_entry(self, entry, probability=None, unique=None, always=None, enabled=None):
        '''
        Add an entry to the table. it can even have its own 
        probability, unique, always and enabled settings

        * Assumption:  The entry implements the IRDSObject interface OR
        implements the methods/properties in IRDSObject
        '''
        
        entry.rds_table = self

        if probability is not None: 
            entry.rds_probability = probability

        if unique is not None: 
            entry.rds_unique = unique

        if always is not None: 
            entry.rds_always = always

        if enabled is not None: 
            entry.rds_enabled = enabled

        self.rds_contents.append(entry)
        

    def remove_entry(self, entry):

        self.rds_contents.remove(entry)
        entry.rds_table = None
        
    
    #
    # Generate the results
    # Override the rds_results getter from IRDSTable
    #

    @property
    def rds_result(self):
        '''
        Generate and return the results.
        return: iterable 
        '''
        self.__uniquedrops = []
        resultset = []
        

        # Do the PreEvaluation on all objects contained in the current table
		# This is the moment where those objects might disable themselves.
        for row in self.rds_contents:
            row.on_rds_pre_result_eval()

        # Add objects that always drop and are enabled to the drop result set.
        # This could mean the actual drop count exceeds what is defined
        determine = lambda x: x.rds_enabled and x.rds_always
        alwaysdrops = list(filter(determine, self.rds_contents))
        for result in alwaysdrops:
            resultset = self.add_to_result(result, resultset)

        # Determine if anything else can be dropped
        real_drop_count = self.rds_count - len(resultset)

        # If there is still room, add more items to the drop
        if real_drop_count > 0:

            for dropcount in range(0, real_drop_count):
                # Find the objects, that can be hit now
                # That have not already been added through the always flag
                determine = lambda x: x.rds_enabled 
                droppables = list(filter(determine, self.rds_contents))

                # If there is nothing to drop
                if len(droppables) <= 0:
                    break

                # Base the hit value off of the sum of probabilities
                totalprob = 0
                for prob in droppables:
                    totalprob += prob.rds_probability

                hitvalue = random.uniform(0, totalprob)
                
                # Find out in a loop which object's probability hits the random value...                
                runningvalue = 0
                for drop in droppables:
                    
                    # Count up until we find the first item that exceeds the hitvalue...
                    runningvalue += drop.rds_probability
                    if (hitvalue < runningvalue):

                        #Add the it to the result set
                        resultset = self.add_to_result(drop, resultset)
                        break
            
            # Now give all objects in the result set the chance to interact with
            # the other objects in the result set.
            for result in resultset:
                result. on_rds_post_result_eval(resultset=resultset)

        # Return the resultset        
        return resultset

    
    def add_to_result(self, drop, resultset):

        #for drop in drops:
            
        if not drop.rds_unique or drop not in self.__uniquedrops:
            
            if drop.rds_unique:
                self.__uniquedrops.append(drop)
            
            if not isinstance(drop, RDSNullValue):
            
                if isinstance(drop, IRDSTable):
                    #Table recursion happens here
                    resultset.extend(drop.rds_result)
                else:
                    resultset.append(drop)
                    drop.on_rds_hit()
            else:
                drop.on_rds_hit()
        
        return resultset



    


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

    