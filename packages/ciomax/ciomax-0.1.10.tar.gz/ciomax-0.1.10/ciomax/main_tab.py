 
import os
import MaxPlus
from PySide2 import QtWidgets, QtCore, QtGui
from ciocore.expander import Expander
import datetime
from ciomax.sections.collapsible_section import CollapsibleSection

from ciomax.sections.general_section import GeneralSection
from ciomax.sections.software_section import SoftwareSection
from ciomax.sections.frames_section import FramesSection
from ciomax.sections.info_section import InfoSection
from ciomax.sections.environment_section import EnvironmentSection
from ciomax.sections.metadata_section import MetadataSection
from ciomax.sections.extra_assets_section import ExtraAssetsSection
from ciomax.sections.advanced_section import AdvancedSection
from ciocore import data as coredata

from ciocore.gpath import Path

FIXTURES_DIR = os.path.expanduser(os.path.join("~", "Conductor", "fixtures"))

class MainTab(QtWidgets.QScrollArea):
    """
    Build the tab that contains the main configuration sections.
    """

    def __init__(self, dialog):
        super(MainTab, self).__init__()

        self.dialog = dialog
        coredata.init(product="maya-io")
        coredata.set_fixtures_dir(FIXTURES_DIR if dialog.store.use_fixtures() else "")
        coredata.data(force=True)

        widget = QtWidgets.QWidget()
        self.setWidget(widget)
        self.setWidgetResizable(1)

        sections_layout = QtWidgets.QVBoxLayout()
        widget.setLayout(sections_layout)

        self._section_classes = sorted(
            CollapsibleSection.__subclasses__(), key=lambda x: x.ORDER)
        self.sections = [cls(self.dialog) for cls in self._section_classes]

        for section in self.sections:
            sections_layout.addWidget(section)

        sections_layout.addStretch()

    def populate_from_store(self):
        for section in self.sections:
            section.populate_from_store()

    def section(self, classname):
        """
        Convenience to find sections by name.

        Makes it easier to allow sections to talk to each other.
        Example: Calculate info from stuff in the frames section
            self.section("InfoSection").calculate(self.section("FramesSection"))

        """

        return next(s for s in self.sections if s.__class__.__name__ == classname)

    def resolve(self, context, **kwargs):
        submission = {}
        expander = Expander(safe=True, **context)
        for section in self.sections:
            submission.update(section.resolve(expander, **kwargs))
        return submission

    def get_context(self):
        scenefile = MaxPlus.FileManager.GetFileNameAndPath()
        if scenefile:
            scenefile = Path(scenefile).posix_path()
            scenedir = os.path.dirname(scenefile)
            scenenamex, ext = os.path.splitext(os.path.basename(scenefile))
        else:
            scenefile = "/NOT_SAVED"
            scenedir = "/NOT_SAVED"
            scenenamex, ext = ("NOT_SAVED", "")
        scenename = "{}{}".format(scenenamex,ext)

        project = MaxPlus.Core.EvalMAXScript(
            'pathConfig.getCurrentProjectFolder()').Get()
        if project:
            project = Path(project).posix_path()
        else:
            project = "/NOT_SET"

        result = {
            "conductor": self.dialog.conductor_location,
            "scenefile": scenefile,
            "scenedir": scenedir,
            "scenenamex": scenenamex,
            "ext": ext,
            "scenename":scenename,
            "project": project,
            "renderer": MaxPlus.RenderSettings.GetProduction().GetClassName(),
            "timestamp": datetime.datetime.now().strftime('%y%m%d_%H%M')
        }
        return result
