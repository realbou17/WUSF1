import dearpygui.dearpygui as dpg
from state import state
from data_loader import load_latest_session, is_sprint_weekend, load_session, get_lap_numbers, get_calendar, extract_telemetry, refresh_done
from themes import hex_to_rgb_text, default_themes
from plots import *
import sys, os

def create_interface():
    load_latest_session(state.round_delay)
    dpg.create_context()
    default_themes()
    dpg.create_viewport(title="WUS F1", width=1280, height=720)

    with dpg.window(label="Real F1 Telemetry Graphs", width=state.screen_w, height=state.screen_h, tag="main_window"):
        if sys.platform != "linux":       # Allow Linux compatibility
            dpg.toggle_viewport_fullscreen()
        dpg.bind_item_theme("main_window", "main_theme")

        # Logo
        if getattr(sys, 'frozen', False):
            base = sys._MEIPASS  
        else:
            base = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        icon_path = os.path.join(base, "logo.ico")

        with dpg.tab_bar(label="view", tag="tab"):
            dpg.add_tab_button(label="Graphs", tag="graphs", callback=lambda: switch_view("graphs"))
            dpg.add_tab_button(label="Histogram", tag="histogram", callback=lambda: switch_view("histogram"))
            dpg.add_tab_button(label="Scatter", tag="scatter", callback=lambda: switch_view("scatter"))
            dpg.add_tab_button(label="Statistics", tag="statistics", callback=lambda: switch_view("stats"))

        with dpg.group(horizontal=True, tag="main_row"):
            with dpg.group(horizontal=False, tag="session_info", height=-1):
                with dpg.child_window(width=state.screen_w*state.INPUT_WINDOW_W, height=-1, no_scrollbar=True):
                    dpg.add_text("Session:")
                    dpg.add_combo(items=state.session_list, tag="session_input", width=-1, default_value=state.sessionID, callback=refresh_done)
                    dpg.add_text("Track:")
                    dpg.add_combo(items=state.calendar, tag="track_input", width=-1, default_value=state.track_default, callback=refresh_session)
                    dpg.add_text("Year:")
                    dpg.add_combo(items=state.possible_years, tag="year_input", width=-1, default_value=state.latest_year, callback=refresh_track)
                    dpg.add_text("Drivers:")
                    with dpg.child_window(width=-1, height=state.screen_h*state.DRIVER_H, auto_resize_x=True, border=False, horizontal_scrollbar=True, tag="driver_tree_container"):
                        dpg.bind_item_theme("driver_tree_container", "transparent_window")
                        with dpg.tree_node(tag="driver_tree", label="Selected drivers (0)"):
                            # Checkboxes for available drivers
                            pass
                    dpg.add_spacer(height=state.screen_h*state.SPACER_H)
                    dpg.add_button(label="Show Telemetry", callback=load_telemetry, height=state.screen_h*state.TELEMBUTTON_H, tag="Show Telemetry")
                    dpg.add_spacer(height=state.screen_h*state.SPACER_H)
                    dpg.add_checkbox(label="Team colors", callback=update_plots, tag="hex", default_value=True)
                    dpg.add_spacer(height=state.screen_h*state.SPACER_H)
                    dpg.add_text("", tag="result_text", wrap=state.screen_w*state.WRAP_W)

                    # Track plot creation
                    plot_track = dpg.add_plot(height=-1, width=-1, tag="my_plot_track", zoom_mod=True, crosshairs=False, no_frame=True, no_menus=True, no_title=True, no_mouse_pos=True)
                    dpg.add_plot_axis(dpg.mvXAxis, parent=plot_track, tag="x_axis", no_gridlines=True, no_highlight=True, no_tick_marks=True, no_tick_labels=True)
                    dpg.add_plot_axis(dpg.mvYAxis, parent=plot_track, tag="y_axis", no_gridlines=True, no_highlight=True, no_tick_marks=True, no_tick_labels=True)
                
            with dpg.group(horizontal=False, tag="lap_telem"):
                # Lap containers
                with dpg.group(horizontal=False, tag="lap_containers", height=-1, width=-1):
                    dpg.add_tree_node(tag="lap_tree", label="Lap selector")
                    pass

                # Plots containers
                with dpg.group(horizontal=False, tag="graphs_containers"):
                    for ch in ["delta", "speed", "rpm", "gear", "throttle", "brake", "glon", "drs"]:
                        with dpg.child_window(tag=f"plot_container_{ch}", width=-1,show=True, border=False):
                            dpg.bind_item_theme(f"plot_container_{ch}", "no_padding_window")
                            pass

                # Histogram container
                with dpg.group(horizontal=False):
                    with dpg.child_window(width=0, autosize_x=True, tag="hist_container", show=False, border=False):
                        dpg.bind_item_theme("hist_container", "no_padding_window")
                        pass

                # Scatter containers
                for ch in ["rpm", "glon"]:
                    with dpg.child_window(tag=f"{ch}_vs_speed", width=-1, show=False, border=False):
                        dpg.bind_item_theme(f"{ch}_vs_speed", "no_padding_window")
                        pass

                # Statistics container
                with dpg.group(horizontal=True):
                    with dpg.child_window(width=0, autosize_x=False, tag="stats", show=False, border=False):
                        pass

        # Mouse tracking
        with dpg.handler_registry():
            dpg.add_mouse_move_handler(callback=update_car_position)
        
        # Mouse tracking for drivers' checkboxes creation
        with dpg.item_handler_registry(tag="driver_tree_regst"):
            dpg.add_item_clicked_handler(callback=refresh_driver_selection)
        dpg.bind_item_handler_registry("driver_tree", "driver_tree_regst")

        with dpg.item_handler_registry(tag="viewport_handler"):
            dpg.add_item_resize_handler(callback=on_resize)
        dpg.bind_item_handler_registry("main_window", "viewport_handler")

        # Delta toggle command
        with dpg.handler_registry():
            dpg.add_key_press_handler(key=dpg.mvKey_D, callback=toggle_delta)

    hex_to_rgb_text()
    dpg.setup_dearpygui()
    if os.path.exists(icon_path) and sys.platform != "linux":
        dpg.set_viewport_small_icon(icon_path)
        dpg.set_viewport_large_icon(icon_path)
    dpg.show_viewport()
    dpg.set_primary_window("main_window", True)         # Removes the window bar
    dpg.maximize_viewport()
    dpg.start_dearpygui()
    dpg.destroy_context()

def on_resize():
    w = dpg.get_viewport_client_width()
    h = dpg.get_viewport_client_height()
    state.screen_w, state.screen_h = w, h
    current_tab_h = dpg.get_item_state("main_row")["rect_min"][1] 
    if current_tab_h > 0:       
        state.tab_h = current_tab_h 
    fixed = state.tab_h

    available = h - fixed - 10
    dpg.configure_item("main_window", width=w, height=h)
    dpg.configure_item("session_info", width=int(w * state.SIDE_W))
    dpg.configure_item("my_plot_track", width=int(w * state.TRACK_W), height=int(h * state.TRACK_H))

    # Graph container height
    year = int(dpg.get_value("year_input") or 2025)
    delta_shown = (state.driver_count > 1 and
                dpg.does_item_exist("plot_container_delta") and
                dpg.is_item_shown("plot_container_delta"))
    if year >= 2026:
        num_channels = 7 if delta_shown else 6
    else:
        num_channels = 8 if delta_shown else 7

    state.graph_h = available / num_channels    # The height of each graph
    for ch in ["delta", "speed", "rpm", "gear", "throttle", "brake", "glon", "drs"]:
        dpg.configure_item(f"plot_container_{ch}", height=state.graph_h)

    # Histogram container height
    dpg.configure_item("hist_container", height=available)

    # Scatter container height
    scatter_h = available / 2
    for ch in ["rpm", "glon"]:
        dpg.configure_item(f"{ch}_vs_speed", height=scatter_h)

    if state.telemetry_data:
        update_plots()

def switch_view(view):
    state.current_view = view

    view_panels = {
        "graphs": ["plot_container_delta", "plot_container_speed", "plot_container_rpm", "plot_container_gear",
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

def toggle_delta():
    if state.driver_count > 1:
        if dpg.does_item_exist("plot_container_delta") and state.current_view == "graphs":
            if dpg.is_item_shown("plot_container_delta"):
                dpg.hide_item("plot_container_delta")
                state.delta = False
            else:
                dpg.show_item("plot_container_delta")
                state.delta = True
    else:
        if dpg.does_item_exist("plot_container_delta"):
            dpg.hide_item("plot_container_delta")
            state.delta = False
    on_resize()

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
    refresh_done()

def refresh_track():
    year = int(dpg.get_value("year_input"))
    get_calendar(year)
    dpg.configure_item("track_input", items=state.calendar)
    refresh_done()

def refresh_driver_selection():
    selected_abb = [] 

    if state.session:
        for num in state.session.drivers:
            tag = f"driver_check_{num}"
            if dpg.does_item_exist(tag) and dpg.get_value(tag):
                number = state.session.get_driver(num)
                selected_abb.append(number["Abbreviation"])
    
    if not selected_abb and state.drivers:
        selected_abb = list(state.drivers)
    
    # Delete previous checkboxes
    dpg.delete_item("driver_tree", children_only=True)

    if state.session is None:
        dpg.add_text("Choose a track and session first", parent="driver_tree")
        return

    driver_list = []
    for drivers_num in state.session.drivers:
        drivers_number = state.session.get_driver(drivers_num)
        drivers_abb = drivers_number["Abbreviation"]
        driver_list.append((drivers_num, drivers_abb))

    num_cols = 3
    with dpg.table(parent="driver_tree", header_row=False,
                borders_innerH=False, borders_outerH=False,
                borders_innerV=False, borders_outerV=False,
                width=-1, tag="driver_selection_table"):
        for _ in range(num_cols):
            dpg.add_table_column(width=-1)
        for i in range(0, len(driver_list), num_cols):
            with dpg.table_row():
                for j in range(num_cols):
                    idx = i + j
                    if idx < len(driver_list):
                        drivers_num, drivers_abb = driver_list[idx]
                        checkbox_tag = f"driver_check_{drivers_num}"
                        is_checked = drivers_abb in selected_abb
                        with dpg.group(horizontal=True):
                            dpg.add_selectable(
                                label=drivers_abb,
                                tag=checkbox_tag,
                                default_value=is_checked,
                                callback=update_driver_tree_label
                            )
            
                    else:
                        dpg.add_text("")
            
    hex_to_rgb_text()
    update_driver_tree_label()

def update_driver_tree_label():
    selected = 0
    new_drivers = []

    if state.session is None:
        dpg.set_item_label("driver_tree", "Selected drivers (0)")
        state.driver_count = 0
        return
    
    for num in state.session.drivers:
        tag = f"driver_check_{num}"
        if dpg.does_item_exist(tag) and dpg.get_value(tag):
            number = state.session.get_driver(num)
            abb = number["Abbreviation"]
            new_drivers.append(abb)
            selected += 1
    
    state.driver_count = selected
    state.drivers = new_drivers

    dpg.set_item_label("driver_tree", f"Selected drivers ({selected})")
    if state.telemetry_data and len(state.telemetry_data) == selected:
        pass
    else:
        refresh_done()

def read_ui_inputs():
    state.track = dpg.get_value("track_input")
    year_str = dpg.get_value("year_input")
    session_input = dpg.get_value("session_input")
    try:
        if not state.track or not year_str or not session_input:
            return None, None, False, dpg.set_value("result_text", "Fill session, track and year")
    except ValueError:
        return

    try:
        year_int = int(year_str)
    except ValueError:
        return None, None, False, "Error: Year mut be numeric."
    
    return year_int, session_input, True, ""

def build_lap_selector(container, driver_index, driver_name, callback):
    lap_numbers, fastest_num, lap_time = get_lap_numbers(driver_name)

    with dpg.group(horizontal=True, parent=container):
        dpg.add_text(f"{driver_name}:")

        for lap_num in lap_numbers:
            button_tag = f"lap_button_{driver_index}_{int(lap_num)}"
            if dpg.does_item_exist(button_tag):
                dpg.delete_item(button_tag)
            dpg.add_button(
                label=f"L{int(lap_num)} {lap_time[int(lap_num)-1]}",
                callback=callback,
                user_data=(driver_index, int(lap_num)),
                width=state.screen_w*state.LAP_BUTTON_W,
                height=state.screen_h*state.LAP_BUTTON_H,
                tag=button_tag
            )
            if lap_num == fastest_num:
                dpg.bind_item_theme(button_tag, "purple_button_theme")

def callback_select_lap(sender, app_data, user_data):
    i, lap_num = user_data
    state.selected_laps[i] = lap_num
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
    
    # Delta calculation
    if len(state.telemetry_data) >= 2:
        ref_idx = state.fastest_driver_index
        ref_data = state.telemetry_data[ref_idx]
        ref_time = np.array(ref_data["TimeAtDist"])

        for i in range(state.driver_count):
            if i == ref_idx:
                state.telemetry_data[i]["Delta"] = [0.0] * len(ref_time)
            else:
                comp_time = np.array(state.telemetry_data[i]["TimeAtDist"])
                delta_manual = comp_time - ref_time
                state.telemetry_data[i]["Delta"] = delta_manual.tolist()
    on_resize()

    lap_label = []
    for d in range (state.driver_count):
        a, fastest_lap, b = get_lap_numbers(state.drivers[d])
        if state.selected_laps[d] == 0:
           lap_label.append(fastest_lap)
        else: 
           lap_label.append(state.selected_laps[d])

    # Create a list of "DRIVER: Lx" by zipping drivers and their laps
    driver_lap = [f"{driver}: L{lap}" for driver, lap in zip(state.drivers, lap_label)]

    # Join them with commas and spaces
    dpg.set_value("result_text",
        f"Telemetry loaded for {', '.join(driver_lap)} - {state.track}")

def load_telemetry(sender, app_data):
    state.telemetry_data = []
    state.selected_laps = []
    
    dpg.set_value("result_text", "Loading... it might take long to load data")

    year_int, session_input, ok, err = read_ui_inputs()
    if not ok:
        dpg.set_value("result_text", err)
        return

    ok, err = load_session(year_int, session_input, True)
    if not ok:
        dpg.set_value("result_text", err)
        return
    
    state.selected_laps = [0] * state.driver_count   # 0 = fastest lap by default
    
    # Get the driver loaded with the fastest lap
    fastest_time = float('inf')
    state.fastest_driver_index = 0
    
    for i, driver in enumerate(state.drivers):
        lap_numbers, fastest_num, lap_times = get_lap_numbers(driver)
        if fastest_num is not None and fastest_num < len(lap_times):
            # Get fastest laptime
            fastest_lap_time_str = lap_times[fastest_num - 1]
            if fastest_lap_time_str != "No Time":
                # From ("mm:ss.mmm") to seconds
                parts = fastest_lap_time_str.split(":")
                if len(parts) == 2:
                    minutes = int(parts[0])
                    seconds = float(parts[1])
                    total_seconds = minutes * 60 + seconds
                    
                    if total_seconds < fastest_time:
                        fastest_time = total_seconds
                        state.fastest_driver_index = i

    # Delete previous lap selectors
    for i in range(1, 22):
        old_tag_c = f"lap_selector_container{i}"
        if dpg.does_item_exist(old_tag_c):
            dpg.delete_item(old_tag_c)
        old_tag_t = f"Lap selector text{i}"
        if dpg.does_item_exist(old_tag_t):
            dpg.delete_item(old_tag_t)

    # Build lap selectors
    for i in range(state.driver_count):
        dpg.add_child_window(width=-1, height=state.screen_h*state.LAP_H, tag=f"lap_selector_container{i+1}", border=False, horizontal_scrollbar=True, parent="lap_tree")
        dpg.bind_item_theme(f"lap_selector_container{i+1}", "transparent_window")
        build_lap_selector(f"lap_selector_container{i+1}", driver_index=i, driver_name=state.drivers[i], callback=callback_select_lap)
        on_resize()
    load_and_update()
    refresh_driver_selection()