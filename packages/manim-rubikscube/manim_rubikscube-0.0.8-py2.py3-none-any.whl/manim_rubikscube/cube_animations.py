from manim.animation.transform import Transform
from manim.animation.animation import Animation
from manim.constants import PI
from manim.mobject.types.vectorized_mobject import VGroup
from .cube_utils import get_axis_from_face

class MoveCube(Transform):
    def __init__(self, mobject, face, **kwargs):
        self.axis = get_axis_from_face(face[0])
        super().__init__(mobject, **kwargs)
        self.cube = self.mobject.copy()
        self.face = face

    def create_target(self):
        if self.cube.indices == {}:
            self.cube.set_indices()
        
        face = self.face
        group = VGroup(*self.cube.get_face(self.face[0]))

        angle = PI/2 if ("R" in face or "F" in face or "D" in face) else -PI/2
        angle = angle if "2" not in face else angle*2
        angle = -angle if "'" in face else angle

        group.rotate(angle, self.axis)
        return self.cube

    def finish(self):
        super().finish()
        self.mobject.adjust_indices(self.mobject.get_face(self.face[0], False))

class CubeMove(Animation):
    def __init__(self, mobject, face, **kwargs):
        self.axis = get_axis_from_face(face[0])
        self.face = face
        self.angle = PI/2 if ("R" in face or "F" in face or "D" in face) else -PI/2
        self.angle = self.angle if "2" not in face else self.angle*2
        self.angle = -self.angle if "'" in face else self.angle
        super().__init__(mobject, **kwargs)

    def create_starting_mobject(self):
        starting_mobject = self.mobject.copy()
        if starting_mobject.indices == {}:
            starting_mobject.set_indices()
        return starting_mobject

    def interpolate_mobject(self, alpha):
        self.mobject.become(self.starting_mobject)
        
        VGroup(*self.mobject.get_face(self.face[0])).rotate(
            alpha * self.angle,
            self.axis
        )

    def finish(self):
        super().finish()
        self.mobject.adjust_indices(self.mobject.get_face(self.face[0], False))