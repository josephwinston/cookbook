import sys

from flytekit import task, workflow
from flytekit.annotated.condition import conditional
from flytekit.annotated import context_manager


@task
def return_true(a:int) -> bool:
    return True


@workflow
def failed(a:int) -> int:
    ctx = context_manager.FlyteContext.current_context()
    user_context = ctx.user_space_params
    user_context.logging.info(f"failed a={a}")
    return a


@workflow
def success(b:int) -> int:
    ctx = context_manager.FlyteContext.current_context()
    user_context = ctx.user_space_params
    user_context.logging.info(f"success b={b}")
    return b


@workflow
def decompose(a:int) -> int:
    result = return_true(a=a)

    #
    # Why does the typecheker say?
    # "Expected type 'None', got 'Union[Condition, Promise]' instead "
    #

    return (conditional("test")
            .if_(result == True)
            .then(success(b=a))
            .else_()
            .then(failed(a=a)))


def main(argv=None):
    if argv is None:
        argv = sys.argv

    #
    # flytekit.__version__ is 0.16.0a3
    #

    decompose(a=1)

    return


if __name__ == "__main__":
    sys.exit(main(sys.argv) or 0)
