import sys

from flytekit import workflow
from flytekit.annotated.condition import conditional


#
# Launch plans are the only means for invoking workflow executions.
# By default, a 'default' launch plan will be created during the serialization (and registration process),
# which will optionally bind any default workflow inputs and any default runtime options specified in the project
# flytekit config (such as user role, etc).
#

from Gardening.DataClass import Context
from Gardening.DataClass import IFracFileHandle
from Gardening.DataClass import DecomposedIFracFileHandle
from Gardening.DataClass import Parameters
from Gardening.DataClass import Platform
from Gardening.DataClass import AWS
from Gardening.DataClass import ADLGen2
from Gardening.DataClass import User
from Gardening.Tasks import report_no_ifrac, validate, split, verify_file_arrived


@workflow
def failed_no_ifrac(context: Context, ifracFileHandle: IFracFileHandle) -> (bool, DecomposedIFracFileHandle):
    report_no_ifrac(context=context, ifracFileHandle=ifracFileHandle)

    return False, DecomposedIFracFileHandle(location="",
                                            parameters=Parameters(),
                                            filenames=[])


@workflow
def ifrac_file_present(context: Context, ifracFileHandle: IFracFileHandle) -> (bool, DecomposedIFracFileHandle):
    validate_result = validate(context=context, ifracFileHandle=ifracFileHandle)

    result = split(context=context, ifracFileHandle=ifracFileHandle)
    return result


@workflow
def decompose(context: Context, ifracFileHandle: IFracFileHandle) -> (bool, DecomposedIFracFileHandle):
    notify_result = verify_file_arrived(context=context, ifracFileHandle=ifracFileHandle)

    return (conditional("ifrac File Present")
            .if_(notify_result == True)
            .then(ifrac_file_present(context=context, ifracFileHandle=ifracFileHandle))
            .else_()
            .then(failed_no_ifrac(context=context, ifracFileHandle=ifracFileHandle)))


def main(argv=None):
    if argv is None:
        argv = sys.argv

    a_user: User = User(name="Power User", email="power.user@company.com")

    a_platform: Platform = AWS()
    a_context: Context = Context(user=a_user, platform=a_platform)

    a_data_lake: ADLGen2 = ADLGen2()
    an_ifracFileHandle = IFracFileHandle(name="dummy.ifrac", lake=a_data_lake)

    result: DecomposedIFracFileHandle = decompose(context=a_context,
                                                  ifracFileHandle=an_ifracFileHandle)

    print("Final result=", result)

    return


if __name__ == "__main__":
    sys.exit(main(sys.argv) or 0)
