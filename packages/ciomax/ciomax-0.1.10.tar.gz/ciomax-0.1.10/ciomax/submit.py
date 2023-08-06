"""
Submit.

"""
import json
import traceback
import MaxPlus

from ciocore import conductor_submit
from ciocore.validator import ValidationError
from pymxs import runtime as rt


def valid(node):

    # try:
    #     validation.run(node)
    # except ValidationError as ex:
    #     pm.displayWarning(str(ex))
    #     return False
    return True


def submit(dialog):

    advanced_section =  dialog.main_tab.section("AdvancedSection")

    filepath = MaxPlus.FileManager.GetFileNameAndPath()
    if not filepath:
        raise ValueError("This file has never been saved")

    if not rt.checkForSave():
        print "Submission canceled by user"
        return

    if not valid(dialog):
        print "Validation failed or cancelled"
        return


    context = dialog.main_tab.get_context()

    if advanced_section.script_component.display_checkbox.isChecked():
        generated_assets = advanced_section.run_presubmit_script(context)


    submission = dialog.main_tab.resolve(context, generated_assets=generated_assets)

    print json.dumps(submission, indent=2)

    show_tracebacks = advanced_section.tracebacks_checkbox.isChecked()
    try:
        remote_job = conductor_submit.Submit(submission)
        response, response_code = remote_job.main()
        result = {"code": response_code, "response": response}
    except BaseException as ex:
        if show_tracebacks:
            msg = traceback.format_exc()
        else:
            msg = ex.message

        result = {"code": "undefined", "response": msg}

    print result
