# Copyright (c) 2015 Shotgun Software Inc.
# 
# CONFIDENTIAL AND PROPRIETARY
# 
# This work is provided "AS IS" and subject to the Shotgun Pipeline Toolkit 
# Source Code License included in this distribution package. See LICENSE.
# By accessing, using, copying or modifying this work you indicate your 
# agreement to the Shotgun Pipeline Toolkit Source Code License. All rights 
# not expressly granted therein are reserved by Shotgun Software Inc.

import sgtk
from sgtk.platform.qt import QtCore, QtGui


class SearchWidget(QtGui.QWidget):
    """
    Small search box widget, similar to the one appearing when you click
    CMD+f in chrome. This widget is typically parented with a QView of some 
    sort, and when enable() is called, it will appear, overlayed on top of the
    parent widget, in the top right corner. It has a text field where a search
    input can be entered.
    
    You can connect to the filter_changed signal to get notified whenever the search
    string is changed.
    """

    # signal emitted whenever the search filter changes
    filter_changed = QtCore.Signal(str)
    
    def __init__(self, view, parent):
        """
        Constructor
        
        :param parent: QT parent object
        """
        QtGui.QWidget.__init__(self, parent)
        self.view = view

        # Setup UI
        self.__setup_ui()

        # set up signals and slots
        self.search.textChanged.connect(self._on_filter_changed)

    def __setup_ui(self):
        """Setup UI of search widget"""
        hlayout = QtGui.QHBoxLayout()
        hlayout.setContentsMargins(0, 0, 0, 0)

        self.search = QtGui.QLineEdit(self.parent())
        self.search.setStyleSheet("QLineEdit{ border-width: 1px; "
                                             "background-image: url(:/res/search.png);"
                                             "background-repeat: no-repeat;"
                                             "background-position: center left;"
                                             "border-radius: 5px; "
                                             "padding-left:20px;"
                                             "margin:4px;"
                                             "height:22px;"
                                             "}")
        self.search.setToolTip("Enter some text to filter the publishes shown in the view below.<br>\n"
                               "Click the magnifying glass icon above to disable the filter.")
        try:
            # this was introduced in qt 4.7, so try to use it if we can... :)
            self.search.setPlaceholderText("Search...")
        except:
            pass

        clear_search = QtGui.QToolButton(self.parent())
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap(":/res/clear_search.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        clear_search.setIcon(icon)
        clear_search.setAutoRaise(True)
        clear_search.clicked.connect(lambda _: self.search.setText(""))
        clear_search.setToolTip("Click to clear your current search.")

        hlayout.addWidget(self.search)
        hlayout.addWidget(clear_search)

        self.setLayout(hlayout)

    def _on_filter_changed(self):
        """Callback for when the text changes"""
        if self.isVisible():
            # emit the search text that is in the view
            search_text = self.search.text()
        else:
            # widget is hidden - emit empty search text
            search_text = ""

        # Get view class
        view_class = self.view.__class__.__name__

        if search_text and len(search_text) > 0:
            # indicate with a blue border that a search is active
            self.view.setStyleSheet("""%s { border-width: 3px;
                                                   border-style: solid;
                                                   border-color: #2C93E2; }
                                       %s::item { padding: 6px; }
                                    """ % (view_class, view_class))
            # expand all nodes in the tree
            if isinstance(self.view, QtGui.QTreeView):
                self.view.expandAll()
        else:
            # revert to default style sheet
            self.view.setStyleSheet("%s::item { padding: 6px; }" % view_class)

        # emit our custom signal
        self.filter_changed.emit(search_text)


