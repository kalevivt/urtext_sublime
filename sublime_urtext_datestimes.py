# Module to handle reverse dating of filenames

import sublime
import sublime_plugin
import datetime
import urtext
import os
import time
import sublime_urtext
import urtext.datestimes


# = 12 dashes in a row starting a line, followed by a newline

def meta_separator():
    settings = sublime.load_settings('urtext-default.sublime-settings')
    meta_separator = settings.get('meta_separator') 
    return meta_separator

class ShowReverseDateFilenameCommand(sublime_plugin.TextCommand):
    """
    Takes the timestamp-formatted date highlighted and converts it into a reverse-dated
    filename which is copied to the clipboard. For file naming.
    """
    def run(self, edit):
        for region in self.view.sel():
            text = self.view.substr(region)
            try:
                
                date = datetime.datetime.strptime(text, urtext.datestimes.timestamp_format)
                sublime.set_clipboard(make_reverse_date_filename(date))
                self.view.show_popup(
                    'Reverse-dated filename copied to clipboard.')
            except:
                self.view.show_popup('Error.')


class UpdateFileCommand(sublime_plugin.TextCommand):
    """ copies the file to a new node with a backreference."""
    def run(self, edit):
        contents = self.view.substr(sublime.Region(0, self.view.size()))
        self.contents = Urtext.meta.clear_meta(contents)
        old_filename = self.view.file_name()
        self.old_filename = old_filename.split('/')[-1]
        now = datetime.datetime.now()
        new_filename = urtext.datestimes.make_reverse_date_filename(now)+'.txt'
        self.view.insert(edit, self.view.size(), '\npulled to: -> '+new_filename +
                         '  | (editorial://open/'+new_filename+'?root=dropbox) ' + now.strftime(timestamp_format))
        self.view.run_command('save')
        window = self.view.window()
        new_view = window.open_file(new_filename)
        sublime.set_timeout(lambda: self.add_content(new_view), 10)

    # https://forum.sublimetext.com/t/wait-until-is-loading-finnish/12062/5
    def add_content(self, view):
        if not view.is_loading():
            view.run_command("insert_snippet", {"contents": self.contents})
            now = datetime.datetime.now()
            Urtext.meta.add_created_timestamp(view, now)
            view.run_command("move_to", {"to": "eof"})
            view.run_command("insert_snippet", {
                             "contents": "pulled from: -> "+self.old_filename + " | (editorial://open/"+self.old_filename+"?root=dropbox)"})
            view.run_command("move_to", {"to": "bof"})
            view.run_command('save')
        else:
            sublime.set_timeout(lambda: self.add_content(view), 10)


class NewNodeCommand(sublime_plugin.WindowCommand):
    """
    Creates a new file with reverse-dated filename and initial metadata
    """
    def run(self):
        sublime_urtext.refresh_nodes(self.window)
        self.path = sublime_urtext._UrtextProject.path
        filename = sublime_urtext._UrtextProject.add(datetime.datetime.now())
        new_view = self.window.open_file(os.path.join(self.path, filename))
 
class ReFile(sublime_plugin.TextCommand):
    def run(self, edit):
        now = datetime.datetime.now()
