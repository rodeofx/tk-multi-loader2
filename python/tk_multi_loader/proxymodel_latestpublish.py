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

from .model_latestpublish import SgLatestPublishModel

shotgun_model = sgtk.platform.import_framework("tk-framework-shotgunutils", "shotgun_model")

class SgLatestPublishProxyModel(QtGui.QSortFilterProxyModel):
    """
    Filter model to be used in conjunction with SgLatestPublishModel
    """
    
    # signal which is emitted whenever a filter changes
    filter_changed = QtCore.Signal()
    
    def __init__(self, parent):
        QtGui.QSortFilterProxyModel.__init__(self, parent)
        self._valid_type_ids = None
        self._show_folders = True
        self._valid_statuses = None
        self._search_filter = ""
        
    def set_search_query(self, search_filter):
        """
        Specify a filter to use for searching
        
        :param search_filter: search filter string
        """
        self._search_filter = search_filter
        self.invalidateFilter()
        self.filter_changed.emit()
        
    def set_filter_by_type_ids(self, type_ids, show_folders):
        """
        Specify which type ids the publish model should allow through
        """
        self._valid_type_ids = type_ids
        self._show_folders = show_folders
        # tell model to repush data
        self.invalidateFilter()
        self.filter_changed.emit()

    def set_filter_by_status(self, statuses):
        self._valid_statuses = statuses.split(' (')[0]
        self.invalidateFilter()
        self.filter_changed.emit()

        
    def filterAcceptsRow(self, source_row, source_parent_idx):
        """
        Overridden from base class.
        
        This will check each row as it is passing through the proxy
        model and see if we should let it pass or not.    
        """
        # get the search filter, as specified via setFilterFixedString()
        search_exp = self.filterRegExp()
        search_exp.setCaseSensitivity(QtCore.Qt.CaseInsensitive)

        model = self.sourceModel()
        
        current_item = model.invisibleRootItem().child(source_row)  # assume non-tree structure
        sg_data = current_item.get_sg_data()
        publish_name = ''
        if sg_data:
            publish_name = sg_data.get('name')
            publish_status = sg_data.get('sg_status_list')
        
        # first analyze any search filtering
        if self._search_filter:
            
            # there is a search filter entered
            field_data = shotgun_model.get_sanitized_data(current_item, SgLatestPublishModel.SEARCHABLE_NAME)
                        
            # all input we are getting from pyside is as unicode objects
            # all data from shotgun is utf-8. By converting to utf-8,
            # filtering on items containing unicode text also work.
            search_str = self._search_filter.encode("UTF-8") 
            
            if search_str.lower() not in field_data.lower(): 
                # item text is not matching search filter
                return False

        is_folder = current_item.data(SgLatestPublishModel.IS_FOLDER_ROLE)

        # See if status matches
        if self._valid_statuses not in (None, 'All'):
            if publish_status != self._valid_statuses:
                return False

        if self._valid_type_ids is None:
            # accept all!
            return True
        
        # now check if folders should be shown
        is_folder = current_item.data(SgLatestPublishModel.IS_FOLDER_ROLE)
        if is_folder:
            return self._show_folders
            
        # lastly, check out type filter checkboxes
        sg_type_id = current_item.data(SgLatestPublishModel.TYPE_ID_ROLE) 
        
        if sg_type_id is None:
            # no type. So always show.
            return True
        elif sg_type_id in self._valid_type_ids:
            return True
        else:
            # get the type id
            sg_type_id = current_item.data(SgLatestPublishModel.TYPE_ID_ROLE) 
            
            # print publish_name, search_exp.indexIn(publish_name)
            if sg_type_id is None:
                # no type. So always show.
                return True
            elif sg_type_id in self._valid_type_ids and search_exp.indexIn(publish_name) != -1:
                return True
            else:
                return False
