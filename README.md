# QuickTableFormat

**Author:** Richard Sitányi (richard@cdbox.sk)

**File:** QuickTableFormat.py

**Version:** 1.0

**Date:** 12/15/2025

## Description

QuickTableFormat is a Python script which, as the name suggests, is used for quick table formatting in Scribus.

With one click, you can set the inner padding of cells, table color, table border style, and cell border style.

## Important information

1. For table color, you can only set the color, you cannot set the shade. Scribus does have a setFillShade() function that allows you to set the shade for a table, but the set value is not displayed in the Table Properties dialog box in Scribus, so it is unusable. The shade is not even displayed in this window even if it is set in the table style for a specific color. The combination of the setFillColor() and setFillShade() functions works for text frames, but for table frames, only the setTableFillColor() function is available, and the setTableFillShade() function is missing. This is probably a bug in Scribus.

2. All colors are taken from Edit > Colors and Fills, which means that the colors you use in the document will also be used in the script.

3. There are only 5 border styles. The rest are not accessible via the Scribus API.

4. If you format the table so that the table border has a different color than the cell border, I recommend that you set the width for the table border slightly wider than for the cell border. This is because if the table border is the same width or narrower than the cell border, Scribus will display it incorrectly. This is probably a bug in Scribus.

5. Scribus does not redraw table immediately. User must:

* click outside the table or
* close the script window or
* change zoom level to force a redraw.

## Tested on versions

Script has been tested on:

* **Scribus 1.6.4 (stable)**
* **Scribus 1.7.0 (development)**
