# -*- coding: utf-8 -*-

import sys
import os
import logging

import pandas as pd

from PyQt5 import QtCore, QtGui, QtWidgets

from spike_recorder.experiments.libet.libet_ui import Ui_Libet
from spike_recorder.experiments.libet.instructions_ui import Ui_dialog_instructions
from spike_recorder.experiments.libet.data import LibetData


# It seems I need to add this to get trace backs to show up on
# uncaught python exceptions.
def catch_exceptions(t, val, tb):
    old_hook(t, val, tb)
    sys.exit(-1)

old_hook = sys.excepthook
sys.excepthook = catch_exceptions


class IntroDialog(QtWidgets.QDialog, Ui_dialog_instructions):
    """
    The intro instructions dialog box. Allows selecting the output file.
    """
    def __init__(self, parent=None):
        QtWidgets.QDialog.__init__(self, parent)
        self.setupUi(self)

        self.button_browse.clicked.connect(self.get_directory)

        # Lets prepopulate the output file name with something
        index = 1
        filename = f"libet_output{index}.csv"
        while os.path.isfile(filename):
            index = index + 1
            filename = f"libet_output{index}.csv"

        self.textbox_file.setText(filename)


    def reject(self):
        """
        If the user clicks cancel, we can't proceeed, exit the app.

        Returns:
            None
        """
        sys.exit(0)

    def get_directory(self):
        dialog = QtWidgets.QFileDialog()
        foo_dir = dialog.getExistingDirectory(self, 'Select an output directory')

        # Add a slash at the end
        foo_dir = foo_dir + '/'

        self.textbox_file.setText(foo_dir)


class LibetMainWindow(QtWidgets.QMainWindow, Ui_Libet):
    """
    The main application class for the Libet experiement.
    """

    NUM_PRACTICE_TRIALS = 20
    NUM_URGE_TRIALS = 20

    def __init__(self, *args, **kwargs):
        QtWidgets.QMainWindow.__init__(self, *args, **kwargs)
        self.setupUi(self)

        # adding action to a buttons
        self.button_next.clicked.connect(self.next_trial_click)
        self.button_retry.clicked.connect(self.retry_trial_click)

        self.data = LibetData()

        self.output_filename = None

        # The first sent of NUM_PRACTICE_TRIALS do not ask the urge time.
        self.urge_mode = False

        self.clock_widget.selectChange.connect(self.on_clock_select_change)


    def update_status(self):
        """
        Update any status fields with the current state of the experiment.

        Returns:
            None
        """
        self.label_status.setText(f"Trial: {self.data.num_trials+1}")

    def restart_trial(self):
        """
        Restart the current trial.

        Returns:
            None
        """
        self.clock_widget.reset_clock()
        self.clock_widget.start_clock()
        self.button_next.setText("Stop")
        self.button_next.setStyleSheet("background-color : red;")
        self.button_retry.setEnabled(False)
        self.button_next.setEnabled(True)
        self.clock_widget.select_enabled = False

        self.update_status()

    def stop_trial(self):
        """
        Stop the trial.

        Returns:

        """
        self.clock_widget.stop_clock()
        self.button_next.setText("Next Trial")
        self.button_next.setStyleSheet("")
        self.button_retry.setEnabled(True)

        # If this is urge mode, make sure they can't go to the next trial without selecting
        # and urge time.
        if self.urge_mode:
            self.button_next.setEnabled(False)
            self.clock_widget.select_enabled = True

        # Check if we have finished our first set of trials, if so, now we need to enter
        # the secondary mode where we ask for the urge time
        if (self.data.num_trials+1) == self.NUM_PRACTICE_TRIALS:
            self.urge_mode = True
            self.clock_widget.select_enabled = True

            QtWidgets.QMessageBox.about(self, "Instructions - Part 2",
                                        f"For the next {self.NUM_URGE_TRIALS} trials, stop the clock whenever you "
                                        f"like. After each trial, click the time on the clock when you first felt the "
                                        f"urge to stop the clock. ")


    def next_trial_click(self):
        """
        When the next trial button is clicked. This can also be the stop clock button when the trial is running.

        Returns:
            None
        """

        if not self.clock_widget.clock_stopped:
            self.stop_trial()
        else:

            # Store the trial's data, unless the clock hasn't been started.
            if self.clock_widget.msecs_elapsed() > 0:
                self.data.add_trial(stop_time_msecs=self.clock_widget.msecs_elapsed(),
                                    urge_time_msecs=self.clock_widget.selected_time)

                # Dump the data back out to file. We will just dump everything back out over and over again
                # so that if the user stops half way through, they have part of their data.
                if self.output_filename is not None:
                    self.data.to_csv(self.output_filename)
                else:
                    logging.warning("Output filename is not definied, results are not being saved.")

            self.restart_trial()

    def retry_trial_click(self):
        """
        Retry the trial, don't save the last trials results.

        Returns:
            None
        """
        self.restart_trial()

    def on_clock_select_change(self):
        """
        Triggered anytime the user selects a time on the clock.
        """

        selected_time = self.clock_widget.selected_time

        # If we are in urge mode, and the user has not selected a urge time, do not allow next trial
        # until they have done so.
        if self.urge_mode:
            if selected_time is not None:
                self.button_next.setEnabled(True)
            else:
                # Don't turn of the next\stop button unless the clock is stopped!
                self.button_next.setEnabled(False)


def main():
    import sys
    app = QtWidgets.QApplication(sys.argv)
    ui = LibetMainWindow(None)
    ui.showNormal()

    # Show the instructions and ask for an output file name. Do some error
    # checking if the file isn't valid.
    fileNoGood = True
    while fileNoGood:
        # Try to open the output file for writing
        try:
            intro_d = IntroDialog()
            intro_d.show()
            intro_d.textbox_file.setFocus()
            intro_d.exec_()

            # Grab the filename from the textbox
            filename = intro_d.textbox_file.text()

            # Check if the file exists already, make sure they want to overwrite?
            if os.path.isfile(filename):
                qm = QtWidgets.QMessageBox
                retval = qm.question(intro_d, "", "This file already exists. "
                                                  "Are you sure you want it to be overwritten?",
                                     qm.Yes | qm.No)

                if retval == qm.No:
                    continue

            # Check if we can open the file. If so, set the output file on the main app
            # and we are ready to go!
            with open(filename, 'w') as f:
                fileNoGood = False
                ui.output_filename = intro_d.textbox_file.text()

        except Exception as ex:
            msg = QtWidgets.QMessageBox()
            msg.setIcon(QtWidgets.QMessageBox.Critical)
            msg.setText("Output file could not be opened. Check the path.")
            msg.setDetailedText(f"{ex}")
            msg.setWindowTitle("Output File Error")
            msg.setStandardButtons(QtWidgets.QMessageBox.Ok)
            msg.exec_()

    # Run the main app
    sys.exit(app.exec_())


if __name__ == "__main__":
    main()