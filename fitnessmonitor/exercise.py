import threading


class Exercise:
    exer_list = {}
    def __init__(self, 
                name: str, 
                primary_joints: dict[str, tuple[int, int]], 
                messages: dict[str, tuple[str, str]],
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
        self.messages = messages
        self.constraining_joints = constraining_joints
        self.previous_angles = dict(zip(self.primary_joints.keys(), [value[0] for value in self.primary_joints.values()]))
        self.exer_list[name] = self
        self._timer = threading.Timer(3, lambda: None)
        self.message = None
        
    def clear_message(self):
        self.message = ""    
        
    def update_message(self, message):
        self.message = message
        
    def update_timer(self, cancel: bool = False, *, msg: str = ""):
        if cancel:
            # User found: Cancel inactivity timer
            if self._timer.is_alive():
                self._timer.cancel()
        else:
            # User not found: Begin inactivity timer
            if not self._timer.is_alive():
                self._timer = threading.Timer(1.75, self.update_message, args=(msg,))
                self._timer.start()
                
    def angle_decreasing(self, joint: str, angle: int):
        if angle < self.previous_angles[joint] - 3:
            return True
        else:
            return False
        
    def angle_increasing(self, joint: str, angle: int):
        if angle > self.previous_angles[joint] + 3:
            return True
        else:
            return False
        
    def process(self, position: int, angles: dict[str, int]) -> tuple[bool, bool, None | str]:
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
                
                if position == 1:
                    # Go up
                    if angle <= min(self.primary_joints[joint]):
                        self.update_timer(True)
                        self.clear_message()
                        primary_flag = True
                    else:
                        if not self.angle_decreasing(joint, angle):
                            message = self.messages[joint][0]
                            self.update_timer(False, msg=message)
                else:
                    # Go down
                    if angle >= max(self.primary_joints[joint]):
                        self.update_timer(True)
                        self.clear_message()
                        primary_flag = True
                    else:
                        if not self.angle_increasing(joint, angle):
                            message = self.messages[joint][1]
                            self.update_timer(False, msg=message)

            elif joint in self.constraining_joints.keys():
                
                if angle < min(self.constraining_joints[joint]):
                    constraint_flag = True
                elif angle > max(self.constraining_joints[joint]):
                    constraint_flag = True
        
        self.previous_angles = angles
        return (primary_flag, constraint_flag)

curl_messages = ("Make sure to go all the way up", "Make sure to go all the way down")
curl = Exercise("curl_right", {"elbow_right": (10, 170)}, {"elbow_right": curl_messages})