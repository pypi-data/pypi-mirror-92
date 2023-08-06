from ...grader.task import Result, Error


class ComplexityResult(Result):
    """The result of a correctness case."""

    kind = "correctness"

    def __init__(self, passing: bool, complete: bool = True, error: Error = None, details: dict = None):
        super().__init__(complete=complete, passing=passing, error=error, details=details)
