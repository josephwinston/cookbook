import sys
import typing

#
# Flyte supports passing JSON's between tasks. But, to simplify the
# usage for the users and introduce type-safety, flytekit supports
# passing custom data objects between tasks. Currently only
# dataclasses that are decorated with @dataclasses_json are supported.
#

from dataclasses import dataclass
from dataclasses_json import dataclass_json

from flytekit import task, workflow, LaunchPlan, current_context
from flytekit.annotated.condition import conditional
from flytekit.annotated import context_manager

#
# Launch plans are the only means for invoking workflow executions.
# By default, a 'default' launch plan will be created during the serialization (and registration process),
# which will optionally bind any default workflow inputs and any default runtime options specified in the project
# flytekit config (such as user role, etc).
#
from Gardening.DataClass import User, Platform, AWS, Context, ADLGen2, IFracFileHandle, DecomposedIFracFileHandle, Azure
from Gardening.Defaults import context, ifracFileHandle
from Gardening.Workflows import decompose


def main(argv=None):
    if argv is None:
        argv = sys.argv

    a_user: User = User(name="Power User", email="power.user@company.com")

    a_platform: Platform = AWS()
    a_context: Context = Context(user=a_user, platform=a_platform)

    a_data_lake: ADLGen2 = ADLGen2()
    an_ifracFileHandle: IFracFileHandle = IFracFileHandle(name="dummy.ifrac", lake=a_data_lake)

    result: DecomposedIFracFileHandle = decompose(context=a_context,
                                                  ifracFileHandle=an_ifracFileHandle)

    print("Final result=", result)

    return

default_lp = LaunchPlan.create(current_context(),
                               decompose,
                               default_inputs={"context": context,
                                               "ifracFileHandle": ifracFileHandle}
                               )

if __name__ == "__main__":
    sys.exit(main(sys.argv) or 0)
