import os
import json

from kabaret import flow
from .maputils import CreateGenericItemAction, ClearMapAction


class UserStatus(flow.values.ChoiceValue):

    CHOICES = ["User", "Admin", "Supervisor"]


class AddUserAction(flow.Action):

    ICON = ("icons.gui", "plus-sign-in-a-black-circle")

    _users = flow.Parent()

    id = flow.Param("").ui(label="ID")
    status = flow.Param("User", UserStatus)

    def get_buttons(self):
        return ["Add", "Cancel"]

    def run(self, button):
        if button == "Cancel":
            return

        user = self._users.add(self.id.get())
        user.status.set(self.status.get())

        self._users.touch()


class User(flow.Object):

    ICON = ("icons.gui", "user")

    status = flow.Param("User", UserStatus)


class Users(flow.Map):

    ICON = ("icons.gui", "team")

    add_user = flow.Child(AddUserAction)
    clear_map = flow.Child(ClearMapAction)

    @classmethod
    def mapped_type(cls):
        return User

    def columns(self):
        return ["ID", "Status"]

    def is_admin(self, username):
        user = self.get_mapped(username)
        return user.status.get() == "Admin"

    def _fill_row_cells(self, row, item):
        row["ID"] = item.name()
        row["Status"] = item.status.get()


class AddEnvVarAction(flow.Action):

    _env = flow.Parent()

    var_name = flow.Param("").ui(label="Name")
    var_value = flow.Param("").ui(label="Value")

    def get_buttons(self):
        return ["Add", "Cancel"]

    def run(self, button):
        if button == "Cancel":
            return

        if self.var_name.get() == "":
            self.message.get("<font color=#D50055>Variable name can't be empty</font>")
            return self.get_result(close=False)

        env_path = self._env.file_path()

        try:
            f = open(env_path, "r")
        except IOError:
            f = open(env_path, "w")
            env = {self.var_name.get(): self.var_value.get()}
        else:
            try:
                env = json.load(f)
            except json.decoder.JSONDecodeError:
                env = {self.var_name.get(): self.var_value.get()}
            else:
                env[self.var_name.get()] = self.var_value.get()

            f = open(env_path, "w")

        json.dump(env, f, indent=4, sort_keys=True)
        f.close()

        os.environ[self.var_name.get()] = self.var_value.get()
        self._env.touch()


class ChangeEnvVarValueAction(flow.Action):

    _var = flow.Parent()
    _env = flow.Parent(2)

    var_value = flow.Param().ui(label="Value")

    def get_buttons(self):
        return ["Confirm", "Cancel"]

    def run(self, button):
        if button == "Cancel":
            return

        env_path = self._env.file_path()

        try:
            f = open(env_path, "r")
        except IOError:
            return

        env = json.load(f)
        env[self._var.name()] = self.var_value.get()

        f = open(env_path, "w")
        json.dump(env, f, indent=4, sort_keys=True)
        f.close()

        self._var.set(self.var_value.get())
        self._var.update()


class EnvVar(flow.values.SessionValue):

    change_value = flow.Child(ChangeEnvVarValueAction)

    def update(self):
        os.environ[self.name()] = self.get()


class UserEnvironment(flow.DynamicMap):

    add_variable = flow.Child(AddEnvVarAction)

    @classmethod
    def mapped_type(cls):
        return EnvVar

    def mapped_names(self, page_num=0, page_size=None):
        try:
            f = open(self.file_path(), "r")
        except IOError:
            return []

        try:
            env = json.load(f)
        except json.decoder.JSONDecodeError:
            # Invalid JSON object
            return []

        return env.keys()

    def file_path(self):
        return "%s/env.json" % self.root().project().get_user_folder()

    def _configure_child(self, child):
        with open(self.file_path(), "r") as f:
            env = json.load(f)
            child.set(env[child.name()])

    def update(self):
        for var in self.mapped_items():
            var.update()

    def columns(self):
        return ["Variable", "Value"]

    def _fill_row_cells(self, row, item):
        row["Variable"] = item.name()
        row["Value"] = item.get()

    def _fill_row_style(self, style, item, row):
        style["activate_oid"] = item.change_value.oid()


class ToggleBookmarkAction(flow.Action):

    _obj = flow.Parent()

    def needs_dialog(self):
        return False

    def allow_context(self, context):
        return context and context.endswith(".details")

    def get_bookmarks(self):
        return self.root().project().admin.bookmarks.user_bookmarks

    def is_bookmarked(self):
        return self.get_bookmarks().has_bookmark(self._obj.oid())

    def run(self, button):
        bookmarks = self.get_bookmarks()

        if self.is_bookmarked():
            self.root().session().log_debug("Remove %s to bookmarks" % self._obj.oid())
            bookmarks.remove(self._obj.oid())
        else:
            self.root().session().log_debug("Add %s to bookmarks" % self._obj.oid())
            bookmarks.add(self._obj.oid())

        bookmarks.touch()
        return self.get_result(refresh=True)

    def _fill_ui(self, ui):
        ui["label"] = ""

        if self.is_bookmarked():
            ui["icon"] = ("icons.gui", "star")
        else:
            ui["icon"] = ("icons.gui", "star-1")


class GotoBookmarkAction(flow.Action):

    _bookmark = flow.Parent()

    def needs_dialog(self):
        return False

    def run(self, button):
        return self.get_result(goto=self._bookmark.get())


class RemoveFromBookmark(flow.Action):

    _bookmark = flow.Parent()
    _bookmarks = flow.Parent(2)

    def needs_dialog(self):
        return False

    def run(self, button):
        self._bookmarks.remove(self._bookmark.get())
        self._bookmarks.touch()


class Bookmark(flow.values.Value):

    remove = flow.Child(RemoveFromBookmark)
    goto = flow.Child(GotoBookmarkAction)


class UserBookmarks(flow.DynamicMap):
    def mapped_names(self, page_num=0, page_size=None):
        try:
            f = open(self.file_path(), "r")
        except IOError:
            return []

        try:
            bookmarks = json.load(f)
        except json.decoder.JSONDecodeError:
            # Invalid JSON object
            return []

        return bookmarks.keys()

    def file_path(self):
        return "%s/bookmarks.json" % self.root().project().get_user_folder()

    def _configure_child(self, child):
        with open(self.file_path(), "r") as f:
            bookmarks = json.load(f)
            child.set(bookmarks[child.name()])

    @classmethod
    def mapped_type(cls):
        return flow.injection.injectable(Bookmark)

    def columns(self):
        return ["Bookmark"]

    def _fill_row_cells(self, row, item):
        oid = item.get()
        objects = (
            self.root()
            .session()
            .cmds.Flow.split_oid(oid, up_to_oid=self.root().project().oid())
        )
        object_names = [obj[0].split(":")[-1] for obj in objects]

        row["Bookmark"] = " > ".join(object_names)

    def _fill_row_style(self, style, item, row):
        style["activate_oid"] = item.goto.oid()

    def has_bookmark(self, oid):
        return oid in [bookmark.get() for bookmark in self.mapped_items()]

    def add(self, oid):
        name = oid[1:].replace("/", "_")

        file_path = self.file_path()

        try:
            f = open(file_path, "r")
        except IOError:
            f = open(file_path, "w")
            bookmarks = {name: oid}
        else:
            try:
                bookmarks = json.load(f)
            except json.decoder.JSONDecodeError:
                bookmarks = {name: oid}
            else:
                bookmarks[name] = oid

            f = open(file_path, "w")

        json.dump(bookmarks, f, indent=4, sort_keys=True)
        f.close()

        self.touch()

    def remove(self, oid):
        name = oid[1:]
        name = name.replace("/", "_")

        file_path = self.file_path()

        try:
            f = open(file_path, "r")
        except IOError:
            # No bookmark saved
            return
        else:
            try:
                bookmarks = json.load(f)
            except json.decoder.JSONDecodeError:
                # No bookmark saved
                return

            bookmarks.pop(name, None)
            f = open(file_path, "w")

        json.dump(bookmarks, f, indent=4, sort_keys=True)
        f.close()

        self.touch()
