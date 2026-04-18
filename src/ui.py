import dearpygui.dearpygui as dpg
from state import state
from data_loader import load_latest_session, is_sprint_weekend, load_session, get_lap_numbers, get_calendar, extract_telemetry
from themes import hex_to_rgb, default_themes
from plots import *
import sys

def create_interface(): 
    load_latest_session()
    dpg.create_context()
    default_themes()
    dpg.create_viewport(title="WUS Telemetry", width=860, height=1100)

    with dpg.window(label="Real F1 Telemetry Graphs", width=1920, height=1008, tag="main_window"):
        if sys.platform != "linux":       # Add Linux compatibility
            dpg.toggle_viewport_fullscreen()
        dpg.bind_item_theme("main_window", "main_theme")

        with dpg.tab_bar(label="view", tag="tab"):
            dpg.add_tab_button(label="Graphs", tag="graphs", callback=lambda: switch_view("graphs"))
            dpg.add_tab_button(label="Histogram", tag="histogram", callback=lambda: switch_view("histogram"))
            dpg.add_tab_button(label="Scatter", tag="scatter", callback=lambda: switch_view("scatter"))
            dpg.add_tab_button(label="Statistics", tag="statistics", callback=lambda: switch_view("stats"))

        with dpg.group(horizontal=True, tag="main_row"):
            with dpg.group(horizontal=False, tag="info", width=380):
                dpg.add_text("Fill inputs", wrap=500)
                dpg.add_text("Session:")
                dpg.add_combo(items=state.session_list, tag="session_input", width=260, default_value=state.sessionID)
                dpg.add_text("Track:")
                dpg.add_combo(items=state.calendar, tag="track_input", width=260, default_value=state.track_default, callback=refresh_session)
                dpg.add_text("Year:")
                dpg.add_input_text(tag="year_input", hint="E.g: 2025", width=260, default_value=state.latest_year, callback=refresh_track)
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
                dpg.add_checkbox(label="Compare", callback=compare_toggle, tag="Compare", default_value=False)
                dpg.add_spacer(height=5)
                dpg.add_button(label="Show Telemetry", callback=load_telemetry, height=22)
                dpg.add_spacer(height=5)
                dpg.add_checkbox(label="Team colors", callback=hex_to_rgb, tag="hex", default_value=False)
                dpg.add_spacer(height=5)
                dpg.add_text("", tag="result_text", wrap=1000)
            dpg.add_spacer(width=700)

            with dpg.group(horizontal=False, tag="track_side"):
                plot_track = dpg.add_plot(label="", height=400, width=650, tag="my_plot_track", zoom_mod=True, crosshairs=True, no_box_select=True, no_frame=True, no_menus=True, no_title=True, no_mouse_pos=True)
                dpg.add_plot_axis(dpg.mvXAxis, parent=plot_track, tag="x_axis", auto_fit=True, no_gridlines=True, no_highlight=True, no_tick_marks=True, no_tick_labels=True)
                dpg.add_plot_axis(dpg.mvYAxis, parent=plot_track, tag="y_axis", auto_fit=True, no_gridlines=True, no_highlight=True, no_tick_marks=True, no_tick_labels=True)
                dpg.add_line_series([], [], parent="y_axis", tag="track_line")
                dpg.bind_item_theme("track_line", "track_line_theme")
                dpg.add_scatter_series([], [], parent="y_axis", tag="track_point")

        with dpg.child_window(width=-1, height=70, tag="lap_selector_container", border=False, horizontal_scrollbar=True):
            dpg.add_text("Lap selector:")
        with dpg.child_window(width=-1, height=70, tag="lap_selector_container2", border=False, horizontal_scrollbar=True, show=False):
            dpg.add_text("Compared driver lap selector:")

        dpg.add_checkbox(label="Show info", callback=hide_inputs, tag="Info", default_value=True)

        # Plots containers
        for ch in ["speed", "rpm", "gear", "throttle", "brake", "glon", "drs"]:
            with dpg.child_window(tag=f"plot_container_{ch}", width=-1, height=160, show=True):
                pass

        # Histogram container
        with dpg.group(horizontal=False):
            with dpg.child_window(width=0, autosize_x=True, tag="hist_container", show=False):
                pass

        # Scatter containers
        for ch in ["rpm", "glon"]:
            with dpg.child_window(tag=f"{ch}_vs_speed", width=-1, height=500, show=False):
                pass

        # Statistics container
        with dpg.group(horizontal=True):
            with dpg.child_window(width=0, autosize_x=False, tag="stats", show=False):
                pass
            
        # Mouse tracking
        with dpg.handler_registry():
            dpg.add_mouse_move_handler(callback=update_car_position)

    dpg.setup_dearpygui()
    dpg.show_viewport()
    dpg.maximize_viewport()
    dpg.start_dearpygui()
    dpg.destroy_context()

def switch_view(view):
    state.current_view = view

    view_panels = {
        "graphs": ["plot_container_speed", "plot_container_rpm", "plot_container_gear",
                    "plot_container_throttle", "plot_container_brake", "plot_container_glon", "plot_container_drs"],
        "histogram": ["hist_container"],
        "scatter": ["rpm_vs_speed", "glon_vs_speed"],
        "stats": ["stats"]
    }

    for panels_in_view in view_panels.values():
        for panel in panels_in_view:
            if dpg.does_item_exist(panel):
                if panel in view_panels[view]:
                    dpg.show_item(panel)
                else:
                    dpg.hide_item(panel)
    update_plots()

def refresh_session():
    track = dpg.get_value("track_input")
    year = int(dpg.get_value("year_input"))

    if "Pre-Season" not in track:
        is_sprint_weekend(year, track)
        state.testing = 0
    else:
        state.session_list = ['Practice 1', 'Practice 2', 'Practice 3']
        state.testing = 1
    dpg.configure_item("session_input", items=state.session_list)

def refresh_track():
    year = int(dpg.get_value("year_input"))
    get_calendar(year)
    dpg.configure_item("track_input", items=state.calendar)

def read_ui_inputs():
    state.track = dpg.get_value("track_input")
    year_str = dpg.get_value("year_input")
    session_input = dpg.get_value("session_input")

    # Update driver list form inputs
    state.drivers = []
    state.drivers.append(dpg.get_value("driver_input"))
    if dpg.get_value("Compare"):
        state.drivers.append(dpg.get_value("driver2_input"))

    # Update selected laps
    state.selected_laps = []
    state.selected_laps.append(int(dpg.get_value("lap_input") or 0))
    if dpg.get_value("Compare"):
        state.selected_laps.append(int(dpg.get_value("lap_input2") or 0))

    if not state.track or not year_str or not state.drivers[0]:
        return None, None, False, "Error: Fill year, track and driver."

    try:
        year_int = int(year_str)
    except ValueError:
        return None, None, False, "Error: Year mut be numeric."

    return year_int, session_input, True, ""

def build_lap_selector(container, driver, callback, tag_prefix):
    dpg.delete_item(container, children_only=True)
    label = "Lap selector:" if "2" not in container else "Lap selector driver 2:"
    dpg.add_text(label, parent=container)

    lap_numbers, fastest_num = get_lap_numbers(driver)

    with dpg.group(horizontal=True, parent=container):
        for lap_num in lap_numbers:
            button_tag = f"{tag_prefix}{int(lap_num)}"
            dpg.add_button(
                label=f"Lap {int(lap_num)}",
                callback=callback,
                user_data=int(lap_num),
                width=80,
                tag=button_tag
            )
            if lap_num == fastest_num:
                dpg.bind_item_theme(button_tag, "purple_button_theme")


def callback_select_lap(sender, app_data, user_data):
    state.selected_laps[0] = user_data
    dpg.set_value("lap_input", user_data)
    load_and_update()


def callback_select_lap2(sender, app_data, user_data):
    state.selected_laps[1] = user_data
    dpg.set_value("lap_input2", user_data)
    load_and_update()


def load_and_update():
    state.telemetry_data = []

    for i, driver in enumerate(state.drivers):
        lap_num = state.selected_laps[i] if i < len(state.selected_laps) else 0
        data, err = extract_telemetry(driver, lap_num)
        if err:
            dpg.set_value("result_text", err)
            return
        state.telemetry_data.append(data)

    update_plots()

    lap_label = state.selected_laps[0] if state.selected_laps[0] != 0 else "fastest"
    dpg.set_value("result_text",
        f"Telemetry loaded: {', '.join(state.drivers)} {state.track} Lap: {lap_label}")


def load_telemetry(sender, app_data):
    dpg.set_value("result_text", "Loading... it might take long to load data")

    year_int, session_input, ok, err = read_ui_inputs()
    if not ok:
        dpg.set_value("result_text", err)
        return

    ok, err = load_session(year_int, session_input)
    if not ok:
        dpg.set_value("result_text", err)
        return

    # Build lap selectors
    build_lap_selector("lap_selector_container", state.drivers[0], callback_select_lap, "lap_button_")
    if dpg.get_value("Compare") and len(state.drivers) > 1:
        build_lap_selector("lap_selector_container2", state.drivers[1], callback_select_lap2, "lap_button2_")

    load_and_update()

def compare_toggle():
    compare = dpg.get_value("Compare")
    (dpg.show_item if compare else dpg.hide_item)("driver_compare")
    (dpg.show_item if compare else dpg.hide_item)("lap_selector_container2")

def hide_inputs():
    show = dpg.get_value("Info")
    compare = dpg.get_value("Compare")

    for item in ("info", "track_side", "lap_selector_container"):
        (dpg.show_item if show else dpg.hide_item)(item)

    if show and compare:
        dpg.show_item("lap_selector_container2")
    elif not show:
        dpg.hide_item("lap_selector_container2")