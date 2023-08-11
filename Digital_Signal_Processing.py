#it display  first graph and combined graph when selected in covlution  section 
# 1)statistucal parameter 2)fourier transform 3)power spectrum 4) convolution with option linear and circular

#import necessary libraries
import streamlit as st
import numpy as np
from scipy.fft import fft
from scipy import signal
from scipy import stats
import pandas as pd
import plotly.graph_objects as go


#connecting streamlit web app with internal CSS for designing the web app
with open("style5.css") as f:
    st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)

# Function to calculate statistical parameters
def calculate_statistics(data):
    mean = np.mean(data)
    rms = np.sqrt(np.mean(np.square(data)))
    std = np.std(data)
    median = np.median(data)
    mode = stats.mode(data)[0][0]
    maximum = np.max(data)
    minimum = np.min(data)
    skewness = stats.skew(data)
    return mean, rms, std, median, mode, maximum, minimum, skewness

# Function to generate sample data for the graph
def generate_data(graph_type, frequency, amplitude, phase, sampling_frequency, normalize= True):
    num_points = int(10 * sampling_frequency)
    t = np.linspace(0, num_points / sampling_frequency, num_points)
    angular_frequency = 2 * np.pi * frequency
    angle = angular_frequency * t + phase * np.pi / 180

    if graph_type == 'sine':
        y = amplitude * np.sin(angle)
    elif graph_type == 'triangle':
        y = (2 * amplitude / np.pi) * np.arcsin(np.sin(angle))
    elif graph_type == 'square':
        y = amplitude * np.sign(np.sin(angle))
    elif graph_type == 'sawtooth':
        y = 2 * amplitude * (t * frequency - np.floor(t * frequency))

    if normalize:
         y = (y - np.min(y)) / (np.max(y) - np.min(y)) - 0.5

    return t, y

# Function to convolve two graph data (linear or circular)
def convolve_graphs(graph1, graph2, mode='linear'):
    num_points_convolution = int(10* (sampling_frequency + second_sampling_frequency))
    t_convolution = np.linspace(0, 2*num_points_convolution / 10, num_points_convolution)

    
    if mode == 'linear':
        convolution = np.convolve(graph1, graph2, mode='same')
    elif mode == 'circular':
        convolution = np.fft.ifft(np.fft.fft(graph1) * np.fft.fft(graph2)).real
    return convolution

# Streamlit app
st.title('Digital Signal Processing')

# Tab selection
tabs = ['Statistical Parameters', 'Fourier Transform', 'Power Spectrum', 'Convolution']
selected_tab = st.radio('Select Tab', tabs)

# Configuration inputs for first graph
st.sidebar.subheader('Generate First Signal')
graph_type = st.sidebar.selectbox('First Graph Type', ['sine', 'triangle', 'square', 'sawtooth'])
frequency = st.sidebar.slider('Frequency', 1, 400, 5)
amplitude = st.sidebar.slider('Amplitude', 10, 100, 50)
phase = st.sidebar.slider('Phase', 0, 360, 0)
sampling_frequency = st.sidebar.slider('Sampling Frequency', 10, 5000, 1000)

# Generate data for the first graph with normalization
t, y = generate_data(graph_type, frequency, amplitude, phase, sampling_frequency)

# Display the first graph

x_range = [0, max(t)]
st.subheader('First Graph')
fig1 = go.Figure(data=go.Scatter(x=t, y=y), layout=dict(title='First Graph', xaxis_title='Time', yaxis_title='Amplitude',xaxis_range=[0,0.5]))
st.plotly_chart(fig1)

# Calculate statistical parameters
mean, rms, std, median, mode, maximum, minimum, skewness = calculate_statistics(y)

# Tab: Statistical Parameters
if selected_tab == 'Statistical Parameters':
    st.subheader('Statistical Parameters')
    df = pd.DataFrame({
        'Parameter': ['Mean', 'RMS Value', 'Standard Deviation', 'Median', 'Mode', 'Maximum', 'Minimum', 'Skewness'],
        'Value': [mean, rms, std, median, mode, maximum, minimum, skewness]
    })
    st.table(df)

# Tab: Fourier Transform
elif selected_tab == 'Fourier Transform':
    st.subheader('Fourier Transform')
    spectrum = fft(y)
    frequencies = np.fft.fftfreq(len(y), d=1.0/sampling_frequency)
    fig2 = go.Figure(data=go.Scatter(x=frequencies, y=np.abs(spectrum)), layout=dict(title='Fourier Transform', xaxis_title='Frequency', yaxis_title='Magnitude'))
    st.plotly_chart(fig2)

# Tab: Power Spectrum
elif selected_tab == 'Power Spectrum':
    st.subheader('Power Spectrum')
    f, Pxx = signal.periodogram(y, fs=sampling_frequency)
    fig3 = go.Figure(data=go.Scatter(x=f, y=Pxx, mode='lines'), layout=dict(title='Power Spectrum', xaxis_title='Frequency', yaxis_title='Power'))
    st.plotly_chart(fig3)

# Tab: Convolution
elif selected_tab == 'Convolution':
    # Configuration inputs for second graph
    # st.subheader('Convolution')

     
    # Display the combination of two graphs
    st.sidebar.subheader('Generate Second Signal')
    second_graph_type = st.sidebar.selectbox('Second Graph Type', ['sine', 'triangle', 'square', 'sawtooth'], key='second_graph_type')
    second_frequency = st.sidebar.slider('Second Frequency', 1, 400, 10, key='second_frequency')
    second_amplitude = st.sidebar.slider('Second Amplitude', 10, 100, 50, key='second_amplitude')
    second_phase = st.sidebar.slider('Second Phase', 0, 360, 0, key='second_phase')
    second_sampling_frequency = st.sidebar.slider('Second Sampling Frequency', 10, 5000, 1000, key='second_sampling_frequency')

    # Generate data for the second graph with normalization
    t2, y2 = generate_data(second_graph_type, second_frequency, second_amplitude, second_phase, second_sampling_frequency)

    
    
    # Combine the first and second graphs
  
    #forplotting thr combination of first and second signal
    x_range = [0, max(t)]                  #for scaling in x-axis
    st.subheader('Combination of First and Second Signal')
    fig4 = go.Figure()
    fig4.add_trace(go.Scatter(x=t, y=y, name='First Graph'))
    fig4.add_trace(go.Scatter(x=t2, y=y2, name='Second Graph'))
    fig4.update_layout(title='Combination of First and Second Signal', xaxis_title='Time', yaxis_title='Amplitude',xaxis_range=[0,0.5])
    st.plotly_chart(fig4)
    

    #next part is convolution
    st.subheader('Convolution')     #heading for convolution
    convolution_mode = st.radio('Select Convolution Mode', ['Linear', 'Circular'])        #mode of convolution

    
    # Display the convolution result
    st.subheader('Convolution Result')              #heading for displaying mode of convolution

    #condition for selecting linear convolution
    if convolution_mode == 'Linear':
        convolution = convolve_graphs(y, y2)

        num_points_convolution = int(10* (sampling_frequency + second_sampling_frequency))     #diplay the convolution doubling of sampling frequency
        t_convolution = np.linspace(0, 2*num_points_convolution / 10, num_points_convolution)   #dispaly the range of x-axis in convolution
        convolution=(convolution-np.min(convolution))/(np.max(convolution)-np.min(convolution))-0.5   #normalize the amplitude

    
    
   #condition for selecting circular convolution
    elif convolution_mode == 'Circular':

           convolution = convolve_graphs(y, y, mode='circular')

           num_points_convolution = int(10* (2*sampling_frequency ))                      #diplay the convolution doubling of sampling frequency
           t_convolution = np.linspace(0, 2*num_points_convolution / 10, num_points_convolution)     #dispaly the range of x-axis in convolution
           convolution=(convolution-np.min(convolution))/(np.max(convolution)-np.min(convolution))-0.5           #normalize the amplitude

            
    # Display the convolution result
    fig6 = go.Figure(data=go.Scatter(x = t_convolution, y=convolution), layout = dict(title='Convolution', xaxis_title='Time', yaxis_title='Amplitude'))
    st.plotly_chart(fig6)


