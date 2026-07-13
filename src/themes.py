import dearpygui.dearpygui as dpg
from state import state
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
            dpg.add_theme_color(dpg.mvPlotCol_Line, (255, 255, 255, 200), category=dpg.mvThemeCat_Plots)    # White

    with dpg.theme(tag="delta_theme0"):
        with dpg.theme_component(dpg.mvLineSeries):
            dpg.add_theme_color(dpg.mvPlotCol_Line, (255, 255, 255, 200), category=dpg.mvThemeCat_Plots)    # White
                    
    with dpg.theme(tag="speed_theme0"):
        with dpg.theme_component(dpg.mvLineSeries):
            dpg.add_theme_color(dpg.mvPlotCol_Line, (0, 0, 255), category=dpg.mvThemeCat_Plots)  # Blue
        with dpg.theme_component(dpg.mvBarSeries):
            dpg.add_theme_color(dpg.mvPlotCol_Fill, (0, 0, 255, 200), category=dpg.mvThemeCat_Plots)

    with dpg.theme(tag="rpm_theme0"):
        with dpg.theme_component(dpg.mvLineSeries):
            dpg.add_theme_color(dpg.mvPlotCol_Line, (255, 105, 180, 255), category=dpg.mvThemeCat_Plots)  # Pink
        with dpg.theme_component(dpg.mvBarSeries):
            dpg.add_theme_color(dpg.mvPlotCol_Fill, (255, 105, 180, 200), category=dpg.mvThemeCat_Plots)
        with dpg.theme_component(dpg.mvScatterSeries):
            dpg.add_theme_color(dpg.mvPlotCol_Line, (255, 105, 180, 255), category=dpg.mvThemeCat_Plots)

    with dpg.theme(tag="gear_theme0"):
        with dpg.theme_component(dpg.mvLineSeries):
            dpg.add_theme_color(dpg.mvPlotCol_Line, (255, 165, 0, 255), category=dpg.mvThemeCat_Plots)  # Orange
        with dpg.theme_component(dpg.mvBarSeries):
            dpg.add_theme_color(dpg.mvPlotCol_Fill, (255, 165, 0, 220), category=dpg.mvThemeCat_Plots)

    with dpg.theme(tag="throttle_theme0"):
        with dpg.theme_component(dpg.mvLineSeries):
            dpg.add_theme_color(dpg.mvPlotCol_Line, (0, 255, 0, 255), category=dpg.mvThemeCat_Plots)  # Green
        with dpg.theme_component(dpg.mvBarSeries):
            dpg.add_theme_color(dpg.mvPlotCol_Fill, (0, 255, 0, 255), category=dpg.mvThemeCat_Plots)

    with dpg.theme(tag="brake_theme0"):
        with dpg.theme_component(dpg.mvLineSeries):
            dpg.add_theme_color(dpg.mvPlotCol_Line, (255, 0, 0, 255), category=dpg.mvThemeCat_Plots)  # Red          

    with dpg.theme(tag="glon_theme0"):
        with dpg.theme_component(dpg.mvLineSeries):
            dpg.add_theme_color(dpg.mvPlotCol_Line, (0, 255, 255, 255), category=dpg.mvThemeCat_Plots)  # Cyan    
        with dpg.theme_component(dpg.mvScatterSeries):
            dpg.add_theme_color(dpg.mvPlotCol_Line, (0, 255, 255, 255), category=dpg.mvThemeCat_Plots)            

    with dpg.theme(tag="drs_theme0"):
        with dpg.theme_component(dpg.mvLineSeries):
            dpg.add_theme_color(dpg.mvPlotCol_Line, (255, 255, 0, 255), category=dpg.mvThemeCat_Plots)  # Yellow

    with dpg.theme(tag="purple_button_theme"):
        with dpg.theme_component(dpg.mvButton):
            dpg.add_theme_color(dpg.mvThemeCol_Button, (128, 0, 128, 255), category=dpg.mvThemeCat_Core)  # Purple background
            dpg.add_theme_color(dpg.mvThemeCol_ButtonHovered, (160, 32, 160, 255), category=dpg.mvThemeCat_Core)  # Lighter purple
            dpg.add_theme_color(dpg.mvThemeCol_ButtonActive, (100, 0, 100, 255), category=dpg.mvThemeCat_Core)  # Darker purple

def hex_to_rgb_text():
    for i in range(len(state.session.drivers)):
        abb = state.session.get_driver(state.session.drivers[i])["Abbreviation"]
        state.hex_colors = plotting.get_driver_color(abb, state.session).lstrip("#")
        state.set_driver_color(i, state.hex_colors)
        rgb_color = state.driver_colors[i]
        transparent_color = (*rgb_color, 100)
        transparent_color_dark = (*rgb_color, 140)

        tag_c = f"driver_check_theme{i}"
        if dpg.does_item_exist(tag_c):
            dpg.delete_item(tag_c)
        with dpg.theme(tag=tag_c):
            with dpg.theme_component(dpg.mvSelectable):
                dpg.add_theme_color(dpg.mvThemeCol_Header, transparent_color)
                dpg.add_theme_color(dpg.mvThemeCol_HeaderActive, transparent_color)
                dpg.add_theme_color(dpg.mvThemeCol_HeaderHovered, transparent_color_dark)
                dpg.add_theme_color(dpg.mvThemeCol_Text, state.driver_colors[i])
            
        # Bind
        driver_number = state.session.drivers[i]
        check = f"driver_check_{driver_number}"

        if dpg.does_item_exist(check):
            dpg.bind_item_theme(check, f"driver_check_theme{i}")   

def hex_to_rgb():
    hex_enabled = dpg.get_value("hex")
    channels = ["delta", "speed", "rpm", "gear", "throttle", "brake", "glon", "drs"]
    used_colors = []

    # Delete previous themes
    for i in range(len(state.drivers)):
        if dpg.does_item_exist(f"track_point_themeT{i}"):
            dpg.delete_item(f"track_point_themeT{i}")
        if dpg.does_item_exist(f"track_line_themeT{i}"):
            dpg.delete_item(f"track_line_themeT{i}")
        for channel in channels:
            if dpg.does_item_exist(f"{channel}_themeT{i}"):
                dpg.delete_item(f"{channel}_themeT{i}")
    
    if hex_enabled:
        # Team colors
        for i in range(len(state.drivers)):
            try:
                abb = state.session.get_driver(state.drivers[i])["Abbreviation"]
                hex_color = plotting.get_driver_color(abb, state.session).lstrip("#")
                state.set_driver_color(i, hex_color)
                rgb_color = state.driver_colors[i]
                transparent_color = (*rgb_color, 100)

                # Track Point
                with dpg.theme(tag=f"track_point_themeT{i}"):
                    with dpg.theme_component(dpg.mvScatterSeries):
                        dpg.add_theme_color(dpg.mvPlotCol_MarkerFill, rgb_color, category=dpg.mvThemeCat_Plots)
                        outline = (255, 255, 255, 200) if hex_color in used_colors else rgb_color
                        dpg.add_theme_color(dpg.mvPlotCol_MarkerOutline, outline, category=dpg.mvThemeCat_Plots)

                # Track Line
                with dpg.theme(tag=f"track_line_themeT{i}"):
                    with dpg.theme_component(dpg.mvLineSeries):
                        line_color = transparent_color if hex_color in used_colors else rgb_color
                        dpg.add_theme_color(dpg.mvPlotCol_Line, line_color, category=dpg.mvThemeCat_Plots)

                # Channels
                for channel in channels:
                    with dpg.theme(tag=f"{channel}_themeT{i}"):
                        with dpg.theme_component(dpg.mvLineSeries):
                            line_color = transparent_color if hex_color in used_colors else rgb_color
                            dpg.add_theme_color(dpg.mvPlotCol_Line, line_color, category=dpg.mvThemeCat_Plots)
                        
                        with dpg.theme_component(dpg.mvBarSeries):
                            dpg.add_theme_color(dpg.mvPlotCol_Fill, rgb_color, category=dpg.mvThemeCat_Plots)
                            if hex_color in used_colors:
                                dpg.add_theme_color(dpg.mvPlotCol_Fill, transparent_color, category=dpg.mvThemeCat_Plots)
                        
                        with dpg.theme_component(dpg.mvScatterSeries):
                            dpg.add_theme_color(dpg.mvPlotCol_MarkerFill, rgb_color, category=dpg.mvThemeCat_Plots)
                            outline = (255, 255, 255, 200) if hex_color in used_colors else rgb_color
                            dpg.add_theme_color(dpg.mvPlotCol_MarkerOutline, outline, category=dpg.mvThemeCat_Plots)

                used_colors.append(hex_color)
            except Exception as e:
                dpg.set_value("result_text", f"Team color error: {e}")
    else:
        pass

    bind_themes()

def bind_themes():
    if not state.drivers:
        return

    hex_enabled = dpg.get_value("hex")
    channels = ["delta", "speed", "rpm", "gear", "throttle", "brake", "glon", "drs"]
    
    if state.current_view == "histogram":
        channels = channels[1:5]
    elif state.current_view == "scatter":
        channels = ["rpm", "glon"]
    elif state.current_view == "stats":
        channels = [] 

    tab_suffix = ""
    if state.current_view == "histogram":
        tab_suffix = "_hist"
    elif state.current_view == "scatter":
        tab_suffix = "_sct"

    for i in range(state.driver_count):
        if hex_enabled:
            theme_suffix = f"T{i}" # Team Colors
        else:
            if i == state.fastest_driver_index:
                theme_suffix = "0" # Custom colors
            else:
                theme_suffix = None # No theme dpg default

        if theme_suffix is not None:
            point_theme = f"track_point_theme{theme_suffix}"
            line_theme = f"track_line_theme{theme_suffix}"
            
            if dpg.does_item_exist(f"track_point{i}") and dpg.does_item_exist(point_theme):
                dpg.bind_item_theme(f"track_point{i}", point_theme)
            
            if dpg.does_item_exist(f"track_line{i}") and dpg.does_item_exist(line_theme):
                dpg.bind_item_theme(f"track_line{i}", line_theme)

            for channel in channels:
                if channels:
                    line_tag = f"{channel}_line{tab_suffix}{i}"
                    theme_tag = f"{channel}_theme{theme_suffix}"
                    
                    if dpg.does_item_exist(line_tag) and dpg.does_item_exist(theme_tag):
                        dpg.bind_item_theme(line_tag, theme_tag)