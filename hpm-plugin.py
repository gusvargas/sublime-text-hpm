import sublime_plugin
import threading
import subprocess
import os

class HpmInstallCommand(sublime_plugin.WindowCommand):
  def run(self):
    window = self.window
    window.show_input_panel("Package:", '',
      lambda s: self.install_package(s), None, None)

  def install_package(self, package):
    command = 'hpm install %s' % package
    thread = CommandThread(command.split(' '))
    thread.start()

    while thread.is_alive():
      pass

    focus_all_views(self.window)


class HpmRequireCommand(sublime_plugin.WindowCommand):
  def run(self):
    window = self.window
    window.show_input_panel("Package:", '',
      lambda s: self.require_package(s), None, None)

  def require_package(self, package):
    file_name = self.window.active_view().file_name()
    command = 'hpm require %s %s' % (package, file_name)
    thread = CommandThread(command.split(' '))
    thread.start()

    while thread.is_alive():
      pass

    focus_all_views(self.window)


class HpmDocsCommand(sublime_plugin.WindowCommand):
  def run(self):
    window = self.window
    window.show_input_panel("Package:", '',
      lambda s: self.open_docs(s), None, None)

  def open_docs(self, package):
    command = 'hpm docs %s' % package
    CommandThread(command.split(' ')).start()


class CommandThread(threading.Thread):
  def __init__(self, command):
    self.command = command
    threading.Thread.__init__(self)

  def run(self):
    subprocess.Popen(self.command, cwd=os.getcwd())


def focus_all_views(window):
  current_view = window.active_view()
  gr_number = window.num_groups()

  for i in range(0, gr_number):
      window.focus_group(i)
      views_in_i = window.views_in_group(i)
      for inner_view in views_in_i:
         window.focus_view(inner_view)

  window.focus_view(current_view)
