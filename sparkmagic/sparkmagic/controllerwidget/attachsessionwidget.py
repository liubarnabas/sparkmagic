# Copyright (c) 2015  aggftw@gmail.com
# Distributed under the terms of the Modified BSD License.
from sparkmagic.controllerwidget.abstractmenuwidget import AbstractMenuWidget


class AttachSessionWidget(AbstractMenuWidget):
    def __init__(self, spark_controller, ipywidget_factory, ipython_display,endpoints, refresh_method):
        # This is nested
        super(AttachSessionWidget, self).__init__(spark_controller, ipywidget_factory, ipython_display, True)
        self.endpoints = endpoints

        self.refresh_method = refresh_method

        self.children = self.get_existing_session_widgets()

        for child in self.children:
            child.parent_widget = self

    def run(self):
        self.refresh_method()

    def get_existing_session_widgets(self):
        session_widgets = []
        session_widgets.append(self.ipywidget_factory.get_html(value="<br>", width="600px"))
        attached_session = self.spark_controller.get_attached_session()
        attached = "no"
        for url, endpoint in self.endpoints.items():
            all_sessions = self.spark_controller.get_all_sessions_endpoint(endpoint)
            if all_sessions is not None:
                # Header
                header = self.get_session_widget("Url","Id", "Kind", "State","attached", endpoint,False)
                session_widgets.append(header)
                session_widgets.append(self.ipywidget_factory.get_html(value="<br>", width="600px"))
    
                # Sessions
                for session in all_sessions:
                    if attached_session != None and attached_session.id == session.id:   
                        attached = "yes"
                    session_widgets.append(self.get_session_widget( url , session.id, session.kind, session.status,attached,endpoint))
    
                session_widgets.append(self.ipywidget_factory.get_html(value="<br>", width="600px"))
            else:
                session_widgets.append(self.ipywidget_factory.get_html(value="No sessions yet.", width="600px"))

        return session_widgets

    def get_session_widget(self, url, session_id, kind, state,attached,endpoint, button=True):
        hbox = self.ipywidget_factory.get_hbox()
        endpoint_w = self.ipywidget_factory.get_html(url, width="300px", padding="4px")
        id_w = self.ipywidget_factory.get_html(value=str(session_id), width="100px", padding="4px")
        kind_w = self.ipywidget_factory.get_html(value=kind, width="100px", padding="4px")
        state_w = self.ipywidget_factory.get_html(value=state, width="100px", padding="4px")
        attached_w = self.ipywidget_factory.get_html(value=attached, width="100px", padding="4px")
        
        if button:
            def attach_on_click(button):
                self.spark_controller.attach_session_by_id(endpoint,session_id)
                self.refresh_method()

            attach_w = self.ipywidget_factory.get_button(description="Attach")
            attach_w.on_click(attach_on_click)
        else:
            attach_w = self.ipywidget_factory.get_html(value="", width="100px", padding="4px")

        hbox.children = [endpoint_w,id_w, kind_w, state_w,attached_w, attach_w]

        return hbox
