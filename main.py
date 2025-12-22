import dearpygui.dearpygui as dpg
import fastf1
from fastf1 import plotting
import numpy as np
from datetime import datetime, timezone
import os

# Global variables
current_view = "telemetry"
telemetry_data = {}
telemetry_data2 = {}
track = {}
latest_year = 0
sessionID = {}
session = {}
hex_color = {}
hex_color2 = {}
r = 0
g = 0
b = 0
r2 = 0
g2 = 0
b2 = 0
driver = {}
driver2 = {}
lap_int = 0
lap_int2 = 0
lap_num2 = 0
lap_num = 0
lap = 0

cache_dir = "fastf1_cache"
os.makedirs(cache_dir, exist_ok=True)
fastf1.Cache.enable_cache(cache_dir)

def load_latest_session():
    global track, latest_year, sessionID

    now = datetime.now(timezone.utc).replace(tzinfo=None)
    latest_year = now.year
    schedule = fastf1.get_event_schedule(latest_year)
    past_events = schedule[schedule['EventDate'] < now]

    if past_events.empty:
        print("There are no past events this year.")
        return False

    last_event = past_events.iloc[-1]
    track = last_event['EventName']
    round_number = int(last_event['RoundNumber'])

    session_order = ['R', 'Q', 'S', 'SQ', 'SS', 'FP3', 'FP2', 'FP1']
    
    for order in session_order:
        try:
            session = fastf1.get_session(latest_year, round_number, order)
            session.load(laps=False, telemetry=False, weather=False)
            if session.date < now:
                sessionID = order
                print(f"Loaded latest session: {track} - {order}")
                return True
        except:
            continue
            
    print("No completed session found for the latest event.")
    return False
load_latest_session()

def create_interface():
    global track, sessionID

    dpg.create_context()
    # Custom colors for graph
    with dpg.theme(tag="speed_theme"):
        with dpg.theme_component(dpg.mvLineSeries):
            dpg.add_theme_color(dpg.mvPlotCol_Line, (0, 0, 255), category=dpg.mvThemeCat_Plots)  # Blue
        with dpg.theme_component(dpg.mvBarSeries):
            dpg.add_theme_color(dpg.mvPlotCol_Fill, (0, 0, 255, 200), category=dpg.mvThemeCat_Plots)
    with dpg.theme(tag="speed_theme2"):
        with dpg.theme_component(dpg.mvLineSeries):
            dpg.add_theme_color(dpg.mvPlotCol_Line, (255, 255, 255, 200), category=dpg.mvThemeCat_Plots)  # White
        with dpg.theme_component(dpg.mvBarSeries):
            dpg.add_theme_color(dpg.mvPlotCol_Fill, (255, 255, 255, 200), category=dpg.mvThemeCat_Plots)

    with dpg.theme(tag="rpm_theme"):
        with dpg.theme_component(dpg.mvLineSeries):
            dpg.add_theme_color(dpg.mvPlotCol_Line, (255, 105, 180, 255), category=dpg.mvThemeCat_Plots)  # Pink
        with dpg.theme_component(dpg.mvBarSeries):
            dpg.add_theme_color(dpg.mvPlotCol_Fill, (255, 105, 180, 200), category=dpg.mvThemeCat_Plots)
    with dpg.theme(tag="rpm_theme2"):
        with dpg.theme_component(dpg.mvLineSeries):
            dpg.add_theme_color(dpg.mvPlotCol_Line, (255, 255, 255, 200), category=dpg.mvThemeCat_Plots)  # White
        with dpg.theme_component(dpg.mvBarSeries):
            dpg.add_theme_color(dpg.mvPlotCol_Fill, (255, 255, 255, 200), category=dpg.mvThemeCat_Plots)

    with dpg.theme(tag="gear_theme"):
        with dpg.theme_component(dpg.mvLineSeries):
            dpg.add_theme_color(dpg.mvPlotCol_Line, (255, 165, 0, 255), category=dpg.mvThemeCat_Plots)  # Orange
        with dpg.theme_component(dpg.mvBarSeries):
            dpg.add_theme_color(dpg.mvPlotCol_Fill, (255, 165, 0, 200), category=dpg.mvThemeCat_Plots)
    with dpg.theme(tag="gear_theme2"):
        with dpg.theme_component(dpg.mvLineSeries):
            dpg.add_theme_color(dpg.mvPlotCol_Line, (255, 255, 255, 200), category=dpg.mvThemeCat_Plots)  # White
        with dpg.theme_component(dpg.mvBarSeries):
            dpg.add_theme_color(dpg.mvPlotCol_Fill, (255, 255, 255, 200), category=dpg.mvThemeCat_Plots)

    with dpg.theme(tag="throttle_theme"):
        with dpg.theme_component(dpg.mvLineSeries):
            dpg.add_theme_color(dpg.mvPlotCol_Line, (0, 255, 0, 255), category=dpg.mvThemeCat_Plots)  # Green
        with dpg.theme_component(dpg.mvBarSeries):
            dpg.add_theme_color(dpg.mvPlotCol_Fill, (0, 255, 0, 255), category=dpg.mvThemeCat_Plots)
    with dpg.theme(tag="throttle_theme2"):
        with dpg.theme_component(dpg.mvLineSeries):
            dpg.add_theme_color(dpg.mvPlotCol_Line, (255, 255, 255, 200), category=dpg.mvThemeCat_Plots)  # White
        with dpg.theme_component(dpg.mvBarSeries):
            dpg.add_theme_color(dpg.mvPlotCol_Fill, (255, 255, 255, 200), category=dpg.mvThemeCat_Plots)

    with dpg.theme(tag="brake_theme"):
        with dpg.theme_component(dpg.mvLineSeries):
            dpg.add_theme_color(dpg.mvPlotCol_Line, (255, 0, 0, 255), category=dpg.mvThemeCat_Plots)  # Red           
    with dpg.theme(tag="brake_theme2"):
        with dpg.theme_component(dpg.mvLineSeries):
            dpg.add_theme_color(dpg.mvPlotCol_Line, (255, 255, 255, 200), category=dpg.mvThemeCat_Plots)  # White

    with dpg.theme(tag="drs_theme"):
        with dpg.theme_component(dpg.mvLineSeries):
            dpg.add_theme_color(dpg.mvPlotCol_Line, (255, 255, 0, 255), category=dpg.mvThemeCat_Plots)  # Yellow
    with dpg.theme(tag="drs_theme2"):
        with dpg.theme_component(dpg.mvLineSeries):
            dpg.add_theme_color(dpg.mvPlotCol_Line, (255, 255, 255, 200), category=dpg.mvThemeCat_Plots)  # White

    with dpg.theme(tag="purple_button_theme"):
        with dpg.theme_component(dpg.mvButton):
            dpg.add_theme_color(dpg.mvThemeCol_Button, (128, 0, 128, 255), category=dpg.mvThemeCat_Core)  # Purple background
            dpg.add_theme_color(dpg.mvThemeCol_ButtonHovered, (160, 32, 160, 255), category=dpg.mvThemeCat_Core)  # Lighter purple
            dpg.add_theme_color(dpg.mvThemeCol_ButtonActive, (100, 0, 100, 255), category=dpg.mvThemeCat_Core)  # Darker purple

    dpg.create_viewport(title="WUS Telemetry", width=860, height=1100)

    with dpg.window(label="Real F1 Telemetry Graphs", width=1920, height=1008, tag="main_window"):
        with dpg.menu_bar():
            with dpg.menu(label="View"):
                dpg.add_menu_item(label="Telemetry Graphs", callback=lambda: switch_view("telemetry"))
                dpg.add_menu_item(label="Histogram", callback=lambda: switch_view("histogram"))
                dpg.add_menu_item(label="Statistics", callback=lambda: switch_view("stats"))

        with dpg.group(horizontal=False, tag="info"):
            dpg.add_text("Fill inputs", wrap=500)
            dpg.add_text("Session:")
            dpg.add_input_text(tag="session_input", hint="E.g: R, Q, FP1...", width=260, default_value=sessionID)
            dpg.add_text("Track:")
            dpg.add_input_text(tag="track_input", hint="E.g: Barcelona", width=260, default_value=track)
            dpg.add_text("Year:")
            dpg.add_input_text(tag="year_input", hint="E.g: 2025", width=260, default_value=latest_year)
            dpg.add_text("Driver (3 capital letters):")
            dpg.add_input_text(tag="driver_input", hint="E.g: PIA", width=260, default_value="PIA")
            with dpg.group(tag="driver_compare", show=False):
                dpg.add_text("Driver to compare (3 capital letters):")
                dpg.add_input_text(tag="driver2_input", hint="E.g: VER", width=260, default_value="VER")
            dpg.add_text("Lap (0 for fastest):", show=False)
            dpg.add_input_text(tag="lap_input", hint="E.g: 1", width=260, default_value=0, show=False)
            dpg.add_text("2nd driver lap (0 for fastest):", show=False)
            dpg.add_input_text(tag="lap_input2", hint="E.g: 1", width=260, default_value=0, show=False)
            dpg.add_spacer(height=5)
            dpg.add_checkbox(label="Compare", callback=compare_inputs, tag="Compare", default_value=False)
            dpg.add_spacer(height=5)
            dpg.add_button(label="Show Telemetry", callback=load_telemetry, height=17)
            dpg.add_spacer(height=5)
            dpg.add_checkbox(label="Team colors", callback=hex_to_rgb, tag="hex", default_value=False)
            dpg.add_spacer(height=5)
            dpg.add_text("", tag="result_text", wrap=1000)
            with dpg.child_window(width=-1, height=70, tag="lap_selector_container", border=False, horizontal_scrollbar=True):
                dpg.add_text("Lap selector:")
            with dpg.child_window(width=-1, height=70, tag="lap_selector_container2", border=False, horizontal_scrollbar=True, show=False):
                dpg.add_text("Compared driver lap selector:")

        dpg.add_checkbox(label="Show info", callback=hide_inputs, tag="Info", default_value=True)
        dpg.add_separator()

        with dpg.child_window(width=-1, height=220, tag="plot_container_speed", show=True):
            pass
        with dpg.child_window(width=-1, height=220, tag="plot_container_rpm", show=True):
            pass
        with dpg.child_window(width=-1, height=220, tag="plot_container_gear", show=True):
            pass
        with dpg.child_window(width=-1, height=220, tag="plot_container_throttle", show=True):
            pass
        with dpg.child_window(width=-1, height=220, tag="plot_container_brake", show=True):
            pass
        with dpg.child_window(width=-1, height=220, tag="plot_container_drs", show=True):
            pass
        with dpg.group(horizontal=True):
            with dpg.child_window(width=0, autosize_x=True, tag="hist_container", show=False):
                pass
        with dpg.group(horizontal=True):
            with dpg.child_window(width=0, autosize_x=False, tag="stats", show=False):
                pass

    dpg.setup_dearpygui()
    dpg.show_viewport()
    dpg.maximize_viewport()
    dpg.start_dearpygui()
    dpg.destroy_context()

def switch_view(view):
    global current_view
    current_view = view
    
    if current_view == "telemetry":
        dpg.show_item("plot_container_speed")
        dpg.show_item("plot_container_rpm")
        dpg.show_item("plot_container_gear")
        dpg.show_item("plot_container_throttle")
        dpg.show_item("plot_container_brake")
        dpg.show_item("plot_container_drs")
        dpg.hide_item("hist_container")
        dpg.hide_item("stats")
    elif current_view == "histogram":
        dpg.hide_item("plot_container_speed")
        dpg.hide_item("plot_container_rpm")
        dpg.hide_item("plot_container_gear")
        dpg.hide_item("plot_container_throttle")
        dpg.hide_item("plot_container_brake")
        dpg.hide_item("plot_container_drs")
        dpg.show_item("hist_container")
        dpg.hide_item("stats")
    elif current_view == "stats":
        dpg.hide_item("plot_container_speed")
        dpg.hide_item("plot_container_rpm")
        dpg.hide_item("plot_container_gear")
        dpg.hide_item("plot_container_throttle")
        dpg.hide_item("plot_container_brake")
        dpg.hide_item("plot_container_drs")
        dpg.hide_item("hist_container")
        dpg.show_item("stats")
    update_plots()

def compare_inputs():
    Compare = dpg.get_value("Compare")

    if Compare:
        dpg.show_item("driver_compare")
        dpg.show_item("lap_selector_container2")
    else:
        dpg.hide_item("driver_compare")
        dpg.hide_item("lap_selector_container2")

def hide_inputs():
    Info = dpg.get_value("Info")
    if not Info:
        dpg.hide_item("info")
    else:
        dpg.show_item("info")

def select_lap_callback(sender, app_data, user_data):
    global lap
    lap = user_data
    dpg.set_value("lap_input", user_data)
    load_data(None)
    update_plots()


def select_lap_callback2(sender, app_data, user_data):
    global lap
    lap = user_data
    dpg.set_value("lap_input2", user_data)
    load_data(None)
    update_plots()

def load_session():
    global session, driver, driver2
    
    dpg.set_value("result_text", "It might take long to load data, be patient and do not close this window.")

    Compare = dpg.get_value("Compare")
    session_input = dpg.get_value("session_input")
    track = dpg.get_value("track_input")
    year = dpg.get_value("year_input")
    driver = dpg.get_value("driver_input")
    driver2 = dpg.get_value("driver2_input") if Compare else {}

    if not track or not year or not driver:
        dpg.set_value("result_text", "Error: Complete track, year and driver.")
        return False
    
    try:
        year_int = int(year)
    except ValueError:
        dpg.set_value("result_text", "Error: Year must be numeric.")
        return False

    try:
        session = fastf1.get_session(year_int, track, session_input)
        session.load()
    except Exception as exc:
        dpg.set_value("result_text", f"The session could not be loaded: {exc}")
        return False
    
def load_data(user_data):
    global lap_int2, lap_int, lap_num, lap_num2, telemetry_data, telemetry_data2, driver, lap, driver2

    Compare = dpg.get_value("Compare")
    lap = dpg.get_value("lap_input")
    if lap == 0:
        print("0")
    else:
        print(lap)
    lap2 = dpg.get_value("lap_input2") if Compare else 0

    dpg.delete_item("lap_selector_container", children_only=True)
    dpg.add_text("Lap selector:", parent="lap_selector_container")
    dpg.delete_item("lap_selector_container2", children_only=True) if Compare else None
    dpg.add_text("Compared driver lap selector:", parent="lap_selector_container2") if Compare else None
    
    try:
        driver_laps = session.laps.pick_driver(driver)
        driver_laps2 = session.laps.pick_driver(driver2) if Compare else None
        lap_numbers = driver_laps['LapNumber'].unique()
        lap_numbers2 = driver_laps2['LapNumber'].unique() if Compare else None
        fastest = driver_laps.pick_fastest()
        fastest2 = driver_laps2.pick_fastest() if Compare else None
        lap_fastest = fastest['LapNumber']
        lap_fastest2 = fastest2['LapNumber'] if Compare else None

        with dpg.group(horizontal=True, parent="lap_selector_container"):
            for lap_num in sorted(lap_numbers):
                button_tag = f"lap_button_{int(lap_num)}"
                if lap_num == lap_fastest:
                    dpg.add_button(
                            label=f"Lap {int(lap_num)}",
                            callback=select_lap_callback,
                            user_data=int(lap_num),
                            width=80,
                            tag=button_tag
                        )

                    dpg.bind_item_theme(button_tag, "purple_button_theme")
                else:
                    dpg.add_button(
                            label=f"Lap {int(lap_num)}",
                            callback=select_lap_callback,
                            user_data=int(lap_num),
                            width=80,
                            tag=button_tag
                        )

        if Compare:            
            with dpg.group(horizontal=True, parent="lap_selector_container2"):
                for lap_num2 in sorted(lap_numbers2):
                    button_tag2 = f"lap_button2_{int(lap_num2)}"
                    if lap_num2 == lap_fastest2:
                        dpg.add_button(label=f"Lap {int(lap_num2)}", callback=select_lap_callback2, user_data=int(lap_num2), width=80, tag=button_tag2)
                        dpg.bind_item_theme(button_tag2, "purple_button_theme")
                    else:
                        dpg.add_button(label=f"Lap {int(lap_num2)}", callback=select_lap_callback2, user_data=int(lap_num2), width=80, tag=button_tag2)
    except Exception as exc:
        dpg.set_value("result_text", f"Error loading laps: {exc}")
        return False

    try:
        lap_int = int(lap)
        lap_int2 = int(lap2)
        if lap_int == 0:
            telemetry = session.laps.pick_driver(driver).pick_fastest().get_telemetry()
            lap_fastest = session.laps.pick_driver(driver).pick_fastest()['LapNumber']
        else:
            lap = session.laps.pick_driver(driver).pick_lap(lap_int)
            telemetry = lap.get_telemetry()
        if Compare:
            if lap_int2 == 0:
                telemetry2 = session.laps.pick_driver(driver2).pick_fastest().get_telemetry()
                lap_fastest2 = session.laps.pick_driver(driver2).pick_fastest()['LapNumber']
            else:
                lap2 = session.laps.pick_driver(driver2).pick_lap(lap_int2)
                telemetry2 = lap2.get_telemetry()
    except Exception as exc:
        dpg.set_value("result_text", f"Telemetry not found: {exc}")
        return False
    
    telemetry_data = {
        "Distance": telemetry["Distance"].to_list(),
        "Speed": telemetry["Speed"].to_list(),
        "RPM": telemetry["RPM"].to_list(),
        "Gear": telemetry["nGear"].to_list(),
        "Throttle": telemetry["Throttle"].to_list(),
        "Brake": telemetry["Brake"].to_list(),
        "DRS": [1 if x >= 10 else 0 for x in telemetry["DRS"].to_list()],
        "Time": telemetry["Time"].dt.total_seconds().to_list()
    }
    if Compare:
        telemetry_data2 = {
            "Distance": telemetry2["Distance"].to_list(),
            "Speed": telemetry2["Speed"].to_list(),
            "RPM": telemetry2["RPM"].to_list(),
            "Gear": telemetry2["nGear"].to_list(),
            "Throttle": telemetry2["Throttle"].to_list(),
            "Brake": telemetry2["Brake"].to_list(),
            "DRS": [1 if x >= 10 else 0 for x in telemetry2["DRS"].to_list()],
            "Time": telemetry2["Time"].dt.total_seconds().to_list()
        }

def update_plots():
    global telemetry_data, telemetry_data2, current_view, session, lap_int, lap_int2, driver, driver2
    
    Compare = dpg.get_value("Compare")

    driver = dpg.get_value("driver_input")
    driver2 = dpg.get_value("driver2_input")
    track = dpg.get_value("track_input")
    year = dpg.get_value("year_input")
    year_int = int(year) if year else 2025

    if not telemetry_data:
        dpg.set_value("result_text", "No telemetry data available. Please load telemetry first.")
        return

    for item in ["my_hist_speed", "my_hist_rpm", "my_hist_gear", "my_hist_throttle", "my_hist_brake",
                "my_plot_speed", "my_plot_rpm", "my_plot_gear", "my_plot_throttle", "my_plot_brake", "my_plot_drs"]:
     if dpg.does_item_exist(item):
         dpg.delete_item(item)

    minSpeed = min(telemetry_data["Speed"]) - 10
    maxSpeed = max(telemetry_data["Speed"]) + 10
    minRPM = min(telemetry_data["RPM"]) - 100
    maxRPM = max(telemetry_data["RPM"]) + 100
    minGear = min(telemetry_data["Gear"]) - 0.05
    maxGear = max(telemetry_data["Gear"]) + 0.08
    minThrottle = min(telemetry_data["Throttle"]) - 2
    maxThrottle = max(telemetry_data["Throttle"]) + 3
    minBrake = min(telemetry_data["Brake"]) - 0.035
    maxBrake = max(telemetry_data["Brake"]) + 0.05

    if Compare and telemetry_data2:
        minSpeed = min(minSpeed, min(telemetry_data2["Speed"]) - 10)
        maxSpeed = max(maxSpeed, max(telemetry_data2["Speed"]) + 10)
        minRPM = min(minRPM, min(telemetry_data2["RPM"]) - 100)
        maxRPM = max(maxRPM, max(telemetry_data2["RPM"]) + 100)
        minGear = min(minGear, min(telemetry_data2["Gear"]) - 0.05)
        maxGear = max(maxGear, max(telemetry_data2["Gear"]) + 0.08)
        minThrottle = min(minThrottle, min(telemetry_data2["Throttle"]) - 2)
        maxThrottle = max(maxThrottle, max(telemetry_data2["Throttle"]) + 3)
        minBrake = min(minBrake, min(telemetry_data2["Brake"]) - 0.035)
        maxBrake = max(maxBrake, max(telemetry_data2["Brake"]) + 0.05)

    if current_view == "histogram":

        # Speed Histogram
        binsS = np.linspace(minSpeed, maxSpeed, 101)
        time_diffs = np.diff(telemetry_data["Time"])
        hist_timeS = np.zeros(len(binsS) - 1)
        for i in range(len(telemetry_data["Speed"]) - 1):
            bin_idx = np.digitize(telemetry_data["Speed"][i], binsS) - 1
            if 0 <= bin_idx < len(hist_timeS):
                hist_timeS[bin_idx] += time_diffs[i]
        bin_edgesS = binsS[:-1]
        speed_hist = dpg.add_plot(label="Speed Histogram (Time)", height=280, width=-1, tag="my_hist_speed", parent="hist_container")
        dpg.add_plot_axis(dpg.mvXAxis, label="Speed (km/h)", parent=speed_hist, tag="x_axis_hist_speed")
        dpg.add_plot_axis(dpg.mvYAxis, label="Time (s)", parent=speed_hist, tag="y_axis_hist_speed")
        dpg.add_bar_series(x=bin_edgesS.tolist(), y=hist_timeS.tolist(), parent="y_axis_hist_speed", label=f"{driver} Speed Time", tag="hist_line_speed")
        max_hist_timeS = max(hist_timeS)
        if Compare and telemetry_data2:
            driver2 = dpg.get_value("driver2_input")
            time_diffs2 = np.diff(telemetry_data2["Time"])
            hist_timeS2 = np.zeros(len(binsS) - 1)
            for i in range(len(telemetry_data2["Speed"]) - 1):
                bin_idx = np.digitize(telemetry_data2["Speed"][i], binsS) - 1
                if 0 <= bin_idx < len(hist_timeS2):
                    hist_timeS2[bin_idx] += time_diffs2[i]
            dpg.add_bar_series(x=bin_edgesS.tolist(), y=hist_timeS2.tolist(), parent="y_axis_hist_speed", label=f"{driver2} Speed Time", tag="hist_line_speed2")
            max_hist_timeS = max(max_hist_timeS, max(hist_timeS2))
        dpg.set_axis_limits("x_axis_hist_speed", ymin=minSpeed, ymax=maxSpeed)
        dpg.set_axis_limits("y_axis_hist_speed", ymin=0, ymax=max_hist_timeS * 1.1)

        # RPM Histogram
        binsR = np.linspace(minRPM, maxRPM, 101)
        time_diffs = np.diff(telemetry_data["Time"])
        hist_timeR = np.zeros(len(binsR) - 1)
        for i in range(len(telemetry_data["RPM"]) - 1):
            bin_idx = np.digitize(telemetry_data["RPM"][i], binsR) - 1
            if 0 <= bin_idx < len(hist_timeR):
                hist_timeR[bin_idx] += time_diffs[i]
        bin_edgesR = binsR[:-1]
        rpm_hist = dpg.add_plot(label="RPM Histogram (Time)", height=280, width=-1, tag="my_hist_rpm", parent="hist_container")
        dpg.add_plot_axis(dpg.mvXAxis, label="RPM", parent=rpm_hist, tag="x_axis_hist_rpm")
        dpg.add_plot_axis(dpg.mvYAxis, label="Time (s)", parent=rpm_hist, tag="y_axis_hist_rpm")
        dpg.add_bar_series(x=bin_edgesR.tolist(), y=hist_timeR.tolist(), parent="y_axis_hist_rpm", label=f"{driver} RPM Time", tag="hist_line_rpm")
        max_hist_timeR = max(hist_timeR)
        if Compare and telemetry_data2:
            time_diffs2 = np.diff(telemetry_data2["Time"])
            hist_timeR2 = np.zeros(len(binsR) - 1)
            for i in range(len(telemetry_data2["RPM"]) - 1):
                bin_idx = np.digitize(telemetry_data2["RPM"][i], binsR) - 1
                if 0 <= bin_idx < len(hist_timeR2):
                    hist_timeR2[bin_idx] += time_diffs2[i]
            dpg.add_bar_series(x=bin_edgesR.tolist(), y=hist_timeR2.tolist(), parent="y_axis_hist_rpm", label=f"{driver2} RPM Time", tag="hist_line_rpm2")
            max_hist_timeR = max(max_hist_timeR, max(hist_timeR2))
        dpg.set_axis_limits("x_axis_hist_rpm", ymin=minRPM, ymax=maxRPM)
        dpg.set_axis_limits("y_axis_hist_rpm", ymin=0, ymax=max_hist_timeR * 1.1)

        # Gear Histogram
        binsG = np.linspace(minGear, maxGear, 101)
        time_diffs = np.diff(telemetry_data["Time"])
        hist_timeG = np.zeros(len(binsG) - 1)
        for i in range(len(telemetry_data["Gear"]) - 1):
            bin_idx = np.digitize(telemetry_data["Gear"][i], binsG) - 1
            if 0 <= bin_idx < len(hist_timeG):
                hist_timeG[bin_idx] += time_diffs[i]
        bin_edgesG = binsG[:-1]
        gear_hist = dpg.add_plot(label="Gear Histogram (Time)", height=280, width=-1, tag="my_hist_gear", parent="hist_container")
        dpg.add_plot_axis(dpg.mvXAxis, label="Gear", parent=gear_hist, tag="x_axis_hist_gear")
        dpg.add_plot_axis(dpg.mvYAxis, label="Time (s)", parent=gear_hist, tag="y_axis_hist_gear")
        dpg.add_bar_series(x=bin_edgesG.tolist(), y=hist_timeG.tolist(), parent="y_axis_hist_gear", label=f"{driver} Gear Time", tag="hist_line_gear")
        max_hist_timeG = max(hist_timeG)
        if Compare and telemetry_data2:
            time_diffs2 = np.diff(telemetry_data2["Time"])
            hist_timeG2 = np.zeros(len(binsG) - 1)
            for i in range(len(telemetry_data2["Gear"]) - 1):
                bin_idx = np.digitize(telemetry_data2["Gear"][i], binsG) - 1
                if 0 <= bin_idx < len(hist_timeG2):
                    hist_timeG2[bin_idx] += time_diffs2[i]
            dpg.add_bar_series(x=bin_edgesG.tolist(), y=hist_timeG2.tolist(), parent="y_axis_hist_gear", label=f"{driver2} Gear Time", tag="hist_line_gear2")
            max_hist_timeG = max(max_hist_timeG, max(hist_timeG2))
        dpg.set_axis_limits("x_axis_hist_gear", ymin=minGear, ymax=maxGear)
        dpg.set_axis_limits("y_axis_hist_gear", ymin=0, ymax=max_hist_timeG * 1.1)
        
        # Throttle Histogram
        binsT = np.linspace(minThrottle, maxThrottle, 101)
        time_diffs = np.diff(telemetry_data["Time"])
        hist_timeT = np.zeros(len(binsT) - 1)
        for i in range(len(telemetry_data["Throttle"]) - 1):
            bin_idx = np.digitize(telemetry_data["Throttle"][i], binsT) - 1
            if 0 <= bin_idx < len(hist_timeT):
                hist_timeT[bin_idx] += time_diffs[i]
        bin_edgesT = binsT[:-1]
        throttle_hist = dpg.add_plot(label="Throttle Histogram (Time)", height=280, width=-1, tag="my_hist_throttle", parent="hist_container")
        dpg.add_plot_axis(dpg.mvXAxis, label="Throttle", parent=throttle_hist, tag="x_axis_hist_throttle")
        dpg.add_plot_axis(dpg.mvYAxis, label="Time (s)", parent=throttle_hist, tag="y_axis_hist_throttle")
        dpg.add_bar_series(x=bin_edgesT.tolist(), y=hist_timeT.tolist(), parent="y_axis_hist_throttle", label=f"{driver} Throttle Time", tag="hist_line_throttle")
        max_hist_timeT = max(hist_timeT)
        if Compare and telemetry_data2:
            time_diffs2 = np.diff(telemetry_data2["Time"])
            hist_timeT2 = np.zeros(len(binsT) - 1)
            for i in range(len(telemetry_data2["Throttle"]) - 1):
                bin_idx = np.digitize(telemetry_data2["Throttle"][i], binsT) - 1
                if 0 <= bin_idx < len(hist_timeT2):
                    hist_timeT2[bin_idx] += time_diffs2[i]
            dpg.add_bar_series(x=bin_edgesT.tolist(), y=hist_timeT2.tolist(), parent="y_axis_hist_throttle", label=f"{driver2} Throttle Time", tag="hist_line_throttle2")
            max_hist_timeT = max(max_hist_timeT, max(hist_timeT2))
        dpg.set_axis_limits("x_axis_hist_throttle", ymin=minThrottle, ymax=maxThrottle)
        dpg.set_axis_limits("y_axis_hist_throttle", ymin=0, ymax=max_hist_timeT * 1.1)

    elif current_view == "stats":

        # Delete table if it exists
        if dpg.does_item_exist("stats_table"):
            dpg.delete_item("stats_table")

        if Compare:
            variables = (f"{driver} Speed", telemetry_data["Speed"]), (f"{driver2} Speed", telemetry_data2["Speed"]), (f"{driver} RPM", telemetry_data["RPM"]), (f"{driver2} RPM", telemetry_data2["RPM"]), (f"{driver} Gear", telemetry_data["Gear"]), (f"{driver2} Gear", telemetry_data2["Gear"]), (f"{driver} Throttle", telemetry_data["Throttle"]), (f"{driver2} Throttle", telemetry_data2["Throttle"]), (f"{driver} Brake", telemetry_data["Brake"]), (f"{driver2} Brake", telemetry_data2["Brake"]), (f"{driver} DRS", telemetry_data["DRS"]), (f"{driver2} DRS", telemetry_data2["DRS"])
        else:
            variables = (f"{driver} Speed", telemetry_data["Speed"]), (f"{driver} RPM", telemetry_data["RPM"]), (f"{driver} Gear", telemetry_data["Gear"]), (f"{driver} Throttle", telemetry_data["Throttle"]), (f"{driver} Brake", telemetry_data["Brake"]), (f"{driver} DRS", telemetry_data["DRS"])

        with dpg.table(parent="stats", tag="stats_table", header_row=True, resizable=True, borders_innerH=True, borders_outerH=True, borders_innerV=True, borders_outerV=True):
            # Columns
            dpg.add_table_column(label="Variable")
            dpg.add_table_column(label="Mean")
            dpg.add_table_column(label="Min")
            dpg.add_table_column(label="Max")
            dpg.add_table_column(label="Median")
            dpg.add_table_column(label="Standard deviation")

            # Rows
            for name, data in variables:
                data_np = np.array(data)
                with dpg.table_row():
                    dpg.add_text(name)
                    dpg.add_text(f"{np.mean(data_np):.2f}")
                    dpg.add_text(f"{np.min(data_np):.2f}")
                    dpg.add_text(f"{np.max(data_np):.2f}")
                    dpg.add_text(f"{np.median(data_np):.2f}")
                    dpg.add_text(f"{np.std(data_np):.2f}")

    elif current_view == "telemetry":
        # Speed Graph
        plot_speed = dpg.add_plot(label="Speed", height=200, width=-1, tag="my_plot_speed", parent="plot_container_speed", crosshairs=True, zoom_mod=True)
        dpg.add_plot_axis(dpg.mvXAxis, label="Distance (m)", parent=plot_speed, tag="x_axis_speed")
        dpg.add_plot_axis(dpg.mvYAxis, label="(km/h)", parent=plot_speed, tag="y_axis_speed")
        dpg.add_line_series(x=telemetry_data["Distance"], y=telemetry_data["Speed"], parent="y_axis_speed", label=f"{driver} Speed", tag="speed_line")
        if Compare and telemetry_data2:
            driver2 = dpg.get_value("driver2_input")
            dpg.add_line_series(x=telemetry_data2["Distance"], y=telemetry_data2["Speed"], parent="y_axis_speed", label=f"{driver2} Speed", tag="speed_line2")

        dpg.set_axis_limits("y_axis_speed", ymin=minSpeed, ymax=maxSpeed)
    
        # RPM Graph
        plot_rpm = dpg.add_plot(label="RPM", height=200, width=-1, tag="my_plot_rpm", parent="plot_container_rpm", crosshairs=True, zoom_mod=True)
        dpg.add_plot_axis(dpg.mvXAxis, label="Distance (m)", parent=plot_rpm, tag="x_axis_rpm")
        dpg.add_plot_axis(dpg.mvYAxis, label="RPM", parent=plot_rpm, tag="y_axis_rpm")
        dpg.add_line_series(x=telemetry_data["Distance"], y=telemetry_data["RPM"], parent="y_axis_rpm", label=f"{driver} RPM", tag="rpm_line")
        if Compare and telemetry_data2:
            dpg.add_line_series(x=telemetry_data2["Distance"], y=telemetry_data2["RPM"], parent="y_axis_rpm", label=f"{driver2} RPM", tag="rpm_line2")
        dpg.set_axis_limits("y_axis_rpm", ymin=minRPM, ymax=maxRPM)

        # Gear Graph
        plot_gear = dpg.add_plot(label="Gear", height=200, width=-1, tag="my_plot_gear", parent="plot_container_gear", crosshairs=True, zoom_mod=True)
        dpg.add_plot_axis(dpg.mvXAxis, label="Distance (m)", parent=plot_gear, tag="x_axis_gear")
        dpg.add_plot_axis(dpg.mvYAxis, label="", parent=plot_gear, tag="y_axis_gear")
        dpg.add_line_series(x=telemetry_data["Distance"], y=telemetry_data["Gear"], parent="y_axis_gear", label=f"{driver} Gear", tag="gear_line")
        if Compare and telemetry_data2:
            dpg.add_line_series(x=telemetry_data2["Distance"], y=telemetry_data2["Gear"], parent="y_axis_gear", label=f"{driver2} Gear", tag="gear_line2")
        dpg.set_axis_limits("y_axis_gear", ymin=minGear, ymax=maxGear)

        # Throttle Graph
        plot_throttle = dpg.add_plot(label="Throttle", height=200, width=-1, tag="my_plot_throttle", parent="plot_container_throttle", crosshairs=True, zoom_mod=True)
        dpg.add_plot_axis(dpg.mvXAxis, label="Distance (m)", parent=plot_throttle, tag="x_axis_throttle")
        dpg.add_plot_axis(dpg.mvYAxis, label="(%)", parent=plot_throttle, tag="y_axis_throttle")
        dpg.add_line_series(x=telemetry_data["Distance"], y=telemetry_data["Throttle"], parent="y_axis_throttle", label=f"{driver} Throttle", tag="throttle_line")
        if Compare and telemetry_data2:
            dpg.add_line_series(x=telemetry_data2["Distance"], y=telemetry_data2["Throttle"], parent="y_axis_throttle", label=f"{driver2} Throttle", tag="throttle_line2")
        dpg.set_axis_limits("y_axis_throttle", ymin=minThrottle, ymax=maxThrottle)

        # Brake Graph
        plot_brake = dpg.add_plot(label="Brake", height=200, width=-1, tag="my_plot_brake", parent="plot_container_brake", crosshairs=True, zoom_mod=True)
        dpg.add_plot_axis(dpg.mvXAxis, label="Distance (m)", parent=plot_brake, tag="x_axis_brake")
        dpg.add_plot_axis(dpg.mvYAxis, label="(on-off)", parent=plot_brake, tag="y_axis_brake")
        dpg.add_line_series(x=telemetry_data["Distance"], y=telemetry_data["Brake"], parent="y_axis_brake", label=f"{driver} Brake", tag="brake_line")
        if Compare and telemetry_data2:
            dpg.add_line_series(x=telemetry_data2["Distance"], y=telemetry_data2["Brake"], parent="y_axis_brake", label=f"{driver2} Brake", tag="brake_line2")
        dpg.set_axis_limits("y_axis_brake", ymin=minBrake, ymax=maxBrake)

        # DRS Graph
        plot_drs = dpg.add_plot(label="DRS", height=200, width=-1, tag="my_plot_drs", parent="plot_container_drs", crosshairs=True, zoom_mod=True)
        dpg.add_plot_axis(dpg.mvXAxis, label="Distance (m)", parent=plot_drs, tag="x_axis_drs")
        dpg.add_plot_axis(dpg.mvYAxis, label="(on-off)", parent=plot_drs, tag="y_axis_drs")
        dpg.add_line_series(x=telemetry_data["Distance"], y=telemetry_data["DRS"], parent="y_axis_drs", label=f"{driver} DRS", tag="drs_line")
        if Compare and telemetry_data2:
            dpg.add_line_series(x=telemetry_data2["Distance"], y=telemetry_data2["DRS"], parent="y_axis_drs", label=f"{driver2} DRS", tag="drs_line2")
        dpg.set_axis_limits("y_axis_drs", ymin=-0.05, ymax=1.05)

    if Compare and telemetry_data2:
        dpg.set_value("result_text", f"Telemetry successfully loaded for {driver} - Lap: {lap_int if lap_int != 0 else "fastest"} and {driver2} - Lap: {lap_int2 if lap_int2 != 0 else "fastest"} {track} {year_int}")
    else:
        dpg.set_value("result_text", f"Telemetry successfully loaded for {driver} {track} {year_int} Lap: {lap_int if lap_int != 0 else "fastest"}")
    hex_to_rgb()

def hex_to_rgb():
    global driver, driver2, r, g, b, r2, g2, b2
    
    driver = dpg.get_value("driver_input")
    driver2 = dpg.get_value("driver2_input")
    hex_enabled = dpg.get_value("hex")
    Compare = dpg.get_value("Compare")

    if not hex_enabled:
        bind_default_themes()
    else:
        try:
            hex_color = fastf1.plotting.get_driver_color(driver, session).lstrip('#')
            r = int(hex_color[0:2], 16)
            g = int(hex_color[2:4], 16)
            b = int(hex_color[4:6], 16)

            if dpg.does_item_exist("speed_themeT"):
                dpg.delete_item("speed_themeT")
            with dpg.theme(tag="speed_themeT"):
                with dpg.theme_component(dpg.mvLineSeries):
                    dpg.add_theme_color(dpg.mvPlotCol_Line, (r, g, b, 200), category=dpg.mvThemeCat_Plots)
                with dpg.theme_component(dpg.mvBarSeries):
                    dpg.add_theme_color(dpg.mvPlotCol_Fill, (r, g, b, 200), category=dpg.mvThemeCat_Plots)

            if dpg.does_item_exist("rpm_themeT"):
                dpg.delete_item("rpm_themeT")
            with dpg.theme(tag="rpm_themeT"):
                with dpg.theme_component(dpg.mvLineSeries):
                    dpg.add_theme_color(dpg.mvPlotCol_Line, (r, g, b, 255), category=dpg.mvThemeCat_Plots)
                with dpg.theme_component(dpg.mvBarSeries):
                    dpg.add_theme_color(dpg.mvPlotCol_Fill, (r, g, b, 200), category=dpg.mvThemeCat_Plots)     
            if dpg.does_item_exist("gear_themeT"):
                dpg.delete_item("gear_themeT")                                  
            with dpg.theme(tag="gear_themeT"):
                with dpg.theme_component(dpg.mvLineSeries):
                    dpg.add_theme_color(dpg.mvPlotCol_Line, (r, g, b, 255), category=dpg.mvThemeCat_Plots)
                with dpg.theme_component(dpg.mvBarSeries):
                    dpg.add_theme_color(dpg.mvPlotCol_Fill, (r, g, b, 200), category=dpg.mvThemeCat_Plots)  

            if dpg.does_item_exist("throttle_themeT"):
                dpg.delete_item("throttle_themeT")                 
            with dpg.theme(tag="throttle_themeT"):
                with dpg.theme_component(dpg.mvLineSeries):
                    dpg.add_theme_color(dpg.mvPlotCol_Line, (r, g, b, 255), category=dpg.mvThemeCat_Plots)
                with dpg.theme_component(dpg.mvBarSeries):
                    dpg.add_theme_color(dpg.mvPlotCol_Fill, (r, g, b, 200), category=dpg.mvThemeCat_Plots)

            if dpg.does_item_exist("brake_themeT"):
                dpg.delete_item("brake_themeT")
            with dpg.theme(tag="brake_themeT"):
                with dpg.theme_component(dpg.mvLineSeries):
                    dpg.add_theme_color(dpg.mvPlotCol_Line, (r, g, b, 255), category=dpg.mvThemeCat_Plots)
            if dpg.does_item_exist("drs_themeT"):
                dpg.delete_item("drs_themeT")
            with dpg.theme(tag="drs_themeT"):
                with dpg.theme_component(dpg.mvLineSeries):
                    dpg.add_theme_color(dpg.mvPlotCol_Line, (r, g, b, 255), category=dpg.mvThemeCat_Plots)      

            if Compare:
                hex_color2 = fastf1.plotting.get_driver_color(driver2, session).lstrip('#')
                r2 = int(hex_color2[0:2], 16)
                g2 = int(hex_color2[2:4], 16)
                b2 = int(hex_color2[4:6], 16)

                if dpg.does_item_exist("speed_themeT2"):
                    dpg.delete_item("speed_themeT2")
                with dpg.theme(tag="speed_themeT2"):
                    with dpg.theme_component(dpg.mvLineSeries):
                        dpg.add_theme_color(dpg.mvPlotCol_Line, (r2, g2, b2, 255), category=dpg.mvThemeCat_Plots)
                    with dpg.theme_component(dpg.mvBarSeries):
                        dpg.add_theme_color(dpg.mvPlotCol_Fill, (r2, g2, b2, 200), category=dpg.mvThemeCat_Plots)

                if dpg.does_item_exist("rpm_themeT2"):
                    dpg.delete_item("rpm_themeT2")
                with dpg.theme(tag="rpm_themeT2"):
                    with dpg.theme_component(dpg.mvLineSeries):
                        dpg.add_theme_color(dpg.mvPlotCol_Line, (r2, g2, b2, 255), category=dpg.mvThemeCat_Plots)
                    with dpg.theme_component(dpg.mvBarSeries):
                        dpg.add_theme_color(dpg.mvPlotCol_Fill, (r2, g2, b2, 200), category=dpg.mvThemeCat_Plots)

                if dpg.does_item_exist("gear_themeT2"):
                    dpg.delete_item("gear_themeT2")
                with dpg.theme(tag="gear_themeT2"):
                    with dpg.theme_component(dpg.mvLineSeries):
                        dpg.add_theme_color(dpg.mvPlotCol_Line, (r2, g2, b2, 255), category=dpg.mvThemeCat_Plots)
                    with dpg.theme_component(dpg.mvBarSeries):
                        dpg.add_theme_color(dpg.mvPlotCol_Fill, (r2, g2, b2, 200), category=dpg.mvThemeCat_Plots)

                if dpg.does_item_exist("throttle_themeT2"):
                    dpg.delete_item("throttle_themeT2")
                with dpg.theme(tag="throttle_themeT2"):
                    with dpg.theme_component(dpg.mvLineSeries):
                        dpg.add_theme_color(dpg.mvPlotCol_Line, (r2, g2, b2, 255), category=dpg.mvThemeCat_Plots)
                    with dpg.theme_component(dpg.mvBarSeries):
                        dpg.add_theme_color(dpg.mvPlotCol_Fill, (r2, g2, b2, 200), category=dpg.mvThemeCat_Plots)
                        
                if dpg.does_item_exist("brake_themeT2"):
                    dpg.delete_item("brake_themeT2")
                with dpg.theme(tag="brake_themeT2"):
                    with dpg.theme_component(dpg.mvLineSeries):
                        dpg.add_theme_color(dpg.mvPlotCol_Line, (r2, g2, b2, 255), category=dpg.mvThemeCat_Plots)

                if dpg.does_item_exist("drs_themeT2"):
                    dpg.delete_item("drs_themeT2")
                with dpg.theme(tag="drs_themeT2"):
                    with dpg.theme_component(dpg.mvLineSeries):
                        dpg.add_theme_color(dpg.mvPlotCol_Line, (r2, g2, b2, 255), category=dpg.mvThemeCat_Plots)
            bind_team_themes()
        except Exception as e:
            dpg.set_value("result_text", f"Error colores equipo: {e}")


def bind_team_themes():
    global current_view

    if current_view == "telemetry":
        dpg.bind_item_theme("speed_line", "speed_themeT")
        dpg.bind_item_theme("rpm_line", "rpm_themeT")
        dpg.bind_item_theme("gear_line", "gear_themeT")
        dpg.bind_item_theme("throttle_line", "throttle_themeT")
        dpg.bind_item_theme("brake_line", "brake_themeT")
        dpg.bind_item_theme("drs_line", "drs_themeT")
    else:
        dpg.bind_item_theme("hist_line_speed", "speed_themeT")
        dpg.bind_item_theme("hist_line_rpm", "rpm_themeT")
        dpg.bind_item_theme("hist_line_gear", "gear_themeT")
        dpg.bind_item_theme("hist_line_throttle", "throttle_themeT")

    if dpg.get_value("Compare"):
        if current_view == "telemetry":
            dpg.bind_item_theme("speed_line2", "speed_themeT2")
            dpg.bind_item_theme("rpm_line2", "rpm_themeT2")
            dpg.bind_item_theme("gear_line2", "gear_themeT2")
            dpg.bind_item_theme("throttle_line2", "throttle_themeT2")
            dpg.bind_item_theme("brake_line2", "brake_themeT2")
            dpg.bind_item_theme("drs_line2", "drs_themeT2")
        else:
            dpg.bind_item_theme("hist_line_speed2", "speed_themeT2")
            dpg.bind_item_theme("hist_line_rpm2", "rpm_themeT2")
            dpg.bind_item_theme("hist_line_gear2", "gear_themeT2")
            dpg.bind_item_theme("hist_line_throttle2", "throttle_themeT2")

def bind_default_themes():
    global current_view

    if current_view == "telemetry":
        dpg.bind_item_theme("speed_line", "speed_theme")
        dpg.bind_item_theme("rpm_line", "rpm_theme")
        dpg.bind_item_theme("gear_line", "gear_theme")
        dpg.bind_item_theme("throttle_line", "throttle_theme")
        dpg.bind_item_theme("brake_line", "brake_theme")
        dpg.bind_item_theme("drs_line", "drs_theme")
    else:
        dpg.bind_item_theme("hist_line_speed", "speed_theme")
        dpg.bind_item_theme("hist_line_rpm", "rpm_theme")
        dpg.bind_item_theme("hist_line_gear", "gear_theme")
        dpg.bind_item_theme("hist_line_throttle", "throttle_theme")

    if dpg.get_value("Compare"):
        if current_view == "telemetry":
            dpg.bind_item_theme("speed_line2", "speed_theme2")
            dpg.bind_item_theme("rpm_line2", "rpm_theme2")
            dpg.bind_item_theme("gear_line2", "gear_theme2")
            dpg.bind_item_theme("throttle_line2", "throttle_theme2")
            dpg.bind_item_theme("brake_line2", "brake_theme2")
            dpg.bind_item_theme("drs_line2", "drs_theme2")
        else:
            dpg.bind_item_theme("hist_line_speed2", "speed_theme2")
            dpg.bind_item_theme("hist_line_rpm2", "rpm_theme2")
            dpg.bind_item_theme("hist_line_gear2", "gear_theme2")
            dpg.bind_item_theme("hist_line_throttle2", "throttle_theme2")

def load_telemetry(sender, app_data, user_data):
    load_session()
    load_data(user_data)
    update_plots()
if __name__ == "__main__":
    create_interface()