# WUSF1
A new way to exploit F1 data, thanks to [Fastf1](https://docs.fastf1.dev/index.html) and Python. 🏎️

<img width="1896" height="901" alt="image" src="https://github.com/user-attachments/assets/cca294df-9d2d-422c-b228-6e159a4fcd0d" />

# 📋Features
- **GUI Menu**: Allows user to easly choose the session to load, and to navigate through the menus
- **Multiple representations**
  - 📈 Graphs: A traditional and clean way to exploit available data
    - Speed, RPM, Gear, Throttle, Brake (on-off), DRS (on-off)
  - 📊 Histograms: A more direct and concise alternative representation (Speed, RPM, Gear and Throttle only)
  - 🔢 Statistics: A table showing vital statistics (minimum, maximum, mean, median and standard deviation) of all available channels
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
- Python 3.8+
- [Fastf1](https://docs.fastf1.dev/index.html)
- Numpy
- Dearpygui
- Datetime

# 💻 Usage
1. In the upper left of the GUI menu **fill** following inputs, following examples:

    <img width="329" height="207" alt="image" src="https://github.com/user-attachments/assets/8fc45e63-84b8-4b47-a620-605ddd480570" />
    
    - **Session**: R -> Race, Q -> Qualy , FPx -> Practice x (Testing sessions considered as practice sessions)
    - **Track**: Type the name of the track/country
    - **Year**: From 2018 to the present
    - **Driver**: His abbreviation (3 capital letters)

      *For more info check [Fastf1 documentation](https://docs.fastf1.dev/events.html).
    - If desired, click the 'Compare' checkbox to show the second driver input field
2. Click **'Show Telemetry'** to display data
    - Select the lap scrolling trough the horizontal menu, fastest lap will be displayed in purple and loaded first by default
3. Choose representation by clicking on **'View'** in the top left
4. Happy Telemetry!



# 🤝License and contributing
This project is under [MIT license](https://tlo.mit.edu/understand-ip/exploring-mit-open-source-license-comprehensive-guide). Feel free to contribute to this project fixing bugs, adding [roadmap's](https://github.com/realbou17/WUSF1/blob/main/roadmap.md) features or even more...
