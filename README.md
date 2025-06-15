# AnatoLabel - Injury Labeling Tool

AnatoLabel is a Python-based graphical tool for annotating anatomical regions on an image with Abbreviated Injury Scale (AIS) levels. It allows users click on predefined body parts, assign an AIS score, repeat it for multiple cases and save the annotations to a JSON file. The tool also provides a report feature to visualize injury frequency across multiple cases.

## Screenshot

![Tool Screenshot](Tool_exampl.png)

## Features

*   **Interactive Annotation**:
    *   Clickable body parts on a base anatomical image.
    *   Enter the case number press Enter and start annotating.
*   **AIS Level Assignment**:
    *   Click on a body part to open a prompt for AIS score (1-6).
    *   Input AIS level via radio buttons or number keys (1-6).
    *   Confirm selection with Enter key or "Confirm" button.
    *   Cancel or close the AIS window to discard the selection.
*   **Toggle Annotation**: Clicking an already annotated part removes the annotation.
*   **Visual Feedback**: Selected body parts are highlighted on the canvas with a fill color corresponding to their AIS level.
*   **Annotation List**: Annotated parts (label and AIS level) are displayed in a listbox.
*   **Data Persistence**:
    *   Save annotations to a JSON file (`annotations.json`).
    *   Annotations are stored per case number.
*   **Case Management**:
    *   Start a new case (clears current annotations).
    *   Import existing datasets from JSON files.
*   **Reporting**: Generate a summary view showing body parts shaded by injury frequency across all annotated cases.
*   **Keyboard Shortcuts**:
    *   `Ctrl+S`: Save current annotations.
    *   `Ctrl+N`: Start a new case (clear current annotations).
    *   `Enter`: Move the focus from the case number entry to the canvas for annotation.
    *   AIS Window:
        *   Number keys `1` to `6`: Select AIS level directly in the AIS window.
        *   `Enter`: Confirm AIS level selection in the AIS window.
        *   `Esc`: Cancel AIS level selection.


## Requirements

*   Python 3.x
*   Tkinter (usually included with Python standard library)

## Setup and Running

1.  **Clone the repository:**
    ```bash
    git clone https://github.com/Rahul-Pi/AnatoLabel.git
    cd AnatoLabel
    ```
    Alternatively, you can download the repository as a ZIP file and extract it to your desired location.
2.  **Place the necessary files in the same directory:**
    *   `injury_label_tool.py` (the main application script)
    *   `anatomial_config.py` (the configuration file for body regions and colors)
    *   `Tool_exampl.png` (the base image for annotation)
3.  **Run the application:**
    Open a terminal or command prompt, navigate to the directory containing the files, and execute:
    ```bash
    python injury_label_tool.py
    ```

## 🛠 How to Use

1.  **Enter Case Number**: Start by entering a unique case number in the "Case #:" field.
2.  **Annotate Body Parts**:
    *   Click on a body part on the image.
    *   A pop-up window will appear. Select the AIS level (1-6) using the radio buttons or by pressing the corresponding number key.
    *   Press Enter or click "Confirm" to save the AIS level for that part.
    *   To remove an annotation, click on an already highlighted body part.
3.  **View Annotations**: The listbox on the right will display all current annotations for the active case (e.g., "head: AIS4").
4.  **Save Annotations**:
    *   Press `Ctrl+S` after annotating each case.
    *   All annotations are saved in a single file `annotations.json`.
5.  **New Case**: Press `Ctrl+N` to clear the current annotations and start a new case. Remember to enter a new case number.
6.  **Import Dataset**: Click the "Import Dataset" button to load annotations from an existing JSON file. This will merge the loaded data with any existing data in memory.
7.  **Report**: Click the "Report" button to view a visual summary of injury frequencies across all loaded cases. Body parts will be colored based on how often they have been annotated.


## 🤝 Contribute

Contributions are welcome! If you find a bug or have a feature request, please open an issue on the GitHub repository. Pull requests are also welcome.

## 📜 License

This project is licensed under the GNU General Public License v3.0. See the [LICENSE](LICENSE) file for details.