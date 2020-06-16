# Building an Estimator
*Fly Car Nanodegree - Project 4*

## Implement Estimator

### Determine standard deviation of measurement noise
In order to determine the standard deviation of the GPS and accelerometer signals I extended the
simulation time by setting `Sim.EndTime` to `20` in order to capture adequate data. I then used
python to import the two log files (`Graph1.txt` and `Graph2.txt`) in order to calculate the
standard deviation of the two signals. The contents of script are included here:

```python
import pandas as pd

GPS = pd.read_csv("config/log/Graph1.txt")
print(f"GPS std: {GPS[' Quad.GPS.X'].std()}")

IMU = pd.read_csv("config/log/Graph2.txt")
print(f"IMU std: {IMU[' Quad.IMU.AX'].std()}")
```

The results were then fed back into `config/6_Sensornoise.txt` as instructed.


### Better rate gyro integration scheme
In order to improve the integration scheme I used a quaternion update step. A quaternion rate can
be calculated from the gyro angular rates using the following:

![omega to quaternion derivative](/figures/quaternion_rate.png)

With the angular rates from the IMU expressed as a quaternion derivative, we can use a simple euler
integration step to update the quaternion representation of the attitude and then convert back to
euler angles.

It turns out that a method is provided (`Quaternion<>::IntegrateBodyRate(...)`) as part of the
`Quaternion` class that handles this math for us.

The only additional caveat is ensuring that the resultant yaw always remains between ±π.


### Prediction step
There were several methods that required updating as part of this step, including:
*  `PredictState()` - This is a basic euler integration step (integrate velocity into position and
   acceleration into velocity). The only gotcha here was accounting for gravity in the acceleration
   measurement. The accelerations from the IMU needed to be rotated from the body frame into the
   inertial frame using the attitude estimation and then gravity needed to be accounted for as well.
*  `GetRbgPrime(...)` - This method provides the derivative of the body to inertial rotation matrix.
   I set each element of the 3 x 3 matrix (where the last row is all zero) using the math provided
	 in the [Estimation for Quadrotors](https://www.overleaf.com/read/vymfngphcccj) document after
	 verifying the accuracy.
*  `Predict(...)` - Here I calculated G' using the output of `GetRbgPrime(...)` and then used G'
   to update the covariance matrix using the standard EKF update math:

![EKF predict](/figures/ekf_predict.png)


### Magnetometer update
This was a fairly trivial step aside from ensuring that the angular error was correct. I implemented
a `recenterAngle` routine that returns an angle that is in the range `[center - pi, center + pi)`.
The code is provided below:

```c++
template <typename T>
inline T recenterAngle(T angle, T center = 0) {
  center -= M_PI;
  return angle - 2 * M_PI * floor((angle - center) / (2 * M_PI));
}
```

The usage of this method in the magnetometer update step is shown here:
```c++
zFromX(0) = recenterAngle(ekfState(6), z(0));
```
which will return the equivalent value of `ekfState(6)` that is within ±π of `z(0)` (the
magnetometer yaw).


### GPS update
This step was fairly trivial from an implementation standpoint (`h'` is a 6 x 6 identity matrix).
The more difficult part was tuning the process noise models in order to ensure good results from
this update step.


## Flight Evaluation

### Performance criteria
I ran my code through each of the provided scenarios to ensure that it meets the various performance
criteria. I received a green box and a `PASS` for all scenarios that provide them.

### Integrating my controller from project 3
I copied my controller code from the previous project into this one. I actually met the performance
criteria without any detuning, however the quad was overly reactive to noise in the estimated state.
I then detuned my controller gains by ~25% and reran the final scenario. The quad appears to fly a
much smoother path, while still maintaining the performance criteria.

