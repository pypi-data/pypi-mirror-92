import os
import json
import gazu
import getpass
import pathlib

from kabaret import flow
from kabaret.app.ui.gui.widgets.flow.flow_view import (
    CustomPageWidget,
    QtWidgets,
    QtCore,
)
from kabaret.app.ui.gui.widgets.editors import editor_factory
from kabaret.flow_contextual_dict import ContextualView, get_contextual_dict
from kabaret.subprocess_manager.runners import Explorer

from .users import Users, UserEnvironment, UserBookmarks
from .film import Sequences
from .lib import Assets
from .runners import (
    Krita,
    Blender,
    VSCodium,
    NotepadPP,
    Firefox,
    DefaultEditor,
    DefaultRunners,
)
from .kitsu import KitsuProject
from .site import Sites, Site, Synchronize, MinioFileUploader, MinioFileDownloader


class LoginPageWidget(CustomPageWidget):
    def build(self):
        # Get project root oid
        self.project_oid = self.session.cmds.Flow.split_oid(self.oid)[0][1]

        # Build UI
        self.label = QtWidgets.QLabel(self)
        self.label.setText("<h2>Connexion page</h2>")
        self.error_label = QtWidgets.QLabel(self)
        self.error_label.setText("")

        # Set server url to login page param value
        self.server_url_oid = self.oid + "/admin/login_page/kitsu_server_url"
        self.lineedit_server_url = QtWidgets.QLineEdit(
            self.session.cmds.Flow.get_value(self.server_url_oid)
        )

        self.lineedit_username = QtWidgets.QLineEdit()
        self.lineedit_password = QtWidgets.QLineEdit()
        self.button_login = QtWidgets.QPushButton("Log in")
        self.button_login.setMinimumWidth(100)

        # Set password field input mode
        self.lineedit_password.setEchoMode(QtWidgets.QLineEdit.Password)
        self.lineedit_password.setInputMethodHints(
            QtCore.Qt.ImhHiddenText
            | QtCore.Qt.ImhNoPredictiveText
            | QtCore.Qt.ImhNoAutoUppercase
        )

        grid_layout = QtWidgets.QGridLayout()
        grid_layout.addWidget(self.label, 0, 0)
        grid_layout.addWidget(self.lineedit_server_url, 1, 0, 1, 2)
        grid_layout.addWidget(self.lineedit_username, 2, 0, 1, 2)
        grid_layout.addWidget(self.lineedit_password, 3, 0, 1, 2)
        grid_layout.addWidget(self.error_label, 4, 0)
        grid_layout.addWidget(self.button_login, 4, 1)
        grid_layout.setColumnStretch(0, 1)

        self.setLayout(grid_layout)

        self.button_login.clicked.connect(self.on_button_login_clicked)

    def on_button_login_clicked(self):
        server_url = self.lineedit_server_url.text()
        valid_host = self.session.cmds.Flow.call(
            self.project_oid, "update_kitsu_host", args={server_url}, kwargs={}
        )

        if not valid_host:
            self.error_label.setText("<font color=#C71B1F>Invalid server url</font>")
            return

        # Save valid server url in login page Param for next connections
        self.session.cmds.Flow.set_value(self.server_url_oid, server_url)

        username = self.lineedit_username.text()
        password = self.lineedit_password.text()
        logged_in = self.session.cmds.Flow.call(
            self.project_oid,
            "log_in",
            args={},
            kwargs={"username": username, "password": password},
        )

        if not logged_in:
            self.error_label.setText(
                "<font color=#C71B1F>Login failed... \
                Check credentials !</font>"
            )
            return

        self.error_label.setText("")
        self.page.refresh()


class LoginPage(flow.Object):

    kitsu_server_url = flow.Param("")


class Bookmarks(flow.Object):

    goto_project = flow.Parent(2)
    user_bookmarks = flow.Child(UserBookmarks).ui(expanded=True, default_height=540)


class SynchronizeFilesResult(flow.Action):

    def allow_context(self, context):
        return False

    def get_buttons(self):
        return ["Close"]
    
    def run(self, button):
        return


class SynchronizeFiles(Synchronize):
    ICON = ("icons.libreflow", "sync_arrow")

    result = flow.Child(SynchronizeFilesResult)

    def needs_dialog(self):
        return True
    
    def get_buttons(self):
        self.message.set((
            "<h3><font color=#D66700>"
            "Synchronizing all requested files may freeze your session for a while."
            "</font></h3>"
        ))
        return ["Confirm", "Cancel"]

    def allow_context(self, context):
        return context and context.endswith(".details")
    
    def run(self, button):
        if button == "Cancel":
            return
        
        current_site = self.root().project().get_current_site()
        nb_waiting_jobs = len(current_site.queue.jobs(status="WAITING"))

        super(SynchronizeFiles, self).run(button)

        nb_processed_jobs = nb_waiting_jobs - len(current_site.queue.jobs(status="WAITING"))

        if nb_processed_jobs == nb_waiting_jobs:
            self.result.message.set((
                "<h3><font color=#029600>"
                "Synchronization successful !"
                "</font></h3>"
            ))
        else:
            self.result.message.set((
                "<h3><font color=#D66700>"
                f"Warning: {nb_processed_jobs}/{nb_waiting_jobs} files synchronized"
                "</font></h3>"
            ))
        return self.get_result(next_action=self.result.oid())


class Synchronization(flow.Object):
    ICON = ("icons.libreflow", "sync_arrow")
    
    _project = flow.Parent()
    synchronize_files = flow.Child(SynchronizeFiles)

    def summary(self):
        current_site = self._project.get_current_site()
        nb_waiting_jobs = len(current_site.queue.jobs(status="WAITING"))
        
        if nb_waiting_jobs > 0:
            return (
                "<font color=#D5000D><b>"
                f"{nb_waiting_jobs} job(s) waiting"
                "</b></font>"
            )


class Admin(flow.Object):

    ICON = ("icons.gui", "team-admin")

    current_site_name = flow.Computed(cached=True)
    root_dir = flow.Computed(cached=True)

    settings = flow.Child(ContextualView)  # .ui(hidden=True)
    users = flow.Child(Users)
    user_environment = flow.Child(UserEnvironment).ui(expanded=True)
    bookmarks = flow.Child(Bookmarks)

    default_applications = flow.Child(DefaultRunners).ui(expanded=True).injectable()
    enable_filesystem_operations = flow.BoolParam(True).ui(
        label="Enable file system operations",
        tooltip="Enable operations on the OS file system (creation, move, delete) \
                when manipulating flow elements.",
    )
    sites = flow.Child(Sites)
    process_jobs = flow.Child(Synchronize)
    login_page = flow.Child(LoginPage).ui(hidden=True)

    def compute_child_value(self, child_value):
        if child_value == self.root_dir:
            '''
            TODO : Override by site on multisite !
            '''
            root_dir = None
            if "ROOT_DIR" in os.environ:
                print("WARNING: ROOT_DIR was defined by the environement !")
                root_dir = os.environ["ROOT_DIR"]
            else:
                # Otherwise, get current site's root dir
                root_dir = self.sites[self.current_site_name.get()].root_folder.get()
            child_value.set(root_dir)
        elif child_value is self.current_site_name:
            site_name = None
            site_name_var = "KABARET_SITE_NAME"

            if site_name_var in os.environ:
                site_name = os.environ[site_name_var]
            else:
                cluster_name = os.environ["KABARET_CLUSTER_NAME"]

                if cluster_name in self.sites.mapped_names():
                    site_name = cluster_name
                else:
                    site_name = "default"
            child_value.set(site_name)


class Project(KitsuProject):

    asset_lib = flow.Child(Assets).ui(expanded=True)
    sequences = flow.Child(Sequences).ui(expanded=True)
    admin = flow.Child(Admin)
    synchronization = flow.Child(Synchronization).ui(expanded=True)

    _show_login_page = flow.Computed().ui(editor="bool")

    _RUNNERS_FACTORY = None

    def get_root(self, alternative=None):
        '''
        alternative can be used if root_dir.get() returns None
        '''
        root_dir = self.admin.root_dir.get()
        if root_dir is None and alternative != None:
            root_dir = alternative
        return root_dir

    def set_user(self, username):
        if self.get_user_folder() is not None:
            user_file = os.path.join(self.get_user_folder(), "user.json")

            with open(user_file, "w+") as f:
                user_config = dict(username=username)
                json.dump(user_config, f)

    def get_user(self):
        if "USER_NAME" in os.environ:
            return os.environ["USER_NAME"]
        
        user_file = os.path.join(self.get_user_folder(), "user.json")

        if os.path.exists(user_file):
            with open(user_file, "r") as f:
                user_config = json.load(f)
                return user_config["username"]

        return getpass.getuser()

    def get_current_site(self):
        """
        Returns the site within which the current
        session is beeing run.
        """
        return self.admin.sites[
            self.admin.current_site_name.get()
        ]
    
    def get_exchange_site(self):
        """
        Returns the first exchange site found in
        project's registered site list.
        """
        for site in self.admin.sites.mapped_items():
            if site.site_type.get() == "Exchange":
                return site

        return None

    def is_admin(self, username):
        try:
            return self.admin.users.is_admin(username)
        except flow.exceptions.MappedNameError:
            # Unregistered user not admin by default
            return False

    def compute_child_value(self, child_value):
        if child_value is self._show_login_page:
            valid_host = self.kitsu_api.host_is_valid()

            if not valid_host:
                logged_in = False
            else:
                logged_in = self.kitsu_api.current_user_logged_in()

            if not logged_in:
                try:
                    f = open("%s/kitsu_config.json" % self.get_user_folder(), "r")
                except IOError:
                    logged_in = False
                else:
                    kitsu_config = json.load(f)
                    self.kitsu_api.set_host(kitsu_config["kitsu_host"])
                    self.kitsu_api.set_tokens(kitsu_config["tokens"])

                    logged_in = self.kitsu_api.current_user_logged_in()

            child_value.set(not self.kitsu_api.host_is_valid() or not logged_in)
        else:
            super(Project, self).compute_child_value(child_value)

    def update_kitsu_host(self, server_url):
        self.kitsu_api.set_server_url(server_url)
        self.kitsu_api.set_host(server_url + "/api")

        return self.kitsu_api.host_is_valid()

    def log_in(self, username, password):
        success = self.kitsu_api.log_in(username, password)

        # Save authentification tokens
        if success:
            tokens = self.kitsu_api.get_tokens()
            kitsu_config = {}
            kitsu_config["tokens"] = tokens
            kitsu_config["kitsu_host"] = self.kitsu_api.get_host()

            user_folder = self.get_user_folder()
            if user_folder is not None:
                with open("%s/kitsu_config.json" % user_folder, "w+") as f:
                    json.dump(kitsu_config, f)

            # Set current user
            self.set_user(username)

        return success

    def get_contextual_view(self, context_name):
        if context_name == "settings":
            return self.admin.settings

    def get_default_contextual_edits(self, context_name):
        if context_name == "settings":
            return dict(
                PROJECT=self.name(),
                default_shot_layout_files="{sequence}_{shot}_layout.blend, {sequence}_{shot}_layout-movie.mov",
                default_shot_animation_files="{sequence}_{shot}_animation.blend, {sequence}_{shot}_animation-movie.mov, {sequence}_{shot}_animation-export.abc",
                default_asset_model_files="{asset_name}_model.blend, {asset_name}_model-movie.mov, {asset_name}_model-export.abc",
                default_asset_rig_files="{asset_name}_rig.blend, {asset_name}_rig-turnaround.mov",
                project_thumbnail="{ROOT_DIR}TECH/{PROJECT}_thumbnail.png",
            )

    def get_user_folder(self):
        '''
        DEPRECATED ! TO DELETE ? 
        '''
        return os.path.join(pathlib.Path.home(), ".libreflow")

    def get_project_thumbnail(self):
        contextual_dict = get_contextual_dict(self, "settings")
        contextual_dict["ROOT_DIR"] = self.get_root()
        if "project_thumbnail" not in contextual_dict:
            return None
        path = None

        try:
            path = contextual_dict["project_thumbnail"].format(**contextual_dict)
        except KeyError:
            return None

        if path and os.path.exists(path):
            return path
        else:
            return None

    def update_user_environment(self):
        self.admin.user_environment.update()

    def _register_runners(self):
        self._RUNNERS_FACTORY.ensure_runner_type(Blender)
        self._RUNNERS_FACTORY.ensure_runner_type(Krita)
        self._RUNNERS_FACTORY.ensure_runner_type(VSCodium)
        self._RUNNERS_FACTORY.ensure_runner_type(NotepadPP)
        self._RUNNERS_FACTORY.ensure_runner_type(Firefox)
        self._RUNNERS_FACTORY.ensure_runner_type(Explorer)
        self._RUNNERS_FACTORY.ensure_runner_type(MinioFileUploader)
        self._RUNNERS_FACTORY.ensure_runner_type(MinioFileDownloader)
        self._RUNNERS_FACTORY.ensure_runner_type(DefaultEditor)

    def ensure_runners_loaded(self):
        session = self.root().session()
        subprocess_manager = session.get_actor("SubprocessManager")

        if self._RUNNERS_FACTORY is None:
            self._RUNNERS_FACTORY = subprocess_manager.create_new_factory(
                "Libre Flow Tools"
            )
            self._register_runners()

        subprocess_manager.ensure_factory(self._RUNNERS_FACTORY)

    def get_factory(self):
        self.ensure_runners_loaded()
        return self._RUNNERS_FACTORY

    def _fill_ui(self, ui):
        if self._RUNNERS_FACTORY is None:
            self.ensure_runners_loaded()

        user_folder = self.get_user_folder()
        if user_folder is not None and not os.path.exists(user_folder):
            os.mkdir(user_folder)

        self.update_user_environment()

        if self._show_login_page.get():
            ui["custom_page"] = "libreflow.baseflow.LoginPageWidget"
