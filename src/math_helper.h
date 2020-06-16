//
//  math_helper.h
//  FCND-CPPSim
//
//  Created by Michael Rose on 6/16/20.
//  Copyright © 2020 Fotokite. All rights reserved.
//

#ifndef math_helper_h
#define math_helper_h

namespace math_helper {

template <typename T>
inline T recenterAngle(T angle, T center = 0) {
  center -= M_PI;
  return angle - 2 * M_PI * floor((angle - center) / (2 * M_PI));
}

}

#endif /* math_helper_h */
