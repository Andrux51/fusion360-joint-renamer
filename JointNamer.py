# Author-Andy Martin
# Description-automatic naming of joints using component names

import adsk.core
import adsk.fusion
import adsk.cam
import traceback

# Global list to keep all event handlers in scope.
# This is only needed with Python.
handlers = []

# debug = True
debug = False


def update_all_joints(component):
    app = adsk.core.Application.get()
    ui = app.userInterface

    joints = component.allJoints

    msgBoxText = (str(len(joints)) + " joints found:\n",)

    for i in range(len(joints)):
        joint = joints[i]
        oldName = joint.name

        newName = joint.occurrenceOne.name + " TO " + joint.occurrenceTwo.name

        if not oldName == newName:
            joint.name = newName
            msgBoxText = msgBoxText + (oldName + " (RENAMED -> " + joint.name + ")",)
        else:
            msgBoxText = msgBoxText + (joint.name,)

    if debug:
        ui.messageBox("\n".join(msgBoxText))


def run(context):
    ui = None
    try:
        app = adsk.core.Application.get()
        ui = app.userInterface

        docEventHandler = JointRenameDocumentEventHandler()

        app.documentSaving.add(docEventHandler)
        handlers.append(docEventHandler)
    except:
        if ui:
            ui.messageBox("Failed:\n{}".format(traceback.format_exc()))


class JointRenameDocumentEventHandler(adsk.core.DocumentEventHandler):
    def __init__(self):
        super().__init__()

    def notify(self, args):
        update_all_joints(adsk.core.Application.get().activeProduct.rootComponent)
