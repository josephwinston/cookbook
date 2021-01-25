import sys

from flytekit import task, workflow
from flytekit.annotated.condition import conditional
from flytekit.annotated import context_manager

from gardening.Gardening import dummy

@task
def return_true(a:int) -> bool:
    return True

@task
def failed_notify(a:int) -> None:
    ctx = context_manager.FlyteContext.current_context()
    user_context = ctx.user_space_params
    user_context.logging.info(f"failed a={a}")
    return


@workflow
def failed(a:int) -> int:
    failed_notify(a=a)
    return a


@task 
def success_notify(b:int) -> None: 
    ctx = context_manager.FlyteContext.current_context()
    user_context = ctx.user_space_params
    user_context.logging.info(f"success b={b}")
    return

@workflow
def success(b:int) -> int:
    success_notify(b=b)
    return b

@workflow
def decompose(a:int, b:int ) -> int:
    result = return_true(a=a)

    #
    # Why does the typecheker say?
    # "Expected type 'None', got 'Union[Condition, Promise]' instead "
    #

    return (conditional("test")
            .if_(result == True)
            .then(success(b=b))
            .else_()
            .then(failed(a=a)))


def main(argv=None):
    if argv is None:
        argv = sys.argv

    print (dummy.try_this())
    
    #
    # flytekit.__version__ is 0.16.0a3
    #

    print("XXXX expect 2", decompose(a=1, b=2))

    return


if __name__ == "__main__":
    sys.exit(main(sys.argv) or 0)
