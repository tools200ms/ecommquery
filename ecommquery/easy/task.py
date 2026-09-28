
class Task:
    @classmethod
    def run(cls, integr: Integrations) -> Task:
        return Task(integr)
