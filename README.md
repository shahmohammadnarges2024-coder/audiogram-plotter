Audiogram Plotting Tool

A Python script for generating publication-quality pure-tone audiograms by entering hearing thresholds directly.
The tool is intended for clinical and genetic hearing-loss studies and produces clean, consistent figures suitable for journal submission.

Requirements: Python 3.8 or newer, with matplotlib and numpy installed.

Usage:
Run the script audiogram_tool_input_thresholds.py.
Enter a subject ID (for example, II-1).
Enter six thresholds for the right ear and six thresholds for the left ear in the following order: 250, 500, 1000, 2000, 4000, 8000 Hz (dB HL).
Type q to exit the program.

Output:
All audiograms are saved automatically in the fig_out_final directory.
Each figure is exported as a PNG, TIFF, PDF, or SVG file, with filenames based on the subject ID.

Author:
Narges Shahmohammad
Qazvin University of Medical Sciences, Iran

License:
For academic and research use only
