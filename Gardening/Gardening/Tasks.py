#
# Flyte supports passing JSON's between tasks. But, to simplify the
# usage for the users and introduce type-safety, flytekit supports
# passing custom data objects between tasks. Currently only
# dataclasses that are decorated with @dataclasses_json are supported.
#

from flytekit import task
from flytekit.annotated import context_manager

from Gardening.DataClass import Context
from Gardening.DataClass import DecomposedIFracFileHandle
from Gardening.DataClass import IFracFileHandle
from Gardening.DataClass import Parameters


#
# Launch plans are the only means for invoking workflow executions.
# By default, a 'default' launch plan will be created during the serialization (and registration process),
# which will optionally bind any default workflow inputs and any default runtime options specified in the project
# flytekit config (such as user role, etc).
#

#
# A function in flyte is decorated with the flytekit.task decorator.
# All inputs and outputs must be annotated with types.
# Additionally, all arguments must be keyword arguments.
#



@task
def verify_file_arrived(context: Context, ifracFileHandle: IFracFileHandle) -> bool:
    """ When an ifrac file is placed in a well known location, send a
    notification so that the next stage of processing can take place.
    Specifically, this is the code that validates the file.  Return
    True if and only if the file exists and the mail is sent

    :param context: Context
    :param ifracFileHandle: IFracFileHandle
    :return: bool on success
    """

    print("in verify_file_arrived")

    result: bool = False

    return result


@task
def validate(context: Context, ifracFileHandle: IFracFileHandle) -> bool:
    """ Ensure that the ifrac file has the correct structure.  Once
    this is complete, notify the next step in the workflow, which is
    to process the ifrac file.

    :param context: Context
    :param ifracFileHandle: IFracFileHandle
    :return: bool on success
    """

    print("in validate")

    result: bool = False

    return result


@task
def split(context: Context, ifracFileHandle: IFracFileHandle) -> (bool, DecomposedIFracFileHandle):
    """ Take the validated ifrac file and decompose into its component
    parts to make scaling easier.  This work includes creating the
    appropriate "directories" in the Azure Data Lake Gen 2, placing
    the csv files in the directories, possibly converting the csv
    files to parquet, and then notifying SQL that files are ready for
    ingest.

    TODO: Decompose into more tasks

    :param context: Context
    :param ifracFileHandle: IFracFileHandle
    :return: DecomposedIFracFileHandle
    """

    print("in split")

    result: DecomposedIFracFileHandle = DecomposedIFracFileHandle(location="local filesystem",
                                                                  parameters=Parameters(),
                                                                  filenames=[])

    return False, result


@task
def notifyBI(context: Context) -> bool:
    """
    Notify on ifrac ready for Business Intelligence Tools Send
    notification to all interested parties that ifrac is now ready to
    be consumed in some set of Business Intelligence (BI)
    applications.

    :param context: Context
    :param an_ifracFile
    :return: bool on success
    """

    print("in notifyBI")
    return


@task
def report_no_ifrac(context: Context, ifracFileHandle: IFracFileHandle) -> None:
    """
    When in a @workflow, the input arguments are promises.  In a task, the values can be
    retrieved.
    """

    print("in report_no_ifrac")

    ctx = context_manager.FlyteContext.current_context()
    user_context = ctx.user_space_params
    user_context.logging.info(f"Could not locate {ifracFileHandle.name}")
    user_context.logging.info(f"Need to notify {context.user.email}")
    return
