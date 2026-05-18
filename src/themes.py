import dearpygui.dearpygui as dpg
from state import state
import fastf1
from fastf1 import plotting

def default_themes():
    with dpg.theme(tag="main_theme"):
        with dpg.theme_component(dpg.mvAll):
            # Main colors
            dpg.add_theme_color(dpg.mvThemeCol_WindowBg, (18, 18, 22, 255))
            dpg.add_theme_color(dpg.mvThemeCol_ChildBg, (22, 22, 28, 255))
            dpg.add_theme_color(dpg.mvThemeCol_PopupBg, (25, 25, 32, 240))
            dpg.add_theme_color(dpg.mvThemeCol_Border, (60, 60, 70, 180))
            dpg.add_theme_color(dpg.mvThemeCol_Tab, (35, 35, 45, 255))
            dpg.add_theme_color(dpg.mvThemeCol_TabHovered, (230, 92, 0, 180))
            dpg.add_theme_color(dpg.mvThemeCol_TabActive, (200, 70, 0, 255))
            dpg.add_theme_color(dpg.mvThemeCol_TitleBg, (18, 18, 22, 255))
            dpg.add_theme_color(dpg.mvThemeCol_TitleBgActive, (25, 25, 32, 255))
           
            # Text and important elements
            dpg.add_theme_color(dpg.mvThemeCol_Text, (235, 235, 240, 255))
            dpg.add_theme_color(dpg.mvThemeCol_TextDisabled, (110, 110, 125, 255))
           
            # Orange
            dpg.add_theme_color(dpg.mvThemeCol_Button, (230, 92, 0, 255))
            dpg.add_theme_color(dpg.mvThemeCol_ButtonHovered, (255, 125, 40, 255))
            dpg.add_theme_color(dpg.mvThemeCol_ButtonActive, (200, 70, 0, 255))    
            dpg.add_theme_color(dpg.mvThemeCol_FrameBg, (35, 35, 45, 255))
            dpg.add_theme_color(dpg.mvThemeCol_FrameBgHovered, (50, 50, 65, 255))
            dpg.add_theme_color(dpg.mvThemeCol_FrameBgActive, (40, 40, 55, 255))
            dpg.add_theme_color(dpg.mvThemeCol_Header, (230, 92, 0, 180))
            dpg.add_theme_color(dpg.mvThemeCol_HeaderHovered, (255, 125, 40, 220))
            dpg.add_theme_color(dpg.mvThemeCol_HeaderActive, (200, 70, 0, 255))
           
            # Rounded edges and spacing
            dpg.add_theme_style(dpg.mvStyleVar_WindowRounding, 2)
            dpg.add_theme_style(dpg.mvStyleVar_FrameRounding, 2)
            dpg.add_theme_style(dpg.mvStyleVar_ChildRounding, 2)
            dpg.add_theme_style(dpg.mvStyleVar_PopupRounding, 2)
            dpg.add_theme_style(dpg.mvStyleVar_FramePadding, 6, 5)
            dpg.add_theme_style(dpg.mvStyleVar_ItemSpacing, 8, 6)

    # Deleted border and transparency for containers
    with dpg.theme(tag="no_padding_window"):
        with dpg.theme_component(dpg.mvChildWindow):
            dpg.add_theme_color(dpg.mvThemeCol_ChildBg, (0, 0, 0, 0))
            dpg.add_theme_style(dpg.mvStyleVar_WindowPadding, 0, 0, category=dpg.mvThemeCat_Core)
            dpg.add_theme_style(dpg.mvStyleVar_ItemSpacing, 0, 0, category=dpg.mvThemeCat_Core)
   
    # Transparent containers
    with dpg.theme(tag="transparent_window"):
        with dpg.theme_component(dpg.mvChildWindow):
            dpg.add_theme_color(dpg.mvThemeCol_ChildBg, (0, 0, 0, 0))
   
    # Custom colors for graphs
    with dpg.theme(tag="track_point_theme"):
        with dpg.theme_component(dpg.mvScatterSeries):
            dpg.add_theme_color(dpg.mvPlotCol_MarkerFill, (255, 105, 180, 255), category=dpg.mvThemeCat_Plots)
            dpg.add_theme_color(dpg.mvPlotCol_MarkerOutline, (255, 105, 180, 255), category=dpg.mvThemeCat_Plots)
    with dpg.theme(tag="track_line_theme"):
        with dpg.theme_component(dpg.mvLineSeries):
            dpg.add_theme_color(dpg.mvPlotCol_Line, (255, 255, 255, 200), category=dpg.mvThemeCat_Plots)
           
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
        with dpg.theme_component(dpg.mvScatterSeries):
            dpg.add_theme_color(dpg.mvPlotCol_Line, (255, 105, 180, 255), category=dpg.mvThemeCat_Plots)

    with dpg.theme(tag="rpm_theme2"):
        with dpg.theme_component(dpg.mvLineSeries):
            dpg.add_theme_color(dpg.mvPlotCol_Line, (255, 255, 255, 200), category=dpg.mvThemeCat_Plots)  # White
        with dpg.theme_component(dpg.mvBarSeries):
            dpg.add_theme_color(dpg.mvPlotCol_Fill, (255, 255, 255, 200), category=dpg.mvThemeCat_Plots)
        with dpg.theme_component(dpg.mvScatterSeries):
            dpg.add_theme_color(dpg.mvPlotCol_Line, (255, 255, 255, 200), category=dpg.mvThemeCat_Plots)

    with dpg.theme(tag="gear_theme"):
        with dpg.theme_component(dpg.mvLineSeries):
            dpg.add_theme_color(dpg.mvPlotCol_Line, (255, 165, 0, 255), category=dpg.mvThemeCat_Plots)  # Orange
        with dpg.theme_component(dpg.mvBarSeries):
            dpg.add_theme_color(dpg.mvPlotCol_Fill, (255, 165, 0, 220), category=dpg.mvThemeCat_Plots)
    with dpg.theme(tag="gear_theme2"):
        with dpg.theme_component(dpg.mvLineSeries):
            dpg.add_theme_color(dpg.mvPlotCol_Line, (255, 255, 255, 200), category=dpg.mvThemeCat_Plots)  # White
        with dpg.theme_component(dpg.mvBarSeries):
            dpg.add_theme_color(dpg.mvPlotCol_Fill, (255, 255, 255, 220), category=dpg.mvThemeCat_Plots)

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

    with dpg.theme(tag="glon_theme"):
        with dpg.theme_component(dpg.mvLineSeries):
            dpg.add_theme_color(dpg.mvPlotCol_Line, (0, 255, 255, 255), category=dpg.mvThemeCat_Plots)  # Cyan    
        with dpg.theme_component(dpg.mvScatterSeries):
            dpg.add_theme_color(dpg.mvPlotCol_Line, (0, 255, 255, 255), category=dpg.mvThemeCat_Plots)            
    with dpg.theme(tag="glon_theme2"):
        with dpg.theme_component(dpg.mvLineSeries):
            dpg.add_theme_color(dpg.mvPlotCol_Line, (255, 255, 255, 200), category=dpg.mvThemeCat_Plots)  # White
        with dpg.theme_component(dpg.mvScatterSeries):
            dpg.add_theme_color(dpg.mvPlotCol_Line, (255, 255, 255, 200), category=dpg.mvThemeCat_Plots)

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

def hex_to_rgb():
    hex_enabled = dpg.get_value("hex")
    Compare = dpg.get_value("Compare")
    channels = ["speed", "rpm", "gear", "throttle", "brake", "glon", "drs"]

    if hex_enabled:
        try:
            state.hex_colors = fastf1.plotting.get_driver_color(state.drivers[0], state.session).lstrip('#')
            state.set_driver_color(0, state.hex_colors)

            if dpg.does_item_exist("track_point_themeT") and dpg.does_item_exist("track_point"):
                    dpg.bind_item_theme("track_point", "track_point_theme")
            if dpg.does_item_exist("track_point_themeT"):
                dpg.delete_item("track_point_themeT")
            with dpg.theme(tag="track_point_themeT"):
                with dpg.theme_component(dpg.mvScatterSeries):
                    dpg.add_theme_color(dpg.mvPlotCol_MarkerOutline, state.driver_colors[0], category=dpg.mvThemeCat_Plots)
                    dpg.add_theme_color(dpg.mvPlotCol_MarkerFill, state.driver_colors[0], category=dpg.mvThemeCat_Plots)

            for channel in channels:
                tag = f"{channel}_themeT"
                if dpg.does_item_exist(tag):
                    dpg.delete_item(tag)
                with dpg.theme(tag=tag):
                    with dpg.theme_component(dpg.mvLineSeries):
                        dpg.add_theme_color(dpg.mvPlotCol_Line, state.driver_colors[0], category=dpg.mvThemeCat_Plots)
                    with dpg.theme_component(dpg.mvBarSeries):
                        dpg.add_theme_color(dpg.mvPlotCol_Fill, state.driver_colors[0], category=dpg.mvThemeCat_Plots)  
                    with dpg.theme_component(dpg.mvScatterSeries):
                        dpg.add_theme_color(dpg.mvPlotCol_Line, state.driver_colors[0], category=dpg.mvThemeCat_Plots)  

            if Compare:
                state.hex_colors = fastf1.plotting.get_driver_color(state.drivers[1], state.session).lstrip('#')
                state.set_driver_color(1, state.hex_colors)

                for channel in channels:
                    tag2 = f"{channel}_themeT2"
                    if dpg.does_item_exist(tag2):
                        dpg.delete_item(tag2)
                    with dpg.theme(tag=tag2):
                        with dpg.theme_component(dpg.mvLineSeries):
                            dpg.add_theme_color(dpg.mvPlotCol_Line, state.driver_colors[1], category=dpg.mvThemeCat_Plots)
                        with dpg.theme_component(dpg.mvBarSeries):
                            dpg.add_theme_color(dpg.mvPlotCol_Fill, state.driver_colors[1], category=dpg.mvThemeCat_Plots)  
                        with dpg.theme_component(dpg.mvScatterSeries):
                            dpg.add_theme_color(dpg.mvPlotCol_Line, state.driver_colors[1], category=dpg.mvThemeCat_Plots)  
        except Exception as e:
            dpg.set_value("result_text", f"Team color error: {e}")
    bind_themes()
           
def bind_themes():
    channels = ["speed", "rpm", "gear", "throttle", "brake", "glon", "drs"]
    hex_enabled = dpg.get_value("hex")
    tab = ""
   
    if hex_enabled:
        suffix = "T"
    else:
        suffix = ""

    if state.current_view == "graphs":
        tab = ""
        channels = ["speed", "rpm", "gear", "throttle", "brake", "glon", "drs"]
    elif state.current_view == "histogram":
        tab = "_hist"
        channels = channels[:4]
    elif state.current_view == "scatter":
        tab = "_sct"
        channels = ["rpm", "glon"]
    elif state.current_view == "stats":
        tab = "stats"

    dpg.bind_item_theme("track_point", f"track_point_theme{suffix}")

    for channel in channels:
        if tab != "stats":
            line = f"{channel}_line{tab}"
            tag = f"{channel}_theme{suffix}"  
            if dpg.does_item_exist(line):          
                dpg.bind_item_theme(line, tag)
               
    if dpg.get_value("Compare"):
        for channel in channels:
            if tab != "stats":
                line2 = f"{channel}_line{tab}2"
                tag2 = f"{channel}_theme{suffix}2"
                if dpg.does_item_exist(line2):  
                    dpg.bind_item_theme(line2, tag2)