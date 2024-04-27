from typing import Literal, Union, List
from invokeai.invocation_api import (
    BaseInvocationOutput,
    BaseInvocation,
    Input,
    InputField,
    InvocationContext,
    OutputField,
    invocation,
    invocation_output,
    FloatCollectionOutput,
)
from pydantic import BaseModel, Field

LIST_OPERATIONS = Literal[
    "ADD",
    "SUBTRACT",
    "MULTIPLY",
    "DIVIDE",
    "ABS",
    "MAG",
    "PAD",
    "APPEND",
    "CLAMP_MIN",
    "CLAMP_MAX",
]

LIST_OPERATIONS_LABELS = {
    "ADD": "Add C=A+B",
    "SUBTRACT": "Subtract C=A-B",
    "MULTIPLY": "Multiply C=A*B",
    "DIVIDE": "Divide C=A/B",
    "ABS": "Absolute Value C=|A|",
    "MAG": "Magnitude C=||A||",
    "PAD": "Pad C=AU{s,...}|l(C)=l(B)",
    "APPEND": "Append C={A,B}",
    "CLAMP_MIN": "Clamp Min C={max(s,x)∀x∈A}",
    "CLAMP_MAX": "Clamp Max C={min(s,x)∀x∈A}",
}


@invocation("float_collection_math",
            title="Float Collection Math",
            tags=["math", "collection"],
            category="math",
            version="1.0.2"
            )
class FloatCollectionMathInvocation(BaseInvocation):
    """Performs a math operation on a collection of floats. Usually truncates to the length of the shorter list"""
    operation: LIST_OPERATIONS = InputField(
        default="ADD", description="The operation to perform", ui_choice_labels=LIST_OPERATIONS_LABELS
    )
    a: Union[float, List[float]] = InputField(default=1, description="The first list (A)")
    b: Union[float, List[float]] = InputField(default=1, description="The second list (B)")
    s: float = InputField(default=0, description="The scalar value (s)", title="s")

    def invoke(self, context: InvocationContext) -> FloatCollectionOutput:
        #if both inputs are scalars, convert them to lists
        if isinstance(self.a, float) and isinstance(self.b, float):
            self.a = [self.a]
            self.b = [self.b]
        #if one input is a scalar, convert it to a list with the same length as the other input
        elif isinstance(self.a, float):
            self.a = [self.a] * len(self.b)
        elif isinstance(self.b, float):
            self.b = [self.b] * len(self.a)


        if self.operation == "ADD":
            result = [x + y for x, y in zip(self.a, self.b)]
        elif self.operation == "SUBTRACT":
            result = [x - y for x, y in zip(self.a, self.b)]
        elif self.operation == "MULTIPLY":
            result = [x * y for x, y in zip(self.a, self.b)]
        elif self.operation == "DIVIDE":
            result = [x / y for x, y in zip(self.a, self.b)]
        elif self.operation == "ABS":
            result = [abs(x) for x in self.a]
        elif self.operation == "MAG":
            result = [sum(x ** 2 for x in self.a) ** 0.5]
        elif self.operation == "PAD":
            result = self.a + [self.s] * (len(self.b) - len(self.a))
        elif self.operation == "APPEND":
            result = self.a + self.b
        elif self.operation == "CLAMP_MIN":
            result = [max(self.s, x) for x in self.a]
        elif self.operation == "CLAMP_MAX":
            result = [min(self.s, x) for x in self.a]
        else:
            raise ValueError(f"Unknown operation: {self.operation}")
        return FloatCollectionOutput(collection=result)

