import fastf1
from state import state
from datetime import datetime, timezone
import os
import numpy as np
import pandas as pd
from scipy.interpolate import interp1d
import sys

# Cache setup
# Constant path for cache
if getattr(sys, 'frozen', False):
    # Executing as .exe
    base_dir = os.path.dirname(sys.executable)
else:
    # Executing as script
    base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

cache_dir = os.path.join(base_dir, "fastf1_cache")
os.makedirs(cache_dir, exist_ok=True)
fastf1.Cache.enable_cache(cache_dir)

def is_sprint_weekend(year, track):
    schedule = fastf1.get_event_schedule(int(year))
    event = schedule[schedule['EventName'] == track]
    fmt = event['EventFormat'].values[0]

    if fmt == 'sprint':
        state.is_sprint = True
        state.session_list = ['R', 'SQ', 'FP2', 'Q', 'FP1']
    elif fmt == 'sprint_shootout':
        state.is_sprint = True
        state.session_list = ['R', 'S', 'SS', 'Q', 'FP1']
    elif fmt == 'sprint_qualifying':
        state.is_sprint = True
        state.session_list = ['R', 'Q', 'S', 'SQ', 'FP1']
    else:
        state.is_sprint = False
        state.session_list = ['R', 'Q', 'FP3', 'FP2', 'FP1']

    return state.is_sprint, state.session_list

def load_latest_session(round_delay):
    now = datetime.now(timezone.utc).replace(tzinfo=None)
    state.latest_year = now.year
    state.possible_years = list(range(state.latest_year, 2017, -1))
    state.schedule = fastf1.get_event_schedule(state.latest_year, include_testing=True)
    past_races = state.schedule[state.schedule['Session1DateUtc'] < now]          # At least one session done 
    last_event = past_races.iloc[-round_delay]
    
    while past_races.empty:
        state.latest_year -= 1
        state.schedule = fastf1.get_event_schedule(state.latest_year, include_testing=True)
        past_races = state.schedule[state.schedule['Session1DateUtc'] < now] 
        print("There are no past events for", state.latest_year)

    state.calendar = state.schedule['EventName'].tolist()
    state.track = last_event['EventName']
    test_events = state.schedule[state.schedule['EventFormat'] == 'testing']

    if last_event['RoundNumber'] == 0:
        load_latest_testing(now, test_events)
    else:
        load_latest_race(now)

    if state.latest_year == 2026:
        state.calendar[0] = "Pre-Season Testing 1"
        state.calendar[1] = "Pre-Season Testing 2"


def load_latest_testing(now, test_events):
    state.session_order = ['Practice 3', 'Practice 2', 'Practice 1']
    state.testing = 1
    session_found = False

    for i in range(len(test_events), 0, -1):
        for order in state.session_order:
            try:
                session = fastf1.get_testing_session(state.latest_year, i, int(order))
                session.load(laps=True, telemetry=False, weather=False)
                if session.date < now and not session.laps.empty:
                    state.session = session
                    state.sessionID = order
                    state.track_default = f"{state.track} {i}"
                    state.test_number = i
                    print(f"Sesion loaded: {state.track} - {order}")
                    session_found = True
                    break
            except Exception:
                continue
        if session_found:
            break

def load_latest_race(now):
    state.track_default = state.track
    state.session_order = ['R', 'Q', 'S', 'SQ', 'SS', 'FP3', 'FP2', 'FP1']
    state.testing = 0
    latest_date = None
    latest_id = ""

    is_sprint_weekend(state.latest_year, state.track)

    for order in state.session_order:
        try:
            session = fastf1.get_session(state.latest_year, state.track, order)
            session.load(laps=False, telemetry=False, weather=False)
            if session.date < now and len(session.drivers) != 0:
                if latest_date is None or session.date > latest_date:
                    latest_date = session.date
                    latest_id = order
                    state.session = session
                    print(f"Latest session detected: {state.track} - {order}")
                    break
        except Exception:
            continue

    if len(session.drivers) == 0:
        state.round_delay +=1
        load_latest_session(state.round_delay) 

    state.sessionID = latest_id

def load_session(year_int, session_input, load):
    try:
        if state.testing == 1:
            if year_int == 2026:
                if state.track == "Pre-Season Testing 1":
                    state.test_number = 1
                elif state.track == "Pre-Season Testing 2":
                    state.test_number = 2
            else:
                for i, track_name in enumerate(state.calendar):
                        if track_name == state.track:
                            state.test_number = i+1
            state.session = fastf1.get_testing_session(year_int, state.test_number, session_input)
        else:
            state.session = fastf1.get_session(year_int, state.track, session_input)
        if load == True:
            state.session.load()
        else:
            state.session.load(laps=False, telemetry=False, weather=False)
    except Exception as exc:
        return False, f"The session could not be loaded: {exc}"

    return True, ""

def refresh_done():
    from ui import read_ui_inputs
    year, session, ok, err = read_ui_inputs()
    if ok and session in state.session_list and state.track in state.calendar:
        load_session(year, session, False)
        return ok
    else:
        return False

def get_lap_numbers(driver):
    try:
        driver_laps = state.session.laps.pick_driver(driver)
        lap_numbers = sorted(driver_laps['LapNumber'].unique().tolist())
        fastest_num = int(driver_laps.pick_fastest()['LapNumber'])
        lap_times = []
        for t in driver_laps["LapTime"]:
            if pd.isna(t):
                lap_times.append("No Time")
            else:
                lap_times.append(f"{int(t.total_seconds()//60)}:{t.total_seconds()%60:06.3f}")

        return lap_numbers, fastest_num, lap_times
    
    except Exception as exc:
        print(f"The session could not be loaded correctly: {exc}")
        return [],  None, []
    
def get_calendar(year):
    if year >= 2018:
        state.schedule = fastf1.get_event_schedule(year, include_testing=True)
        state.calendar = state.schedule['EventName'].tolist()
    if year == 2026:
        state.calendar[0] = "Pre-Season Testing 1"
        state.calendar[1] = "Pre-Season Testing 2"

def extract_telemetry(driver, lap_num):
    try:
        driver_laps = state.session.laps.pick_driver(driver)
        lap = driver_laps.pick_fastest() if lap_num == 0 else driver_laps.pick_lap(lap_num)
        tel = lap.get_telemetry()
    except Exception as exc:
        return None, f"Telemetry not found most likely due to a lack of API support"

    data = {
        "Distance": tel["Distance"].to_list(),
        "Speed": tel["Speed"].to_list(),
        "RPM": tel["RPM"].to_list(),
        "Gear": tel["nGear"].to_list(),
        "Throttle": tel["Throttle"].to_list(),
        "Brake": tel["Brake"].to_list(),
        "DRS": [1 if x >= 10 else 0 for x in tel["DRS"].to_list()],
        "Time": tel["Time"].dt.total_seconds().to_list(),
        "x": tel["X"].to_list(),
        "y": tel["Y"].to_list()
    }

    # Longitudinal forces calculation -> d(V_car)
    # Get variables
    time = np.array(data["Time"])
    speed = np.array(data["Speed"]) / 3.6  # to m/s

    # Interpolation to constant 10 Hz
    t_uniform = np.arange(time[0], time[-1], 0.1)  # step of 0.1s = 10 Hz
    interp_fn  = interp1d(time, speed, kind="linear", fill_value="extrapolate")
    speed_uniform = interp_fn(t_uniform)

    # Derivate over "clean" signal
    G_MAX = 6.5  # approximate maximum value for F1
    glon_uniform  = np.gradient(speed_uniform, t_uniform) / 9.81 # to G
    glon_clip = np.clip(glon_uniform, -G_MAX, G_MAX)  # limits impossible max/min values

    # Reinterpolate back to original signal
    glon_interp = interp1d(t_uniform, glon_clip, kind="linear", fill_value="extrapolate")
    glon = glon_interp(time)
    data["glon"] = glon.tolist()

    # Delta calculation
    max_dist = max(data['Distance'])
    distances = np.linspace(0, max_dist, 2000)
    time_at_dist = np.interp(distances, data['Distance'], data['Time'])
    
    data["Distances"] = distances.tolist()
    data["TimeAtDist"] = time_at_dist.tolist()
    
    return data, ""