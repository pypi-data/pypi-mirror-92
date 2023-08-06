from PySide2 import QtWidgets, QtGui

from ciomax.sections.collapsible_section import CollapsibleSection
from ciomax.components.software_combo_box_grp import SoftwareComboBoxGrp
from ciocore import data as coredata
from ciocore.package_environment import PackageEnvironment


class SoftwareSection(CollapsibleSection):
    ORDER = 20

    def __init__(self, dialog):

        super(SoftwareSection, self).__init__(dialog, "Software")

        self.component = SoftwareComboBoxGrp(False)
        self.content_layout.addWidget(self.component)
        self.configure_combo_boxes()

        # Write to store when values change
        self.component.combobox_renderer_version.currentTextChanged.connect(
            self.on_change)

    def on_change(self, value):

        store = self.dialog.store
        store.set_host_version(self.component.combobox_host.currentText())
        store.set_renderer_version(
            "{} {}".format(
                self.component.combobox_renderer_name.currentText(),
                self.component.combobox_renderer_version.currentText()
            )
        )

    def populate_from_store(self):
        store = self.dialog.store
        super(SoftwareSection, self).populate_from_store(store )
        # We have to save the renderer from the store in a variable before
        # setting the host, because when we set the host, a cascade of events
        # take place which ultimately set the store value.
        # TODO : Use activated() instead of currentTextChanged()
        host_version = store.host_version()
        renderer_version = store.renderer_version()

        self.component.set_host_by_text(host_version)
        self.component.set_renderer_by_text(renderer_version)

    def configure_combo_boxes(self):
        if not coredata.valid():
            print "Invalid packages data"
            return False

        model = QtGui.QStandardItemModel()
        software_data = coredata.data()["software"]
        hosts = software_data.supported_host_names()
        for host in hosts:
            host_item = QtGui.QStandardItem(host)
            plugins = software_data.supported_plugins(host)
            for plugin in plugins:
                plugin_item = QtGui.QStandardItem(plugin["plugin"])
                for version in plugin["versions"]:
                    version_item = QtGui.QStandardItem(version)
                    #
                    plugin_item.appendRow(version_item)
                host_item.appendRow(plugin_item)
            model.appendRow(host_item)

        self.component.set_model(model)

    def resolve(self, expander, **kwargs):
        extra_environment = self.dialog.main_tab.section(
            "EnvironmentSection").get_entries(expander)

        packages_data = self.get_packages()
        if not packages_data:
            return []

        packages_data["env"].extend(extra_environment)
        return {
            "environment": dict(packages_data["env"]),
            "software_package_ids": packages_data["ids"]
        }






    def get_packages(self):
        if not coredata.valid():
            return
        tree_data = coredata.data()["software"]
        paths = []
        host_path = self.component.combobox_host.currentText()

        renderer_path = "{}/{}".format(host_path,
                                       self.component.get_renderer())
        paths = [host_path, renderer_path]

        # HACK TO REMOVE VRAY VARS
        print "paths",paths
        if renderer_path.split("/")[1].startswith("v-ray"):
            paths = []
        print "paths",paths



        result = {
            "ids": [],
            "env": PackageEnvironment()
        }
        for package in filter(None, [tree_data.find_by_path(path) for path in paths if path]):
            result["ids"].append(package["package_id"])
            result["env"].extend(package)

        return result
