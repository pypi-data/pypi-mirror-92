"""
This module contains the smart backspace mode
"""
from pyqode.qt.QtCore import Qt
from pyqode.core.api import Mode


class SmartBackSpaceMode(Mode):
    """ Improves backspace behaviour.

    If the cursor is at the end of a line, then all trailing whitespace is
    removed at once. If the cursor is not at the end of a line, but preceded
    by whitespace, then we de-indent to the next level. Otherwise, the
    backspace just works as a regular backspace.
    """
    
    def on_state_changed(self, state):
        if state:
            self.editor.key_pressed.connect(self._on_key_pressed)
        else:
            self.editor.key_pressed.disconnect(self._on_key_pressed)

    def _on_key_pressed(self, event):
        if (
            event.key() != Qt.Key_Backspace or
            event.modifiers() != Qt.NoModifier or
            event.isAccepted()
        ):
            return
        cursor = self.editor.textCursor()
        cursor.beginEditBlock()
        # If there's a selection, delete it
        if cursor.hasSelection():
            cursor.removeSelectedText()
        # If we're at the start of a block, simply delete the previous
        # character, which is the newline that takes the cursor to the previous
        # block. If the cursor was initially at a line of only whitespace, we
        # delete the whitespace so that it's not carried over to the previous
        # block.
        elif cursor.atBlockStart():
            if cursor.block().text().isspace():
                cursor.movePosition(cursor.EndOfBlock, cursor.KeepAnchor)
                cursor.removeSelectedText()
            cursor.deletePreviousChar()
        else:
            orig_pos = cursor.position()
            # Select all the whitespace before the cursor
            while not cursor.atBlockStart():
                cursor.movePosition(
                    cursor.Left,
                    cursor.KeepAnchor
                )
                if not cursor.selectedText().isspace():
                    cursor.setPosition(cursor.position() + 1)
                    break
            # Select all the characters until the end of the block. If they
            # are all whitespace, delete them all. If not, do a regular
            # backspace.
            cursor.setPosition(cursor.position())
            cursor.movePosition(cursor.EndOfBlock, cursor.KeepAnchor)
            selected_text = cursor.selectedText()
            selected_whitespace = selected_text.isspace() and selected_text
            selected_entire_block = cursor.block().text() == selected_text
            # If we've selected some whitespace, delete this selection. But not
            # if the entire line is whitespace, because then we want
            # to de-indent.
            if selected_whitespace and not selected_entire_block:
                cursor.removeSelectedText()
            # Otherwise, return the cursor to its original position and
            # fall back to a de-indent-like behavior, such that as many
            # whitespaces are removed as are necessary to de-indent by one
            # level.
            else:
                cursor.setPosition(orig_pos)
                # If there's only whitespace on the line, we also remove the
                # trailing whitespace.
                if selected_whitespace:
                    cursor.movePosition(cursor.EndOfBlock, cursor.KeepAnchor)
                    cursor.removeSelectedText()
                if self.editor.use_spaces_instead_of_tabs:
                    cursor_pos = cursor.positionInBlock()
                    n_del = cursor_pos % self.editor.tab_length
                    ch_del = ' '
                    if not n_del:
                        n_del = self.editor.tab_length
                    if n_del > cursor_pos:  # Don't delete beyond the line
                        n_del = cursor_pos
                else:
                    n_del = 1
                    ch_del = '\t'
                for i in range(n_del):
                    cursor.movePosition(
                        cursor.PreviousCharacter,
                        cursor.KeepAnchor
                    )
                    if cursor.selectedText() == ch_del:
                        cursor.removeSelectedText()
                    # The first time, we also delete non-whitespace characters.
                    # However, this means that we are not de-indenting, and
                    # therefore we break out of the loop. In other words, this
                    # is a regular backspace.
                    else:
                        if not i:
                            cursor.removeSelectedText()
                        else:
                            cursor.clearSelection()
                            cursor.movePosition(cursor.Right)
                        break
        cursor.endEditBlock()
        self.editor.setTextCursor(cursor)
        event.accept()
