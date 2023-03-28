#!/usr/bin/python3
# coding=utf-8
###############################################################################
#    Copyright 2023 Michael Ryan Hunsaker, M.Ed., Ph.D.                       #
#    email: hunsakerconsulting@gmail.com                                      #
#                                                                             #
#    Licensed under the Apache License, Version 2.0 (the "License");          #
#    you may not use this file except in compliance with the License.         #
#    You may obtain a copy of the License at                                  #
#                                                                             #
#        http://www.apache.org/licenses/LICENSE-2.0                           #
#                                                                             #
#    Unless required by applicable law or agreed to in writing, software      #
#    distributed under the License is distributed on an "AS IS" BASIS,        #
#    WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied. #
#    See the License for the specific language governing permissions and      #
#    limitations under the License.                                           #
###############################################################################

import os
import random
import textwrap
from pathlib import Path

import louis
import wx
import wx.html
import wx.html2
import wx.lib.scrolledpanel as scrolled

defaultDir = '/mnt/c/Users/ryhunsaker/OneDrive/Desktop'

os.chdir(
        os.path.dirname(
                os.path.abspath(
                        __file__
                        )
                )
        )
ROOT_DIR = os.path.dirname(
        os.path.abspath(
                __file__
                )
        )

justRight = wx.Colour(239, 214, 192)
whiteRock = wx.Colour(241, 240, 226)
khaki = wx.Colour(238, 231, 142)
poloBlue = wx.Colour(136, 150, 198)
downy = wx.Colour(107, 205, 156)
twilight = wx.Colour(224, 199, 215)
coral = wx.Colour(255, 140, 85)
heather = wx.Colour(191, 202, 214)
colorList = [justRight, whiteRock, khaki, poloBlue, downy, twilight, coral, heather]


class mainDisplay(scrolled.ScrolledPanel):
    """

    """

    def __init__(
            self,
            parent
            ):
        scrolled.ScrolledPanel.__init__(
                self,
                parent,
                -1
                )
        vbox = wx.BoxSizer(
                wx.VERTICAL
                )
        vbox.Add(
                wx.StaticLine(
                        self,
                        -1,
                        size = (
                                2000,
                                -1)
                        ),
                0,
                wx.ALL,
                5
                )
        vbox.Add(
                wx.StaticLine(
                        self,
                        -1,
                        size = (
                                -1,
                                2000)
                        ),
                0,
                wx.ALL,
                5
                )
        vbox.Add(
                (
                        20,
                        20
                        )
                )
        self.SetSizer(
                vbox
                )
        self.SetupScrolling()
        self.SetBackgroundColour(
                random.choice(
                        colorList
                        )
                )
        # Panel title
        wx.StaticText(
                self,
                -1,
                "TEXT INPUT",
                pos = (
                        80,
                        125
                        ),
                size = (
                        720,
                        30
                        ),
                style = wx.ALIGN_CENTRE_HORIZONTAL
                )
        wx.StaticText(
                self,
                -1,
                "BRAILLE OUTPUT",
                pos = (
                        850,
                        125
                        ),
                size = (
                        720,
                        30
                        ),
                style = wx.ALIGN_CENTRE_HORIZONTAL
                )
        self.text = wx.TextCtrl(
                self,
                -1,
                style = wx.TE_RICH2 | wx.TE_MULTILINE,
                pos = (
                        80,
                        180
                        ),
                size = (
                        720,
                        800
                        )
                )
        self.text.SetFont(
                wx.Font(
                        16,
                        wx.MODERN,
                        wx.NORMAL,
                        wx.NORMAL,
                        False,
                        u'JetBrains Mono NL'
                        )
                )
        self.braille = wx.TextCtrl(
                self,
                -1,
                style = wx.TE_RICH2 | wx.TE_MULTILINE,
                pos = (
                        850,
                        180
                        ),
                size = (
                        720,
                        800
                        )
                )
        self.braille.SetFont(
                wx.Font(
                        16,
                        wx.MODERN,
                        wx.NORMAL,
                        wx.BOLD,
                        False,
                        u'Braille29'
                        )
                )
        self.btn1 = wx.Button(
                self,
                202,
                "SAVE",
                pos = (
                        700,
                        1000
                        ),
                size = (
                        70,
                        30
                        )
                )
        self.btn2 = wx.Button(
                self,
                203,
                "OPEN",
                pos = (
                        800,
                        1000
                        ),
                size = (
                        70,
                        30
                        )
                )
        self.Btn = wx.Button(
                self,
                201,
                "EXIT",
                pos = (
                        900,
                        1000
                        ),
                size = (
                        70,
                        30
                        )
                )
        self.Bind(
                wx.EVT_BUTTON,
                self.OnQuit,
                id = 201
                )
        self.Bind(
                wx.EVT_BUTTON,
                self.OnSave,
                id = 202
                )
        self.Bind(
                wx.EVT_BUTTON,
                self.OnOpen,
                id = 203
                )

    def OnQuit(
            self,
            e
            ):
        wx.Exit()

    def OnSave(
            self,
            e
            ):
        brailleFile = self.braille.GetValue()
        with wx.FileDialog(
                self,
                "Save braille file",
                defaultDir,
                wildcard = "BRF files (*.brf)|*.brl",
                style = wx.FD_SAVE | wx.FD_OVERWRITE_PROMPT
                ) as fileDialog:

            if fileDialog.ShowModal() == wx.ID_CANCEL:
                return  # the user changed their mind

            # save the current contents in the file
            pathname = fileDialog.GetPath()
            try:
                with open(
                        pathname,
                        'w'
                        ) as file:
                    file.write(brailleFile)
                    file.close()
            except IOError:
                wx.LogError(
                        "Cannot save current data in file '%s'." % pathname
                        )

    def OnOpen(
            self,
            e
            ):
        with wx.FileDialog(
                self,
                "Open Text file",
                defaultDir,
                wildcard = "Text files (*.txt,*.md)|*.txt; *.md",
                style = wx.FD_OPEN | wx.FD_FILE_MUST_EXIST
                ) as fileDialog:

            if fileDialog.ShowModal() == wx.ID_CANCEL:
                return  # the user changed their mind

                # Proceed loading the file chosen by the user
            pathname = fileDialog.GetPath()

            try:
                with open(
                        pathname,
                        'r'
                        ) as file:
                    self.text.SetValue(
                            file.read()
                            )

                tmp = os.path.splitext(
                        pathname
                        )[0]
                print(tmp)
                fileOut = Path(
                        tmp
                        ).with_suffix(
                        '.brf'
                        )
                print(
                        fileOut
                        )
                Path.touch(
                        fileOut
                        )
                tableList = ['unicode.dis', 'en-ueb-g2.ctb']
                lineLength = 40
                with open(
                        pathname,
                        'r'
                        ) as file:
                    with open(
                            fileOut, 'wt'
                            ) as outputFile:
                        for line in file:
                            line2 = line.strip()
                            if len(line2) > 0:
                                translation = louis.translateString(
                                        tableList,
                                        line2,
                                        0,
                                        0
                                        )
                                outputFile.write(
                                        textwrap.fill(
                                                translation,
                                                lineLength,
                                                initial_indent = '  '
                                                )
                                        )
                                outputFile.write(
                                        '\n'
                                        )
                with open(
                        fileOut,
                        'r'
                        ) as braillefile:
                    print(
                            braillefile
                            )
                    self.braille.SetValue(
                            braillefile.read()
                            )
                    self.braille.SetFont(
                            wx.Font(
                                    18,
                                    wx.MODERN,
                                    wx.NORMAL,
                                    wx.BOLD,
                                    False,
                                    u'Braille29'
                                    )
                            )
                braillefile.close()
            except IOError:
                wx.LogError(
                        "Cannot open file '%s'."
                        )


class Transcription(
        wx.Frame,
        wx.Accessible
        ):
    """

    """

    def __init__(
            self,
            parent,
            title
            ):
        super(
                Transcription,
                self
                ).__init__(
                parent,
                title = "Braille Proofreading System",
                size = (
                        1650,
                        1200
                        )
                )
        self.SetBackgroundColour(
                random.choice(
                        colorList
                        )
                )
        self.SetFont(
                wx.Font(
                        14,
                        wx.MODERN,
                        wx.NORMAL,
                        wx.NORMAL,
                        False,
                        u'JetBrains Mono NL'
                        )
                )
        self.initui()

    def initui(self):
        """

        """
        nb = wx.Notebook(
                self
                )
        nb.AddPage(
                mainDisplay(nb),
                "BRAILLE PROOFREADING PROGRAM"
                )
        self.Centre()
        self.Show(True)


app = wx.App()
frame = Transcription(
        None,
        'Braille Transcription Proofer'
        )

frame.Centre()
frame.Show()
app.MainLoop()
