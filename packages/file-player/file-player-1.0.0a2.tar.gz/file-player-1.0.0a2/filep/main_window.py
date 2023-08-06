import enum
import sys
import logging
import os
import platform
import subprocess
import filep.config
import functools
import time
from PyQt5 import QtCore
from PyQt5 import QtWidgets
from PyQt5 import QtGui
try:
    # noinspection PyUnresolvedReferences
    from PyQt5 import QtMultimedia
except ImportError:
    logging.error("ImportError for QtMultimedia - maybe because there's no sound card available")
    sys.exit(1)
    # -If the system does not have a sound card (as for example Travis CI)
    # -An alternative to this approach is to use this: http://doc.qt.io/qt-5/qaudiodeviceinfo.html#availableDevices
logging.basicConfig(level=logging.DEBUG)

"""

self.sound_effect.setSource(audio_source_qurl)
self.sound_effect.setVolume(float(i_volume / 100))
self.sound_effect.play()

"""


TIMEOUT_MSECS_INT = 100
supported_suffixes_list = [".ogg", ".mp3", ".flac", ".wav"]


class ListWidget(QtWidgets.QListWidget):
    item_dropped_signal = QtCore.pyqtSignal()

    def __init__(self, i_parent):
        super().__init__(parent=i_parent)
        self.setDragDropMode(QtWidgets.QListWidget.InternalMove)

    def dropEvent(self, event: QtGui.QDropEvent) -> None:
        # https://doc.qt.io/qt-5/qdropevent.html
        super().dropEvent(event)
        logging.debug("dropEvent")
        self.item_dropped_signal.emit()


def get_media_from_path(i_file_path: str) -> QtMultimedia.QMediaContent:
    file_qurl = QtCore.QUrl.fromLocalFile(i_file_path)
    qmediacontent = QtMultimedia.QMediaContent(file_qurl)
    return qmediacontent


def debug_dr(func):
    @functools.wraps(func)
    def wrapper_func(self, *args, **kwargs):
        logging.debug(f"Calling function {func.__name__} with arguments _____")
        ret_val = func(self, *args, **kwargs)
        logging.debug(f"{func.__name__} returned {ret_val!r}")
        return ret_val
    return wrapper_func


def open_fd(i_fd_path: str):
    system_str = platform.system()
    if system_str == "Windows":
        os.startfile(i_fd_path)
    elif system_str == "Darwin":
        subprocess.Popen(["open", i_fd_path])
    else:
        subprocess.Popen(["xdg-open", i_fd_path])


def user_interaction_dr(func):
    @functools.wraps(func)
    def wrapper_func(self, *args, **kwargs):
        logging.debug(f"Calling function {func.__name__}")
        if self.updating_gui_bool:
            logging.debug(f"GUI update ongoing, exiting user interaction function {func.__name__}")
            return
        ret_val = func(self, *args, **kwargs)
        return ret_val
    return wrapper_func


def gui_update_dr(func):
    @functools.wraps(func)
    def wrapper_func(self, *args, **kwargs):
        # logging.debug(f"{self.updating_gui_bool=}")
        self.updating_gui_bool = True
        # logging.debug(f"{self.updating_gui_bool=}")
        logging.debug(f"Calling function {func.__name__} through the gui_update_dr decoractor")
        ret_val = func(self, *args, **kwargs)
        self.updating_gui_bool = False
        # logging.debug(f"{self.updating_gui_bool=}")
        return ret_val
    return wrapper_func


class FadeTimer(QtCore.QObject):
    update_signal = QtCore.pyqtSignal(bool, int)
    # -int is the new volume (0-100), or has just stopped (-1)

    def __init__(self):
        super().__init__()

        self.ms_elapsed_int = 0
        self.start_time_ms_int = -1
        self.start_volume_int = -1
        self.volume_interval_per_ms_ft = -1
        self.fade_qtimer = None
        self.callback_func = None

    def start(self, i_start_time_ms: int, i_start_volume: int, i_callback_func):
        if i_start_time_ms == 0:
            self.update_signal.emit(True, i_start_volume)
            return
        self.ms_elapsed_int = 0
        self.volume_interval_per_ms_ft = i_start_volume / i_start_time_ms
        self.start_volume_int = i_start_volume
        self.start_time_ms_int = i_start_time_ms
        self.callback_func = i_callback_func
        if self.fade_qtimer is not None and self.fade_qtimer.isActive():
            self.fade_qtimer.stop()
        self.fade_qtimer = QtCore.QTimer(self)
        self.fade_qtimer.timeout.connect(self.timeout)
        self.fade_qtimer.start(TIMEOUT_MSECS_INT)

    def get_percent_done(self) -> int:
        ret_val_int = int(100 * (self.ms_elapsed_int / self.start_time_ms_int))
        return ret_val_int

    def stop(self):
        if self.fade_qtimer is not None and self.fade_qtimer.isActive():
            self.fade_qtimer.stop()
            logging.debug("timer stopped")
        self.ms_elapsed_int = 0
        self.update_signal.emit(True, self.start_volume_int)

    def is_active(self):
        if self.fade_qtimer is None:
            return False
        ret_is_active_bool = self.fade_qtimer.isActive()
        return ret_is_active_bool

    def timeout(self):
        self.ms_elapsed_int += TIMEOUT_MSECS_INT
        # logging.debug("time_remaining " + str(self.secs_remaining_int))
        if self.ms_elapsed_int <= self.start_time_ms_int:
            new_volume_int = self.start_volume_int - int(self.ms_elapsed_int * self.volume_interval_per_ms_ft)
            self.update_signal.emit(False, new_volume_int)
        else:
            self.stop()


class GuiAreasEnum(enum.Enum):
    fd_list = enum.auto()
    fd_controls = enum.auto()
    pl_list = enum.auto()
    pl_controls = enum.auto()
    # all = enum.auto()


class StateEnum(enum.Enum):
    stopped = enum.auto()  # -inactive, start state
    playing = enum.auto()
    paused = enum.auto()
    # -these are comparable to https://doc.qt.io/qt-5/qmediaplayer.html#State-enum

    pausing_fade = enum.auto()
    stopping_fade = enum.auto()
    switching_fade = enum.auto()
    # -please note that we only fade out

    stop_after_current = enum.auto()


class HLine(QtWidgets.QFrame):
    def __init__(self):
        super().__init__()
        self.setFrameShape(QtWidgets.QFrame.HLine)
        # self.setPalette()
        self.setLineWidth(1)


class MainWindow(QtWidgets.QMainWindow):
    """
    Please note the difference in naming between:
    * mpl: the playlist itself
    * playlist: the list widget we are using to show the mpl

    """
    def __init__(self):
        super().__init__()

        self.state_enum = StateEnum.stopped
        self.fd_ref_list = []
        self.pl_ref_list = []
        # -unused but must be here to avoid this error:
        # -"#"wrapped C/C++ object of type QListWidgetItem has been deleted"
        self.updating_gui_bool = False
        self.updating_playlist_bool = False
        self.active_dir_path_str = ""
        self.fav_dirs_dict = filep.config.get_fav_dict()

        self.fade_timer = FadeTimer()
        self.fade_timer.update_signal.connect(self.on_fade_timer_updated)
        self.media_player = None
        try:
            # noinspection PyArgumentList
            self.media_player = QtMultimedia.QMediaPlayer(parent=self)
            # , flags=QtMultimedia.QMediaPlayer.
        except NameError:
            logging.debug("NameError - Cannot play audio since QtMultimedia has not been imported")
            sys.exit(1)

        self.media_player.setAudioRole(QtMultimedia.QAudio.MusicRole)
        self.media_player.positionChanged.connect(self.on_media_pos_changed)
        self.media_player.durationChanged.connect(self.on_duration_changed)
        self.media_player.currentMediaChanged.connect(self.on_current_media_changed)

        self.setWindowTitle("File Player")

        self.central_widget = QtWidgets.QWidget(parent=self)
        self.setCentralWidget(self.central_widget)

        vbox_l2 = QtWidgets.QVBoxLayout()
        self.central_widget.setLayout(vbox_l2)

        hbox_l3 = QtWidgets.QHBoxLayout()
        vbox_l2.addLayout(hbox_l3)

        self.fd_qgb = QtWidgets.QGroupBox()
        hbox_l3.addWidget(self.fd_qgb)

        vbox_l4 = QtWidgets.QVBoxLayout()
        self.fd_qgb.setLayout(vbox_l4)

        self.favorites_qcb = QtWidgets.QComboBox()
        self.favorites_qcb.setPlaceholderText("Favorite dirs")
        # -not working, probably a bug
        vbox_l4.addWidget(self.favorites_qcb)
        self.favorites_qcb.activated.connect(self.on_fav_activated)


        self.active_dir_path_qll = QtWidgets.QLabel()
        vbox_l4.addWidget(self.active_dir_path_qll)
        self.active_dir_path_qll.setWordWrap(True)

        hbox_l5 = QtWidgets.QHBoxLayout()
        vbox_l4.addLayout(hbox_l5)

        self.dir_up_qpb = QtWidgets.QPushButton("Up")
        hbox_l5.addWidget(self.dir_up_qpb)
        self.dir_up_qpb.setFixedWidth(50)
        self.dir_up_qpb.clicked.connect(self.on_dir_up_clicked)

        hbox_l5.addStretch(1)

        hbox_l5.addWidget(QtWidgets.QLabel("Show dirs: "))
        self.show_dirs_first_last_qbg = QtWidgets.QButtonGroup()

        self.show_dirs_first_qrb = QtWidgets.QRadioButton("First")
        hbox_l5.addWidget(self.show_dirs_first_qrb)
        self.show_dirs_first_last_qbg.addButton(self.show_dirs_first_qrb)

        self.show_dirs_last_qrb = QtWidgets.QRadioButton("Last")
        hbox_l5.addWidget(self.show_dirs_last_qrb)
        self.show_dirs_first_last_qbg.addButton(self.show_dirs_last_qrb)

        self.show_dirs_first_last_qbg.buttonClicked.connect(self.on_show_dirs_first_last_button_clicked)


        self.fd_qlw = QtWidgets.QListWidget(parent=self)
        vbox_l4.addWidget(self.fd_qlw)
        self.fd_qlw.setSelectionMode(QtWidgets.QAbstractItemView.ExtendedSelection)
        self.fd_qlw.setDragDropMode(QtWidgets.QAbstractItemView.DragOnly)
        self.fd_qlw.setDragEnabled(True)
        self.fd_qlw.currentRowChanged.connect(self.on_fd_current_row_changed)
        # self.fd_qlw.setSortingEnabled(True)
        self.fd_qlw.itemDoubleClicked.connect(self.on_fd_item_double_clicked)

        fm_hbox_l5 = QtWidgets.QHBoxLayout()
        vbox_l4.addLayout(fm_hbox_l5)

        self.add_to_playlist_qpb = QtWidgets.QPushButton("Add")
        fm_hbox_l5.addWidget(self.add_to_playlist_qpb)
        self.add_to_playlist_qpb.clicked.connect(self.on_add_to_playlist_clicked)

        self.add_to_playlist_as_next_qpb = QtWidgets.QPushButton("Add as next")
        fm_hbox_l5.addWidget(self.add_to_playlist_as_next_qpb)
        self.add_to_playlist_as_next_qpb.clicked.connect(self.on_add_to_playlist_as_next_clicked)

        self.add_to_playlist_as_next_and_play_qpb = QtWidgets.QPushButton("Add as next + play")
        fm_hbox_l5.addWidget(self.add_to_playlist_as_next_and_play_qpb)
        self.add_to_playlist_as_next_and_play_qpb.clicked.connect(self.on_add_to_playlist_as_next_and_play_clicked)

        vbox_l4.addWidget(HLine())
        fm_hbox_l5 = QtWidgets.QHBoxLayout()
        vbox_l4.addLayout(fm_hbox_l5)

        self.open_dir_qpb = QtWidgets.QPushButton("Open dir")
        fm_hbox_l5.addWidget(self.open_dir_qpb)
        self.open_dir_qpb.clicked.connect(self.on_open_dir_clicked)

        self.set_as_start_dir_qpb = QtWidgets.QPushButton("Set as start dir")
        fm_hbox_l5.addWidget(self.set_as_start_dir_qpb)
        self.set_as_start_dir_qpb.clicked.connect(self.on_set_as_start_dir_clicked)

        self.is_fav_qcb = QtWidgets.QCheckBox("Is fav")
        fm_hbox_l5.addWidget(self.is_fav_qcb)
        self.is_fav_qcb.toggled.connect(self.on_is_fav_toggled)

        """
        self.set_as_playlist_dir_qpb = QtWidgets.QPushButton("Set as playlist dir")
        fm_hbox_l5.addWidget(self.set_as_playlist_dir_qpb)
        self.set_as_playlist_dir_qpb.clicked.connect(self.on_set_as_playlist_dir_clicked)
        """

        self.playlist_qgb = QtWidgets.QGroupBox()
        hbox_l3.addWidget(self.playlist_qgb)

        vbox_l4 = QtWidgets.QVBoxLayout()
        self.playlist_qgb.setLayout(vbox_l4)

        self.playlist_qlw = ListWidget(self)
        vbox_l4.addWidget(self.playlist_qlw)
        # self.playlist_qlw.setAcceptDrops(True)
        # self.playlist_qlw.setDragDropMode(QtWidgets.QAbstractItemView.InternalMove)
        # .DropOnly
        self.playlist_qlw.setSelectionMode(QtWidgets.QAbstractItemView.ExtendedSelection)
        self.playlist_qlw.itemDoubleClicked.connect(self.on_playlist_item_dc)
        self.playlist_qlw.item_dropped_signal.connect(self.on_playlist_item_dropped)

        fm_hbox_l5 = QtWidgets.QHBoxLayout()
        vbox_l4.addLayout(fm_hbox_l5)

        self.remove_from_playlist_qpb = QtWidgets.QPushButton("Remove from playlist")
        fm_hbox_l5.addWidget(self.remove_from_playlist_qpb)
        self.remove_from_playlist_qpb.clicked.connect(self.on_remove_from_playlist_clicked)

        self.clear_playlist_qpb = QtWidgets.QPushButton("Clear")
        fm_hbox_l5.addWidget(self.clear_playlist_qpb)
        self.clear_playlist_qpb.clicked.connect(self.on_clear_playlist_clicked)

        self.now_playing_qgb = QtWidgets.QGroupBox()
        vbox_l2.addWidget(self.now_playing_qgb)

        btm_vbox_l3 = QtWidgets.QVBoxLayout()
        self.now_playing_qgb.setLayout(btm_vbox_l3)

        state_hbox_l4 = QtWidgets.QHBoxLayout()
        btm_vbox_l3.addLayout(state_hbox_l4)

        self.track_title_qll = QtWidgets.QLabel()
        state_hbox_l4.addWidget(self.track_title_qll)
        state_hbox_l4.addStretch(1)
        self.state_qll = QtWidgets.QLabel()
        state_hbox_l4.addWidget(self.state_qll)
        self.state_qpb = QtWidgets.QProgressBar()
        state_hbox_l4.addWidget(self.state_qpb)
        self.state_qpb.setFixedWidth(140)
        self.state_qpb.setFixedHeight(16)
        # self.state_qpb.setFormat("fading out")
        self.state_qpb.setFormat("")
        # -possible bug: The progress bar is not updated as often if we set an empty or custom text format

        hbox_l4 = QtWidgets.QHBoxLayout()
        btm_vbox_l3.addLayout(hbox_l4)

        self.play_qpb = QtWidgets.QPushButton("Play")
        self.play_qpb.clicked.connect(self.on_play_clicked)
        hbox_l4.addWidget(self.play_qpb)

        self.pause_qpb = QtWidgets.QPushButton("Pause")
        self.pause_qpb.clicked.connect(self.on_pause_clicked)
        hbox_l4.addWidget(self.pause_qpb)

        self.stop_qpb = QtWidgets.QPushButton("Stop")
        self.stop_qpb.clicked.connect(self.on_stop_clicked)
        hbox_l4.addWidget(self.stop_qpb)

        self.stop_after_current_qpb = QtWidgets.QPushButton("Stop after current")
        self.stop_after_current_qpb.clicked.connect(self.stop_after_current_clicked)
        hbox_l4.addWidget(self.stop_after_current_qpb)

        self.next_qpb = QtWidgets.QPushButton("Next")
        self.next_qpb.clicked.connect(self.on_next_clicked)
        hbox_l4.addWidget(self.next_qpb)

        hbox_l4 = QtWidgets.QHBoxLayout()
        btm_vbox_l3.addLayout(hbox_l4)

        start_vol_int = filep.config.get_start_volume()
        # vbox_l2.addWidget(QtWidgets.QLabel("lowering the volume for the next iteration"))
        self.volume_qsr = QtWidgets.QSlider()
        # self.volume_qsr.setInvertedAppearance(True)
        self.volume_qsr.valueChanged.connect(self.on_volume_slider_changed)
        self.volume_qsr.setOrientation(QtCore.Qt.Horizontal)
        self.volume_qsr.setMinimum(0)
        self.volume_qsr.setMaximum(100)
        self.volume_qsr.setMaximumWidth(150)
        self.volume_qsr.setValue(start_vol_int)
        hbox_l4.addWidget(self.volume_qsr)

        self.fade_qsb = QtWidgets.QSpinBox()
        hbox_l4.addWidget(self.fade_qsb)
        self.fade_qsb.setValue(5)

        self.share_qpb = QtWidgets.QPushButton("Share")
        self.share_qpb.clicked.connect(self.on_share_clicked)
        hbox_l4.addWidget(self.share_qpb)

        self.seek_qsr = QtWidgets.QSlider()
        self.seek_qsr.setTracking(False)
        self.seek_qsr.setSingleStep(2500)
        self.seek_qsr.setPageStep(15000)
        self.seek_qsr.valueChanged.connect(self.on_seek_changed)
        self.seek_qsr.setOrientation(QtCore.Qt.Horizontal)
        self.seek_qsr.setMinimum(0)
        hbox_l4.addWidget(self.seek_qsr)

        self.duration_qll = QtWidgets.QLabel()
        hbox_l4.addWidget(self.duration_qll)

        self.mpl_qmp = QtMultimedia.QMediaPlaylist()
        self.mpl_qmp.mediaChanged.connect(self.on_mpl_media_udpated)
        self.mpl_qmp.mediaInserted.connect(self.on_mpl_media_udpated)
        self.mpl_qmp.mediaRemoved.connect(self.on_mpl_media_udpated)
        # self.playlist_qmp.currentMediaChanged.connect(self.on_current_media_changed)
        # self.now_playing_qgb

        icon_path_str = filep.config.get_appl_path("icon.png")
        self.pixmap = QtGui.QPixmap(icon_path_str)
        self.icon = QtGui.QIcon(self.pixmap)

        self.setWindowIcon(self.icon)

        # System tray
        self.tray_icon = QtWidgets.QSystemTrayIcon()
        self.tray_icon.setIcon(self.icon)
        self.tray_menu = QtWidgets.QMenu()
        self.tray_restore_action = QtWidgets.QAction("Restore")
        # noinspection PyUnresolvedReferences
        self.tray_restore_action.triggered.connect(self.showNormal)
        self.tray_menu.addAction(self.tray_restore_action)
        self.tray_quit_action = QtWidgets.QAction("Quit")
        # noinspection PyUnresolvedReferences
        self.tray_quit_action.triggered.connect(sys.exit)
        self.tray_menu.addAction(self.tray_quit_action)
        self.tray_icon.setContextMenu(self.tray_menu)
        self.tray_icon.show()

        # Main menu

        self.main_menu = self.menuBar()
        self.file_menu = QtWidgets.QMenu("File")
        self.main_menu.addMenu(self.file_menu)

        self.quit_qaction = QtWidgets.QAction("Quit")
        self.file_menu.addAction(self.quit_qaction)
        self.quit_qaction.triggered.connect(self.on_quit_action_triggered)

        self.settings_menu = QtWidgets.QMenu("Settings")
        self.main_menu.addMenu(self.settings_menu)

        self.use_current_win_geometry_at_start_qaction = QtWidgets.QAction("Use current win geometry at start")
        self.settings_menu.addAction(self.use_current_win_geometry_at_start_qaction)
        self.use_current_win_geometry_at_start_qaction.triggered.connect(
            self.on_use_current_win_geometry_at_start_triggered)

        self.playlists_menu = QtWidgets.QMenu("Playlists")
        self.main_menu.addMenu(self.playlists_menu)

        self.set_playlist_start_dir_qaction = QtWidgets.QAction("Set playlist dir")
        self.playlists_menu.addAction(self.set_playlist_start_dir_qaction)
        self.set_playlist_start_dir_qaction.triggered.connect(self.on_set_playlist_start_dir_triggered)

        self.open_playlist_dir_qaction = QtWidgets.QAction("Open playlist dir")
        self.playlists_menu.addAction(self.open_playlist_dir_qaction)
        self.open_playlist_dir_qaction.triggered.connect(self.on_open_playlist_dir_qaction)

        self.save_playlist_qaction = QtWidgets.QAction("Save playlist")
        self.playlists_menu.addAction(self.save_playlist_qaction)
        self.save_playlist_qaction.triggered.connect(self.on_save_playlist_qaction)

        self.load_playlist_qaction = QtWidgets.QAction("Load playlist")
        self.playlists_menu.addAction(self.load_playlist_qaction)
        self.load_playlist_qaction.triggered.connect(self.on_load_playlist_qaction)

        self.playlists_in_start_dir_qmenu = QtWidgets.QMenu("Playlists in start dir")
        self.playlists_menu.addMenu(self.playlists_in_start_dir_qmenu)
        self.playlists_in_start_dir_qmenu.aboutToShow.connect(self.on_playlists_in_start_dir_about_to_show)
        #self.on_playlists_in_start_dir_about_to_show()

        # Setup

        self.media_player.setPlaylist(self.mpl_qmp)
        start_dir = filep.config.get_start_dir()
        self._change_active_dir(start_dir)
        all_areas = [e for e in GuiAreasEnum]
        self.update_gui(all_areas)
        self.show_dirs_first_qrb.click()

        self.setGeometry(
            filep.config.get_win_x(), filep.config.get_win_y(),
            filep.config.get_win_width(), filep.config.get_win_height()
        )

    def on_show_dirs_first_last_button_clicked(self):
        self.update_gui([GuiAreasEnum.fd_list])

    def on_quit_action_triggered(self):
        sys.exit()

    def on_use_current_win_geometry_at_start_triggered(self):
        filep.config.set_win_x(self.x())
        filep.config.set_win_y(self.y())
        filep.config.set_win_width(self.width())
        filep.config.set_win_height(self.height())

    def on_open_dir_clicked(self):
        open_fd(self.active_dir_path_str)

    def on_playlists_in_start_dir_about_to_show(self):
        self.playlists_in_start_dir_qmenu.clear()
        dir_path_str = filep.config.get_playlist_dir()
        for file_name_str in os.listdir(dir_path_str):
            if file_name_str.lower().endswith(".m3u"):
                file_path_str = os.path.join(dir_path_str, file_name_str)
                logging.debug(f"on_playlists_in_start_dir_about_to_show, {file_path_str=}")
                load_this_playlist_func = functools.partial(self._load_playlist, file_path_str)
                load_this_playlist_qaction = QtWidgets.QAction(
                    text=file_name_str,
                    parent=self.playlists_in_start_dir_qmenu
                )
                load_this_playlist_qaction.triggered.connect(load_this_playlist_func)
                self.playlists_in_start_dir_qmenu.addAction(load_this_playlist_qaction)

    def _load_playlist(self, i_file_path_str):
        qurl = QtCore.QUrl.fromLocalFile(i_file_path_str)
        playlist_format_str = "m3u"
        self.mpl_qmp.load(qurl, playlist_format_str)

    def on_load_playlist_qaction(self):
        dir_path_str = filep.config.get_playlist_dir()
        (file_path_str, ok) = QtWidgets.QFileDialog.getOpenFileName(
            parent=self, caption="Please select playlist to load",
            directory=dir_path_str, filter="*.m3u"
        )
        if ok:
            qurl = QtCore.QUrl.fromLocalFile(file_path_str)
            playlist_format_str = "m3u"
            self.mpl_qmp.load(qurl, playlist_format_str)
            # adding a function for handling the loadFailed signal
            # https://doc.qt.io/qt-5/qmediaplaylist.html#loadFailed

            # Idea: check for playlist errors?

    def on_save_playlist_qaction(self):
        dir_path_str = filep.config.get_playlist_dir()
        (save_file_path_str, ok) = QtWidgets.QFileDialog.getSaveFileName(
            parent=self, caption="Please choose a place and name for your playlist file",
            directory=dir_path_str, filter="*.m3u"
        )
        if ok:
            qurl = QtCore.QUrl.fromLocalFile(save_file_path_str)
            playlist_format_str = "m3u"
            success_bool = self.mpl_qmp.save(qurl, playlist_format_str)
            if not success_bool:
                error_str = self.mpl_qmp.errorString()
                logging.warning(f"{error_str=}")

    def on_open_playlist_dir_qaction(self):
        dir_path_str = filep.config.get_playlist_dir()
        open_fd(dir_path_str)

    def on_set_playlist_start_dir_triggered(self):
        old_dir_path_str = filep.config.get_playlist_dir()
        dir_path_str = QtWidgets.QFileDialog.getExistingDirectory(
            parent=self, caption="Please select the start dir for playlists",
            directory=old_dir_path_str
        )
        if dir_path_str:
            filep.config.set_playlist_dir(dir_path_str)

    def on_playlist_item_dropped(self):
        self._update_mpl()

    def _update_mpl(self):
        self.updating_playlist_bool = True
        self.mpl_qmp.clear()
        for i in range(0, self.playlist_qlw.count()):
            qlwi = self.playlist_qlw.item(i)
            file_path_str = qlwi.data(QtCore.Qt.UserRole)
            self._add_file_to_playlist(file_path_str)
            # media_content = get_media_from_path(file_path_str)
            # self.playlist_qmp.addMedia(media_content)
        self.updating_playlist_bool = False

    @user_interaction_dr
    def on_fav_activated(self, index: int):
        # i_dir: str
        dir_str = self.favorites_qcb.itemText(index)
        self._change_active_dir(dir_str)
        self.update_gui([GuiAreasEnum.fd_controls])

    @user_interaction_dr
    def on_is_fav_toggled(self, i_checked: bool):
        key_str = self.active_dir_path_str
        if i_checked:
            now_unix_ts_int = int(time.time())
            self.fav_dirs_dict[key_str] = now_unix_ts_int
        else:
            return_value_bool = bool(self.fav_dirs_dict.pop(key_str, False))
            if return_value_bool:
                pass
            else:
                logging.warning("Tried to remove nonexisting key from fav_dirs_dict")
        self.update_gui([GuiAreasEnum.fd_controls])

    def on_share_clicked(self):
        media = self.mpl_qmp.currentMedia()
        qurl = media.canonicalUrl()
        path_of_file_str = qurl.path()
        name_of_file_str = os.path.basename(path_of_file_str)
        logging.debug(f"{path_of_file_str=}")
        # path_of_file_str = "/home/sunyata/Downloads/fågelsång-mobil/storlom.mp3"

        if path_of_file_str:
            subject_email_str = f"A song i want to share with you! --- {name_of_file_str}"
            body_email_str = "Shared using SunyataZero's mediaplayer"
            message_composition_str = (
                    "to=''," +
                    "subject='" + subject_email_str + "'," +
                    "body='" + body_email_str + "'," +
                    "attachment='" + path_of_file_str + "'"
            )
            subprocess.Popen(["thunderbird", "-compose", message_composition_str])

        # other sharing options?

    def on_dir_up_clicked(self):
        parent_dir_path_str = os.path.dirname(self.active_dir_path_str)
        self._change_active_dir(parent_dir_path_str)

    def _change_active_dir(self, i_new_dir: str):
        self.active_dir_path_str = i_new_dir
        self.active_dir_path_qll.setText(i_new_dir)
        self.update_gui([GuiAreasEnum.fd_list])

    def on_fd_item_double_clicked(self, i_qlwi: QtWidgets.QListWidgetItem):
        path_str = i_qlwi.data(QtCore.Qt.UserRole)
        if os.path.isdir(path_str):
            pass
        elif path_str.endswith(tuple(supported_suffixes_list)):
            self.on_add_to_playlist_as_next_and_play_clicked()
        else:
            open_fd(path_str)

    def on_fd_current_row_changed(self, i_row: int):
        if i_row == -1:
            return
        qlwi = self.fd_qlw.item(i_row)
        fd_path_str = qlwi.data(QtCore.Qt.UserRole)
        if os.path.isdir(fd_path_str):
            self._change_active_dir(fd_path_str)

    def on_clear_playlist_clicked(self):
        self.on_stop_clicked()
        self.mpl_qmp.clear()
        # self.playlist_qlw.clear()

    def on_remove_from_playlist_clicked(self):
        selected_indexes_list = self.playlist_qlw.selectedIndexes()
        selected_rows_list = []
        for model_index in selected_indexes_list:
            row_int = model_index.row()
            selected_rows_list.append(row_int)
        selected_rows_list = sorted(selected_rows_list, reverse=True)
        # -so that the last rows are removed first
        for row_int in selected_rows_list:
            self.mpl_qmp.removeMedia(row_int)

    def on_add_to_playlist_as_next_clicked(self):
        curr_index_int = self.mpl_qmp.currentIndex()
        selected_items_list = self.fd_qlw.selectedItems()
        for qlwi in selected_items_list:
            path_str = qlwi.data(QtCore.Qt.UserRole)
            pos_int = curr_index_int + 1
            self._add_file_to_playlist(path_str, i_pos=pos_int)
        self.fd_qlw.clearSelection()

    def _add_file_to_playlist(self, i_file_path: str, i_pos: int=-1):
        qmediacontent = get_media_from_path(i_file_path)
        if i_pos == -1:
            self.mpl_qmp.addMedia(qmediacontent)
        else:
            self.mpl_qmp.insertMedia(i_pos, qmediacontent)

        if self.media_player.isMetaDataAvailable():
            meta_data_keys_strlist = self.media_player.availableMetaData()
            logging.debug(f"{meta_data_keys_strlist=}")
            for meta_data_key_str in meta_data_keys_strlist:
                meta_data_value_str = self.media_player.metaData(meta_data_key_str)
                logging.debug(f"key: {meta_data_key_str}, value: {meta_data_value_str}")
        else:
            logging.debug("no meta data available")

    ##### STATE CHANGES #####

    def on_playlist_item_dc(self, i_qlwi: QtWidgets.QListWidgetItem):
        if self.state_enum == StateEnum.playing:
            self.state_enum = StateEnum.switching_fade
            fade_ms_int = 1000 * self.fade_qsb.value()
            start_vol_int = self.volume_qsr.value()
            self.fade_timer.start(fade_ms_int, start_vol_int, self.playlist_item_dc_callback)
        else:
            self.playlist_item_dc_callback()
        self.update_gui()

    def playlist_item_dc_callback(self):
        self.media_player.stop()
        current_row_nr_int = self.playlist_qlw.currentRow()
        self.mpl_qmp.setCurrentIndex(current_row_nr_int)
        self.state_enum = StateEnum.playing
        self.media_player.play()
        error_enum = self.media_player.error()
        if error_enum != QtMultimedia.QMediaPlayer.NoError:
            error_str = self.media_player.errorString()
            logging.warning(f"{error_str=}")
        self.update_gui()

    def on_play_clicked(self):
        self.state_enum = StateEnum.playing
        self.media_player.play()
        self.update_gui()

    def on_next_clicked(self):
        self.state_enum = StateEnum.switching_fade
        fade_ms_int = 1000 * self.fade_qsb.value()
        start_vol_int = self.volume_qsr.value()
        self.fade_timer.start(fade_ms_int, start_vol_int, self.next_clicked_callback)
        self.update_gui()

    def next_clicked_callback(self):
        self.state_enum = StateEnum.playing
        self.mpl_qmp.next()
        self.update_gui()

    def on_stop_clicked(self):
        self.state_enum = StateEnum.stopping_fade
        fade_ms_int = 1000 * self.fade_qsb.value()
        start_vol_int = self.volume_qsr.value()
        self.fade_timer.start(fade_ms_int, start_vol_int, self.stop_clicked_callback)
        self.update_gui()

    def stop_clicked_callback(self):
        self.state_enum = StateEnum.stopped
        self.media_player.stop()
        self.update_gui()

    def stop_after_current_clicked(self):
        self.state_enum = StateEnum.stop_after_current
        self.mpl_qmp.setPlaybackMode(QtMultimedia.QMediaPlaylist.CurrentItemOnce)
        self.update_gui()

    def on_pause_clicked(self):
        self.state_enum = StateEnum.pausing_fade
        fade_ms_int = 1000 * self.fade_qsb.value()
        start_vol_int = self.volume_qsr.value()
        self.fade_timer.start(fade_ms_int, start_vol_int, self.pause_clicked_callback)
        self.update_gui()

    def pause_clicked_callback(self):
        self.state_enum = StateEnum.paused
        self.media_player.pause()
        self.update_gui()

    def on_fade_timer_updated(self, i_is_done: bool, i_new_volume: int):
        percent_done_int = self.fade_timer.get_percent_done()
        self.state_qpb.setValue(percent_done_int)
        self.volume_qsr.setValue(i_new_volume)
        if i_is_done:
            self.fade_timer.callback_func()

    def on_add_to_playlist_as_next_and_play_clicked(self):
        self.on_add_to_playlist_as_next_clicked()
        if self.media_player.state() == QtMultimedia.QMediaPlayer.StoppedState:
            self.on_play_clicked()
        elif self.media_player.state() in (QtMultimedia.QMediaPlayer.PlayingState, QtMultimedia.QMediaPlayer.PausedState):
            self.on_next_clicked()
        # self.playlist_qmp.next()
        self.update_gui()

    def on_set_as_start_dir_clicked(self):
        filep.config.set_start_dir(self.active_dir_path_str)

    def on_add_to_playlist_clicked(self):
        selected_indexes_list = self.fd_qlw.selectedIndexes()
        for model_index in selected_indexes_list:
            row_int = model_index.row()
            qlwi = self.fd_qlw.item(row_int)
            path_str = qlwi.data(QtCore.Qt.UserRole)
            self._add_file_to_playlist(path_str)
        self.fd_qlw.clearSelection()

        """
        Why doesn't this code (below) work when the above code does???

        selected_items_list = self.fd_qlw.selectedItems()
        for qlwi in selected_items_list:
            path_str = qlwi.data(QtCore.Qt.UserRole)
            self._add_file_to_playlist(path_str)
        self.fd_qlw.clearSelection()
        """

    def on_duration_changed(self, i_new_duration_ms: int):
        # if self.media_player.isSeekable():
        # currentmediachanged durationchanged signal
        # duration_ms_int = self.media_player.duration()
        logging.debug(f"on_duration_changed, {i_new_duration_ms=}")
        self.seek_qsr.setMaximum(i_new_duration_ms)

        durations_secs_int = i_new_duration_ms // 1000
        duration_minutes_int = durations_secs_int // 60
        duration_remaining_secs_int = durations_secs_int % 60
        duration_remaining_secs_str = str(duration_remaining_secs_int).zfill(2)
        duration_str = f"{duration_minutes_int}:{duration_remaining_secs_str}"
        self.duration_qll.setText(duration_str)

    def on_current_media_changed(self, i_media: QtMultimedia.QMediaContent):
        qurl = i_media.canonicalUrl()
        file_name_str = qurl.fileName()
        logging.debug(f"on_current_media_changed, {file_name_str=}")
        # self.now_playing_qgb.setTitle(file_name_str)
        self.track_title_qll.setText(file_name_str)
        if self.mpl_qmp.playbackMode() == QtMultimedia.QMediaPlaylist.CurrentItemOnce:
            self.mpl_qmp.setPlaybackMode(QtMultimedia.QMediaPlaylist.Sequential)
            # future: restore playback mode
        self.update_gui([GuiAreasEnum.pl_list])

    def on_mpl_media_udpated(self, i_start: int, i_end: int):
        if self.updating_playlist_bool:
            return
        self.update_gui([GuiAreasEnum.pl_list])

    def on_media_pos_changed(self, i_new_pos_ms: int):
        self.updating_pos_bool = True
        self.seek_qsr.setValue(i_new_pos_ms)
        self.updating_pos_bool = False

    def on_seek_changed(self, i_new_value: int):
        if self.updating_pos_bool:
            return
        logging.debug(f"on_seek_changed, {i_new_value=}")
        self.media_player.setPosition(i_new_value)

    def on_volume_slider_changed(self, i_new_volume):
        self.media_player.setVolume(i_new_volume)

    def on_about_to_quit(self):
        filep.config.set_fav_dict(self.fav_dirs_dict)

    @gui_update_dr
    def update_gui(self, i_gui_areas: [GuiAreasEnum] = None):
        if i_gui_areas is None:
            i_gui_areas = []

        state_str = self.state_enum.name
        self.state_qll.setText("State: " + state_str)

        if GuiAreasEnum.fd_list in i_gui_areas:
            if not self.active_dir_path_str:
                return
            self.fd_qlw.clear()
            fd_name_list = os.listdir(self.active_dir_path_str)
            fd_name_list = sorted(fd_name_list)
            dir_name_list = []
            music_file_name_list = []
            other_file_name_list = []
            for fd_name_str in fd_name_list:
                fd_path_str = os.path.join(self.active_dir_path_str, fd_name_str)
                if fd_path_str.startswith("."):
                    continue  # -skipped
                elif os.path.isdir(fd_path_str):
                    dir_name_list.append(fd_name_str)
                elif fd_name_str.lower().endswith(tuple(supported_suffixes_list)):
                    music_file_name_list.append(fd_name_str)
                else:
                    other_file_name_list.append(fd_name_str)

            def add_directories():
                for name_str in sorted(dir_name_list):
                    path_str = os.path.join(self.active_dir_path_str, name_str)
                    qlwi = QtWidgets.QListWidgetItem(parent=self.fd_qlw)
                    # self.fd_ref_list.append(qlwi)
                    qlwi.setFlags(QtCore.Qt.ItemIsEnabled)
                    color = QtGui.QColor(180, 180, 180)
                    start_color = QtGui.QColor(240, 240, 240)
                    stop_color = QtGui.QColor(255, 255, 255)
                    gradient = QtGui.QLinearGradient()
                    gradient.setSpread(QtGui.QLinearGradient.PadSpread)
                    gradient.setStart(0, 0)
                    gradient.setFinalStop(0, 20)
                    gradient.setColorAt(0, start_color)
                    gradient.setColorAt(1, stop_color)
                    brush = QtGui.QBrush(color)
                    qlwi.setBackground(brush)
                    qlwi.setText("> " + name_str)
                    qlwi.setData(QtCore.Qt.UserRole, path_str)
                    self.fd_qlw.addItem(qlwi)
            if self.show_dirs_first_qrb.isChecked():
                add_directories()
            for name_str in sorted(music_file_name_list):
                path_str = os.path.join(self.active_dir_path_str, name_str)
                qlwi = QtWidgets.QListWidgetItem(parent=self.fd_qlw)
                # self.fd_ref_list.append(qlwi)
                qlwi.setText(name_str)
                qlwi.setData(QtCore.Qt.UserRole, path_str)
                self.fd_qlw.addItem(qlwi)
            for name_str in sorted(other_file_name_list):
                path_str = os.path.join(self.active_dir_path_str, name_str)
                qlwi = QtWidgets.QListWidgetItem(parent=self.fd_qlw)
                # self.fd_ref_list.append(qlwi)
                qlwi.setFlags(QtCore.Qt.ItemIsEnabled)
                # qlwi.setFlags(QtCore.Qt.NoItemFlags)
                color = QtGui.QColor(100, 100, 100)
                brush = QtGui.QBrush(color)
                qlwi.setForeground(brush)
                qlwi.setText(name_str)
                qlwi.setData(QtCore.Qt.UserRole, path_str)
                self.fd_qlw.addItem(qlwi)
            if self.show_dirs_last_qrb.isChecked():
                add_directories()

        if GuiAreasEnum.fd_controls in i_gui_areas:
            self.favorites_qcb.clear()
            for key, value in self.fav_dirs_dict.items():
                self.favorites_qcb.addItem(key)
            self.favorites_qcb.setCurrentIndex(-1)

        if GuiAreasEnum.fd_list in i_gui_areas:
            if self.active_dir_path_str in self.fav_dirs_dict.keys():
                self.is_fav_qcb.setChecked(True)
            else:
                self.is_fav_qcb.setChecked(False)

        if GuiAreasEnum.pl_list in i_gui_areas:
            self.pl_ref_list = []
            self.playlist_qlw.clear()
            for i in range(0, self.mpl_qmp.mediaCount()):
                media = self.mpl_qmp.media(i)
                qurl = media.canonicalUrl()
                file_name_str = qurl.fileName()
                file_path_str = qurl.path()
                # media_list.append(file_name_str)
                qlwi = QtWidgets.QListWidgetItem(file_name_str)
                self.pl_ref_list.append(qlwi)
                qlwi.setData(QtCore.Qt.UserRole, file_path_str)
                font = QtGui.QFont()
                qlwi.setFont(font)
                # qlwi.setData()
                self.playlist_qlw.addItem(qlwi)
            cur_index_int = self.mpl_qmp.currentIndex()
            if cur_index_int != -1:
                qlwi = self.playlist_qlw.item(cur_index_int)
                font = qlwi.font()
                font.setBold(True)
                qlwi.setFont(font)


