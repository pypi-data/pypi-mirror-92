"""Provides the MainFrame class."""

from pathlib import Path
from typing import Any, Dict

from attr import attrs

from earwax.mixins import DumpLoadMixin

try:
    import wx
    from synthizer import Context
except ModuleNotFoundError:
    from . import pretend_wx as wx
    Context = object

from earwax.cmd.project import Project
from earwax.yaml import CDumper, CLoader, dump, load

from ...constants import project_filename
from .events import EVT_SAVE, SaveEvent
from .panels.credits_panel import CreditsPanel
from .panels.levels_panel import LevelsPanel
from .panels.project_settings import ProjectSettings
from .panels.variables_panel import VariablesPanel

state_path: Path = Path.cwd() / '.gui.yaml'


@attrs(auto_attribs=True)
class AppState(DumpLoadMixin):
    """Save application state."""

    notebook_page: int = 0


class MainFrame(wx.Frame):
    """The main frame of the earwax gui client."""

    def __init__(self) -> None:
        """Initialise the window."""
        self.context: Context = Context()
        super().__init__(None, title='Earwax')
        self.project: Project = Project.from_filename(project_filename)
        self.set_title()
        self.Bind(EVT_SAVE, self.on_save)
        p: wx.Panel = wx.Panel(self)
        s: wx.BoxSizer = wx.BoxSizer(orient=wx.VERTICAL)
        self.notebook: wx.Notebook = wx.Notebook(p, name='')
        self.project_settings: ProjectSettings = ProjectSettings(self)
        self.levels_panel: LevelsPanel = LevelsPanel(self)
        self.variables_panel: VariablesPanel = VariablesPanel(self)
        self.credits_panel: CreditsPanel = CreditsPanel(self)
        self.notebook.AddPage(self.project_settings, 'Project &Settings')
        self.notebook.AddPage(self.levels_panel, '&Levels')
        self.notebook.AddPage(self.variables_panel, '&Variables')
        self.notebook.AddPage(self.credits_panel, '&Credits')
        s.Add(self.notebook, 1, wx.GROW)
        p.SetSizerAndFit(s)
        mb: wx.MenuBar = wx.MenuBar()
        fm: wx.Menu = wx.Menu()
        self.Bind(
            wx.EVT_MENU, self.do_save, fm.Append(
                wx.ID_SAVE, '&Save\tCTRL+S', 'Save the project'
            )
        )
        mb.Append(fm, '&File')
        self.SetMenuBar(mb)
        self.Bind(wx.EVT_CLOSE, self.on_close)
        if state_path.is_file():
            with state_path.open('r') as f:
                data: Dict[str, Any] = load(f, Loader=CLoader)
            state: AppState = AppState.load(data)
            self.notebook.SetSelection(state.notebook_page)

    def set_title(self) -> None:
        """Set the window title."""
        self.SetTitle(f'Earwax - {self.project.name}')

    def do_save(self, event: wx.CommandEvent) -> None:
        """Performa  save."""
        event = SaveEvent(project=self.project)
        wx.PostEvent(self, event)

    def on_save(self, event: SaveEvent) -> None:
        """Perform the save."""
        self.project.save(project_filename)
        event.Skip()

    def on_close(self, event: wx.CloseEvent) -> None:
        """Save the current notebook page."""
        event.Skip()
        state: AppState = AppState(notebook_page=self.notebook.GetSelection())
        with state_path.open('w') as f:
            dump(state.dump(), f, Dumper=CDumper)
