"""
Exception Factory: registry of Hermes predefined exception
"""

class HermesAbstractException(Exception):
    def __init__(self, message=None):
        if message is None:
            super().__init__(self.message)
        else:
            super().__init__(message)
        
def register_exception(name, default_message='Abstract Exception'):
    x = type(name, (HermesAbstractException,), {})
    x.message = default_message
    return x


LengthMismatched = register_exception('LengthMismatched', 'Lengths b/w 2 arrays are mismatched')
InvalidProbabilityValueRange = register_exception('InvalidProbabilityValueRange', 'Value of Probablity must be in range (0, 1)')
InvalidMulticlassLabel = register_exception('InvalidMulticlassLabel', 'Detect multiclass label while problem is binary label')
InvalidOneClassLabel = register_exception('InvalidOneClassLabel', 'Found 1 class only in label, please check it')
InvalidBinaryLabel = register_exception('InvalidBinaryLabel', 'Invalid binary value label, please check it')
DiscreteException = register_exception('DiscreteException', 'Discrete number is required for this variable')
IterableException = register_exception('IterableException', 'This variable must be a type of list/dataframe/series/ or numpy array')