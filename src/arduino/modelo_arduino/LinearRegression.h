#pragma once
namespace Eloquent {
    namespace ML {
        namespace Port {
            class LinearRegression {
                public:
                    float predict(float *x) {
                        return dot(x,
                            -1.10044053,
                            -8.97775527,
                            -0.00000000,
                            -1.23552997,
                            -7.72430131,
                            0.00000000,
                            0.00000000,
                            -3.19941472,
                            0.20131996
                        ) + 7.07227139;
                    }

                protected:
                    float dot(float *x, ...) {
                        va_list w;
                        va_start(w, 9);
                        float dot = 0.0;
                        for (uint16_t i = 0; i < 9; i++) {
                            const float wi = va_arg(w, double);
                            dot += x[i] * wi;
                        }
                        return dot;
                    }
            };
        }
    }
}
