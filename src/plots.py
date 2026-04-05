import dearpygui.dearpygui as dpg
from state import state
from themes import hex_to_rgb
import numpy as np

def update_plots():
    Compare = dpg.get_value("Compare")
    year = dpg.get_value("year_input")
    year_int = int(year) if year else 2025

    if not state.telemetry_data:
        dpg.set_value("result_text", "No telemetry data available. Please load telemetry first.")
        return

    for item in ["my_hist_speed", "my_hist_rpm", "my_hist_gear", "my_hist_throttle", "my_hist_brake",
                "my_plot_speed", "my_plot_rpm", "my_plot_gear", "my_plot_throttle", "my_plot_brake", "my_plot_drs"]:
     if dpg.does_item_exist(item):
         dpg.delete_item(item)

    minSpeed = min(state.telemetry_data[0]["Speed"]) - 10
    maxSpeed = max(state.telemetry_data[0]["Speed"]) + 10
    minRPM = min(state.telemetry_data[0]["RPM"]) - 100
    maxRPM = max(state.telemetry_data[0]["RPM"]) + 100
    minGear = min(state.telemetry_data[0]["Gear"]) - 0.05
    maxGear = max(state.telemetry_data[0]["Gear"]) + 0.08
    minThrottle = min(state.telemetry_data[0]["Throttle"])
    maxThrottle = max(state.telemetry_data[0]["Throttle"])
    minBrake = min(state.telemetry_data[0]["Brake"]) - 0.035
    maxBrake = max(state.telemetry_data[0]["Brake"]) + 0.05
    maxTime = max(state.telemetry_data[0]["Time"]) + 2

    dpg.configure_item("track_line", y=state.telemetry_data[0]["y"], x=state.telemetry_data[0]["x"])

    if Compare and state.telemetry_data[1]:
        minSpeed = min(minSpeed, min(state.telemetry_data[1]["Speed"]) - 10)
        maxSpeed = max(maxSpeed, max(state.telemetry_data[1]["Speed"]) + 10)
        minRPM = min(minRPM, min(state.telemetry_data[1]["RPM"]) - 100)
        maxRPM = max(maxRPM, max(state.telemetry_data[1]["RPM"]) + 100)
        minGear = min(minGear, min(state.telemetry_data[1]["Gear"]) - 0.05)
        maxGear = max(maxGear, max(state.telemetry_data[1]["Gear"]) + 0.08)
        minThrottle = min(minThrottle, min(state.telemetry_data[1]["Throttle"]))
        maxThrottle = max(maxThrottle, max(state.telemetry_data[1]["Throttle"]))
        minBrake = min(minBrake, min(state.telemetry_data[1]["Brake"]) - 0.035)
        maxBrake = max(maxBrake, max(state.telemetry_data[1]["Brake"]) + 0.05)    
    
    channel_config = [
        ("speed",    "Speed",    "(km/h)",  "%.3g", minSpeed,    maxSpeed),
        ("rpm",      "RPM",      "RPM",     None,   minRPM,      maxRPM),
        ("gear",     "Gear",     "Count",   "%0.1f",minGear,     maxGear),
        ("throttle", "Throttle", "%",       "%.3g", minThrottle-2, maxThrottle+3),
        ("brake",    "Brake",    "on-off",  "%.3g", minBrake,    maxBrake),
        ("drs",      "DRS",      "on-off",  "%.3g", -0.05,       1.05),
    ]       

    if state.current_view == "telemetry":
        real_height = ((dpg.get_item_height("plot_container_speed")-17) + (dpg.get_item_height("plot_container_rpm")-17) + (dpg.get_item_height("plot_container_gear")-17) + (dpg.get_item_height("plot_container_throttle")-17) + (dpg.get_item_height("plot_container_brake")-17) + (dpg.get_item_height("plot_container_drs")-17)) / 6 
        for ch, label, y_label, tick_fmt, ymin, ymax in channel_config:
            plot = dpg.add_plot(label=label, height=real_height, width=-1, tag=f"my_plot_{ch}", parent=f"plot_container_{ch}", crosshairs=True, zoom_mod=True, no_frame=True, no_menus=True)
            dpg.add_plot_axis(dpg.mvXAxis, parent=plot, tag=f"x_axis_{ch}", no_highlight=True, no_tick_labels=True)
            dpg.add_plot_axis(dpg.mvYAxis, label=y_label, parent=plot, tag=f"y_axis_{ch}", no_highlight=True, tick_format=tick_fmt)
            dpg.add_line_series(x=state.telemetry_data[0]["Distance"], y=state.telemetry_data[0][label], parent=f"y_axis_{ch}", label=f"{state.drivers[0]} {label}", tag=f"{ch}_line")
            if Compare and state.telemetry_data[1]:
                dpg.add_line_series(x=state.telemetry_data[1]["Distance"], y=state.telemetry_data[1][label], parent=f"y_axis_{ch}", label=f"{state.drivers[1]} {label}", tag=f"{ch}_line2")
            dpg.set_axis_limits(f"y_axis_{ch}", ymin=ymin, ymax=ymax)

    elif state.current_view == "histogram":
        for ch, label, y_label, tick_fmt, ymin, ymax in channel_config[:4]:
            hist = dpg.add_plot(height=218, width=-1, label=label, tag=f"my_hist_{ch}", parent="hist_container", no_frame=True, no_menus=True)
            dpg.add_plot_axis(dpg.mvXAxis, parent=hist, tag=f"x_axis_hist_{ch}", no_highlight=True)
            dpg.add_plot_axis(dpg.mvYAxis, parent=hist, tag=f"y_axis_hist_{ch}", no_highlight=True)
            hist_s, bins_s = np.histogram(a=state.telemetry_data[0][label], bins=200)
            total = len(state.telemetry_data[0][label])
            hist_s_percent = (hist_s/total) * 100
            bin_center_s = (bins_s[:-1] + bins_s[1:]) / 2
            dpg.add_bar_series(x = bin_center_s.astype(np.float64), y = hist_s_percent.astype(np.float64), parent=f"y_axis_hist_{ch}", label=f"{state.drivers[0]} {label}", tag=f"{ch}_line_hist", weight=0.8)
            dpg.set_axis_limits(f"x_axis_hist_{ch}", ymin=ymin, ymax=ymax)
            dpg.set_axis_limits(f"y_axis_hist_{ch}", ymin=0, ymax=max(hist_s_percent))
            if Compare and state.telemetry_data[1]:
                hist_s2, bins_s2 = np.histogram(a=state.telemetry_data[1][label], bins=200)
                total2 = len(state.telemetry_data[1][label])
                hist_s_percent2 = (hist_s2/total2) * 100
                bin_center_s2 = (bins_s2[:-1] + bins_s2[1:]) / 2
                dpg.add_bar_series(x = bin_center_s2.astype(np.float64), y = hist_s_percent2.astype(np.float64), parent=f"y_axis_hist_{ch}", label=f"{state.drivers[1]} {label}", tag=f"{ch}_line_hist2", weight=0.8)
                dpg.set_axis_limits(f"x_axis_hist_{ch}", ymin=ymin, ymax=ymax)
                dpg.set_axis_limits(f"y_axis_hist_{ch}", ymin=0, ymax=max(hist_s_percent2))

    elif state.current_view == "stats":
        # Delete table if it exists
        if dpg.does_item_exist("stats_table"):
            dpg.delete_item("stats_table")

        variables = []
        if Compare:
            for ch, label, y_label, tick_fmt, ymin, ymax in channel_config:
                variables.append((f"{state.drivers[0]} {label}", state.telemetry_data[0][label]))
                variables.append((f"{state.drivers[1]} {label}", state.telemetry_data[1][label]))
        else:
            for ch, label, y_label, tick_fmt, ymin, ymax in channel_config:
                variables.append((f"{state.drivers[0]} {label}", state.telemetry_data[0][label]))
            
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
        
    if Compare and state.telemetry_data[1]:
        dpg.set_value("result_text", f"Telemetry successfully loaded for {state.drivers[0]} Lap: {state.selected_laps[0] if state.selected_laps[0] != 0 else "fastest"} and {state.drivers[1]} Lap: {state.selected_laps[1] if state.selected_laps[1] != 0 else "fastest"} {state.track} {year_int}")
    else:
        dpg.set_value("result_text", f"Telemetry successfully loaded for {state.drivers[0]} {state.track} {year_int} Lap: {state.selected_laps[0] if state.selected_laps[0] != 0 else "fastest"}")
    hex_to_rgb()

def update_car_position(user_data):
    if state.telemetry_data:
        distance = state.telemetry_data[0]["Distance"]
    
        plot_tags = ["my_plot_speed", "my_plot_rpm", "my_plot_gear", "my_plot_throttle", "my_plot_brake", "my_plot_drs"]
        is_hovered = any(dpg.is_item_hovered(tag)
            for tag in plot_tags
            if dpg.does_item_exist(tag))
        if not is_hovered:
            return
        try:
            mouse_pos = dpg.get_plot_mouse_pos()
            mouse_x = mouse_pos[0]
            idx = min(range(len(distance)), key=lambda i: abs(distance[i] - mouse_x))
            plot_x = state.telemetry_data[0]["x"][idx]
            plot_y = state.telemetry_data[0]["y"][idx]
            dpg.configure_item("track_point", x=[plot_x], y=[plot_y])
        except Exception:
            pass