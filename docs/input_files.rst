Input files
===========

:py:mod:`edxia` requires raw maps in text format from the microscope/EDS software.
The text format is required to easily accept data from various acquisition software.

The text format must be one of the various csv-type formats.
The exact delimiter, and normalization to apply are described by :py:class:`edxia.io.raw_io.TextMapFormat`.
Several predefined format are available in this module (:py:mod:`edxia.io.raw_io`).

All maps from a a set must be in the same folder.
Using the default classes, the user only select the BSE map, and the program find the other maps available based on the filenames.
For example, the following is a valid set of names for the maps:

    - cement/durability/slag_28d_BSE.txt
    - cement/durability/slag_28d_Ca.txt
    - cement/durability/slag_28d_Al.txt
    - cement/durability/slag_28d_Si.txt

 The corresponding pattern would be
 
    - cement/durability/slag_28d_component}.txt
    
The choice of this pattern was made to avoid selecting every single patterns.
However, it means that the name of the files need to be consistent so they can be recognized.


This is the default in :mod:edxia: but the user can defines it's own loading functions by specializing :py:class:`edxia.io.loader.base_loader.AbstractLoader`.
