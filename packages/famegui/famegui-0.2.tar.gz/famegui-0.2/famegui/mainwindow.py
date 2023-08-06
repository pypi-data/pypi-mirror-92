# This Python file uses the following encoding: utf-8
import os
import logging
import getpass

from PySide2.QtWidgets import QApplication, QMainWindow
from PySide2 import QtCore, QtGui, QtWidgets

import famegui.qt_resources_rc
from famegui.ui_mainwindow import Ui_MainWindow
from famegui.newagent_dialog import NewAgentDialog
from famegui.newcontract_dialog import NewContractDialog
from famegui.scenario_graph_view import ScenarioGraphView
from famegui.agent_controller import AgentController

from famegui import models
from famegui.scenario_controller import ScenarioController


class PropertyTreeItem(QtWidgets.QTreeWidgetItem):
    def __init__(self, parent, name, value):
        QtWidgets.QTreeWidgetItem.__init__(self, parent, [name, value])
        self.setFlags(self.flags() | QtCore.Qt.ItemIsEditable)

    def setData(self, column, role, value):
        """ Override QTreeWidgetItem.setData() """
        if (role == QtCore.Qt.EditRole):
            logging.info("new value: {}".format(value))

        QtWidgets.QTreeWidgetItem.setData(self, column, role, value)


class MainWindow(QMainWindow):
    def __init__(self):
        super(MainWindow, self).__init__()
        self._tree_items_for_agent_types = {}
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)
        self._init_ui()
        self._connect_actions()
        self._connect_slots()
        self._on_project_closed()

    def _init_ui(self):
        # create an attach the scene
        self._graph_view = ScenarioGraphView(self)
        self._graph_view.setSceneRect(0, 0, 2000, 2000)
        self.ui.graphicsView.setScene(self._graph_view)
        # customize main window
        self.ui.labelUserName.setText(getpass.getuser())
        self.ui.graphicsView.setBackgroundBrush(QtGui.QColor(230, 230, 230))
        self.setWindowTitle(
            QtWidgets.QApplication.instance().applicationDisplayName())
        # project struture tree view
        self.ui.treeProjectStructure.setSelectionMode(
            QtWidgets.QAbstractItemView.SingleSelection)
        self.ui.treeProjectStructure.setColumnCount(1)
        self.ui.treeProjectStructure.setHeaderLabels(["Agents"])
        # properties tree view
        self.ui.treeProperties.setSelectionMode(
            QtWidgets.QAbstractItemView.SingleSelection)
        self.ui.treeProperties.setRootIsDecorated(False)
        self.ui.treeProperties.setColumnCount(2)
        self.ui.treeProperties.setHeaderLabels(["Property", "Value"])
        self.ui.treeProperties.setColumnWidth(0, 140)
        self.ui.treeProperties.setAlternatingRowColors(True)
        # init and attach controllers
        self._scenario_ctrl = ScenarioController()
        self._scenario_ctrl.has_scenario_data_changed.connect(
            self._enable_views)
        self._scenario_ctrl.agent_added.connect(self._on_agent_added)
        self._scenario_ctrl.contract_added.connect(self._on_contract_added)
        self._scenario_ctrl.file_path_changed.connect(
            self.ui.labelProjectName.setText)
        self._scenario_ctrl.selected_agent_changed.connect(
            self._on_selected_agent_changed)

    def _connect_actions(self):
        # new
        self.ui.actionNewProject.triggered.connect(self.new_project)
        # open
        self.ui.actionOpenProject.triggered.connect(
            self.show_open_scenario_file_dlg)
        # save (enabled only when a change has been done)
        self.ui.actionSaveProject.triggered.connect(self.save_project)
        self._scenario_ctrl.has_unsaved_changes_changed.connect(
            self.ui.actionSaveProject.setEnabled)
        self.ui.actionSaveProject.setEnabled(
            self._scenario_ctrl.has_unsaved_changes)
        # save as
        self.ui.actionSaveProjectAs.triggered.connect(self.save_project_as)
        # close
        self.ui.actionCloseProject.triggered.connect(self.close_project)
        # exit
        self.ui.actionExit.triggered.connect(self.close)

    def _connect_slots(self):
        self.ui.sliderZoomFactor.valueChanged.connect(
            self._on_zoom_value_changed)
        self._graph_view.selected_agent_changed.connect(
            self._scenario_ctrl.set_selected_agent_id)
        self._graph_view.contract_creation_requested.connect(
            self._on_contract_creation_requested)
        self._graph_view.agent_creation_requested.connect(
            self._on_agent_creation_requested)
        self.ui.treeProjectStructure.currentItemChanged.connect(
            self._on_tree_view_current_item_changed)
        self.ui.lineFilterPattern.textChanged.connect(
            self._filter_pattern_changed)

    def _on_zoom_value_changed(self):
        zoomFactor = self.ui.sliderZoomFactor.value()
        assert zoomFactor > 0
        scaleFactor = zoomFactor * 0.01
        self.ui.graphicsView.setTransform(
            QtGui.QTransform.fromScale(scaleFactor, scaleFactor))
        self.ui.labelZoomFactor.setText("{} %".format(zoomFactor))

    def _on_tree_view_current_item_changed(self):
        assert self._scenario_ctrl.has_scenario_data

        selected_agent_id = None

        tree_item = self.ui.treeProjectStructure.currentItem()
        if tree_item is not None:
            # note: the given id value can be None
            selected_agent_id = tree_item.data(0, QtCore.Qt.UserRole)

        self._scenario_ctrl.set_selected_agent_id(selected_agent_id)

    def _on_agent_creation_requested(self, x: int, y: int):
        assert self._scenario_ctrl.has_scenario_data

        dlg = NewAgentDialog(self)
        if dlg.exec_() != 0:
            new_agent = dlg.make_new_agent(
                self._scenario_ctrl.generate_new_agent_id())
            self._scenario_ctrl.add_new_agent(new_agent, x, y)

    def _on_contract_creation_requested(self, sender_id: int, receiver_id: int):
        dlg = NewContractDialog(self.parent(), sender_id, receiver_id)
        if dlg.exec_() != 0:
            self._scenario_ctrl.add_new_contract(dlg.make_new_contract())

    def _on_selected_agent_changed(self, agent_ctrl: AgentController):
        if agent_ctrl is None:
            # clear selection
            self.ui.treeProjectStructure.clearSelection()
            self._graph_view.clearSelection()
            self.ui.treeProperties.clear()
            return

        # block signals
        self.ui.treeProjectStructure.blockSignals(True)
        self._graph_view.blockSignals(True)

        # update graph view
        self._graph_view.clearSelection()
        agent_ctrl.scene_item.setSelected(True)
        # update tree view
        self.ui.treeProjectStructure.setCurrentItem(agent_ctrl.tree_item)
        # update agent view
        self.ui.treeProperties.clear()
        item_type = QtWidgets.QTreeWidgetItem(self.ui.treeProperties, [
            "Type", agent_ctrl.type])
        item_type.setBackgroundColor(1, agent_ctrl.svg_color)
        QtWidgets.QTreeWidgetItem(self.ui.treeProperties, [
                                  "ID", agent_ctrl.id_str])
        for f in agent_ctrl.field_list:
            PropertyTreeItem(self.ui.treeProperties, f.name, str(f.value))

        # unblock signals
        self.ui.treeProjectStructure.blockSignals(False)
        self._graph_view.blockSignals(False)

    def _filter_pattern_changed(self):
        pattern = self.ui.lineFilterPattern.text().lower()
        for a in self._scenario_ctrl.agent_list:
            hide = (a.type.lower().find(pattern) == -1)
            a.tree_item.setHidden(hide)

    def _tree_item_parent_for_agent(self, agent_ctrl) -> QtWidgets.QTreeWidgetItem:
        # return existing if it already exists
        if agent_ctrl.type in self._tree_items_for_agent_types:
            return self._tree_items_for_agent_types[agent_ctrl.type]
        item = QtWidgets.QTreeWidgetItem(
            self.ui.treeProjectStructure, [agent_ctrl.type])
        item.setExpanded(True)
        item.setBackgroundColor(0, agent_ctrl.svg_color)
        self._tree_items_for_agent_types[agent_ctrl.type] = item
        return item

    def _create_agent_tree_item(self, agent_ctrl: AgentController):
        parent_item = self._tree_item_parent_for_agent(agent_ctrl)
        # create tree item
        item = QtWidgets.QTreeWidgetItem(parent_item, [agent_ctrl.id_str])
        item.setBackgroundColor(0, agent_ctrl.svg_color)
        item.setData(0, QtCore.Qt.UserRole, agent_ctrl.id)
        item.setToolTip(0, agent_ctrl.tooltip_text)
        # add item
        agent_ctrl.tree_item = item
        self.ui.treeProjectStructure.addTopLevelItem(item)

    def _on_agent_added(self, agent_ctrl: AgentController):
        self._graph_view.add_agent(agent_ctrl)
        self._create_agent_tree_item(agent_ctrl)

    def _on_contract_added(self, sender: AgentController, receiver: AgentController, contract: models.Contract):
        # update scene graph
        self._graph_view.add_contract(sender, receiver)
        # update tree view
        sender_tree_item = QtWidgets.QTreeWidgetItem(
            sender.tree_item, ["{} ({})".format(receiver.id_str, contract.product_name)])
        sender_tree_item.setIcon(0, QtGui.QIcon(u":/icons/16px-login.png"))
        receiver_tree_item = QtWidgets.QTreeWidgetItem(
            receiver.tree_item, ["{} ({})".format(sender.id_str, contract.product_name)])
        receiver_tree_item.setIcon(0, QtGui.QIcon(u":/icons/16px-logout.png"))

    def _confirm_current_project_can_be_closed(self) -> bool:
        if self._scenario_ctrl.has_unsaved_changes:
            choice = QtWidgets.QMessageBox.warning(
                self,
                self.tr("Modifications will be lost"),
                self.tr("Modifications done to the current scenario have not been saved. You will loose them if you continue!\n\nDo you want to discard unsaved changes?"),
                QtWidgets.QMessageBox.StandardButtons(
                    QtWidgets.QMessageBox.Yes | QtWidgets.QMessageBox.No),
                QtWidgets.QMessageBox.No
            )
            if choice != QtWidgets.QMessageBox.Yes:
                return False
        return True

    def _on_project_closed(self):
        self._graph_view.clear()
        # reset zoom
        self.ui.sliderZoomFactor.setValue(50)
        # reset properties
        self._tree_items_for_agent_types = {}
        # reset scenario
        self._scenario_ctrl.reset()
        # reset ui
        self.ui.treeProjectStructure.clear()
        self.ui.treeProperties.clear()
        self.ui.lineFilterPattern.clear()
        self.ui.labelProjectName.clear()

    def new_project(self):
        if not self._confirm_current_project_can_be_closed():
            return
        self._scenario_ctrl.reset()
        self._on_project_closed()
        self._scenario_ctrl.create_new_scenario()

    def save_project(self):
        if not self._scenario_ctrl.has_scenario_data:
            return
        self._do_save_project_as(self._scenario_ctrl.file_path)

    def save_project_as(self):
        if not self._scenario_ctrl.has_scenario_data:
            return
        self._do_save_project_as("")

    def _do_save_project_as(self, file_path: str):
        assert self._scenario_ctrl.has_scenario_data

        if file_path == "":
            file_path, _ = QtWidgets.QFileDialog.getSaveFileName(
                self,
                self.tr("Save scenario file"),
                "",
                "Scenario file (*.yaml *.yml)")
            if file_path == "":
                return

        try:
            self._scenario_ctrl.save_to_file(file_path)
        except Exception as e:
            logging.error(e)
            msg = "Error: {}.".format(e)
            if e.__cause__:
                msg += "\n\nDetails: {}".format(e.__cause__)
            title = "{}".format(type(e).__name__)
            QtWidgets.QMessageBox.critical(self, title, msg)

    def close_project(self) -> bool:
        if not self._confirm_current_project_can_be_closed():
            return
        self._on_project_closed()

    def show_open_scenario_file_dlg(self):
        if not self._confirm_current_project_can_be_closed():
            return

        file_path, _ = QtWidgets.QFileDialog.getOpenFileName(
            self,
            self.tr("Open scenario file"),
            "",
            "Scenario file (*.yaml *.yml)")
        if file_path != "":
            self.load_scenario_file(file_path)

    def _enable_views(self, enabled):
        self.ui.treeProjectStructure.setEnabled(enabled)
        self.ui.treeProperties.setEnabled(enabled)
        self.ui.lineFilterPattern.setEnabled(enabled)
        self.ui.graphicsView.setEnabled(enabled)

    def load_scenario_file(self, file_path):
        try:
            self._on_project_closed()
            self._scenario_ctrl.load_file(file_path)
        except Exception as e:
            logging.error(e)
            msg = "Error: {}.".format(e)
            if e.__cause__:
                msg += "\n\nDetails: {}".format(e.__cause__)
            title = "{}".format(type(e).__name__)
            QtWidgets.QMessageBox.critical(self, title, msg)
            self._on_project_closed()

    # prevent data loss when closing the main window
    def closeEvent(self, event):
        if not self._confirm_current_project_can_be_closed():
            event.ignore()
        else:
            event.accept()
