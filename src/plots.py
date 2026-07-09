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
                "my_plot_speed", "my_plot_rpm", "my_plot_gear", "my_plot_throttle", "my_plot_brake", "my_plot_glon", "my_plot_drs",
                "my_rpm_vs_speed", "my_glon_vs_speed"]:
     if dpg.does_item_exist(item):
         dpg.delete_item(item)

    minSpeed = []          
    maxSpeed = []
    minRPM = []
    maxRPM = []
    minGear = []
    maxGear= [] 
    minThrottle = []
    maxThrottle = []
    minBrake = []
    maxBrake = []
    minGlon = []
    maxGlon = []

    for i in range(state.driver_count):
        minSpeed.append(min(state.telemetry_data[i]["Speed"]) - 10)          
        maxSpeed.append(max(state.telemetry_data[i]["Speed"]) + 10)
        minRPM.append(min(state.telemetry_data[i]["RPM"]) - 100)
        maxRPM.append(max(state.telemetry_data[i]["RPM"]) + 100)
        minGear.append(min(state.telemetry_data[i]["Gear"]) - 0.05)
        maxGear.append(max(state.telemetry_data[i]["Gear"]) + 0.08)
        minThrottle.append(min(state.telemetry_data[i]["Throttle"]))
        maxThrottle.append(max(state.telemetry_data[i]["Throttle"]))
        minBrake.append(min(state.telemetry_data[i]["Brake"]) - 0.035)
        maxBrake.append(max(state.telemetry_data[i]["Brake"]) + 0.05)
        minGlon.append(min(state.telemetry_data[i]["glon"]) - 1)
        maxGlon.append(max(state.telemetry_data[i]["glon"]) + 1)

        # For more than 1 driver
        if state.driver_count >= 1 and i >= 1:
            minSpeed_g = min(minSpeed[i], minSpeed[i-1])
            maxSpeed_g = max(maxSpeed[i], maxSpeed[i-1])
            minRPM_g = min(minRPM[i], minRPM[i-1])
            maxRPM_g = max(maxRPM[i], maxRPM[i-1])
            minGear_g = min(minGear[i], minGear[i-1])
            maxGear_g = max(maxGear[i], maxGear[i-1])
            minThrottle_g = min(minThrottle[i], minThrottle[i-1])
            maxThrottle_g = max(maxThrottle[i], maxThrottle[i-1])
            minBrake_g = min(minBrake[i], minBrake[i-1])
            maxBrake_g = max(maxBrake[i], maxBrake[i-1])
            minGlon_g = min(minGlon[i], minGlon[i-1])
            maxGlon_g = max(maxGlon[i], maxGlon[i-1])
        else:
            minSpeed_g = minSpeed[i]
            maxSpeed_g = maxSpeed[i]
            minRPM_g = minRPM[i] 
            maxRPM_g = maxRPM[i]
            minGear_g = minGear[i]
            maxGear_g = maxGear[i]
            minThrottle_g = minThrottle[i]
            maxThrottle_g = maxThrottle[i]
            minBrake_g = minBrake[i]
            maxBrake_g = maxBrake[i]
            minGlon_g = minGlon[i]
            maxGlon_g = maxGlon[i]

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
        ("speed", "Speed", "%.3g", minSpeed_g, maxSpeed_g),
        ("rpm", "RPM", "%.3g", minRPM_g, maxRPM_g),
        ("gear", "Gear", "%0.1f",minGear_g, maxGear_g),
        ("throttle", "Throttle", "%.3g", minThrottle_g-2, maxThrottle_g+3),
        ("brake", "Brake",  "%.3g", minBrake_g, maxBrake_g),
        ("glon", "glon", "%3.0f", minGlon_g, maxGlon_g),
        ("drs", "DRS", "%.3g", -0.05, 1.05)    
    ]

    # Remove inactive DRS from 2026
    if year_int >= 2026:
        del channel_config[-1]
        dpg.hide_item("plot_container_drs")
    else:
        if state.current_view == "graphs":
            dpg.show_item("plot_container_drs")

    if state.current_view == "graphs":
        for ch, label, tick_fmt, ymin, ymax in channel_config:
            plot = dpg.add_plot(height=state.graph_h, width=-1, tag=f"my_plot_{ch}", parent=f"plot_container_{ch}", crosshairs=True, zoom_mod=True, no_frame=True, no_title=True, no_menus=True)
            dpg.add_plot_legend(parent="my_plot_speed")
            dpg.add_plot_axis(dpg.mvXAxis, parent=plot, tag=f"x_axis_{ch}", no_highlight=True, no_tick_labels=True)
            if ch == channel_config[-1]:
                dpg.add_plot_axis(dpg.mvXAxis, label="Distance (m)", parent=plot, tag=f"x_axis_{ch}", no_highlight=True, no_tick_labels=True)
            dpg.add_plot_axis(dpg.mvYAxis, label=label, parent=plot, tag=f"y_axis_{ch}", no_highlight=True, tick_format=tick_fmt)
            for i in range(state.driver_count):
                dpg.add_line_series(x=state.telemetry_data[i]["Distance"], y=state.telemetry_data[i][label], parent=f"y_axis_{ch}", label=f"{state.drivers[i]}", tag=f"{ch}_line{i}")
            dpg.set_axis_limits(f"y_axis_{ch}", ymin=ymin, ymax=ymax)
            if ch == "rpm":
                dpg.set_axis_ticks("y_axis_rpm", (("7k", 7000), ("8k", 8000), ("9k", 9000), ("10k", 10000), ("11k", 11000), ("12k", 12000)))
            if ch == "brake":
                dpg.set_axis_ticks("y_axis_brake", (("  0", 0), ("  1", 1)))
   
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