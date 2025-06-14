import streamlit as st
import pandas as pd
import numpy as np
import plotly.graph_objects as go
import plotly.express as px
from plotly.subplots import make_subplots
import fastf1
import warnings
import os
warnings.filterwarnings('ignore')

# Configure FastF1 cache - create organized directory structure
data_dir = 'data'
cache_dir = os.path.join(data_dir, 'cache')
if not os.path.exists(data_dir):
    os.makedirs(data_dir)
if not os.path.exists(cache_dir):
    os.makedirs(cache_dir)
fastf1.Cache.enable_cache(cache_dir)

# Page configuration
st.set_page_config(
    page_title="F1 Driver Signature Analysis",
    page_icon="🏎️",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS for better styling
st.markdown("""
<style>
    .main > div {
        padding-top: 2rem;
    }
    .stMetric {
        background-color: var(--secondary-background-color);
        border: 1px solid var(--text-color);
        padding: 1rem;
        border-radius: 0.5rem;
        box-shadow: 0 1px 3px rgba(0,0,0,0.12);
        color: var(--text-color);
    }
            
    .stMetric label, .stMetric span {
        color: var(--text-color);
    }
            
    .metric-container {
        display: flex;
        justify-content: space-around;
        margin: 1rem 0;
    }
</style>
""", unsafe_allow_html=True)

def load_session_data(year, gp, session_type):
    """Load F1 session data using FastF1"""
    try:
        session = fastf1.get_session(year, gp, session_type)
        session.load()
        return session
    except Exception as e:
        st.error(f"Error loading session data: {str(e)}")
        return None

def get_driver_telemetry(session, driver_code):
    """Get telemetry data for a specific driver"""
    try:
        driver = session.laps.pick_driver(driver_code)
        if driver.empty:
            return None
        
        # Get fastest lap telemetry
        fastest_lap = driver.pick_fastest()
        if fastest_lap.empty:
            return None
            
        telemetry = fastest_lap.get_telemetry()
        return telemetry, fastest_lap
    except Exception as e:
        st.error(f"Error getting telemetry for {driver_code}: {str(e)}")
        return None, None

def calculate_braking_aggressiveness(telemetry):
    """Calculate average deceleration G-force during braking events"""
    try:
        # Identify braking events (where brake is applied and speed is decreasing)
        braking_mask = (telemetry['Brake'] > 0) & (telemetry['Speed'].diff() < 0)
        
        if not braking_mask.any():
            return 0.0
        
        # Calculate deceleration (negative acceleration)
        speed_ms = telemetry['Speed'] / 3.6  # Convert km/h to m/s
        acceleration = speed_ms.diff() / telemetry['Time'].diff().dt.total_seconds()
        
        # Get braking deceleration (positive values)
        braking_decel = -acceleration[braking_mask]
        braking_g_force = braking_decel / 9.81  # Convert to G-force
        
        return braking_g_force.mean()
    except:
        return 0.0

def calculate_throttle_smoothness(telemetry):
    """Calculate throttle application smoothness (lower std = smoother)"""
    try:
        throttle_changes = telemetry['Throttle'].diff().abs()
        return throttle_changes.std()
    except:
        return 0.0

def calculate_cornering_consistency(telemetry):
    """Calculate cornering consistency based on speed variance in corners"""
    try:
        # Identify cornering sections (low throttle, high steering)
        corner_mask = (telemetry['Throttle'] < 50) & (abs(telemetry['Speed'].diff()) > 1)
        
        if not corner_mask.any():
            return 0.0
        
        corner_speeds = telemetry.loc[corner_mask, 'Speed']
        return corner_speeds.std()
    except:
        return 0.0

def calculate_gear_shift_frequency(telemetry):
    """Calculate gear shift frequency per minute"""
    try:
        gear_changes = (telemetry['nGear'].diff() != 0).sum()
        total_time_minutes = (telemetry['Time'].iloc[-1] - telemetry['Time'].iloc[0]).total_seconds() / 60
        
        if total_time_minutes > 0:
            return gear_changes / total_time_minutes
        return 0.0
    except:
        return 0.0

def analyze_driver_style(session, driver_code):
    """Analyze a driver's style metrics"""
    telemetry, lap = get_driver_telemetry(session, driver_code)
    
    if telemetry is None or telemetry.empty:
        return None
    
    metrics = {
        'braking_aggressiveness': calculate_braking_aggressiveness(telemetry),
        'throttle_smoothness': calculate_throttle_smoothness(telemetry),
        'cornering_consistency': calculate_cornering_consistency(telemetry),
        'gear_shift_frequency': calculate_gear_shift_frequency(telemetry)
    }
    
    return metrics, lap

def create_comparison_charts(driver1_data, driver2_data, driver1_name, driver2_name):
    """Create comparison visualizations"""
    
    # Prepare data for charts
    metrics_names = ['Braking\nAggressiveness (G)', 'Throttle\nSmoothness', 'Cornering\nConsistency', 'Gear Shifts\nper Min']
    driver1_values = [
        driver1_data['braking_aggressiveness'],
        driver1_data['throttle_smoothness'],
        driver1_data['cornering_consistency'],
        driver1_data['gear_shift_frequency']
    ]
    driver2_values = [
        driver2_data['braking_aggressiveness'],
        driver2_data['throttle_smoothness'],
        driver2_data['cornering_consistency'],
        driver2_data['gear_shift_frequency']
    ]
    
    # Create subplots
    fig = make_subplots(
        rows=1, cols=2,
        subplot_titles=['Style Metrics Comparison', 'Driver Style Fingerprint'],
        specs=[[{"secondary_y": False}, {"type": "polar"}]]
    )
    
    # Bar chart comparison
    fig.add_trace(
        go.Bar(name=driver1_name, x=metrics_names, y=driver1_values, 
               marker_color='#FF6B6B', opacity=0.8),
        row=1, col=1
    )
    fig.add_trace(
        go.Bar(name=driver2_name, x=metrics_names, y=driver2_values,
               marker_color='#4ECDC4', opacity=0.8),
        row=1, col=1
    )
    
    # Radar chart for style fingerprint
    fig.add_trace(
        go.Scatterpolar(
            r=driver1_values,
            theta=metrics_names,
            fill='toself',
            name=driver1_name,
            line_color='#FF6B6B',
            fillcolor='rgba(255, 107, 107, 0.3)'
        ),
        row=1, col=2
    )
    fig.add_trace(
        go.Scatterpolar(
            r=driver2_values,
            theta=metrics_names,
            fill='toself',
            name=driver2_name,
            line_color='#4ECDC4',
            fillcolor='rgba(78, 205, 196, 0.3)'
        ),
        row=1, col=2
    )
    
    fig.update_layout(
        height=600,
        showlegend=True,
        title_text="F1 Driver Style Analysis",
        title_x=0.5
    )
    
    return fig

def main():
    st.title("🏎️ F1 Driver Signature Analysis & Performance Dissector")
    st.markdown("---")
    
    # Sidebar for session selection
    st.sidebar.header("Session Selection")
    
    # Year selection
    years = list(range(2018, 2024))
    selected_year = st.sidebar.selectbox("Select Season", years, index=len(years)-1)
    
    # GP selection
    try:
        schedule = fastf1.get_event_schedule(selected_year)
        gp_names = schedule['EventName'].tolist()
        selected_gp = st.sidebar.selectbox("Select Grand Prix", gp_names)
    except:
        st.error("Failed to load season schedule. Please try again.")
        return
    
    # Session type selection
    session_types = ['Practice 1', 'Practice 2', 'Practice 3', 'Qualifying', 'Race']
    selected_session = st.sidebar.selectbox("Select Session", session_types, index=1)
    
    st.sidebar.markdown("---")
    st.sidebar.header("Driver Selection")
    
    # Load session data
    if st.sidebar.button("Load Session Data"):
        with st.spinner("Loading session data..."):
            session = load_session_data(selected_year, selected_gp, selected_session)
            st.session_state['session'] = session
            
            if session:
                # Get available drivers
                drivers = session.laps['Driver'].unique()
                st.session_state['drivers'] = sorted(drivers)
                st.success(f"✅ Loaded {selected_session} data for {selected_gp} {selected_year}")
    
    # Driver selection
    if 'drivers' in st.session_state:
        col1, col2 = st.sidebar.columns(2)
        
        with col1:
            driver1 = st.selectbox("Driver 1", st.session_state['drivers'], key="driver1")
        with col2:
            driver2 = st.selectbox("Driver 2", st.session_state['drivers'], 
                                 index=1 if len(st.session_state['drivers']) > 1 else 0, key="driver2")
        
        # Analysis button
        if st.sidebar.button("🔍 Analyze Drivers", type="primary"):
            if driver1 == driver2:
                st.error("Please select two different drivers for comparison.")
                return
            
            session = st.session_state['session']
            
            with st.spinner("Analyzing driver styles..."):
                # Analyze both drivers
                driver1_result = analyze_driver_style(session, driver1)
                driver2_result = analyze_driver_style(session, driver2)
                
                if driver1_result is None or driver2_result is None:
                    st.error("Failed to analyze one or both drivers. Please try different drivers or session.")
                    return
                
                driver1_metrics, driver1_lap = driver1_result
                driver2_metrics, driver2_lap = driver2_result
                
                # Display results
                st.header(f"Driver Comparison: {driver1} vs {driver2}")
                
                # Context information
                col1, col2, col3 = st.columns(3)
                with col1:
                    st.info(f"**Season:** {selected_year}")
                with col2:
                    st.info(f"**Grand Prix:** {selected_gp}")
                with col3:
                    st.info(f"**Session:** {selected_session}")
                
                # Metrics display
                st.subheader("📊 Style Metrics Comparison")
                
                col1, col2, col3, col4 = st.columns(4)
                
                with col1:
                    st.metric(
                        "Braking Aggressiveness (G)",
                        f"{driver1_metrics['braking_aggressiveness']:.2f}",
                        delta=f"{driver1_metrics['braking_aggressiveness'] - driver2_metrics['braking_aggressiveness']:.2f}"
                    )
                    st.caption(f"{driver2}: {driver2_metrics['braking_aggressiveness']:.2f}")
                
                with col2:
                    st.metric(
                        "Throttle Smoothness",
                        f"{driver1_metrics['throttle_smoothness']:.2f}",
                        delta=f"{driver1_metrics['throttle_smoothness'] - driver2_metrics['throttle_smoothness']:.2f}",
                        delta_color="inverse"
                    )
                    st.caption(f"{driver2}: {driver2_metrics['throttle_smoothness']:.2f}")
                
                with col3:
                    st.metric(
                        "Cornering Consistency",
                        f"{driver1_metrics['cornering_consistency']:.2f}",
                        delta=f"{driver1_metrics['cornering_consistency'] - driver2_metrics['cornering_consistency']:.2f}",
                        delta_color="inverse"
                    )
                    st.caption(f"{driver2}: {driver2_metrics['cornering_consistency']:.2f}")
                
                with col4:
                    st.metric(
                        "Gear Shifts/Min",
                        f"{driver1_metrics['gear_shift_frequency']:.2f}",
                        delta=f"{driver1_metrics['gear_shift_frequency'] - driver2_metrics['gear_shift_frequency']:.2f}"
                    )
                    st.caption(f"{driver2}: {driver2_metrics['gear_shift_frequency']:.2f}")
                
                # Visualization
                st.subheader("📈 Visual Comparison")
                fig = create_comparison_charts(driver1_metrics, driver2_metrics, driver1, driver2)
                st.plotly_chart(fig, use_container_width=True)
                
                # Lap time comparison
                st.subheader("⏱️ Lap Time Comparison")
                col1, col2 = st.columns(2)
                
                with col1:
                    st.info(f"**{driver1}** - Lap Time: {driver1_lap['LapTime']}")
                with col2:
                    st.info(f"**{driver2}** - Lap Time: {driver2_lap['LapTime']}")
                
                # Style interpretation
                st.subheader("🎯 Style Analysis Summary")
                
                # Determine style characteristics
                if driver1_metrics['braking_aggressiveness'] > driver2_metrics['braking_aggressiveness']:
                    braking_leader = driver1
                else:
                    braking_leader = driver2
                
                if driver1_metrics['throttle_smoothness'] < driver2_metrics['throttle_smoothness']:
                    smooth_leader = driver1
                else:
                    smooth_leader = driver2
                
                st.markdown(f"""
                **Key Insights:**
                - **Most Aggressive Braker:** {braking_leader} shows higher deceleration forces
                - **Smoothest Throttle Application:** {smooth_leader} demonstrates more consistent throttle inputs
                - **Driving Style Differences:** The radar chart shows each driver's unique signature across all metrics
                """)
    
    else:
        st.info("👈 Please load session data first using the sidebar controls.")
    
    # Footer
    st.markdown("---")
    st.markdown("Built with FastF1 Python package")
    st.markdown("NOTICE:")
    st.markdown("FastF1 and this website are unofficial and are not associated in any way with the Formula 1 companies. F1, FORMULA ONE, FORMULA 1, FIA FORMULA ONE WORLD CHAMPIONSHIP, GRAND PRIX and related marks are trade marks of Formula One Licensing B.V.")

if __name__ == "__main__":
    main()