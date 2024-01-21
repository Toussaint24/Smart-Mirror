from typing import Literal

class Exercise:
    exer_list = {}
    def __init__(self, name: str):
        self.name = name
        self.exer_list[name] = self
        
class Curl(Exercise):
    def __init__(self, arm="right"):
        super().__init__("curl")
        self.arm = arm
        
    @property
    def arm(self):
        return self._arm
    
    @arm.setter
    def arm(self, arm:Literal["left", "right"]):
        if arm in ["left", "right"]:
            self._arm = arm
        else:
            if type(arm) == str:
                raise ValueError(f"Expected type str; got {type(arm)}!")
            raise TypeError(f"Value for arm property should be 'left' or 'right' not {arm}")
    
    def process(self):
        # To start: hand should be completely lowered
        # Next, signal to begin
        # User should slowly bend elbow raising wrist upwards
        # Then user should straighten elbow lowering wrist
        # Increment counter?
        pass