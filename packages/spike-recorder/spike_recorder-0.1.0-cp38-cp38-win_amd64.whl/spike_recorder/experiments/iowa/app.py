# -*- coding: utf-8 -*-
import sys
import os

from PyQt5 import QtCore, QtGui, QtWidgets

from spike_recorder.experiments.iowa.instructions_ui import Ui_dialog_instructions
from spike_recorder.experiments.iowa.iowa_ui import Ui_main_window
from spike_recorder.experiments.iowa.win_message_ui import Ui_Dialog as Ui_win_message
from spike_recorder.experiments.iowa.deck import Deck
from spike_recorder.experiments.iowa.data import IowaData

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
        filename = f"iowa_output{index}.csv"
        while os.path.isfile(filename):
            index = index + 1
            filename = f"iowa_output{index}.csv"

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


class WinDialog(QtWidgets.QDialog, Ui_win_message):
    """
    A modal dialog that displays wins and losses from a deck pull and pauses the
    experiement for a bit.
    """

    def __init__(self, parent=None, win_amount=0, loss_amount=0, delay_seconds=3):
        QtWidgets.QDialog.__init__(self, parent)
        self.setupUi(self)

        self.label.setText(f'<html><head/><body><p style="color:#0571b0">Win: ${win_amount}</p>'
                           f'<p style="color:#ca0020">Loss: ${loss_amount}</p></body></html>')

        self.lcdNumber.display(delay_seconds)

        # Setup a time to invoke the render function and see if its time to close
        timer = QtCore.QTimer(self)
        timer.timeout.connect(self.update)
        timer.start(1000)

    def update(self):
        """
        Update the countdown timer, close the dialog when it is done.

        Returns:
            None
        """
        self.lcdNumber.display(self.lcdNumber.intValue() - 1)

        if self.lcdNumber.intValue() == 0:
            self.done(0)


class IowaMainWindow(QtWidgets.QMainWindow, Ui_main_window):
    """
    The main window GUI for the Iowa Gambling task experiment.
    """

    # The maximum number of deck pulls to allow the user.
    MAX_DECK_PULLS = 100

    MAX_WINNINGS = MAX_DECK_PULLS * 350

    MAX_LOSSES = MAX_DECK_PULLS * 350

    # The starting winnings
    INITIAL_WINNINGS = 2000

    # How long to pause between deck pulls
    DELAY_SECS = 3

    def __init__(self, *args, **kwargs):
        QtWidgets.QMainWindow.__init__(self, *args, **kwargs)
        self.setupUi(self)

        # Setup the exerpiment status variables
        self.winnings = self.INITIAL_WINNINGS
        self.losses = 0
        self.last_win = 0
        self.last_loss = 0
        self.deck_pull_index = 0
        self.is_hunch = False
        self.is_sure = False

        self.progress_winnings.setMaximum(self.MAX_WINNINGS)
        self.progress_losses.setMaximum(self.MAX_LOSSES)

        # Define the deck behaviour
        deck1 = Deck.make_finite_deck(win_amounts=100,
                               loss_amounts=[0, 150, 200, 250, 300, 350],
                               loss_weights=[50, 10, 10, 10, 10, 10])
        deck2 = Deck.make_finite_deck(win_amounts=100,
                               loss_amounts=[0, 1250],
                               loss_weights=[90, 10])
        deck3 = Deck.make_finite_deck(win_amounts=50,
                               loss_amounts=[0, 25, 50, 75],
                               loss_weights=[40, 30, 20, 10])
        deck4 = Deck.make_finite_deck(win_amounts=50,
                               loss_amounts=[0, 250],
                               loss_weights=[90, 10])

        # Assign each deck to a button
        self.decks = {self.deck_button1: deck1,
                      self.deck_button2: deck2,
                      self.deck_button3: deck3,
                      self.deck_button4: deck4}

        # Send all the deck button presses to a single handler
        for button, deck in self.decks.items():
            button.clicked.connect(self.deck_button_pressed)

        self.hunch_button.clicked.connect(self.update_hunch)

        # Update the status
        self.update_status()

        # Setup the data recording
        self.data = IowaData()

    def deck_button_pressed(self):
        """
        The user has drawn from a deck. Lets see what they win. This is the main event of the application.

        Returns:
            None
        """

        # Get the button that was clicked
        button = self.sender()

        # Get the deck for this button
        deck = self.decks[button]

        deck_index = list(self.decks.values()).index(deck)

        # Pull a card from this deck
        (win_amount, loss_amount) = deck.pull()

        self.winnings = self.winnings + win_amount
        self.losses = self.losses + loss_amount
        self.last_win = win_amount
        self.last_loss = loss_amount

        # Update the status display
        self.update_status()

        # Add the data and rewrite the experiemental data to the file.
        self.data.add_trial(deck=deck_index, win_amount=win_amount, loss_amount=loss_amount,
                            hunch=self.is_hunch, sure=self.is_sure)

        # Dump the data back out to file. We will just dump everything back out over and over again
        # so that if the user stops half way through, they have part of their data.
        if self.output_filename is not None:
            self.data.to_csv(self.output_filename)
        else:
            logging.warning("Output filename is not definied, results are not being saved.")

        if self.DELAY_SECS and self.DELAY_SECS > 0:
            win_diag = WinDialog(win_amount=win_amount, loss_amount=loss_amount, delay_seconds=self.DELAY_SECS)
            win_diag.exec_()

        if self.get_num_pulls() >= self.MAX_DECK_PULLS:
            msg = QtWidgets.QMessageBox()
            msg.setText("Experiment Complete!")
            msg.setWindowTitle("Done")
            msg.setStandardButtons(QtWidgets.QMessageBox.Ok)
            msg.exec_()

            self.close()


    def update_hunch(self):
        """
        Allow the user to record when they get a hunch by pressing a button.

        Returns:
            None
        """
        if not self.is_hunch:
            self.is_hunch = True
            self.hunch_button.setText("I am pretty sure!")

            # Set event to spike recorder to mark in the recording when a hunch was recorded
        else:
            if not self.is_sure:
                self.is_sure = True
                self.hunch_button.setEnabled(False)

                # Set and event in the spike recorder to mark in the recording when the user is sure.


    def get_num_pulls(self):
        """
        Check how many pulls we have made on the decks.

        Returns:
            The number of pulls
        """
        return sum([deck.num_pulls for button, deck in self.decks.items()])

    def update_status(self):
        """
        Update any status fields with the current state of the experiment.

        Returns:
            None
        """
        self.label_last_win.setText(f'Winnings on last trial: <font color="#0571b0">${self.last_win}</font>')
        self.label_last_loss.setText(f'Losses on last trial: <font color="#ca0020">${self.last_loss}</font>')
        net = self.last_win - self.last_loss
        color = "#0571b0" if net >= 0 else "#ca0020"
        self.label_net_win.setText(f'Net Winnings: <font color="{color}">${net}</font>')
        self.label_pull_count.setText(f"Pull {self.get_num_pulls()}/{self.MAX_DECK_PULLS}")

        # Update the progress bars
        self.progress_winnings.setValue(self.winnings)
        self.progress_winnings.setFormat(f"${self.winnings}")
        self.progress_losses.setValue(self.losses)
        self.progress_losses.setFormat(f"${self.losses}")


def main():
    import sys
    app = QtWidgets.QApplication(sys.argv)
    ui = IowaMainWindow(None)
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