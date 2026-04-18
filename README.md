# WUSF1
A new way to exploit F1 data, thanks to [Fastf1](https://docs.fastf1.dev/index.html) and Python. 🏎️

<img width="1886" height="820" alt="image" src="./resources/Graphs.png" />

# 📋Features
- **GUI Menu**: Allows user to easly choose the session to load, and to navigate through the menus
- **Multiple representations**
  - 📈 **Graphs**: A traditional and clean way to exploit available data
    - Speed, RPM, Gear, Throttle, Brake (on-off), Glon, DRS (on-off)
  - 📊 **Histograms**: A more direct and concise alternative representation (Speed, RPM, Gear and Throttle only)
  - 🔵 **Scatter**: A visual correlation tool that plots two channels against each other to reveal relationships — ideal for variables like RPM vs Speed (for gear ratios and optimization) or Glon vs Speed (to spot car balance at different speeds)
  - 🔢 **Statistics**: A table showing vital statistics (minimum, maximum, mean, median and standard deviation) of all available channels
  - 🛰️ **Track**: The outline of the track loaded, with a dot representing the position of the car according to mouse position in the graphs
- **All sessions available**: Watch telemetry from every session since 2018, including FPs, qualy, races and even winter tests
- **Customization**:
    - Choose between driver's team color or a traditional color palette for telemetry channels
    - Hide input fileds for a clearer visualization
- **Comparison**: Compare telemetry for up to 2 drivers


# ⚙️ Requirements
**Easy to install:**
```bash
pip install -r requirements.txt
```
- Python 3.10+
- [Fastf1](https://docs.fastf1.dev/index.html)
- Numpy
- Dearpygui
...

# 💻 Usage
1. In the upper left of the GUI menu **fill** following inputs, following examples:

    \*latest session will be loaded by default

    <img width="390" height="266" alt="image" src="./resources/Inputfield.png" />

    - **Session**: R -> Race, Q -> Qualy , FPx -> Practice x (Testing sessions considered as practice sessions)
    - **Track**: Select the name of the track/country by unfolding the dropdown menu
    - **Year**: From 2018 to the present
    - **Driver**: His abbreviation (3 capital letters)

      *For more info check [Fastf1 documentation](https://docs.fastf1.dev/events.html).
    - If desired, click the 'Compare' checkbox to show the second driver input field
2. Click **'Show Telemetry'** to display data
    - Select the lap scrolling trough the horizontal menu, fastest lap will be displayed in purple and loaded first by default
3. Choose representation by switching **tabs** in the top left
4. Happy Telemetry!



# 🤝License and contributing
This project is under [MIT license](https://tlo.mit.edu/understand-ip/exploring-mit-open-source-license-comprehensive-guide). Feel free to contribute to this project fixing bugs, adding [roadmap's](https://github.com/realbou17/WUSF1/blob/main/roadmap.md) features or even more...
