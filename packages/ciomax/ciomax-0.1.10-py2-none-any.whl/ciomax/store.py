
"""
Encapsulation of a max dummy object to use as a settings store.

The purpose of the store is to make it possible to persist the state of the
dialog (settings) in the scene file.

The Object IDs are abstracted here.
Therefore we can present a public API containing the following methods for each setting:
def attribute():
def set_attribute(value):

The store is NOT the single source of truth while dialog is open. The widgets are.

So the flow is:

- User opens dialog:
- Check if scene has an instance of the conductor_store.
    - If not, make one and reset it to factory defaults.
- Populate the UI from the store.

When the user changes some value, persist it to the store.

"""

import MaxPlus


import os
import json
from ciocore.gpath import Path
from pymxs import runtime as rt
from ciomax.renderer import Renderer


DEFAULT_TITLE = u"3dsmax <upper renderer> <scenenamex>"

STORE_NAME = u"ConductorStore"

DEFAULT_DESTINATION = '<project>/renderoutput'

# IDS: 

# Each setting is accessed by ID. 
# 
# NOTE Always add to the end - Don't insert! Don't ever reorder or remove
# entries, even if an attribute becomes redundant. If you do it will make old
# scenes incompatible.

X = 2000
TITLE = X = X+1
PROJECT = X = X+1
DESTINATION = X = X+1
EXTRA_ASSETS = X = X+1
INSTANCE_TYPE = X = X+1
PREEMPTIBLE = X = X+1
CHUNK_SIZE = X = X+1
USE_CUSTOM_RANGE = X = X+1
CUSTOM_RANGE = X = X+1
USE_SCOUT_FRAMES = X = X+1
SCOUT_FRAMES = X = X+1
TASK_TEMPLATE = X = X+1
EXTRA_ENVIRONMENT = X = X+1
METADATA = X = X+1
USE_UPLOAD_DAEMON = X = X+1
UPLOAD_ONLY = X = X+1
RETRIES_WHEN_PREEMPTED = X = X+1
USE_AUTOSAVE = X = X+1
AUTOSAVE_FILENAME = X = X+1
AUTOSAVE_CLEANUP = X = X+1
LOCATION_TAG = X = X+1
SHOW_TRACEBACKS = X = X+1
HOST_VERSION = X = X+1
RENDERER_VERSION = X = X+1
EMAILS = X = X+1
USE_EMAILS = X = X+1
USE_FIXTURES = X = X+1
FIXTURES_PATH = X = X+1
OVERRIDE_DESTINATION = X = X+1
DEFAULT_TASK_TEMPLATE = X = X+1
USE_SCRIPT = X = X+1
SCRIPT_FILENAME = X = X+1

SECTIONS_OPEN = {}
SECTIONS_OPEN["GeneralSection"] = X = X+1
SECTIONS_OPEN["SoftwareSection"] = X = X+1
SECTIONS_OPEN["FramesSection"] = X = X+1
SECTIONS_OPEN["InfoSection"] = X = X+1
SECTIONS_OPEN["EnvironmentSection"] = X = X+1
SECTIONS_OPEN["MetadataSection"] = X = X+1
SECTIONS_OPEN["ExtraAssetsSection"] = X = X+1
SECTIONS_OPEN["AdvancedSection"] = X = X+1


def print_ids():
    print "TITLE ID:", TITLE
    print "PROJECT ID:", PROJECT
    print "DESTINATION ID:", DESTINATION
    print "EXTRA_ASSETS ID:", EXTRA_ASSETS
    print "INSTANCE_TYPE ID:", INSTANCE_TYPE
    print "PREEMPTIBLE ID:", PREEMPTIBLE
    print "CHUNK_SIZE ID:", CHUNK_SIZE
    print "USE_CUSTOM_RANGE ID:", USE_CUSTOM_RANGE
    print "CUSTOM_RANGE ID:", CUSTOM_RANGE
    print "USE_SCOUT_FRAMES ID:", USE_SCOUT_FRAMES
    print "SCOUT_FRAMES ID:", SCOUT_FRAMES
    print "TASK_TEMPLATE ID:", TASK_TEMPLATE
    print "EXTRA_ENVIRONMENT ID:", EXTRA_ENVIRONMENT
    print "METADATA ID:", METADATA
    print "USE_UPLOAD_DAEMON ID:", USE_UPLOAD_DAEMON
    print "UPLOAD_ONLY ID:", UPLOAD_ONLY
    print "RETRIES_WHEN_PREEMPTED ID:", RETRIES_WHEN_PREEMPTED
    print "USE_AUTOSAVE ID:", USE_AUTOSAVE
    print "AUTOSAVE_FILENAME ID:", AUTOSAVE_FILENAME
    print "AUTOSAVE_CLEANUP ID:", AUTOSAVE_CLEANUP
    print "LOCATION_TAG ID:", LOCATION_TAG
    print "SHOW_TRACEBACKS ID:", SHOW_TRACEBACKS
    print "HOST_VERSION ID:", HOST_VERSION
    print "RENDERER_VERSION ID:", RENDERER_VERSION
    print "EMAILS ID:", EMAILS
    print "USE_EMAILS ID:", USE_EMAILS
    print "USE_FIXTURES ID:", USE_FIXTURES
    print "OVERRIDE_DESTINATION ID:", OVERRIDE_DESTINATION
    print "DEFAULT_TASK_TEMPLATE ID:", DEFAULT_TASK_TEMPLATE
    print "USE_SCRIPT:", USE_SCRIPT
    print "SCRIPT_FILENAME:", SCRIPT_FILENAME


class ConductorStore(object):
    """
    The store is used to persist a submission recipe in the scene file, and to
    repopulate the dialog when it's rebuilt.
    """

    def __init__(self):
        self.node = MaxPlus.INode.GetINodeByName(STORE_NAME)
        if not self.node:
            dummy = MaxPlus.Factory.CreateDummyObject()
            self.node = MaxPlus.Factory.CreateNode(dummy, STORE_NAME)
            self.reset()
        
        self.set_renderer()
        # print_ids()

    def clear(self):
        self.node.ClearAllAppData()

    def reset(self):

        print "IN STORE RESET:"

        self.clear()

        self.set_title(DEFAULT_TITLE)

        self.set_project(u"default")
        self.set_instance_type(u"n1-highcpu-8")
        self.set_preemptible(True)
        self.set_chunk_size(1)
        self.set_use_custom_range(False)
        self.set_custom_range(u"1-10")
        self.set_use_scout_frames(True)
        self.set_scout_frames(u"auto:3")

        self.set_destination(DEFAULT_DESTINATION)
     

        self.set_task_template("")
        # self.set_DEFAULT_task_template(True)
        self.set_extra_environment()
        self.set_metadata()

        self.set_use_upload_daemon(False)
        self.set_upload_only(False)
        self.set_retries_when_preempted(1)

        self.set_location_tag("")
        self.set_emails(u"artist@example.com, producer@example.com")
        self.set_use_emails(False)

        self.set_show_tracebacks(False)
        self.set_use_fixtures(True)

        self.set_assets()
        self.set_host_version(u"maya-io 2020.SP4")
        self.set_renderer_version("")

        self.set_use_script(True)
        self.set_script_filename("")

        self.set_section_open("GeneralSection", True)
        self.set_section_open("SoftwareSection", True)
        self.set_section_open("FramesSection", False)
        self.set_section_open("InfoSection", True)
        self.set_section_open("EnvironmentSection", False)
        self.set_section_open("MetadataSection", False)
        self.set_section_open("ExtraAssetsSection", False)
        self.set_section_open("AdvancedSection", False)



    def set_renderer(self):
        """Set renderer is called every time we open the dialog."""
        renderer = Renderer.get()
        render_template = renderer.templates[0] # 0 is the default
        current_renderer_version = renderer.get_version()
        current_renderer_type = current_renderer_version.split(" ")[0]

        print "current_renderer_version", current_renderer_version
        if not self.script_filename():
            self.set_script_filename(render_template["script"])
        
        if not self.task_template(): 
            self.set_task_template(render_template["command"])

        # If different render type selected, overwrite the stored renderer.
        stored_renderer_type = self.renderer_version().split(" ")[0]  or ""
        if not current_renderer_type == stored_renderer_type:
            self.set_renderer_version(current_renderer_version)

    def title(self):
        return self.node.GetAppData(TITLE)

    def set_title(self, value):
        try:
            self.node.DeleteAppData(TITLE)
        except RuntimeError:
            pass
        self.node.SetAppData(TITLE, value)

    def project(self):
        return self.node.GetAppData(PROJECT)

    def set_project(self, value):
        try:
            self.node.DeleteAppData(PROJECT)
        except RuntimeError:
            pass
        self.node.SetAppData(PROJECT, value)

    def instance_type(self):
        return self.node.GetAppData(INSTANCE_TYPE)

    def set_instance_type(self, value):
        try:
            self.node.DeleteAppData(INSTANCE_TYPE)
        except RuntimeError:
            pass
        self.node.SetAppData(INSTANCE_TYPE, value)

    def preemptible(self):
        return json.loads(self.node.GetAppData(PREEMPTIBLE))

    def set_preemptible(self, value):
        try:
            self.node.DeleteAppData(PREEMPTIBLE)
        except RuntimeError:
            pass
        self.node.SetAppData(PREEMPTIBLE, json.dumps(value))

    def destination(self):
        return self.node.GetAppData(DESTINATION)

    def set_destination(self, value):
        try:
            self.node.DeleteAppData(DESTINATION)
        except RuntimeError:
            pass
        self.node.SetAppData(DESTINATION, value)

    def chunk_size(self):
        return json.loads(self.node.GetAppData(CHUNK_SIZE))

    def set_chunk_size(self, value):
        try:
            self.node.DeleteAppData(CHUNK_SIZE)
        except RuntimeError:
            pass
        self.node.SetAppData(CHUNK_SIZE,  json.dumps(value))

    def use_custom_range(self):
        return json.loads(self.node.GetAppData(USE_CUSTOM_RANGE))

    def set_use_custom_range(self, value):
        try:
            self.node.DeleteAppData(USE_CUSTOM_RANGE)
        except RuntimeError:
            pass
        self.node.SetAppData(USE_CUSTOM_RANGE, json.dumps(value))

    def custom_range(self):
        return self.node.GetAppData(CUSTOM_RANGE)

    def set_custom_range(self, value):
        try:
            self.node.DeleteAppData(CUSTOM_RANGE)
        except RuntimeError:
            pass
        self.node.SetAppData(CUSTOM_RANGE, value)

    def use_scout_frames(self):
        return json.loads(self.node.GetAppData(USE_SCOUT_FRAMES))

    def set_use_scout_frames(self, value):
        try:
            self.node.DeleteAppData(USE_SCOUT_FRAMES)
        except RuntimeError:
            pass
        self.node.SetAppData(USE_SCOUT_FRAMES, json.dumps(value))

    def scout_frames(self):
        return self.node.GetAppData(SCOUT_FRAMES)

    def set_scout_frames(self, value):
        try:
            self.node.DeleteAppData(SCOUT_FRAMES)
        except RuntimeError:
            pass
        self.node.SetAppData(SCOUT_FRAMES, value)
 
    def task_template(self):
        return self.node.GetAppData(TASK_TEMPLATE)

    def set_task_template(self, value):
        try:
            self.node.DeleteAppData(TASK_TEMPLATE)
        except RuntimeError:
            pass
        self.node.SetAppData(TASK_TEMPLATE, value)

    def extra_environment(self):
        return json.loads(self.node.GetAppData(EXTRA_ENVIRONMENT)) or []

    def set_extra_environment(self, obj=[]):
        try:
            self.node.DeleteAppData(EXTRA_ENVIRONMENT)
        except RuntimeError:
            pass
        self.node.SetAppData(EXTRA_ENVIRONMENT,  json.dumps(obj))

    def metadata(self):
        return json.loads(self.node.GetAppData(METADATA)) or []

    def set_metadata(self, obj=[]):
        try:
            self.node.DeleteAppData(METADATA)
        except RuntimeError:
            pass
        self.node.SetAppData(METADATA, json.dumps(obj))

    def use_upload_daemon(self):
        return json.loads(self.node.GetAppData(USE_UPLOAD_DAEMON))

    def set_use_upload_daemon(self, value):
        try:
            self.node.DeleteAppData(USE_UPLOAD_DAEMON)
        except RuntimeError:
            pass
        self.node.SetAppData(USE_UPLOAD_DAEMON, json.dumps(value))

    def upload_only(self):
        return json.loads(self.node.GetAppData(UPLOAD_ONLY))

    def set_upload_only(self, value):
        try:
            self.node.DeleteAppData(UPLOAD_ONLY)
        except RuntimeError:
            pass
        self.node.SetAppData(UPLOAD_ONLY,  json.dumps(value))

    def retries_when_preempted(self):
        return json.loads(self.node.GetAppData(RETRIES_WHEN_PREEMPTED))

    def set_retries_when_preempted(self, value):
        try:
            self.node.DeleteAppData(RETRIES_WHEN_PREEMPTED)
        except RuntimeError:
            pass
        self.node.SetAppData(RETRIES_WHEN_PREEMPTED, json.dumps(value))

    def use_autosave(self):
        return json.loads(self.node.GetAppData(USE_AUTOSAVE))

    def set_use_autosave(self, value):
        try:
            self.node.DeleteAppData(USE_AUTOSAVE)
        except RuntimeError:
            pass
        self.node.SetAppData(USE_AUTOSAVE, json.dumps(value))

    def autosave_filename(self):
        return self.node.GetAppData(AUTOSAVE_FILENAME)

    def set_autosave_filename(self, value):
        try:
            self.node.DeleteAppData(AUTOSAVE_FILENAME)
        except RuntimeError:
            pass
        self.node.SetAppData(AUTOSAVE_FILENAME, value)

    def autosave_cleanup(self):
        return json.loads(self.node.GetAppData(AUTOSAVE_CLEANUP))

    def set_autosave_cleanup(self, value):
        try:
            self.node.DeleteAppData(AUTOSAVE_CLEANUP)
        except RuntimeError:
            pass
        self.node.SetAppData(AUTOSAVE_CLEANUP, json.dumps(value))

    def location_tag(self):
        return self.node.GetAppData(LOCATION_TAG)

    def set_location_tag(self, value):
        try:
            self.node.DeleteAppData(LOCATION_TAG)
        except RuntimeError:
            pass
        self.node.SetAppData(LOCATION_TAG, value)

    def show_tracebacks(self):
        return json.loads(self.node.GetAppData(SHOW_TRACEBACKS))

    def set_show_tracebacks(self, value):
        try:
            self.node.DeleteAppData(SHOW_TRACEBACKS)
        except RuntimeError:
            pass
        self.node.SetAppData(SHOW_TRACEBACKS,  json.dumps(value))

    def use_fixtures(self):
        return json.loads(self.node.GetAppData(USE_FIXTURES))

    def set_use_fixtures(self, value):
        try:
            self.node.DeleteAppData(USE_FIXTURES)
        except RuntimeError:
            pass
        self.node.SetAppData(USE_FIXTURES, json.dumps(value))

    def host_version(self):
        return self.node.GetAppData(HOST_VERSION)

    def set_host_version(self, value):
        try:
            self.node.DeleteAppData(HOST_VERSION)
        except RuntimeError:
            pass
        self.node.SetAppData(HOST_VERSION, value)

    def renderer_version(self):
        return self.node.GetAppData(RENDERER_VERSION)

    def set_renderer_version(self, value):
        try:
            self.node.DeleteAppData(RENDERER_VERSION)
        except RuntimeError:
            pass
        self.node.SetAppData(RENDERER_VERSION, value)

    def use_emails(self):
        return json.loads(self.node.GetAppData(USE_EMAILS))

    def set_use_emails(self, value):
        try:
            self.node.DeleteAppData(USE_EMAILS)
        except RuntimeError:
            pass
        self.node.SetAppData(USE_EMAILS, json.dumps(value))

    def emails(self):
        return self.node.GetAppData(EMAILS)

    def set_emails(self, value):
        try:
            self.node.DeleteAppData(EMAILS)
        except RuntimeError:
            pass
        self.node.SetAppData(EMAILS, value)

    def assets(self):
        return json.loads(self.node.GetAppData(EXTRA_ASSETS))

    def set_assets(self, assets=[]):
        try:
            self.node.DeleteAppData(EXTRA_ASSETS)
        except RuntimeError:
            pass
        self.node.SetAppData(EXTRA_ASSETS, json.dumps(assets))

    def use_script(self):
        return json.loads(self.node.GetAppData(USE_SCRIPT))

    def set_use_script(self, value):
        try:
            self.node.DeleteAppData(USE_SCRIPT)
        except RuntimeError:
            pass
        self.node.SetAppData(USE_SCRIPT, json.dumps(value))

    def script_filename(self):
        return self.node.GetAppData(SCRIPT_FILENAME)

    def set_script_filename(self, value):
        try:
            self.node.DeleteAppData(SCRIPT_FILENAME)
        except RuntimeError:
            pass
        self.node.SetAppData(SCRIPT_FILENAME, value)
 
    # section_open("general")
    def section_open(self, section):
        return json.loads(self.node.GetAppData(SECTIONS_OPEN[section]))
    # set_section_open("advanced")
    def set_section_open(self, section, value):
        try:
            self.node.DeleteAppData(SECTIONS_OPEN[section])
        except RuntimeError:
            pass
        self.node.SetAppData(SECTIONS_OPEN[section], json.dumps(value))
