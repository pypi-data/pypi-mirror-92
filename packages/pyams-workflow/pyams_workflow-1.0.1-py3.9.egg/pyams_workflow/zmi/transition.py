#
# Copyright (c) 2015-2021 Thierry Florac <tflorac AT ulthar.net>
# All Rights Reserved.
#
# This software is subject to the provisions of the Zope Public License,
# Version 2.1 (ZPL).  A copy of the ZPL should accompany this distribution.
# THIS SOFTWARE IS PROVIDED "AS IS" AND ANY AND ALL EXPRESS OR IMPLIED
# WARRANTIES ARE DISCLAIMED, INCLUDING, BUT NOT LIMITED TO, THE IMPLIED
# WARRANTIES OF TITLE, MERCHANTABILITY, AGAINST INFRINGEMENT, AND FITNESS
# FOR A PARTICULAR PURPOSE.
#

"""PyAMS_workflow.zmi.transition module

This module defines a base transition form.
"""

from pyramid.decorator import reify
from zope.lifecycleevent import ObjectModifiedEvent

from pyams_form.ajax import ajax_form_config
from pyams_form.field import Fields
from pyams_form.interfaces import HIDDEN_MODE
from pyams_form.interfaces.form import IAJAXFormRenderer
from pyams_layer.interfaces import IPyAMSLayer
from pyams_utils.adapter import ContextRequestViewAdapter, adapter_config
from pyams_utils.registry import query_utility
from pyams_utils.traversing import get_parent
from pyams_utils.url import absolute_url
from pyams_workflow.interfaces import IWorkflow, IWorkflowCommentInfo, IWorkflowInfo, \
    IWorkflowManagedContent, \
    IWorkflowState, IWorkflowTransitionInfo, IWorkflowVersion
from pyams_zmi.form import AdminModalAddForm
from pyams_zmi.interfaces import IAdminLayer

__docformat__ = 'restructuredtext'


@ajax_form_config(name='wf-transition.html', context=IWorkflowVersion, layer=IPyAMSLayer)
class WorkflowContentTransitionForm(AdminModalAddForm):
    # pylint: disable=abstract-method
    """Workflow content transition form"""

    prefix = 'workflow.'

    @reify
    def transition(self):
        """Transition property getter"""
        parent = get_parent(self.context, IWorkflowManagedContent)
        workflow = query_utility(IWorkflow, name=parent.workflow_name)
        return workflow.get_transition_by_id(
            self.request.params.get('workflow.widgets.transition_id'))

    @property
    def legend(self):
        """Legend getter"""
        return self.request.localizer.translate(self.transition.title)

    fields = Fields(IWorkflowTransitionInfo) + \
        Fields(IWorkflowCommentInfo)

    @property
    def edit_permission(self):
        return self.transition.permission

    def update_widgets(self, prefix=None):
        super().update_widgets(prefix)
        transition_id = self.widgets.get('transition_id')
        if transition_id is not None:
            transition_id.mode = HIDDEN_MODE
            transition_id.value = transition_id.extract()

    def create_and_add(self, data):
        data = data.get(self, {})
        info = IWorkflowInfo(self.context)
        info.fire_transition(self.transition.transition_id, comment=data.get('comment'))
        info.fire_automatic()
        IWorkflowState(self.context).state_urgency = data.get('urgent_request') or False
        self.request.registry.notify(ObjectModifiedEvent(self.context))
        return info

    def next_url(self):
        return absolute_url(self.context, self.request, 'summary.html')


@adapter_config(required=(IWorkflowVersion, IAdminLayer, WorkflowContentTransitionForm),
                provides=IAJAXFormRenderer)
class WorkflowContentTransitionFormRenderer(ContextRequestViewAdapter):
    """Workflow content transition form AJAX renderer"""

    def render(self, changes):  # pylint: disable=no-self-use
        """Form changes renderer"""
        if not changes:
            return None
        return {
            'status': 'reload'
        }
