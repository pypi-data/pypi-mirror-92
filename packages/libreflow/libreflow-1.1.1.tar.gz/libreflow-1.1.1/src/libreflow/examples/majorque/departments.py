import os

from kabaret import flow
from kabaret.subprocess_manager.flow import RunAction
from kabaret.flow_contextual_dict import get_contextual_dict

from libreflow import baseflow


class Department(baseflow.departments.Department):
    _parent = flow.Parent(2)
    play_last_playblast = flow.Child(None)


class PlayLastBlastAction(baseflow.file.OpenWithDefaultApp):

    ICON = ("icons.gui", "youtube-logo")

    _parent = flow.Parent()

    def allow_context(self, context):
        return context and isinstance(self.get_parent(), Department)

    def get_buttons(self):
        self.message.set("")

        parent = self.get_parent()

        if not parent.files.has_mapped_name("preview"):
            self.message.set(
                "<font color=#D5000D>No <i>preview</i> folder in %s files</font>"
                % parent.name()
            )
            return ["Cancel"]

        if not self._files:
            self.message.set(
                "<font color=#D5000D>No playblast in <i>preview</i> folder.</font>"
            )
            return ["Cancel"]

    def get_parent(self):
        """
        Parent must be a Departement object or Bookmark object
        whose oid param refers to a Department.
        """
        if isinstance(self._parent, baseflow.users.Bookmark):
            return self.root().get_object(self._parent.get())
        else:
            return self._parent

    def needs_dialog(self):
        parent = self.get_parent()

        if not parent.files.has_mapped_name("preview"):
            return True

        contextual_dict = get_contextual_dict(parent, "settings", ["path"])
        preview_folder_path = os.path.join(
            self.root().project().get_root(), contextual_dict["path"], "preview"
        )
        files = os.listdir(preview_folder_path)
        files = map(lambda f: os.path.join(preview_folder_path, f), files)
        sort_func = lambda f: -os.path.getmtime(f)
        self._files = sorted(files, key=sort_func)

        return not bool(self._files)

    def extra_argv(self):
        return [self._playblast_path]

    def run(self, button):
        if button == "Cancel":
            return

        self._playblast_path = self._files[0]
        super(PlayLastBlastAction, self).run(button)


Department.play_last_playblast.set_related_type(PlayLastBlastAction)
