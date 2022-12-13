// analogFFT.ino
//
// Author: Owen Deng 2022
// Description: Arduino code for sending measured fundamental frequency to RPi
// Ref: https://www.tutorialspoint.com/fast-fourier-transform-fft-on-arduino

#include "arduinoFFT.h"

arduinoFFT FFT = arduinoFFT(); // Create FFT object
const unsigned long samples = 1024; //This value MUST ALWAYS be a power of 2

const double MAX_FREQ = 600;
const double MIN_FREQ = 150;

int sensorPin = A7;   // select the input pin for the potentiometer
int sensorValue = 0;  // variable to store the value coming from the sensor

double vReal[samples];
double vImag[samples];
double vReal_tmp[samples];

void setup() {
  Serial.begin(115200);
  Serial1.begin(9600);
}

void loop() {
  unsigned long start_fft;
  unsigned long end_fft;
  unsigned long end_sample;

  start_fft = micros();

  // read samples
  for (int i = 0; i < samples; i++){
    vReal[i] = analogRead(sensorPin);
    vImag[i] = 0.0;

    delayMicroseconds(200);
  }

  end_sample = micros();

  double sampling_freq = 1000000.0 / ((double)(end_sample - start_fft) / samples); 
  
  // compute fft
  FFT.Windowing(vReal, samples, FFT_WIN_TYP_HAMMING, FFT_FORWARD);
  FFT.Compute(vReal, vImag, samples, FFT_FORWARD);
  FFT.ComplexToMagnitude(vReal, vImag, samples); // Compute magnitudes

  // calculate harmonic product spectrum up to 4
  // https://cnx.org/contents/i5AAkZCP@2/Pitch-Detection-Algorithms
  for (int i = 0; i < samples; i ++){
    vReal_tmp[i] = vReal[i];
  }

  for (int j = 2; j <= 7; j++){
    for (int i = 0; i < samples / j; i++){
      vReal[i] *= vReal_tmp[i*j];
      vReal[i] = vReal[i] / 1000;
    }
  }

  // find major peak
  int lower_search_bound = MIN_FREQ * samples / sampling_freq;
  int upper_search_bound = MAX_FREQ * samples / sampling_freq;
  double max_val = vReal[lower_search_bound];
  int max_idx = lower_search_bound;
  for (int i = lower_search_bound; i <= upper_search_bound; i++){
    if (vReal[i] > max_val){
      max_val = vReal[i];
      max_idx = i;
    }
  }

  // if major peak is at the first harmonic, return the base peak instead
  for (int i = max_idx / 2 - 3; i <= max_idx / 2 + 3; i++){
    if (vReal[i] >= vReal[max_idx] / 4 && max_idx / 2 >= lower_search_bound){
      max_idx = max_idx / 2;
      break;
    }
  }

  double peak = sampling_freq / samples * max_idx;

  end_fft = micros();

  Serial.print("sampling frequency = ");
  Serial.print(sampling_freq);

  Serial.print(" | major peak = ");
  Serial.print(peak);

  Serial.print(" | major peak val = ");
  Serial.print(vReal[max_idx]);

  Serial.print(" | time to complete 1 fft = ");
  Serial.print((end_fft - start_fft)/1000);
  Serial.println(" ms");

  // UART to Pi
  Serial1.println(peak);
}