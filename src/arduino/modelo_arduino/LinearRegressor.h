#pragma once
namespace Eloquent {
    namespace ML {
        namespace Port {
            class LinearRegression {
                public:
                    float predict(float *x) {
                        return dot(x,
                            3.86592994e-01, -8.47659016e-01, -1.22124533e-15,  2.80615086e-02,
                            9.46279415e-01,  0.00000000e+00,  0.00000000e+00,  2.94401535e-02,
                            2.15873185e-01
                        ) + 2.72852233676976;
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
