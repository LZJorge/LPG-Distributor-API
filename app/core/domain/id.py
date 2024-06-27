from uuid import UUID, uuid4


class ID(UUID):

    @classmethod
    def generate(cls) -> str:
        return uuid4()
