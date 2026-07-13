import dearpygui.dearpygui as dpg
from state import state
import numpy as np
from themes import hex_to_rgb
from data_loader import get_lap_numbers

def update_plots():
    year = dpg.get_value("year_input")
    year_int = int(year) if year else 2025

    if not state.telemetry_data:
        dpg.set_value("result_text", "No telemetry data available. Please load telemetry first.")
        return

    for item in ["my_hist_speed", "my_hist_rpm", "my_hist_gear", "my_hist_throttle", "my_hist_brake",
                "my_plot_delta", "my_plot_speed", "my_plot_rpm", "my_plot_gear", "my_plot_throttle", "my_plot_brake", "my_plot_glon", "my_plot_drs",
                "my_rpm_vs_speed", "my_glon_vs_speed"]:
     if dpg.does_item_exist(item):
         dpg.delete_item(item)

    # Minimums and maximums
    offsets_min = {
        "Speed": 10, "RPM": 100, "Gear": 0.05, "Throttle": 2, "Brake": 0.035, "glon": 1, "Delta": 0
    }
    offsets_max = {
        "Speed": 10, "RPM": 100, "Gear": 0.08, "Throttle": 3, "Brake": 0.05, "glon": 1, "Delta": 0
    }
    min_vals = {k: [] for k in ["Speed", "RPM", "Gear", "Throttle", "Brake", "glon", "Delta"]}
    max_vals = {k: [] for k in ["Speed", "RPM", "Gear", "Throttle", "Brake", "glon", "Delta"]}
    
    if state.driver_count <= 1:
        max_vals.pop("Delta", None)
        min_vals.pop("Delta", None)

    min_g = {k: None for k in min_vals.keys()}
    max_g = {k: None for k in max_vals.keys()}
    
    for i in range(state.driver_count):
        # Individual
        telemetry = state.telemetry_data[i]
        for key in min_vals.keys():
            raw_min = min(telemetry[key])
            raw_max = max(telemetry[key])
            
            min_vals[key].append(raw_min - offsets_min[key])
            max_vals[key].append(raw_max + offsets_max[key])

        # For more than 1 driver (Cumulative)
        if state.driver_count >= 1 and i >= 1:
            for key in min_vals.keys():
                min_g[key] = min(min_vals[key][i], min_g[key])
                max_g[key] = max(max_vals[key][i], max_g[key])
        else:
            for key in min_vals.keys():
                min_g[key] = min_vals[key][i]
                max_g[key] = max_vals[key][i]

    # Track trace
    for d in range(1, 22):
        if dpg.does_item_exist(f"track_point{d}"):
            dpg.delete_item(f"track_point{d}")
        if dpg.does_item_exist(f"track_line{d}"):
            dpg.delete_item(f"track_line{d}")

    for i in range(state.driver_count):
        if dpg.does_item_exist(f"track_line{i}"):
            dpg.delete_item(f"track_line{i}")
        dpg.add_line_series(y=state.telemetry_data[i]["y"], x=state.telemetry_data[i]["x"], parent="y_axis", tag=f"track_line{i}")

        if dpg.does_item_exist(f"track_point{i}"):
            dpg.delete_item(f"track_point{i}")
        dpg.add_scatter_series(x=[], y=[], parent="y_axis", tag=f"track_point{i}")

        dpg.fit_axis_data("y_axis")
        dpg.fit_axis_data("x_axis")

    channel_config = [
        ("speed", "Speed", "%4.0f", min_g["Speed"], max_g["Speed"]),
        ("rpm", "RPM", "%4.0f", min_g["RPM"], max_g["RPM"]),
        ("gear", "Gear", "%4.0f",min_g["Gear"], max_g["Gear"]),
        ("throttle", "Throttle", "%4.0f", min_g["Throttle"], max_g["Throttle"]),
        ("brake", "Brake",  "%4.0f", min_g["Brake"], max_g["Brake"]),
        ("glon", "glon", "%4.1f", min_g["glon"], max_g["glon"]),
        ("drs", "DRS", "%4.0f", -0.05, 1.05)    
    ]

    # Remove inactive DRS from 2026
    if year_int >= 2026:
        del channel_config[-1]
        dpg.hide_item("plot_container_drs")
    else:
        if state.current_view == "graphs":
            dpg.show_item("plot_container_drs")

    # Remove delta for single driver
    if state.driver_count > 1 and state.delta and state.current_view == "graphs":
        dpg.show_item("plot_container_delta")
        if "Delta" in min_g:
            channel_config.insert(0, ("delta", "Delta", "%4.1f", min_g["Delta"], max_g["Delta"]))
    else:
        dpg.hide_item("plot_container_delta")

    if state.current_view == "graphs":
        for ch, label, tick_fmt, ymin, ymax in channel_config:
            plot = dpg.add_plot(height=state.graph_h, width=-1, tag=f"my_plot_{ch}", parent=f"plot_container_{ch}", crosshairs=True, zoom_mod=True, no_frame=True, no_title=True, no_menus=True)
            if ch == "speed":
                dpg.add_plot_legend(parent="my_plot_speed")
            dpg.add_plot_axis(dpg.mvXAxis, parent=plot, tag=f"x_axis_{ch}", no_highlight=True, no_tick_labels=True)
            if ch == channel_config[-1]:
                dpg.add_plot_axis(dpg.mvXAxis, label="Distance (m)", parent=plot, tag=f"x_axis_{ch}", no_highlight=True, no_tick_labels=True)
            dpg.add_plot_axis(dpg.mvYAxis, label=label, parent=plot, tag=f"y_axis_{ch}", no_highlight=True, tick_format=tick_fmt)
            for i in range(state.driver_count):
                x_data = state.telemetry_data[i]["Distances"] if ch == "delta" else state.telemetry_data[i]["Distance"]
                dpg.add_line_series(x=x_data, y=state.telemetry_data[i][label], parent=f"y_axis_{ch}", label=f"{state.drivers[i]}", tag=f"{ch}_line{i}")
            dpg.set_axis_limits(f"y_axis_{ch}", ymin=ymin, ymax=ymax)
            if ch == "rpm":
                dpg.set_axis_ticks("y_axis_rpm", ((" 7k", 7000), (" 8k", 8000), (" 9k", 9000), (" 10k", 10000), (" 11k", 11000), (" 12k", 12000)))
            if ch == "brake":
                dpg.set_axis_ticks("y_axis_brake", (("   0", 0), ("   1", 1)))
   
    elif state.current_view == "histogram":
        real_height_h = dpg.get_item_height("hist_container") / 4
        for ch, label, tick_fmt, ymin, ymax in channel_config[:4]:
            hist = dpg.add_plot(height=real_height_h, width=-1, label=label, tag=f"my_hist_{ch}", parent="hist_container", no_frame=True, no_menus=True, zoom_mod=True)
            dpg.add_plot_axis(dpg.mvXAxis, parent=hist, tag=f"x_axis_hist_{ch}", no_highlight=True)
            dpg.add_plot_axis(dpg.mvYAxis, parent=hist, tag=f"y_axis_hist_{ch}", no_highlight=True, tick_format="%3g")
            for i in range(state.driver_count):
                data = np.array(state.telemetry_data[i][label])
                h, b = np.histogram(data, bins=200)
                total = len(data)
                hist_percent = (h / total) * 100
                bin_centers = (b[:-1] + b[1:]) / 2
                dpg.add_bar_series(x = bin_centers.astype(np.float64), y = hist_percent.astype(np.float64), parent=f"y_axis_hist_{ch}", label=f"{state.drivers[i]} {label}", tag=f"{ch}_line_hist{i}", weight=0.8)
                dpg.set_axis_limits(f"x_axis_hist_{ch}", ymin=ymin, ymax=ymax)

    elif state.current_view == "scatter":
        # RPM vs Speed
        scatterR = dpg.add_plot(height=-1, width=-1, tag="my_rpm_vs_speed", parent="rpm_vs_speed", crosshairs=True, zoom_mod=True, no_frame=True, no_title=True, no_menus=True)
        dpg.add_plot_axis(dpg.mvXAxis, parent=scatterR, tag="x_axis_glon_r", no_highlight=True)
        dpg.add_plot_axis(dpg.mvYAxis, label="RPM", parent=scatterR, tag="y_axis_speed_r", no_highlight=True)
        dpg.set_axis_ticks("y_axis_speed_r", (("7k", 7000), ("8k", 8000), ("9k", 9000), ("10k", 10000), ("11k", 11000), ("12k", 12000)))
        for i in range(state.driver_count):
            dpg.add_scatter_series(x = state.telemetry_data[i]["Speed"], y = state.telemetry_data[i]["RPM"], parent="y_axis_speed_r", tag=f"rpm_line_sct{i}")
       
        # Glon vs Speed
        scatterG = dpg.add_plot(height=-1, width=-1, tag="my_glon_vs_speed", parent="glon_vs_speed", crosshairs=True, zoom_mod=True, no_frame=True, no_title=True, no_menus=True)
        dpg.add_plot_axis(dpg.mvXAxis, label="Speed", parent=scatterG, tag="x_axis_glon_g", no_highlight=True)
        dpg.add_plot_axis(dpg.mvYAxis, label="Longitudinal Forces (G)", parent=scatterG, tag="y_axis_speed_g", no_highlight=True, tick_format="%3.0f")
        for i in range(state.driver_count):
            dpg.add_scatter_series(x = state.telemetry_data[i]["Speed"], y = state.telemetry_data[i]["glon"], parent="y_axis_speed_g", tag=f"glon_line_sct{i}")

    elif state.current_view == "stats":
        # Delete table if it exists
        if dpg.does_item_exist("stats_table"):
            dpg.delete_item("stats_table")

        variables = []
        for ch, label, tick_fmt, ymin, ymax in channel_config:
            for i in range(state.driver_count):
                variables.append((f"{state.drivers[i]} {label}", state.telemetry_data[i][label]))
           
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
    hex_to_rgb()

def update_car_position(user_data):
    plot_tags = ["my_plot_speed", "my_plot_rpm", "my_plot_gear", "my_plot_throttle", "my_plot_brake", "my_plot_glon", "my_plot_drs"]
    is_hovered = any(dpg.is_item_hovered(tag)
        for tag in plot_tags
        if dpg.does_item_exist(tag))
    if not is_hovered:
        return
    try:
        for i in range(state.driver_count):
            mouse_pos = dpg.get_plot_mouse_pos()
            mouse_x = mouse_pos[0]
            if state.telemetry_data:
                distance = state.telemetry_data[i]["Distance"]
            idx = min(range(len(distance)), key=lambda i: abs(distance[i] - mouse_x))
        
            plot_x = state.telemetry_data[i]["x"][idx]
            plot_y = state.telemetry_data[i]["y"][idx]
            dpg.configure_item(item=f"track_point{i}", x=[plot_x], y=[plot_y])

    except Exception:
        pass