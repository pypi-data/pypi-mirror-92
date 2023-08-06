_CONTAINER = "contayner"


class Container:

    def __init__(self):
        pass

    def __str__(self):
        output = []
        output.append("Container:")
        for name, val in vars(self).items():
            output.append(f"{name}: {val}")
        return "\n\t".join(output)


def destroy_container():
    if not hasattr(container, _CONTAINER):
        return
    delattr(container, _CONTAINER)


def container():
    if not hasattr(container, _CONTAINER):
        setattr(container, _CONTAINER, Container())

    return getattr(container, _CONTAINER)
