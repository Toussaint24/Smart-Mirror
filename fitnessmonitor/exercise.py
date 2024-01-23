from typing import Literal

class Exercise:
    exer_list = {}
    def __init__(self, 
                name: str, 
                primary_joints: dict[str, tuple[int, int]], 
                constraining_joints: dict[str, tuple[int, int]] = {}
                ):
        """
        Initialize an exercise object

        Args:
            name (str): a label describing the exercise.
            
            primary_joints (dict[str, tuple[int, int]]): a dictionary with the key being a str of the
            label describing the middle joint in a set of three keypoints and the value being a tuple 
            of integers representing the range of motion required of the angle of the joint. Only include
            joints which must go from the angle at the low end to the angle at the high end.
            
            constraining_joints (dict[str, tuple[int, int]], optional): a dictionary with the key being a str of the
            label describing the middle joint in a set of three keypoints and the value being a tuple 
            of integers representing the range of motion required of the angle of the joint. Only include
            joints which must stay in between the range of angles. Defaults to {}.
        """
        self.name = name
        self.primary_joints = primary_joints
        self.constraining_joints = constraining_joints
        self.exer_list[name] = self
        
    def process(self, position: int, angles: dict[str, int]) -> tuple[bool, bool]:
        """
        Determine if passed results indicate proper progression of the exercise and return result
        
        The exercise is presumed to have progressed if a primary joint reaches the target angle for its position.
        E.g. a bicep curl might have an "up" and a "down" position. The exercise may progress from the down position 
        to the up position by contracting the elbow up to have an angle of < 10 degrees. Alternatively, a progression 
        from up to down may be realized by relaxing the elbow to angle of > 170 degrees. Furthermore, examines the 
        angles of constraining joints to determine if any are outside the acceptable range. 

        Args:
            position (int): represents the user's current position in the exercise. Determines how to
            determine if there was progression.
            angles (dict[str, int]): the current angle of the corresponding joint.

        Returns:
            tuple[bool, bool]: the first element indicates whether the user was determined to have progressed in the
            exercise. The second element indicates whether the user strayed outside of the defined constraints.
        """
        primary_flag = False
        constraint_flag = False
        for joint, angle in angles.items():
            
            if joint in self.primary_joints.keys():
                
                if position == 0:
                    if angle <= min(self.primary_joints[joint]):
                        primary_flag = True
                else:
                    if angle >= max(self.primary_joints[joint]):
                        primary_flag = True

            elif joint in self.constraining_joints.keys():
                
                if angle < min(self.constraining_joints[joint]):
                    constraint_flag = True
                elif angle > max(self.constraining_joints[joint]):
                    constraint_flag = True
        
        return (primary_flag, constraint_flag)
    
curl = Exercise("curl_right", {"elbow_right": (10, 170)})