#pragma once
namespace Eloquent {
    namespace ML {
        namespace Port {
            class LinearRegression {
                public:
                    float predict(float *x) {
                        return dot(x,
                            1.30169996, -8.73234688, 0.0, 0.0,
                            0.00706742, 0.15669159, 0.0, 0.0,
                            0.00538109, -0.13119439
                        ) + 8.78645833;
                    }

                protected:
                    float dot(float *x, ...) {
                        va_list w;
                        va_start(w, 10); // <- 10 features
                        float dot = 0.0;
                        for (uint16_t i = 0; i < 10; i++) {
                            const float wi = va_arg(w, double);
                            dot += x[i] * wi;
                        }
                        return dot;
                    }
            };
        }
    }
}
