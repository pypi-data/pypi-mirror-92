# speechaugs
Single-channel *waveforms* augmentations for *speech recognition* models.
***
### Augmentations:
* Time Stretch
* Forward Time Shift
* Pitch Shift
* Colored Noise (white, pink, brown, blue, violet, grey)
* Zero Samples
* Clipping samples
* Inversion
* Loudness Change
* Short Noises
* File Noise
---
<a href="https://github.com/waveletdeboshir/speechaugs/blob/master/examples/Augmentations_Example.ipynb"> **Colab Example**</a>
You can see examples of all augmentations and listen to resulting audios on <a href="https://github.com/waveletdeboshir/speechaugs/blob/master/examples/Augmentations_Example.ipynb"> this page</a> with Colab notebook.
***
## Installation
`pip install speechaugs`
***
## Time Stretch
Stretch a wavefom in time with randomly chosen rate. Is implemented using <a href="https://librosa.org/doc/main/generated/librosa.effects.time_stretch.html"> *librosa.effects.time_stretch*</a>. 
<p>
<img src="https://raw.githubusercontent.com/waveletdeboshir/speechaugs/master/images/timestretch.png" width="700"/> 
</p>

## Forward Time Shift
Shift a waveform forwards in time.
<p>
<img src="https://raw.githubusercontent.com/waveletdeboshir/speechaugs/master/images/forwardtimeshift.png" width="400"/> 
</p>

## Pitch Shift
Shift a pitch by *n_steps* semitones. Is implemented using <a href="https://librosa.org/doc/main/generated/librosa.effects.pitch_shift.html"> *librosa.effects.pitch_shift*</a>. 

The work of PitchShift can be better illustrated on the MelSpectrograms of waveforms. 

**Higher pitch (+9 semitones):**
<p>
<img src="https://raw.githubusercontent.com/waveletdeboshir/speechaugs/master/images/higherpitch.png" width="600" title="Higher pitch (+9 semitones)"/> 
</p>

**Lower pitch (-5 semitones)**
<p>
<img src="https://raw.githubusercontent.com/waveletdeboshir/speechaugs/master/images/lowerpitch.png" width="600"  title="Lower pitch (-5 semitones)"/> 
</p>

## Colored Noise
Add noise of different color to a waveform.
Color of noise depends on the spectral density of the noise. You can go to <a href="https://en.wikipedia.org/wiki/Colors_of_noise">wiki page</a> for more information.

This class is implemented using <a href="https://github.com/felixpatzelt/colorednoise">colorednoise package</a>. The color of noise is randomly choosen.

**White Noise**
<p>
<img src="https://raw.githubusercontent.com/waveletdeboshir/speechaugs/master/images/whitenoise.png" width="600" title="White Noise"/> 
</p>

**Brown Noise**
<p>
<img src="https://raw.githubusercontent.com/waveletdeboshir/speechaugs/master/images/brownnoise.png" width="600" title="Brown Noise"/> 
</p>

## Zero Samples
Set some percentage of samples to zero.
## Clipping Samples
Clip some percentage of samples from a waveform.
<p>
<img src="https://raw.githubusercontent.com/waveletdeboshir/speechaugs/master/images/clipping.png" width="400" title="Clip Samples"/> 
</p>

## Inversion
Change sign of waveform samples.
<p>
<img src="https://raw.githubusercontent.com/waveletdeboshir/speechaugs/master/images/inversion.png" width="400" title="Inversion"/> 
</p>

## Loudness Change
Change loudness of intervals of a waveform. For example, in the figure below initial waveform was splitted into 3 intervals and samples from each of them were multiplied by different random factors.
<p>
<img src="https://raw.githubusercontent.com/waveletdeboshir/speechaugs/master/images/loudnesschange.png" width="400" title="Loudness"/> 
</p>

## Short Noises
Add several short noises to different parts of a waveform.
<p>
<img src="https://raw.githubusercontent.com/waveletdeboshir/speechaugs/master/images/shortnoises.png" width="400" title="ShortNoises"/> 
</p>

## File Noise
Add noise from randomly chosen file from specified folder. 
<p>
<img src="https://raw.githubusercontent.com/waveletdeboshir/speechaugs/master/images/filenoise.png" width="400" title="FileNoise"/> 
</p>

***
## Usage example (with default parameters)
Import:
```python
from speechaugs import TimeStretchLibrosa, ForwardTimeShift, PitchShiftLibrosa, ColoredNoise, Inversion, ZeroSamples, ClippingSamples
```    
Other libs:
```python
import torch, torchaudio
import albumentations as A
```
Usage:
```python

ex_waveform, sr = torchaudio.load('audio_filename')

transforms = A.Compose([
    ForwardTimeShift(p=0.5),
    Inversion(p=0.5),
    A.OneOf([ZeroSamples(p=0.5), ClippingSamples(p=0.5)], p=0.5),
    A.OneOf([TimeStretchLibrosa(p=0.5), PitchShiftLibrosa(p=0.5)], p = 0.5),
    ColoredNoise(p=0.5)
], p=1.0)

augmented = transforms(waveform=ex_waveform)['waveform']
```